from django.shortcuts import render,redirect,HttpResponse
from django.db import IntegrityError
from .models import Invoice , UnitConversion, DeliveryOrder
import plotly.express as px
import pandas as pd
from datetime import datetime
from .functions import convert_quantity
from django.http import JsonResponse,HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json
import urllib.parse
from decimal import Decimal
#import auth
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login

def signup_view(request):
    if request.method=='POST':
        print("hello")
        uname=request.POST.get('name1')
        email=request.POST.get('email1')
        password=request.POST.get('password1')
        my_user=User.objects.create_user(uname,email,password)
        my_user.save()
        return redirect('sign-in')
        print(uname,email,password)
    return render(request, 'sign-up.html')

def signin_view(request):
    if request.method == 'POST':
        username1 = request.POST.get('name')
        password1 = request.POST.get('password')
        user = authenticate(request, username=username1, password=password1)
        if user is not None:
            login(request , user)

            return redirect('dashboard')
        else:
            # Display an error message on the sign-in page
            return HttpResponse ("leeee")
    return render(request, 'sign-in.html')

#Receive Invoices data
@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        try:
            # Get the raw data from the request body
            raw_data = request.body.decode('utf-8')
        
            # Convert the URL query string to JSON format
            decoded_data = urllib.parse.parse_qs(raw_data)
            
            # Convert the dictionary into a JSON object
            json_data = {key: value[0] for key, value in decoded_data.items()}
            print(json_data)
            unique_field = 'Id'
            existing_invoice = Invoice.objects.filter(**{unique_field: json_data[unique_field]}).first()

            # If the record exists, delete it
            if existing_invoice:
                existing_invoice.delete()

            # Create a new record
            invoice = Invoice.objects.create(**json_data)
            
            # Respond with the received data
            return JsonResponse({'data': json_data})
        except Exception as e:
            # Handle any exceptions and respond with an error message
            return JsonResponse({'error': str(e)}, status=400)
    else:
        # Handle the case where the request method is not POST
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)

#Receive DeliveryOrders data
@csrf_exempt
def receive_deliveryorders(request):
    if request.method == 'POST':
        try:
            # Get the raw data from the request body
            rawdv_data = request.body.decode('utf-8')
        
            # Convert the URL query string to JSON format
            decodeddv_data = urllib.parse.parse_qs(rawdv_data)
            
            # Convert the dictionary into a JSON object
            dv_data = {key: value[0] for key, value in decodeddv_data.items()}
            print(dv_data)
            unique_field = 'Id'
            existing_invoice = Invoice.objects.filter(**{unique_field: dv_data[unique_field]}).first()

            # If the record exists, update it; otherwise, create a new record
            if existing_invoice:
                # Update the existing record with the new data
                for key, value in dv_data.items():
                    setattr(existing_invoice, key, value)
                existing_invoice.save()
            else:
                # Create a new record
                invodeliveryorderice = DeliveryOrder.objects.create(**dv_data)

            # Respond with the received data
            return JsonResponse({'data': dv_data})
        except Exception as e:
            # Handle any exceptions and respond with an error message
            return JsonResponse({'error': str(e)}, status=400)
    else:
        # Handle the case where the request method is not POST
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)

def aircraft_list(request: HttpRequest):
    Invoice1 = Invoice.objects.all()        
    UnitConversion1 = UnitConversion.objects.all()
    # Assuming x1 and x2 are lists of dates and corresponding data
    x1 = [c.StartDate for c in Invoice1]
    x2 = [float(c.TotalQuantity) for c in Invoice1]
    x3 = [c.UnitCode for c in Invoice1]
    x2_in_liters = []
    for quantity, unit_code in zip(x2, x3):
        converted_quantity = convert_quantity(quantity, unit_code, "M3")
        x2_in_liters.append(converted_quantity)
    # Create a DataFrame from the lists

    df = pd.DataFrame({'Date': x1, 'Data': x2_in_liters})

    # Convert 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y %H:%M')

    # Sort the DataFrame by 'Date' column
    sorted_df = df.sort_values(by='Date')

    # Extract sorted dates and corresponding data
    sorted_x1 = sorted_df['Date'].dt.strftime('%d/%m/%Y').tolist()
    sorted_x2 = sorted_df['Data'].tolist()
    total_sum = round(df['Data'].sum())
    Unit = 'M3'

    data = {
        'labels1' : sorted_x1,
        'dataa1' : sorted_x2,
        'sum' : total_sum,
        'unit' : Unit,

    }
    current_path = request.path
    return render(request, 'dashboard.html', {'data': data, 'current_path': current_path})


def suppliers_view(request : HttpRequest):
    current_path = request.path
    return render(request, 'suppliers.html', {'current_path': current_path})

def prevision_view(request):
    return render(request, 'rtl.html') 

def prevision_view(request):
    return render(request, 'profile.html')
