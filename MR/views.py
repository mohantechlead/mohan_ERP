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
from GRN.models import inventory_GRN_items, GRN_item
from django import template
from openpyxl import Workbook
from openpyxl.styles import *
import openpyxl
from itertools import chain
import plotly.graph_objs as go
from plotly.offline import plot
from DN.models import inventory_DN_items

@login_required(login_url="login_user")
def create_MR(request):
    MRFormSet = formset_factory(MRItemForm, extra=1)
    recieved_to = sorted(set(MR.objects.values_list('desc', flat=True)))
    recieved_from = sorted(set(MR.objects.values_list('MR_store', flat=True)))

    if request.method == 'POST':
        form = MRForm(request.POST)
        formset = MRFormSet(request.POST, prefix="items")

        if form.is_valid() and formset.is_valid():
            # Save the MR form
            MR_instance = form.save()

            # Process the formset
            for form_item in formset:
                if form_item.cleaned_data.get('DELETE'):
                    # If delete checkbox is checked, delete the item
                    if form_item.instance.pk:
                        form_item.instance.delete()
                else:
                    item_name = form_item.cleaned_data.get('item_name')
                    quantity = form_item.cleaned_data.get('quantity')
                    no_of_unit = form_item.cleaned_data.get('no_of_unit')

                    if item_name:
                        try:
                            inventory_item = inventory.objects.get(item_name=item_name)
                            inventory_item.quantity -= quantity
                            inventory_item.no_of_unit -= no_of_unit
                            inventory_item.save()
                        except inventory.DoesNotExist:
                            inventory_item = inventory(item_name=item_name, quantity=-quantity)
                            inventory_item.save()

                        # Save each MRItem form with the corresponding MR instance
                        form_item.instance.MR_no = MR_instance
                        form_item.save()

            return redirect('create_MR')

        else:
            # Return the form errors if form or formset is invalid
            form_errors = dict(form.errors.items())
            formset_errors = {f"formset_{i}": dict(form_item.errors) for i, form_item in enumerate(formset) if form_item.errors}
            errors = {**form_errors, **formset_errors}
            return JsonResponse({'form_errors': errors}, status=400)

    else:
        form = MRForm()
        formset = MRFormSet(prefix="items")

    return render(request, 'create_mr.html', {'form': form, 'formset': formset, 'recieved_from': recieved_from, 'recieved_to': recieved_to})

@login_required(login_url="login_user")
def edit_parent_and_children(request, MR_no):
    parent = get_object_or_404(MR, MR_no=MR_no)
    if request.method == 'POST':
        parent_form = MRForm(request.POST, instance=parent)
        child_formset = MRItemForm(request.POST, queryset=parent.children.all())

        if parent_form.is_valid() and child_formset.is_valid():
            parent_form.save()
            child_formset.save()
            return redirect('some-view-name')
    else:
        parent_form = MRItemForm(instance=parent)
        child_formset = MRItemForm(queryset=parent.children.all())

    context = {
        'parent_form': parent_form,
        'child_formset': child_formset,
    }

    return render(request, 'edit_mr.html', context )

    

@login_required(login_url="login_user")
def display_MR(request):
    mr_list = MR.objects.all()
    mr_list = mr_list.order_by('MR_no')

    mrs_data = []
    for mr in mr_list:

        items = MR_item.objects.filter(MR_no=mr.MR_no)

        mr_data = {
                'MR_no': mr.MR_no,
                'date': mr.date,  # Assuming 'date' is a field in CosmicOrder
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

@login_required(login_url="login_user")
def display_inventory(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)

        if form.errors:
            print(form.errors)

        if form.is_valid():
            form.save()
            return redirect('display_inventory')
    
    mr_names = set(inventory.objects.values_list('item_name', flat=True))
    
    form = InventoryItemForm()

    names_a = set(inventory_GRN_items.objects.values_list('item_name', flat=True))
    names_b = set(inventory_MR_items.objects.values_list('item_name', flat=True))
    names_c = set(opening_balance.objects.values_list('item_name', flat=True))
    names_d = set(inventory_DN_items.objects.values_list('item_name', flat=True))

    all_names = names_a.union(names_b).union(names_c).union(names_d)

    for name in all_names:
        # Get the quantity from each model
        if name in mr_names:
            quantity_a = inventory_GRN_items.objects.filter(item_name=name).first()
            quantity_b = inventory_MR_items.objects.filter(item_name=name).first()
            quantity_c = opening_balance.objects.filter(item_name=name).first()
            quantity_d = inventory_DN_items.objects.filter(item_name = name).first()

            # Initialize the quantities or set to 0 if not found
            quantity_a_value = quantity_a.total_quantity if quantity_a else 0
            quantity_b_value = quantity_b.total_quantity if quantity_b else 0
            quantity_c_value = quantity_c.quantity if quantity_c else 0
            quantity_d_value = quantity_d.total_quantity if quantity_d else 0

            units_a_value = quantity_a.total_no_of_unit if quantity_a else 0
            units_b_value = quantity_b.total_no_of_unit if quantity_b else 0
            units_c_value = quantity_c.no_of_unit if quantity_c else 0
            units_d_value = quantity_d.total_no_of_unit if quantity_d else 0
            
            # Calculate the result: Subtract ModelA and ModelC, and add ModelB
            result_quantity =  quantity_c_value - quantity_b_value +  quantity_a_value - quantity_d_value
            result_units = units_c_value - units_b_value + units_a_value - units_d_value
            
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

@login_required(login_url="login_user")
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

@login_required(login_url="login_user")
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

@login_required(login_url="login_user")
def display_single_mr(request, MR_no):
    if request.method == 'GET':
        try:
            # Fetch the MR object using the URL parameter
            mr = get_object_or_404(MR, MR_no=MR_no)
            
            # Fetch related MR_items for the MR
            mr_items = MR_item.objects.filter(MR_no=MR_no)
            
            context = {
                'mr_item': mr_items,
                'my_mr': mr,
            }
        except Exception as e:
            # Handle any unexpected exceptions gracefully
            context = {
                'mr_item': [],
                'my_mr': None,
                'error_message': f"An error occurred: {str(e)}",
            }
        
        return render(request, 'display_single_mr.html', context)

@login_required(login_url="login_user")
def export_mr(request):

    # my_mr_items = MR_item.objects.all().order_by('item_name')

    # for item in my_mr_items:
    #     mr_details = get_object_or_404(MR, MR_no=item.MR_no)
    items = MR_item.objects.select_related('MR_no').all().order_by('item_name','MR_no__date')
    # my_inventory = inventory.objects.all()

    context = {
        'items':items,
        # 'my_inventory':my_inventory
        # 'detail':mr_details
    }
    return render(request, 'export_mr.html', context)

@login_required(login_url="login_user")
def export_mr_pdf(request):
    # Create a workbook and add a worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'MR'

    # Add headers to the worksheet
    headers = ['MR Date', 'Item Name', 'MR No', 'Quantity', 'No of Units']
    worksheet.append(headers)

    # Filter data based on request parameters
    selected_month = request.GET.get('month')
    selected_branch = request.GET.get('branch')
    
    # Replace with your actual query
    items = MR_item.objects.select_related('MR_no').all().order_by('item_name','MR_no__date')

    # Apply filters if provided
    if selected_month:
        items = items.filter(MR_no__date__month=selected_month)
    if selected_branch:
        items = items.filter(MR_no__branch=selected_branch)

    if items.exists():
        month_year = items.first().MR_no.date.strftime("%B %Y")  # Example format: "August 2024"
    else:
        month_year = "N/A"

    # Add the title to the worksheet
    title = f"List of MR in the Month {month_year}"
    worksheet.merge_cells('A1:E1')  # Merge cells for the title
    worksheet['A1'] = title
    worksheet['A1'].font = openpyxl.styles.Font(size=14, bold=True)  # Set font size and bold

    worksheet['A2'] = 'Date'
    worksheet['B2'] = 'Description'
    worksheet['C2'] = 'MR No'
    worksheet['D2'] = 'Quantity'
    worksheet['E2'] = 'No of Unit'


    # Variables to keep track of totals
    current_item_name = None
    total_quantity = 0
    total_no_of_units = 0

    for item in items:
        if item.item_name != current_item_name:
            # If moving to a new item name, append totals of the previous item
            if current_item_name is not None:
                worksheet.append([
                    # '',  # Empty MR Date for totals row
                    'Total',
                    '',
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
            item.MR_no.date.strftime("%d/%m/%Y"),  # Adjust based on your model's date field
            item.item_name,
            item.MR_no.MR_no,  # Adjust based on your model's MR number field
            item.quantity,
            item.no_of_unit
        ])

    # Append the totals for the last group of items
    if current_item_name is not None:
        worksheet.append([
                    # '',  # Empty MR Date for totals row
                    'Total',
                    '',
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

@login_required(login_url="login_user")
def get_date(item):
    if hasattr(item, 'GRN_no') and item.GRN_no:
        return getattr(item.GRN_no, 'date', None)
    elif hasattr(item, 'MR_no') and item.MR_no:
        return getattr(item.MR_no, 'date', None)
    return None

@login_required(login_url="login_user")
def stock_card(request):
    selected_item = request.GET.get('item_name')
    items = inventory.objects.all()

    print('selected_item', selected_item)

    # Fetch items and related dates
    grn_items = GRN_item.objects.filter(item_name=selected_item).select_related('GRN_no')
    mr_items = MR_item.objects.filter(item_name=selected_item).select_related('MR_no')

    for item in mr_items:
        print(f"MR Item ID: {item.MR_no}, Date: {item.MR_no.date}")

    for item in grn_items:
        date = getattr(item.GRN_no, 'date', 'No date available')
        print(f"GRN Item ID: {item.GRN_no}, Date: {date}")

    sorted_grn_items = sorted(
        grn_items,
        key=lambda item: getattr(item.GRN_no, 'date', None) if hasattr(item, 'GRN_no') else None,
    )
    
    sorted_mr_items = sorted(
        mr_items,
         key=lambda item: getattr(item.MR_no, 'date', None) if hasattr(item, 'MR_no') else None

    )

    combined_items = list(chain(sorted_grn_items, sorted_mr_items))

    sorted_combined_items = sorted(
        combined_items,
        key=get_date
    )

    print(combined_items)

    for item in sorted_combined_items:
        if hasattr(item, 'GRN_no'):
            print(f"Sorted GRN Item ID: {item.GRN_no}, Date: {item.GRN_no.date if item.GRN_no else 'No date'}")
        elif hasattr(item, 'MR_no'):
            print(f"Sorted MR Item ID: {item.MR_no}, Date: {item.MR_no.date if item.MR_no else 'No date'}")

    # Get the opening balance, or default to 0 if it doesn't exist
    opening_balance_obj = opening_balance.objects.filter(item_name=selected_item).first()
    opening_balances = opening_balance_obj.quantity if opening_balance_obj else 0

    current_balance = opening_balances
    for item in sorted_combined_items:
        if hasattr(item, 'GRN_no'):  # If it's a GRN_item
            item.received = item.quantity
            current_balance += item.received
            item.balance = current_balance
        elif hasattr(item, 'MR_no'):  # If it's a MR_item
            item.issued = item.quantity
            current_balance -= item.issued
            item.balance = current_balance

    context = {
        'orders': sorted_combined_items,
        'opening_balance': opening_balances,
        'items': items,
    }

    return render(request, 'stock_card.html', context)

def inventory_chart(request):
    # Fetch all inventory items for the first chart
    inventory_items = inventory.objects.all()

    # Prepare data for the all-items chart
    item_names = [item.item_name for item in inventory_items]
    quantities = [item.quantity for item in inventory_items]

    # Create a Plotly bar chart for all items
    fig_all_items = go.Figure(
        data=[
            go.Bar(x=item_names, y=quantities, marker_color='blue')
        ],
        layout=go.Layout(
            title="Inventory Quantities for All Items",
            xaxis_title="Item Name",
            yaxis_title="Quantity"
        )
    )

    # Generate the plot div for all items
    chart_all_items_div = plot(fig_all_items, output_type='div')

    # Handle the quantity change chart for the selected item
    selected_item = request.GET.get('item_name', None)
    chart_quantity_change_div = None

    if selected_item:
        # Fetch all MR_items for the selected item
        item_records = MR_item.objects.filter(item_name=selected_item).select_related('MR_no')
        
        # Prepare the data for the second chart
        dates = [record.MR_no.date for record in item_records]
        quantities_over_time = [record.quantity for record in item_records]

        # Create a Plotly line chart for quantity change over time
        fig_quantity_change = go.Figure(
            data=[
                go.Scatter(x=dates, y=quantities_over_time, mode='lines+markers', name=selected_item)
            ],
            layout=go.Layout(
                title=f"Quantity Change Over Time for {selected_item}",
                xaxis_title="Date",
                yaxis_title="Quantity"
            )
        )

        # Generate the plot div for quantity change
        chart_quantity_change_div = plot(fig_quantity_change, output_type='div')

    # Render the template
    return render(request, 'inventory_chart.html', {
        'inventory_items': inventory_items,
        'chart_all_items_div': chart_all_items_div,
        'chart_quantity_change_div': chart_quantity_change_div
    })
