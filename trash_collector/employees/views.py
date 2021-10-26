from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.apps import apps
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from .models import Employees

# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.


def index(request):
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
    Customer = apps.get_model('customers.Customer')
    all_customers = Customer.objects.all()
    
    # The following line will get the logged-in user (if there is one) within any view function
    logged_in_user = request.user
    try:
        # This line will return the customer record of the logged-in user if one exists
        days = ['Monday','Tuesday', 'Wednesday','Thursday','Friday','Saturday','Sunday']
        today = date.today()
        logged_in_employees = Employees.objects.get(user=logged_in_user)
        customer_in_zip_code = all_customers.filter(zip_code=logged_in_employees.zip_code) 
        customer_pickup_date = customer_in_zip_code.filter(Q(weekly_pickup = days[date.weekday(today)]) | Q(one_time_pickup=date.today()))
        customer_suspended_dates = customer_pickup_date.exclude(Q(suspend_start__gte = date.today()) | Q(suspend_end__lte = date.today()))
        customer_trash_picked_up = customer_suspended_dates.exclude(date_of_last_pickup = date.today())
        
        
        context = {
            'logged_in_employees': logged_in_employees,
            'today': today,
            'customer_in_zip_code': customer_in_zip_code,
            'customer_pickup_date': customer_pickup_date,
            'customer_suspended_dates': customer_suspended_dates,
            'customer_trash_picked_up': customer_trash_picked_up
        }
        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('employees:create'))

def create(request):
    logged_in_user = request.user
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        zip_from_form = request.POST.get('zip_code')
        new_employees = Employees(name=name_from_form, user=logged_in_user, zip_code=zip_from_form)
        new_employees.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')  

def edit_profile(request):
    logged_in_user = request.user
    logged_in_employees = Employees.objects.get(user=logged_in_user)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        zip_from_form = request.POST.get('zip_code')
        logged_in_employees.name = name_from_form
        logged_in_employees.zip_code = zip_from_form
        logged_in_employees.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        context = {
            'logged_in_employees': logged_in_employees
        }
        return render(request, 'employees/edit_profile.html', context)
       
def date_of_last_pickup_confirmation(request, customer_id):
    Customer = apps.get_model('customers.Customer')
    current_customer = Customer.objects.get(pk=customer_id)
    if request.method == "POST":
        date_from_form = request.POST.get('date')
        current_customer.date_of_last_pickup = date_from_form
        current_customer.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        context = {
            'current_customer': current_customer
        }
        return render(request, 'employees/date_of_last_pickup.html', context)       
      
       
