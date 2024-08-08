from django.shortcuts import render
from .models import *
from django.forms import formset_factory
from .forms import *
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
import uuid
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from MR.models import *
from .decorators import allowed_users

# Create your views here.
# @login_required(login_url='login_user')
# @allowed_users(allowed_roles=['admin'])
def create_fgrn(request):
    if request.method == 'POST':
        form = FGRNForm(request.POST)
        
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
    form = FGRNForm()
    formset = formset_factory(FGRNItemForm, extra= 1)
    formset = formset(prefix="items")
    # print(formset)
    items = items_list.objects.all()
    context = {
            'my_item':items,
            'form': form, 
            'formset': formset
    }
    return render(request,'create_fgrn.html',context)

def create_fgrn_items(request):
    if request.method == 'POST':
        formset = formset_factory(FGRNItemForm, extra=1 , min_num= 1)
        formset = formset(request.POST or None, prefix="items")

        if formset.errors:
            print(formset.errors)

        non_empty_forms = [form for form in formset if form.cleaned_data.get('item_name')]
        pr_no = request.POST.get('FGRN_no')
        print(pr_no,"pr")
        if non_empty_forms:
            if formset.is_valid():
                FGRN_instance = FGRN.objects.get(FGRN_no = pr_no)
                final_quantity = 0.0
                total_bag = 0.0
                total_crt  = 0.0
                total_pkg = 0.0
                for form in non_empty_forms:
                    form.instance.FGRN_no = FGRN_instance
                   
                    quantity = form.cleaned_data['quantity']
                    unit_type = form.cleaned_data['unit_type']
                    no_of_unit = form.cleaned_data['no_of_unit']
                    description = form.cleaned_data['description']

                    finished_item = finished_goods.objects.get(item_name = description)
                    if unit_type == 'Bag':
                        total_bag += no_of_unit
                    elif unit_type == 'Crt':
                        total_crt += no_of_unit
                    elif unit_type == 'Pkg':
                        total_pkg += no_of_unit
                    final_quantity += quantity
                    finished_item.quantity += quantity
                    finished_item.no_of_unit += no_of_unit
                    finished_item.save()
                    form.save()
         
                    FGRN_instance.total_quantity = final_quantity
                    FGRN_instance.save()
                    
                    
            else:
                print(formset.data,"nval")
                errors = dict(formset.errors.items())
                return JsonResponse({'form_errors': errors}, status=400)
        
            pr_form = FGRNForm(prefix="orders")
            formset = formset_factory(FGRNItemForm, extra=1)
            formset = formset(prefix="items")

            context = {
                'pr_form': pr_form,
                'formset': formset,
                # 'message':success_message,
            }
            return render(request, 'create_fgrn.html', context)
    else:
       
        formset = formset_factory(FGRNItemForm, extra=1)
        formset = formset(prefix="items")

    context = {
        'formset': formset,
    }
    return render(request, 'create_fgrn.html', context)

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

def display_single_fgrn(request):
    if request.method == 'GET':
        fgrn_no = request.GET['FGRN_no']
        
        try:
            fgrns = FGRN.objects.get(FGRN_no=fgrn_no)
            fgrn_items = FGRN_item.objects.all()
            fgrn_items = fgrn_items.filter(FGRN_no=fgrn_no)
            print(fgrn_items)

            if fgrn_items.exists():
                print(fgrn_items,"yes")
                context = {
                            'fgrn_item': fgrn_items,
                            'my_fgrn': fgrns,
                        }
                return render(request, 'display_single_fgrn.html', context)
        
        except FGRN.DoesNotExist:
                fgrns = None 
       
        print("no")
        
        context = {
                        'my_fgrn': fgrns,
                    }
    return render(request, 'display_single_fgrn.html')


def display_goods(request):
    goods = finished_goods.objects.all()
    return render(request, 'display_goods.html',{'goods':goods})
