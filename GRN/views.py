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
def is_admin(user):
    return user.is_superuser
# Create your views here.

def grn_number(request):
    context = {}
    if request.method == 'GET':
        grn_form = GRNForm(prefix="purchases")
        formset = formset_factory(GRNItemForm, extra=1)
        formset = formset(prefix="GRN_items")
        number = request.GET['grn_number']
        names = purchase_orders.objects.all()
        # try:
        #     order = purchase_orders.objects.get(PR_no=number)
        #     pr_items = PR_item.objects.all()
        #     pr_items = pr_items.filter(PR_no=number)
        #     print(pr_items)
        # except purchase_orders.DoesNotExist:
        #     # If it's not found in purchase_orders, try searching in import_PR
           
        #     order = None 
        # print(pr_items,"ittt")
        context = {
            # 'order': order,
            # 'pr_items':pr_items,
            'grn_form': grn_form,
            'formset': formset,
            'names':names
        }
        return render(request, 'create_grn.html', context)
    return render(request, 'trial_grn.html', context)

def create_trial_grn(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'trial_grn.html', context)
    if request.method == 'POST':
        grn_form = GRNForm(request.POST )
       
        
        print(grn_form.data,"y")
        if grn_form.errors:
            print(grn_form.errors)  
       
        if grn_form.is_valid():
            print("yes 1")
            pr_no = grn_form.cleaned_data['PR_no']
           
            if pr_no != None:
                print(pr_no)
                pr = purchase_orders.objects.get(PR_no = pr_no)
                print(pr,"pr")
                
                if pr.status == "Approved" or pr.status == "approved":
                    grn = grn_form.save()
                    print("yes")
                else:
                    error_message =  "PR is not Approved."
                    print("not")
                    return render(request, 'create_grn.html', {'error_message': error_message})
            else:
                print("?")
                grn = grn_form.save()
            return render(request, 'trial_submit_grn.html')
    
    grn_form = GRNForm(prefix="purchases")
    formset = formset_factory(GRNItemForm, extra=1)
    formset = formset(prefix="GRN_items")
    items = PR_item.objects.all()
    context = {
        'grn_form': grn_form,
        'formset': formset,
        'items':items
    }
    return render(request, 'trial_submit_grn.html', context)


def create_grn(request):
    
    if request.method == 'POST':
        grn_form = GRNForm(request.POST )
       
        
        print(grn_form.data,"y")
        if grn_form.errors:
            print(grn_form.errors)  
       
        if grn_form.is_valid():
            print("yes 1")
            # pr_no = grn_form.cleaned_data['PR_no']
            grn = grn_form.save()

           
        else:
            print("?")
            grn = grn_form.save()
        return render(request, 'create_grn.html')
    
    grn_form = GRNForm(prefix="purchases")
    formset = formset_factory(GRNItemForm, extra=1)
    formset = formset(prefix="GRN_items")
    items = PR_item.objects.all()
    context = {
        'grn_form': grn_form,
        'formset': formset,
        'items':items
    }
    return render(request, 'create_grn.html', context)

def create_grn_items(request):
    
    if request.method == 'POST':
        formset = formset_factory(GRNItemForm, extra=1, min_num=1)
        formset = formset(request.POST or None,prefix="GRN_items")
        print(formset.data,"r")
      
        if formset.errors:
                        print(formset.errors) 
        # Check if 'PR_no' field is empty in each form within the formset
        non_empty_forms = [form for form in formset if form.cleaned_data.get('item_name')]

        print(non_empty_forms,"forms")
        if non_empty_forms:
            if formset.is_valid():
                # pr_no = request.POST.get('PR_no')
                # pr = purchase_orders.objects.get(PR_no = pr_no)
                grn_no = request.POST.get('GRN_no')
                grn = GRN.objects.get(GRN_no = grn_no)
                for form in non_empty_forms:
                    # form.instance.PR_no = pr
                    form.instance.GRN_no = grn
                    print("yessir")
                    
                    item_name = form.cleaned_data['item_name']
                    # item = item.filter(item_name = items).first()
                    # code = item.hs_code
                    # form.instance.hs_code = code
                    quantity = form.cleaned_data['quantity']
                    # items = PR_item.objects.get(item_name=item_name)
                    
                    # print(items,"r")
                    # items.remaining = items.remaining - quantity

                    # items.save()

                    # try:
                    #     inventory_item = inventory.objects.get(item_name = item_name)
                    #     inventory_item.quantity += quantity
                    #     inventory_item.save()
                    # except inventory.DoesNotExist:
                    #     print(item_name, quantity, "yes")
                    #     inventory_item = inventory(item_name = item_name, quantity = quantity)
                    #     inventory_item.save()

                    form.save()
                    
                grn.save()
                               
                    
                    
                context = {
        'formset': formset,
        # 'code': code,
                          }

            return render(request,'create_grn_items.html', context)
    else:
       
        formset = formset_factory(GRNItemForm, extra=1)
        formset = formset(prefix="GRN_items")

    context = {
        'formset': formset,
    }
    return render(request, 'create_grn_items.html', context)

# def create_grn_items(request):
    
#     if request.method == 'POST':
#         formset = formset_factory(GRNItemForm, extra=1, min_num=1)
        
#         formset = formset(request.POST or None,prefix="items")
        
#         if formset.errors:
#             print(formset.errors)   
        
#         # Check if 'PR_no' field is empty in each form within the formset
#         for form in formset:
#             print(form,"form")
#         non_empty_forms = [form for form in formset if form.cleaned_data.get('item_name')]
#         # vat_is_checked = request.POST.get('vat_is_checked')
        
#         if non_empty_forms:
#             if formset.is_valid():
#                 grn_no = request.POST.get('GRN)no')
#                 print(grn_no)
#                 grn = GRN.objects.get(GRN_no = grn_no)
#                 for form in non_empty_forms:
#                     # if vat_is_checked:
#                     #     print("yessay")
#                     #     form.instance.total_price = form.cleaned_data['before_vat']
#                     form.instance.quantity = form.cleaned_data['quantity']
#                     form.instance.GRN_no = grn
#                     items = form.cleaned_data['item_name']
#                     item = HS_code.objects.all()
#                     item = item.filter(item_name = items).first()
#                     code = item.hs_code
#                     form.instance.hs_code = code
#                     # before_vat_price += float(form.cleaned_data['before_vat'])
#                     # final_quantity += form.cleaned_data['quantity']
#                     # if form.cleaned_data['total_price']:
#                     #     final_price += float(form.cleaned_data['total_price'])
                    
#                     form.save()
#                 # print(final_price,before_vat_price)
                
#                 # pr.total_quantity = final_quantity
#                 # pr.remaining = final_quantity
#                 grn.save()    
#             grn_form = GRNForm(prefix="purchases")
#             formset = formset_factory(PRItemForm, extra=1)
#             formset = formset(prefix="items")

#             context = {
#                 'grn_form': grn_form,
#                 'formset': formset,
#                 'code': code,
#             }

#             return render(request, 'create_grn.html', context)
#     else:
       
#         formset = formset_factory(GRNItemForm, extra=1)
#         formset = formset(prefix="items")

#     context = {
#         'formset': formset,
#     }
#     return render(request, 'create_grn_items.html', context)

def display_items(request,pr_no):
    if request.method == 'GET':
        pr_no = pr_no
        my_order = get_object_or_404(purchase_orders, PR_no=pr_no)
        items = PR_item.objects.all()
        items = items.filter(PR_no=pr_no)
        if items.exists():
            context = {
                        'items': items,
                        'my_order': my_order,
                    }
            return render(request, 'my_items.html', context)
            
        else:
            print("none")
            return render(request, 'single_delivery.html', context)

    else:
        context = {
                        'deliveries': deliveries,
                    }
        return render(request, 'single_delivery.html', context)



def display_search_items(request):
    if request.method == 'GET':
        items = PR_item.objects.all()
        items = items.order_by('PR_no')
        context = {
                    'my_items': items,
                    #'my_imports': import_prs,
                }
          
        return render(request, 'display_items.html', context)

def display_grn(request):
    if request.method == 'GET':
        orders = GRN.objects.all().order_by('GRN_no')
        
        return render(request, 'display_grn.html', {'my_order':orders})

        my_order = get_object_or_404(purchase_orders, PR_no=pr_no)
        my_order = get_object_or_404(purchase_orders, PR_no=pr_no)
   
def display_grns(request):
    if request.method == 'GET':
        grn_no = request.GET['GRN_no']
        orders = GRN.objects.get(GRN_no=grn_no)
        # pr_no = orders.PR_no.PR_no
        # pr_items = PR_item.objects.all()
        grn_items = GRN_item.objects.all()
        grn_items = grn_items.filter(GRN_no=grn_no)
        if grn_items.exists():
            context = {
                        'grn_items': grn_items,
                        'my_order': orders,
                    }
            return render(request, 'display_grns.html', context)
        context = {
                        
                        'my_order': orders,
                    }
    return render(request, 'display_grns.html', context)

def search_prs(request,pr_no):
    
    if request.method == 'GET':
        pr_no = pr_no
        my_order = get_object_or_404(purchase_orders, PR_no=pr_no)
        
   
        # If the order exists,
        if my_order:
            print(my_order)
            print('yes')
            context = {
                        'my_order': my_order,
                    }
            return render(request, 'single_pr.html', context)

        else:
            print("none")
            return render(request, 'single_pr.html', context)

    else:
        context = {
                        'my_order': my_order,
                    }
        return render(request, 'display_pr.html')
    
# def search_grn(request,grn_no):
    
#     if request.method == 'GET':
#         grn_no = grn_no
#         my_order = get_object_or_404(GRN, grn=grn_no)
        
   
#         # If the order exists,
#         if my_order:
#             print(my_order)
#             print('yes')
#             context = {
#                         'my_order': my_order,
#                     }
#             return render(request, 'single_pr.html', context)

#         else:
#             print("none")
#             return render(request, 'single_pr.html', context)

#     else:
#         context = {
#                         'my_order': my_order,
#                     }
#         return render(request, 'display_pr.html')

def search_customer(request):
    if request.method == 'GET':
        customer_name = request.GET['vendor_name']
        print(customer_name,"name")
        #my_order = get_object_or_404(orders, customer_name=customer_name)
        my_order = purchase_orders.objects.filter(vendor_name__icontains= customer_name)
        
        if my_order.exists():
            
            context = {
                        'my_order': my_order,
                    }
            return render(request, 'customer_details_page.html', context)
            
        else:
            print("none")
            return render(request, 'customer_details_page.html', context)

    else:
        context = {
                        'my_order': my_order,
                    }
        return render(request, 'customer_details_page.html', context)

def search_items(request):
    if request.method == 'GET':
        item_name = request.GET['item_name']
        #print(customer_name,"name")
        #my_order = get_object_or_404(orders, customer_name=customer_name)
        my_items = PR_item.objects.filter(item_name__icontains= item_name)
        
        if my_items.exists():
            
            context = {
                        'my_items': my_items,
                    }
            return render(request, 'item_details_page.html', context)
            
        else:
            print("none")
            return render(request, 'item_details_page.html', context)

    else:
        context = {
                        'my_order': my_order,
                    }
        return render(request, 'item_details_page.html', context)


def search_pr_item(request):
    if request.method == 'GET':
        pr_no = request.GET['PR_no']
        my_order = get_object_or_404(purchase_orders, PR_no= pr_no)
        pr_items = PR_item.objects.all()
        pr_items = pr_items.filter(PR_no=pr_no)
        if pr_items.exists():
            context = {
                        'pr_items': pr_items,
                        'my_order': my_order,
                    }
            return render(request, 'print_pr.html', context)
            
        else:
            print("none")
            return render(request, 'print_pr.html', context)

    else:
        context = {
                        'deliveries': deliveries,
                    }
        return render(request, 'print_pr.html', context)

def print_format(request):
    orders = purchase_orders.objects.get(PR_no="123")
    context = {
                'my_order': orders,
            }
    return render(request, 'print_format.html', context)

def print_pr(request):
    if request.method == 'GET':
        pr_no = request.GET['PR_no']
        
        try:
            orders = purchase_orders.objects.get(PR_no=pr_no)
            pr_items = PR_item.objects.all()
            pr_items = pr_items.filter(PR_no=pr_no)
            print(pr_items)
        except purchase_orders.DoesNotExist:
            # If it's not found in purchase_orders, try searching in import_PR
            
            order = None 
       
        print("no")
        if pr_items.exists():
            print(pr_items,"yes")
            context = {
                        'pr_items': pr_items,
                        'my_order': orders,
                    }
            return render(request, 'print_pr.html', context)
        context = {
                        
                        'my_order': orders,
                    }
    return render(request, 'print_pr.html', context)


def search_grns(request):
    if request.method == 'GET':
        PR_no = request.GET['PR_no']
        my_order = get_object_or_404(purchase_orders, PR_no=PR_no)
        delivery_qs = GRN.objects.all()
        deliveries = delivery_qs.filter(PR_no=PR_no)
        if deliveries.exists():
            context = {
                        'deliveries': deliveries,
                        'my_order': my_order,
                    }
            return render(request, 'single_GRN.html', context)
            
        else:
            print("none")
            return render(request, 'single_GRN.html', context)
    
    
    else:
        context = {
                        'deliveries': deliveries,
                    }
        return render(request, 'single_delivery.html', context)