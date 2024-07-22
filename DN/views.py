from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from .models import orders, delivery
from .forms import DeliveryForm, OrderForm
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.db.models import Q
from django.core.mail import send_mail
from datetime import datetime
from django.core import serializers
from django.db.models import Sum, Case, When, F, Value, IntegerField
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.functions import ExtractMonth,ExtractWeek
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.contrib import messages
from .models import *
# Create your views here.
@api_view(['GET','POST'])
def order_list(request):
    if request.method == 'GET':
        my_orders = orders.objects.all()
        serializer =  OrderSerializer(my_orders,many=True)
        return JsonResponse({"Orders":serializer.data})

    if request.method == 'POST':
        serializer = OrderSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

@api_view(['GET','POST'])
def delivery_list(request):
    if request.method == 'GET':
        my_deliveries = orders.objects.all()
        serializer =  DeliverySerializer(my_deliveries,many=True)
        return JsonResponse({"Deliveries":serializer.data})

    if request.method == 'POST':
        serializer = DeliverySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

def input_delivery(request):
    my_orders = orders.objects.all()
    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        delivery_number = request.POST['delivery_number']
        if delivery.objects.filter(delivery_number__icontains = delivery_number).exists():
            messages.error(request, 'Delivery Number already exists')
            return redirect('input_delivery')
        else: 
            if form.is_valid():
                # delivery = form
                delivery_number = form.cleaned_data['delivery_number']
                serial_no = form.cleaned_data['serial_no']
                delivery_quantity = form.cleaned_data['delivery_quantity']
                delivery_number = form.cleaned_data['delivery_number']
                order = orders.objects.get(serial_no=serial_no.serial_no)
                order.remaining = order.remaining - delivery_quantity
                if order.remaining < 0:
                    error_message = 'Over Delivery'
                    form.save()
                    order.save()
                    return render(request, 'input_delivery.html', {'form': form, 'error_message': error_message})
                else:
                    form.save()
                    order.save() 
                return redirect('input_delivery')
            if form.errors:
                print(form.errors)
    else:
        form = DeliveryForm()
    return render(request, 'input_delivery.html', {'form': form,'my_orders':my_orders})


#To display the delivery notes for a specific order number
def deliveries(request):
  my_orders = orders.objects.all()
  deliveries = []
  for order in my_orders:
    my_delivery = delivery.objects.filter(order_number=my_orders.order_number).first()
    if my_delivery:
      deliveries.append(my_delivery)

  context = {
    'orders': orders,
    'deliveries': deliveries,
  }

  return render(request, 'deliveries.html', context)

#for creating Orders
def input_orders(request):
    print(orders.objects.all()[1:10])
    my_orders = orders.objects.all()
    the_orders = orders.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
       
        if form.is_valid():
            order_number = form.cleaned_data['serial_no']
           
            # Save the value to the database
            form.instance.before_vat = float(form.instance.order_quantity) * float(form.instance.price) 
            form.instance.before_vat = round(form.instance.before_vat, 2)
            
            form.instance.total_price = float(form.instance.order_quantity) * float(form.instance.price) + (float(form.instance.order_quantity) * float(form.instance.price) * 0.15)
            form.instance.total_price = round(form.instance.total_price, 2)
            
            form.instance.withholding_amount = float(form.instance.before_vat * 0.02)
            form.instance.withholding_amount = round(form.instance.withholding_amount, 2)
            order = form.save()
            order.remaining = form.cleaned_data['order_quantity']
            order.save()
            return redirect('input_orders')
    
    else:
        
        form = OrderForm()
    return render(request, 'input_orders.html', {'form': form ,'orders':my_orders,'the_orders':the_orders})

def display_orders(request):
    my_orders = orders.objects.all()
    the_orders = orders.objects.all()
    my_customers = orders.objects.all()

    sort_param = request.GET.get('sort')

    # Sort the orders based on the selected parameter
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        the_orders = the_orders.filter(date__range=[start_date, end_date])
        the_orders = the_orders.order_by('date')
    elif sort_param == 'date':
        the_orders = the_orders.order_by('date')
    elif sort_param == 'customer name':
        the_orders = the_orders.order_by('customer_name')
    else :
        the_orders = the_orders.order_by('-serial_no')
    return render(request, 'display_orders.html', {'my_orders': my_orders,'the_orders': the_orders,'my_customers':my_customers})

def display_remaining(request):
    my_orders = orders.objects.filter(remaining__gt=0)
    return render(request, 'display_remaining.html', {'my_orders': my_orders})
    
def display_single_order(request, serial_no):
    my_order = get_object_or_404(orders, serial_no=serial_no)
    
    #deliveries = orders.delivery_set.prefetch_related('delivery_date')
    return render(request, 'single_order.html', {'my_order': my_order})

def display_delivery(request):
    my_customers = orders.objects.all()
    deliveries = delivery.objects.all()
    my_order = orders.objects.all()
    my_delivery = delivery.objects.all()
    # Join the two tables on the serial_no column
    sort_param = request.GET.get('sort')

    # Sort the orders based on the selected parameter
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Filter orders within the specified date range
    if start_date and end_date:
        my_delivery = my_delivery.filter(delivery_date__range=[start_date, end_date])
        my_delivery = my_delivery.order_by('delivery_date')
    elif sort_param == 'date':
        my_delivery = my_delivery.order_by('delivery_date')
    elif sort_param == 'customer_name':
        my_delivery = my_delivery.order_by('serial_no__customer_name')
    elif sort_param == 'delivery number':
        my_delivery = my_delivery.order_by('delivery_number')
    
    return render(request, 'display_delivery.html', {'my_delivery': my_delivery,'my_order':my_order,'my_customers':my_customers})

def search_customer(request):
    if request.method == 'GET':
        customer_name = request.GET['customer_name']
        #my_order = get_object_or_404(orders, customer_name=customer_name)
        my_order = orders.objects.filter(customer_name__icontains= customer_name)
        
        if my_order.exists():
            context = {
                        'my_order': my_order,
                    }
            return render(request, 'customer_details.html', context)
            
        else:
            print("none")
            return render(request, 'customer_details.html', context)

    else:
        context = {
                        'my_order': my_order,
                    }
        return render(request, 'customer_details.html', context)
# Create your views here.

def customer_date(request):
    customer_name = request.GET.get('customer_name')
    my_order = orders.objects.filter(customer_name__icontains= customer_name)
    my_delivery = delivery.objects.filter('serial_no__customer_name')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Filter orders within the specified date range
    if start_date and end_date:
        my_delivery = my_delivery.filter(delivery_date__range=[start_date, end_date])
        my_delivery = my_delivery.order_by('delivery_date')
    context = {
                    'my_orders': my_delivery,
                }
    if request.method == 'GET':
        customer_name = request.GET['customer_name']
        #my_order = get_object_or_404(orders, customer_name=customer_name)
        my_order = orders.objects.filter(customer_name__icontains= customer_name)
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        # Filter orders within the specified date range
        if start_date and end_date:
            my_order = my_order.filter(delivery_date__range=[start_date, end_date])
            my_order = my_order.order_by('delivery_date')
        context = {
                        'my_order': my_order,
                    }
    else:
        context = {
                        'my_order': my_order,
                    }
        return render(request, 'customer_details.html', context)
def search_orders(request):
    print("in")
    if request.method == 'GET':
        serial_no = request.GET['serial_no']

        # Get the order by serial number
        #my_order = orders.objects.filter(serial_no=serial_no)
        my_order = get_object_or_404(orders, serial_no=serial_no)
        # If the order exists,
        if my_order:
            print(my_order)
            print('yes')
            context = {
                        'my_order': my_order,
                    }
            return render(request, 'single_order.html', context)
            
        else:
            print("none")
            return render(request, 'single_order.html', context)

    else:
        context = {
                        'my_order': my_order,
                    }
        return render(request, 'display_orders.html')
# Create your views here.
def search_delivery(request):
    if request.method == 'GET':
        serial_no = request.GET['serial_no']
        my_order = get_object_or_404(orders, serial_no=serial_no)
        delivery_qs = delivery.objects.all()
        deliveries = delivery_qs.filter(serial_no=serial_no)
        if deliveries.exists():
            context = {
                        'deliveries': deliveries,
                        'my_order': my_order,
                    }
            return render(request, 'single_delivery.html', context)
            
        else:
            print("none")
            return render(request, 'single_delivery.html', context)
    
    
    else:
        context = {
                        'deliveries': deliveries,
                    }
        return render(request, 'single_delivery.html', context)

def search_customer_delivery(request):
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if request.method == 'GET':
        customer_name = request.GET.get('customer_name')
        my_order = orders.objects.filter(customer_name__icontains=customer_name)
        delivery_qs = delivery.objects.filter(serial_no__customer_name=customer_name)

        if start_date and end_date:
            # Parse the date strings to datetime objects
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            # Apply date filtering
            delivery_qs = delivery_qs.filter(delivery_date__range=[start_date, end_date])

        # Order the filtered deliveries
        my_delivery = delivery_qs.order_by('delivery_date')

        context = {
            'deliveries': my_delivery,
            'my_order': my_order,
            'customer_name': customer_name,
        }
        return render(request, 'customer_delivery.html', context)
    else:
        context = {
            'deliveries': [],
        }
        return render(request, 'customer_delivery.html', context)

def dashboard_with_pivot(request):
    return render(request, 'analytics_dashboard.html', {})


def pivot_data(request):
    dataset = orders.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)

def dashboards(request):
    my_order = orders.objects.all()
    limit = 10
    chart_type = 'bar'
    if request.method == 'GET':
        limit = int(request.GET.get('limit', 10))
        items = int(request.GET.get('items', 10))
        chart_type = request.GET.get('chart_type', 'bar')
        if limit <= 0 or items<= 0:
            return HttpResponseBadRequest("Invalid limit value. Please provide a positive integer for the 'limit' parameter.")
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Filter orders within the specified date range
    if start_date and end_date:
        my_order = my_order.filter(date__range=[start_date, end_date])
        my_order = my_order.order_by('date')

    data = orders.objects.values('customer_name').annotate(total_sales=Sum('total_price'))
    data = sorted(data,key=lambda x:x['total_sales'],reverse = True)
    top_customers = data[:limit]

    item_data = orders.objects.values('description').annotate(total_items=Sum('order_quantity'))
    item_data = sorted(item_data,key = lambda x:x['total_items'], reverse = True)
    top_items = item_data[:items]
    # Create a list of dictionaries with customer name and total sales
    revenue_data = my_order.annotate(month=ExtractMonth('date'),week=ExtractWeek('date')).values('month', 'week').annotate(total_revenue=Sum('total_price')).order_by('month', 'week')
    # weekly_sales = my_order.annotate(week=ExtractWeek('date')).values('week').annotate(total_sales=Sum('total_price')).order_by('week')
    monthly_sales = my_order.annotate(month=ExtractMonth('date')).values('month').annotate(total_monthly_sales=Sum('total_price')).order_by('month')
    
    # Extract data and labels
    revenue_labels = [revenue['month'] for revenue in revenue_data]
    revenue_data = [revenue['total_revenue'] for revenue in revenue_data]
    # weekly_revenue_labels = [revenue['week'] for revenue in weekly_sales]
    # weekly_revenue_data = [revenue['total_sales'] for revenue in weekly_sales]
 
    monthly_revenue_labels = [revenue['month'] for revenue in monthly_sales]
    monthly_revenue_data = [revenue['total_monthly_sales'] for revenue in monthly_sales]
   
    chart_data = [{'customer_name': entry['customer_name'], 'total_sales': entry['total_sales']} for entry in top_customers]
    item_chart = [{'description': entry['description'], 'total_items': entry['total_items']} for entry in top_items]
    # Prepare data as JSON
    
    json_data = {
        'labels': [entry['customer_name'] for entry in chart_data],
        'data': [entry['total_sales'] for entry in chart_data],
        'item_labels': [item['description'] for item in item_chart],
        'item_data': [item['total_items'] for item in item_chart],
        #'revenue_labels': revenue_labels,
        'revenue_labels':revenue_labels,
        'revenue_data': revenue_data,
        'monthly_revenue_labels': monthly_revenue_labels,
        'monthly_revenue_data' : monthly_revenue_data,
        'chart_type':chart_type
    }
    return render(request, 'dashboard.html', {'json_data': json_data})


def customer_table(request):
    my_customers = orders.objects.all()
  
    my_order = orders.objects.all()
    # Join the two tables on the serial_no column
    sort_param = request.GET.get('sort')

    # Sort the orders based on the selected parameter
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Filter orders within the specified date range
    if start_date and end_date:
        my_order = my_order.filter(date__range=[start_date, end_date])
        my_order = my_order.order_by('date')
   
    
    customer_data = my_order.values('customer_name').annotate(
        total_sales_kgs=Sum(
            Case(
                When(measurement='kgs', then=F('order_quantity')),
                default=Value(0),
                output_field=IntegerField(),
            )
        ),
        total_sales_pairs=Sum(
        Case(
            When(measurement='pairs', then=F('order_quantity')),
            default=Value(0),
            output_field=IntegerField(),
        )
        ),
        total_sales_pcs=Sum(
            Case(
                When(measurement='pcs', then=F('order_quantity')),
                default=Value(0),
                output_field=IntegerField(),
            )
        ),
    
        total_quantity=Sum('order_quantity'),
        item_list=ArrayAgg('description', distinct=True)  # Assuming 'item' is the name of the field for items
    )
    
    json_data = {
        'data': [
            {
                'customer_name': entry['customer_name'],
                'total_sales_kgs': entry['total_sales_kgs'],
                'total_quantity': entry['total_quantity'],
                'item_list': entry['item_list'],
                'total_sales_pairs': entry['total_sales_pairs'],
                'total_sales_pcs': entry['total_sales_pcs']
            }
            for entry in customer_data
        ]
    }
    return render(request, 'dashboard_tables.html', {'json_data': json_data, })

def item_table(request):
    item_data = orders.objects.filter(measurement='pairs').values('description').annotate(
        total_sales=Sum('total_price'),
        total_quantity=Sum('order_quantity') # Assuming 'item' is the name of the field for items
    )
    
    json_data = {
        'data': [
            {
                'description': entry['description'],
                'total_sales': entry['total_sales'],
                'total_quantity': entry['total_quantity']
            }
            for entry in item_data
        ]
    }
    return render(request, 'item_table.html', {'json_data': json_data})

def sales_contract(request):
    if request.method == 'GET':
    
        serial_no = request.GET['serial_no']
        print(serial_no,"seirla")
        my_order = get_object_or_404(orders, serial_no=serial_no)
        return render(request,'sales_contract.html',{'my_order':my_order})

    else:
        
        return render(request,'sales_contract.html')