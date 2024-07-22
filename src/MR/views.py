from django.shortcuts import render
from .models import *
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
                    measurement_type = form.cleaned_data['measurement_type']
                    try:
                        inventory_item = inventory.objects.get(item_name = item_name)
                        inventory_item.quantity -= quantity
                        inventory_item.measurement_type = measurement_type
                        inventory_item.save()
                    except inventory.DoesNotExist:
                        print(item_name, quantity, measurement_type, "yes")
                        inventory_item = inventory(item_name = item_name, quantity = -quantity, measurement_type = measurement_type)
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
            return render(request, 'create_MR.html', context)
    else:
       
        formset = formset_factory(MRItemForm, extra=1)
        formset = formset(prefix="items")

    context = {
        'formset': formset,
    }
    return render(request, 'create_MR.html', context)

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
    items = inventory.objects.all()
    print(items)
    context = {
        'items':items,
        'form':form,
    }

    return render(request,'display_inventory.html',context)