from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.apps import apps
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from .models import Employees

# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.


def index(request):
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
    Customer = apps.get_model('customers.Customer')
    # The following line will get the logged-in user (if there is one) within any view function
    logged_in_user = request.user
    try:
        # This line will return the customer record of the logged-in user if one exists
        logged_in_employees = Employees.objects.get(user=logged_in_user)

        today = date.today()
        
        context = {
            'logged_in_employees': logged_in_employees,
            'today': today
        }
        return render(request, 'employees/index.html')
    except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('employees:create'))
    
