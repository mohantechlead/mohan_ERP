from django.shortcuts import render
from .models import *
from .models import opening_balance
from .forms import *
from django.shortcuts import render, redirect,get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required,user_passes_test
from django.forms import formset_factory
from django.db.models import Sum
from django.http import JsonResponse,HttpResponse
from django.template.loader import get_template
from django.contrib.auth.models import User, auth
from num2words import num2words
from GRN.models import inventory_GRN_items
from django import template
from openpyxl import Workbook
from openpyxl.styles import *
import openpyxl


# Create your views here.
def create_MR(request):
    if request.method == 'POST':
        form = MRForm(request.POST)
        
        if form.errors:
            print(form.errors)

        if form.is_valid():
            print(form.data,"val")

            form.save()
            return redirect('create_MR')
        else:
            print(form.data,"nval")
            errors = dict(form.errors.items())
            print(errors,"errors")
            return JsonResponse({'form_errors': errors}, status=400)
    form = MRForm()
    formset = formset_factory(MRItemForm, extra= 1)
    formset = formset(prefix="items")
    print(formset)
    return render(request,'create_mr.html',{'form': form, 'formset': formset})

def create_MR_items(request):
    if request.method == 'POST':
        formset = formset_factory(MRItemForm, extra=1 , min_num= 1)
        formset = formset(request.POST or None, prefix="items")

        if formset.errors:
            print(formset.errors)

        non_empty_forms = [form for form in formset if form.cleaned_data.get('item_name')]
        pr_no = request.POST.get('MR_no')
        print(pr_no,"pr")
        if non_empty_forms:
            if formset.is_valid():
                MR_instance = MR.objects.get(MR_no = pr_no)
                print(MR_instance,"inst")
                for form in non_empty_forms:
                    form.instance.MR_no = MR_instance
                    item_name = form.cleaned_data['item_name']
                    quantity = form.cleaned_data['quantity']
                    no_of_unit = form.cleaned_data['no_of_unit']
                    # measurement_type = form.cleaned_data['measurement_type']
                    try:
                        inventory_item = inventory.objects.get(item_name = item_name)
                        inventory_item.quantity -= quantity
                        inventory_item.no_of_unit -= no_of_unit
                        # inventory_item.measurement_type = measurement_type
                        inventory_item.save()
                    except inventory.DoesNotExist:
                        # print(item_name, quantity, measurement_type, "yes")
                        inventory_item = inventory(item_name = item_name, quantity = -quantity)
                        inventory_item.save()
                    form.save()
            else:
                print(formset.data,"nval")
                errors = dict(formset.errors.items())
                return JsonResponse({'form_errors': errors}, status=400)
        
            pr_form = MRForm(prefix="orders")
            formset = formset_factory(MRItemForm, extra=1)
            formset = formset(prefix="items")

            context = {
                'pr_form': pr_form,
                'formset': formset,
                # 'message':success_message,
            }
            return render(request, 'create_mr.html', context)
    else:
       
        formset = formset_factory(MRItemForm, extra=1)
        formset = formset(prefix="items")

    context = {
        'formset': formset,
    }
    return render(request, 'create_mr.html', context)

def display_MR(request):
    mr_list = MR.objects.all()
    mr_list = mr_list.order_by('MR_no')

    mrs_data = []
    for mr in mr_list:

        items = MR_item.objects.filter(MR_no=mr.MR_no)

        mr_data = {
                'MR_no': mr.MR_no,
                'MR_date': mr.MR_date,  # Assuming 'date' is a field in CosmicOrder
                'mr_items': items,  # Assuming a related name 'order_items' on CosmicOrder pointing to OrderItem
                'MR_store': mr.MR_store,  # Assuming 'PR_before_vat' is a field in CosmicOrder
                'desc': mr.desc,  # A  # Assuming 'status' is a field in CosmicOrder
            }
        mrs_data.append(mr_data)

    context = {
        'my_order': mrs_data,
        'mr_list': mr_list
    }

    return render(request,'display_MR.html', context)

def display_inventory(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)

        if form.errors:
            print(form.errors)

        if form.is_valid():
            form.save()
            return redirect('display_inventory')
    
    form = InventoryItemForm()

    names_a = set(inventory_GRN_items.objects.values_list('item_name', flat=True))
    names_b = set(inventory_MR_items.objects.values_list('item_name', flat=True))
    names_c = set(opening_balance.objects.values_list('item_name', flat=True))

    all_names = names_a.union(names_b).union(names_c)

    for name in all_names:
        # Get the quantity from each model
        quantity_a = inventory_GRN_items.objects.filter(item_name=name).first()
        quantity_b = inventory_MR_items.objects.filter(item_name=name).first()
        quantity_c = opening_balance.objects.filter(item_name=name).first()
        
        # Initialize the quantities or set to 0 if not found
        quantity_a_value = quantity_a.total_quantity if quantity_a else 0
        quantity_b_value = quantity_b.total_quantity if quantity_b else 0
        quantity_c_value = quantity_c.quantity if quantity_c else 0

        units_a_value = quantity_a.total_no_of_unit if quantity_a else 0
        units_b_value = quantity_b.total_no_of_unit if quantity_b else 0
        units_c_value = quantity_c.no_of_unit if quantity_c else 0
        
        # Calculate the result: Subtract ModelA and ModelC, and add ModelB
        result_quantity =  quantity_c_value - quantity_b_value +  quantity_a_value 
        result_units = units_c_value - units_b_value + units_a_value
        
        # Save or update the result in ModelD
        inventory.objects.update_or_create(
            item_name=name,
            defaults={'quantity': result_quantity,
                      'no_of_unit': result_units}
        )

    items = inventory.objects.all().order_by('item_name')
    print(items)
    context = {
        'items':items,
        'form':form,
    }

    return render(request,'display_inventory.html',context)

def opening_balances(request):
    if request.method == 'POST':
        form = OpeningBalanceItemForm(request.POST)

        if form.errors:
            print(form.errors)

        if form.is_valid():
            form.save()
            return redirect('opening_balances')
    
    form = OpeningBalanceItemForm()
    items = opening_balance.objects.all().order_by('item_name')    
    print(items)
    context = {
        'items':items,
        'form':form,
    }

    return render(request,'opening_balances.html',context)

def display_MR_items(request):

    item_quantities = MR_item.objects.values('item_name').annotate(total_quantity=Sum('quantity'), total_no_of_unit=Sum('no_of_unit'))
  
    for item in item_quantities:
        inventory_MR_items.objects.update_or_create(
            item_name=item['item_name'],
            defaults={'total_quantity': item['total_quantity'],
                      'total_no_of_unit': item['total_no_of_unit']}
            
        )
        print(f"Name: {item['item_name']}, Total Quantity: {item['total_quantity']}, Total No of Unit: {item['total_no_of_unit']}")
    

    items = inventory_MR_items.objects.all().order_by('item_name')    
    print(items)
    context = {
        # 'total_quantity':item_quantities,
        'items':items,
        
    }

    return render(request,'display_MR_items.html',context)

def display_single_mr(request):
    if request.method == 'GET':
        mr_no = request.GET['MR_no']
        
        try:
            mr = MR.objects.get(MR_no=mr_no)
            mr_items = MR_item.objects.all()
            mr_items = mr_items.filter(MR_no=mr_no)
            print(mr_items)

            if mr_items.exists():
                print(mr_items,"yes")
                context = {
                            'mr_item': mr_items,
                            'my_mr': mr,
                        }
                return render(request, 'display_single_mr.html', context)
        
        except MR.DoesNotExist:
                mr = None 
       
        print("no")
        
        context = {
                        'my_mr': mr,
                    }
    return render(request, 'display_single_mr.html')

def export_mr(request):

    # my_mr_items = MR_item.objects.all().order_by('item_name')

    # for item in my_mr_items:
    #     mr_details = get_object_or_404(MR, MR_no=item.MR_no)
    items = MR_item.objects.select_related('MR_no').all().order_by('MR_no__MR_date','item_name')
    # my_inventory = inventory.objects.all()

    context = {
        'items':items,
        # 'my_inventory':my_inventory
        # 'detail':mr_details
    }
    return render(request, 'export_mr.html', context)

def export_mr_pdf(request):
    # Create a workbook and add a worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Exported Data'

    # Add headers to the worksheet
    headers = ['MR Date', 'Item Name', 'MR No', 'Quantity', 'No of Units']
    worksheet.append(headers)

    # Filter data based on request parameters
    selected_month = request.GET.get('month')
    selected_branch = request.GET.get('branch')
    
    # Replace with your actual query
    items = MR_item.objects.select_related('MR_no').all().order_by('item_name','MR_no__MR_date')

    # Apply filters if provided
    if selected_month:
        items = items.filter(MR_no__MR_date__month=selected_month)
    if selected_branch:
        items = items.filter(MR_no__branch=selected_branch)

    if items.exists():
        month_year = items.first().MR_no.MR_date.strftime("%B %Y")  # Example format: "August 2024"
    else:
        month_year = "N/A"

    # Add the title to the worksheet
    title = f"List of MR in the Month {month_year}"
    worksheet.merge_cells('A1:E1')  # Merge cells for the title
    worksheet['A1'] = title
    worksheet['A1'].font = openpyxl.styles.Font(size=14, bold=True)  # Set font size and bold


    # Variables to keep track of totals
    current_item_name = None
    total_quantity = 0
    total_no_of_units = 0

    for item in items:
        if item.item_name != current_item_name:
            # If moving to a new item name, append totals of the previous item
            if current_item_name is not None:
                worksheet.append([
                    '',  # Empty MR Date for totals row
                    f'Total for {current_item_name}',
                    '',  # Empty MR No for totals row
                    total_quantity,
                    total_no_of_units
                ])

            # Reset totals and update current item name
            current_item_name = item.item_name
            total_quantity = 0
            total_no_of_units = 0

        # Add the current item's values to the totals
        total_quantity += item.quantity
        total_no_of_units += item.no_of_unit

        # Write the current item's data to the worksheet
        worksheet.append([
            item.MR_no.MR_date.strftime("%d/%m/%Y"),  # Adjust based on your model's date field
            item.item_name,
            item.MR_no.MR_no,  # Adjust based on your model's MR number field
            item.quantity,
            item.no_of_unit
        ])

    # Append the totals for the last group of items
    if current_item_name is not None:
        worksheet.append([
            '',  # Empty MR Date for totals row
            f'Total for {current_item_name}',
            '',  # Empty MR No for totals row
            total_quantity,
            total_no_of_units
        ])

    # Create an HTTP response with the Excel content
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="exported_data.xlsx"'

    # Save the workbook to the response
    workbook.save(response)

    return response
