from django.shortcuts import render
from .models import *
from django.forms import formset_factory
from .forms import *
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
import uuid
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from MR.models import *
from .decorators import allowed_users
from DN.models import delivery_items, inventory_DN_items, inventory_order_items
from GRN.models import inventory_GRN_items

@login_required(login_url="login_user")
def create_fgrn(request):
    FGRNFormSet = formset_factory(FGRNItemForm, extra=1)
    recieved_by = sorted(set(FGRN.objects.values_list('recieved_by', flat=True)))
    
    if request.method == 'POST':
        form = FGRNForm(request.POST)
        formset = FGRNFormSet(request.POST, prefix="items")

        if form.is_valid() and formset.is_valid():
            # Save the MR form
            FGRN_instance = form.save()

            # Process the formset
            for form_item in formset:
                if form_item.cleaned_data.get('DELETE'):
                    # If delete checkbox is checked, delete the item
                    if form_item.instance.pk:
                        form_item.instance.delete()
                else:
                    description = form_item.cleaned_data.get('description')
                    quantity = form_item.cleaned_data.get('quantity')
                    no_of_unit = form_item.cleaned_data.get('no_of_unit')

                    if description:
                        try:
                            inventory_item = finished_goods.objects.get(item_name=description)
                            inventory_item.quantity += quantity
                            inventory_item.no_of_unit += no_of_unit
                            inventory_item.save()
                        except finished_goods.DoesNotExist:
                            inventory_item = finished_goods(item_name=description, quantity=quantity)
                            inventory_item.save()

                        # Save each MRItem form with the corresponding MR instance
                        form_item.instance.FGRN_no = FGRN_instance
                        form_item.save()

            return redirect('create_fgrn')

        else:
            # Return the form errors if form or formset is invalid
            form_errors = dict(form.errors.items())
            formset_errors = {f"formset_{i}": dict(form_item.errors) for i, form_item in enumerate(formset) if form_item.errors}
            errors = {**form_errors, **formset_errors}
            return JsonResponse({'form_errors': errors}, status=400)

    else:
        form = FGRNForm()
        formset = FGRNFormSet(prefix="items")

    print(recieved_by)

    return render(request, 'create_fgrn.html', {'form': form, 'formset': formset, 'recieved_by': recieved_by})

@login_required(login_url="login_user")
def display_FGRN(request):
    mr_list = FGRN.objects.all()
    mr_list = mr_list.order_by('FGRN_no')

    mrs_data = []
    for mr in mr_list:

        items = FGRN_item.objects.filter(FGRN_no=mr.FGRN_no)

        mr_data = {
                'FGRN_no': mr.FGRN_no,
                'date': mr.date,  # Assuming 'date' is a field in CosmicOrder
                'FGRN_items': items,  # Assuming a related name 'order_items' on CosmicOrder pointing to OrderItem
                'recieved_from': mr.recieved_from,  # Assuming 'PR_before_vat' is a field in CosmicOrder
                  # A  # Assuming 'status' is a field in CosmicOrder
            }
        mrs_data.append(mr_data)

    context = {
        'my_order': mrs_data,
        'mr_list': mr_list
    }

    return render(request,'display_fgrn.html', context)

@login_required(login_url="login_user")
def display_single_fgrn(request, FGRN_no):
    if request.method == 'GET':
        try:
            # Fetch the MR object using the URL parameter
            fgrn_no = get_object_or_404(FGRN, FGRN_no=FGRN_no)

            fgrns = FGRN.objects.get(FGRN_no = fgrn_no)
            
            # Fetch related MR_items for the MR
            fgrn_items = FGRN_item.objects.filter(FGRN_no=fgrn_no)
            
            context = {
                            'fgrn_item': fgrn_items,
                            'my_fgrn': fgrns,
                        }
        except Exception as e:
            # Handle any unexpected exceptions gracefully
            context = {
                'fgrn_items': [],
                'fgrns': None,
                'error_message': f"An error occurred: {str(e)}",
            }
        
        return render(request, 'display_single_fgrn.html', context)

@login_required(login_url="login_user")
def display_goods(request):
    # Fetch all DN items
    dn_items = inventory_DN_items.objects.all().order_by('item_name')

    # Get all groups from inventory_order_items
    order_items_with_groups = inventory_order_items.objects.values('item_name', 'group')

    # Create a mapping of groups to item names
    group_to_items = {}
    for item in order_items_with_groups:
        group = item['group']
        item_name = item['item_name']
        if group:  # Ensure group is not empty or null
            if group not in group_to_items:
                group_to_items[group] = []
            group_to_items[group].append(item_name)

    # Iterate through DN items to calculate
    for dn_item in dn_items:
        item_name = dn_item.item_name

        # Check if item has a group name, else use item_name itself
        group_name = None
        for group, item_names in group_to_items.items():
            if item_name in item_names:
                group_name = group
                break
        
        # If no group is found, use the item_name itself
        if not group_name:
            group_name = item_name

        # Initialize totals for the group/item
        total_quantity_a = 0
        total_quantity_b = 0
        total_quantity_c = 0

        total_units_a = 0
        total_units_b = 0
        total_units_c = 0

        # Aggregate values for all items in the group or for the item itself
        if group_name == item_name:
            # Item does not belong to a group, calculate based on the item itself
            quantity_a = inventory_FGRN_items.objects.filter(item_name=item_name).first()
            quantity_b = inventory_DN_items.objects.filter(item_name=item_name).first()
            quantity_c = FGRNopening_balance.objects.filter(item_name=item_name).first()

            total_quantity_a = quantity_a.total_quantity if quantity_a else 0
            total_quantity_b = quantity_b.total_quantity if quantity_b else 0
            total_quantity_c = quantity_c.quantity if quantity_c else 0

            total_units_a = quantity_a.total_no_of_unit if quantity_a else 0
            total_units_b = quantity_b.total_no_of_unit if quantity_b else 0
            total_units_c = quantity_c.no_of_unit if quantity_c else 0
        else:
            # If group exists, calculate for the group
            for item_name_in_group in group_to_items[group_name]:
                quantity_a = inventory_FGRN_items.objects.filter(item_name=item_name_in_group).first()
                quantity_b = inventory_DN_items.objects.filter(item_name=item_name_in_group).first()
                quantity_c = FGRNopening_balance.objects.filter(item_name=group_name).first()

                # Accumulate quantities
                total_quantity_a += quantity_a.total_quantity if quantity_a else 0
                total_quantity_b += quantity_b.total_quantity if quantity_b else 0
                total_quantity_c += quantity_c.quantity if quantity_c else 0

                # Accumulate units
                total_units_a += quantity_a.total_no_of_unit if quantity_a else 0
                total_units_b += quantity_b.total_no_of_unit if quantity_b else 0
                total_units_c += quantity_c.no_of_unit if quantity_c else 0

        # Calculate the final result for the group or item
        result_quantity = total_quantity_c - total_quantity_b + total_quantity_a
        result_units = total_units_c - total_units_b + total_units_a

        # Log the group or item being updated for debugging
        print(f"Updating or creating: {group_name} with result_quantity: {result_quantity} and result_units: {result_units}")

        # Update or create in finished_goods using the group name or item_name
        finished_goods.objects.update_or_create(
                item_name=name,
                defaults={'quantity': result_quantity,
                        'no_of_unit': result_units}
            )

    # Render the context
    items = finished_goods.objects.all().order_by('item_name')
    context = {
        'items': items,
    }

    return render(request, 'display_goods.html', context)

@login_required(login_url="login_user")
def fgrn_opening_balances(request):
    if request.method == 'POST':
        form = OpeningBalanceItemForm(request.POST)

        if form.errors:
            print(form.errors)

        if form.is_valid():
            form.save()
            return redirect('fgrn_opening_balance')
    
    form = OpeningBalanceItemForm()
    items = FGRNopening_balance.objects.all().order_by('item_name')    
    context = {
        'items':items,
        'form':form,
    }

    return render(request,'fgrn_opening_balance.html',context)

@login_required(login_url="login_user")
def display_FGRN_items(request):

    item_quantities = FGRN_item.objects.values('description').annotate(total_quantity=Sum('quantity'), total_no_of_unit=Sum('no_of_unit'))
  
    for item in item_quantities:
        inventory_FGRN_items.objects.update_or_create(
            item_name=item['description'],
            defaults={'total_quantity': item['total_quantity'],
                      'total_no_of_unit': item['total_no_of_unit']}
            
        )
        print(f"Name: {item['description']}, Total Quantity: {item['total_quantity']}, Total No of Unit: {item['total_no_of_unit']}")
    

    items = inventory_FGRN_items.objects.all().order_by('item_name')    
    print(items)
    context = {
        # 'total_quantity':item_quantities,
        'items':items,
        
    }

    return render(request,'display_FGRN_items.html',context)
