from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta
import json
import pandas as pd
from decimal import Decimal

from .models import Account, BiteReport, NormalUser
from .forms import UnitForm, DateRangeForm, DateGeoRangeForm, CurrencyForm, SupplierDateRangeForm
from myapp.forms import NoteForm

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        if NormalUser.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)
        if NormalUser.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        user = NormalUser(email=email, username=username, password=password)
        user.save()
        return JsonResponse({'success': True, 'user_id': user.id})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def loginn(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        try:
            user = NormalUser.objects.get(email=email)
            if user.password == password:
                return JsonResponse({'success': True, 'user_id': user.id})
            else:
                return JsonResponse({'error': 'Invalid password'}, status=400)
        except NormalUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def report_bite_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        place_of_bite = data.get('place_of_bite')
        longitude = data.get('longitude')
        latitude = data.get('latitude')
        date = parse_date(data.get('date'))
        time_since_bite = data.get('time_since_bite')
        symptom = data.get('symptom')
        phone_number = data.get('phone_number')

        bite_report = BiteReport(
            place_of_bite=place_of_bite,
            longitude=longitude,
            latitude=latitude,
            date=date,
            time_since_bite=time_since_bite,
            symptom=symptom,
            phone_number=phone_number
        )
        bite_report.save()

        return JsonResponse({'success': True, 'message': 'Bite report submitted successfully'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

# Assuming user has an associated Account object
@login_required
def overview(request : HttpRequest):
    account = request.user.account  
    
    current_path = request.path
    return render(request, 'Overview.html', {'current_path':current_path})

@login_required
def cartographie(request : HttpRequest):
    account = request.user.account  # Assuming user has an associated Account object
    
    
    current_path = request.path
    return render(request, 'Cartographie.html', {'current_path':current_path})

@login_required
def especes(request : HttpRequest):
    account = request.user.account  # Assuming user has an associated Account object
    
    
    current_path = request.path
    return render(request, 'Especes.html', {'current_path':current_path})

@login_required
def medecin(request : HttpRequest):
    account = request.user.account  # Assuming user has an associated Account object
    
    
    current_path = request.path
    return render(request, 'Medecin.html', {'current_path':current_path})

@login_required
def urgence(request : HttpRequest):
    account = request.user.account  # Assuming user has an associated Account object
    
    urgence
    current_path = request.path
    return render(request, 'Urgence.html', {'current_path':current_path})


def signin_view(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')
        remember_me = request.POST.get('rememberMe')  # Get the value of Remember Me checkbox

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Set session expiry based on Remember Me checkbox
            if remember_me:
                request.session.set_expiry(60 * 60 * 24 * 30)  # 30 days expiry
            else:
                request.session.set_expiry(0)  # Browser session expiry
            return redirect('overview')  # Redirect to the profile page
        else:
            # Display an error message on the sign-in page
            return render(request, 'sign-in.html', {'error': True})

    return render(request, 'sign-in.html')


# Geo View Code ##########
@login_required
def geo_view(request: HttpRequest):
    if request.user.is_authenticated:
        account = request.user.account
        to_unit_code = account.units
        to_currency_code = account.currency
        username1 = request.user.username
        selection_filter = account.geography_global_selection
        custom_Startdate = account.start_geo_date
        custom_Enddate = account.end_geo_date
        dark_mode = int(account.dark_mode)
        geo_filter_id = account.geography_filter_id
        
    dv = DeliveryOrder.objects.all()
    iv = Invoice.objects.all()
    
    
    # Extract data from objects DeliveryOrder
    x1 = [c.StartOperation for c in dv]
    x2 = [float(c.Quantity) for c in dv]
    x3 = [c.UnitCode for c in dv]
    x4 = [c.CountryCode for c in dv]
    x5 = [c.StopOver for c in dv]
    x6 = [c.Town for c in dv]
    
    # Extract data from objects Invoices
    y0 = [c.StartDate for c in iv]
    y00 = [c.EndDate for c in iv]    
    y1 = [float(c.AmountIncludingTax) for c in iv]
    y2 = [c.CurrencyCode for c in iv]
    y3 = [c.CountryCode for c in iv]
    y4 = [c.StopOver for c in iv]
    y5 = [c.Town for c in iv]

    # Convert the Fuel unit DeliveryOrder
    x2_in_liters = []
    for quantity, unit_code in zip(x2, x3):
        converted_quantity = convert_quantity(quantity, unit_code, to_unit_code)
        x2_in_liters.append(converted_quantity)

    y2_in_new = []
    for amount , start_date, end_date, currency_code in zip(y1,y0,y00,y2):
        converted_amount = calculate_converted_amount(start_date ,end_date ,currency_code,to_currency_code, amount)
        y2_in_new.append(converted_amount)

    
    # Store delivery_orders_data into dataframe : df
    df = pd.DataFrame({'Date': x1, 'Data': x2_in_liters, 'Countries': x4, 'StopOver': x5, 'Town': x6})

    # Store invoices_data into dataframe : df
    df1 = pd.DataFrame({'Date': y0,'Data': y2_in_new, 'Countries': y3, 'StopOver': y4, 'Town': y5 })
    
    # Convert 'Date' column to datetime format in df
    df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d %H:%M:%S.%f')
    # Convert 'Date' column to datetime format in d1
    df1['Date'] = pd.to_datetime(df1['Date'], format='%d/%m/%Y %H:%M')
    
    # Extract only the date component
    df['Date'] = df['Date'].dt.date 
    df1['Date'] = df1['Date'].dt.date 

    # If custom_startDate and custom_endDate are None, use earliest_date and latest_date from the DataFrame
    if custom_Startdate is None or custom_Enddate is None:
        if selection_filter == 1:
            earliest_date = df['Date'].min()
            latest_date = df['Date'].max()
        else:
            earliest_date = df1['Date'].min()
            latest_date = df1['Date'].max()
    else:
        earliest_date = custom_Startdate
        latest_date = custom_Enddate

    print(earliest_date)
    print(latest_date)
    
    # Filter the DataFrame to include only the data between the earliest date and the latest date
    if selection_filter == 1:
        df = df[(df['Date'] >= earliest_date) & (df['Date'] <= latest_date)]
        empty = 1 if df.empty else 0
    else :
        df1 = df1[(df1['Date'] >= earliest_date) & (df1['Date'] <= latest_date)]
        empty = 1 if df1.empty else 0

    print(empty)

    # Check the value of select variable
    select = int(selection_filter)
    if select == 1 and empty == 0:
        
            # Group by 'Countries' and sum the 'Data' for each provider from deliveryOrders
            sum_by_country = df.groupby('Countries')['Data'].sum()
            sum_by_town = df.groupby('Town')['Data'].sum()
            sum_by_StopOver = df.groupby('StopOver')['Data'].sum()
            # Sort Countries by fuel quantities in descending order
            sorted_Countries = sum_by_country.sort_values(ascending=False)
            sorted_Town = sum_by_town.sort_values(ascending=False)
            sorted_StopOver= sum_by_StopOver.sort_values(ascending=False)
            
            top_country = sorted_Countries.index[0]
            top_town = sorted_Town.index[0]
            top_stopover = sorted_StopOver.index[0]
            
            if geo_filter_id == 1:
                # Process for country
                formatted_data = [['Country', 'Fuel Consumption']]
                # Iterate over sorted providers and format the data
                for country, quantity in sorted_Countries.items():
                    formatted_quantity = quantity  # Round to the nearest integer
                    formatted_data.append([country, formatted_quantity])

                top_filter_selection = sorted_Countries.index[0]  # Extract the index (country name) of the first item in the sorted Series

                Unit = to_unit_code
                unit_name = from_unitcode_to_unitname(Unit)
            elif geo_filter_id == 2:
                # Process for country
                formatted_data = []
                # Iterate over sorted providers and format the data
                for town, quantity in sorted_Town.items():
                    formatted_quantity = quantity  # Round to the nearest integer
                    formatted_data.append([town, formatted_quantity])

                top_filter_selection = sorted_Town.index[0]  # Extract the index (country name) of the first item in the sorted Series

                Unit = to_unit_code
                unit_name = from_unitcode_to_unitname(Unit)
            elif geo_filter_id == 3:
                # Process for country
                formatted_data = []
                # Iterate over sorted providers and format the data
                for stopover, quantity in sorted_StopOver.items():
                    formatted_quantity = quantity  # Round to the nearest integer
                    formatted_data.append([stopover, formatted_quantity])

                top_filter_selection = sorted_Town.index[0]  # Extract the index (country name) of the first item in the sorted Series

                Unit = to_unit_code
                unit_name = from_unitcode_to_unitname(Unit)
    elif select == 0 and empty == 0:
            # Group by 'Countries' and sum the 'Data' for each provider from expenses
            expenses_sum_by_country = df1.groupby('Countries')['Data'].sum()
            expenses_sum_by_town = df1.groupby('Town')['Data'].sum()
            expenses_sum_by_StopOver = df1.groupby('StopOver')['Data'].sum()
            # Sort Countries by expenses in descending order
            sorted_expenses_countries = expenses_sum_by_country.sort_values(ascending=False)
            sorted_expenses_Town = expenses_sum_by_town.sort_values(ascending=False)
            sorted_expenses_StopOver = expenses_sum_by_StopOver.sort_values(ascending=False)
            
            top_country = 'No Data' if sorted_expenses_countries.empty else sorted_expenses_countries.index[0]
            top_town = 'No Data' if sorted_expenses_Town.empty else sorted_expenses_Town.index[0]
            top_stopover = 'No Data' if sorted_expenses_StopOver.empty else sorted_expenses_StopOver.index[0]
            
            if geo_filter_id == 1:
                # Process for country
                formatted_data = [['Country', 'Fuel Consumption']]
                # Iterate over sorted providers and format the data
                for country, quantity in sorted_expenses_countries.items():
                    formatted_quantity = quantity  # Round to the nearest integer
                    formatted_data.append([country, formatted_quantity])

                top_filter_selection = 'No Data' if sorted_expenses_countries.empty else sorted_expenses_countries.index[0]

                Unit = to_unit_code
                unit_name = from_unitcode_to_unitname(Unit)
            elif geo_filter_id == 2:
                # Process for country
                formatted_data = []
                # Iterate over sorted providers and format the data
                for town, quantity in sorted_expenses_Town.items():
                    formatted_quantity = quantity  # Round to the nearest integer
                    formatted_data.append([town, formatted_quantity])

                top_filter_selection = 'No Data' if sorted_expenses_Town.empty else sorted_expenses_Town.index[0]

                Unit = to_unit_code
                unit_name = from_unitcode_to_unitname(Unit)
            elif geo_filter_id == 3:
                # Process for country
                formatted_data = []
                # Iterate over sorted providers and format the data
                for stopover, quantity in sorted_expenses_StopOver.items():
                    formatted_quantity = quantity  # Round to the nearest integer
                    formatted_data.append([stopover, formatted_quantity])

                top_filter_selection = 'No Data' if sorted_expenses_StopOver.empty else sorted_expenses_StopOver.index[0]

                Unit = to_unit_code
                unit_name = from_unitcode_to_unitname(Unit)
    else :
        formatted_data = []
        top_country = 'No Data'
        top_town = 'No Data'
        top_stopover = 'No Data'
        top_filter_selection = 'No Data'
        unit_name = 'No Data'

    
    if formatted_data and len(formatted_data) > 1:
        # Check if the first row matches [['Country', 'Fuel Consumption']]
        if formatted_data[0] == ['Country', 'Fuel Consumption']:
            formatted_data_1 = formatted_data[1:]
        else:
            formatted_data_1 = formatted_data
    else:
        formatted_data_1 = formatted_data

    if geo_filter_id == 1:
        geo_filter_name = 'Country'
    elif geo_filter_id ==2:
        geo_filter_name = 'Town'
    else:
        geo_filter_name = 'StopOver'
        
    data = {
        'username': username1,
        'formatted_data': formatted_data,
        'formatted_data_1': formatted_data_1,
        'start_date': earliest_date,
        'end_date': latest_date,
        'top_filter_selection': top_filter_selection,
        'top_country' : top_country,
        'top_town' : top_town,
        'top_stopover' : top_stopover,
        'geo_filter_name' : geo_filter_name,
        'empty': empty,
        'unit': unit_name,
        'currency' : to_currency_code,
        'selection_filter_code': select,
        'dark_mode': dark_mode,
        'geo_filter':geo_filter_id,
    }
    current_path = request.path
    return render(request, 'geography.html', {'data': data, 'current_path': current_path})


#Time View Code ##########
@login_required
def time_view(request : HttpRequest):
    if request.user.is_authenticated:
        account = request.user.account
        selection_filter_code = account.time_global_selection
        chart_type = account.time_chart_type
        to_unit_code = account.units
        to_currency_code = account.currency
        custom_startDate = account.start_date
        custom_endDate = account.end_date
        overview_list_value = account.time_by_filter
        username1 = request.user.username
        dark_mode = int(account.dark_mode)
    
    
    if overview_list_value is None :
         every = 7
    else:
        every = overview_list_value
        
    # Print the received value for debugging
    # Print("Received value:", overview_list_value)
    
    DelivOrd = DeliveryOrder.objects.all()        
    iv = Invoice.objects.all()
    # Assuming x1 and x2 are lists of dates and corresponding data
    x1 = [c.StartOperation for c in DelivOrd]
    x2 = [float(c.Quantity) for c in DelivOrd]
    x3 = [c.UnitCode for c in DelivOrd]
    
    y1 = [c.StartDate for c in iv]
    y11 = [c.EndDate for c in iv]
    y2 = [float(c.AmountIncludingTax) for c in iv]
    y3 = [c.CurrencyCode for c in iv]
    
    #Convert the Fuel unit
    x2_in_liters = []
    for quantity, unit_code in zip(x2, x3):
        converted_quantity = convert_quantity(quantity, unit_code, to_unit_code)
        x2_in_liters.append(converted_quantity)
     
    y2_in_new = []
    for amount , start_date, end_date, currency_code in zip(y2,y1,y11,y3):
        converted_amount = calculate_converted_amount(start_date ,end_date ,currency_code,to_currency_code, amount)
        y2_in_new.append(converted_amount)
        
    # Create a DeliveryOrder DataFrame from the lists
    df = pd.DataFrame({'Date': x1, 'Data': x2_in_liters})
    
    # Create a Invoice DataFrame from the lists
    df1 = pd.DataFrame({'Date': y1, 'Data': y2_in_new})
    
    # Convert 'Date' column to datetime format in df
    df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d %H:%M:%S.%f')
   
    # Convert 'Date' column to datetime format in d1
    df1['Date'] = pd.to_datetime(df1['Date'], format='%d/%m/%Y %H:%M')
    
    # Extract only the date component
    df['Date'] = df['Date'].dt.date 
    df1['Date'] = df1['Date'].dt.date 
    
    # Initialize the end date as None
    end_date = None
    # If custom_startDate and custom_endDate are None, use earliest_date and latest_date from the DataFrame
    if custom_startDate is None or custom_endDate is None:
        if selection_filter_code == 1:
            earliest_date = df['Date'].min()
            latest_date = df['Date'].max()
        else:
            earliest_date = df1['Date'].min()
            latest_date = df1['Date'].max()
    else:
        earliest_date = custom_startDate
        latest_date = custom_endDate

    fixed_earliest_date = earliest_date
    # days = int(overview_list_value) if overview_list_value is not None else 7
    days = int(overview_list_value) if overview_list_value is not None else 7

    # Define the time increment using the corrected value of days
    time_increment = timedelta(days=days)

    dates = []
    data= []
    
    if earliest_date <= latest_date :
        # Loop until the end date is found in the dataset
        while earliest_date <= latest_date :
            # Calculate the end date by adding the time increment to the earliest date
            end_date = earliest_date + time_increment
            # Check if the end date exceeds the latest date
            if end_date > latest_date:
                break
            
            if selection_filter_code == 1:
                # Perform your logic here based on the time range (e.g., summing consumption)
                sum_consumption = df.loc[(df['Date'] >= earliest_date) & (df['Date'] < end_date), 'Data'].sum()
            else:
                # Perform your logic here based on the time range (e.g., summing consumption)
                sum_consumption = df1.loc[(df1['Date'] >= earliest_date) & (df1['Date'] < end_date), 'Data'].sum()
                
            # Output the time range and sum of consumption (or other result of your logic)
            dates.append(earliest_date.strftime('%Y-%m-%d'))
            data.append(sum_consumption)
            # Update the earliest date to the end date for the next iteration
            earliest_date = end_date

        # End of loop when end date is found in the dataset
        print("End date found in the dataset.")
        
        total_sum = round(sum(data))
        Unit = to_unit_code
        
        if total_sum == 0:
            empty = 1
        else :
            empty = 0
            
        if len(dates) <= 1:
            dates = []
            data = []
        else:
            print("There is enough data")

        enough_data = len(dates) > 1 
        if selection_filter_code == 1: 
            interpretation = generate_textual_interpretation(data, fixed_earliest_date, latest_date, time_increment,Unit)
        else : 
            interpretation = generate_textual_interpretation_for_expenses(data, fixed_earliest_date, latest_date, time_increment,to_currency_code)
    else:
        enough_data = True
        empty = 1
        total_sum = 'No Data'
        Unit = to_unit_code
        interpretation = 'No Data'
        
    if chart_type == 1 :
        chart_name = 'line'
    else:
        chart_name = 'bar'
        
    print(chart_name)
    data = {
        'username': username1,
        'selection_filter_code':selection_filter_code,
        'chart_type' : chart_type,
        'chart_type_name' : chart_name,
        'enough_data': enough_data,
        'empty': empty,
        'labels1' : dates,
        'dataa1' : data,
        'every': every,
        'start_month' : fixed_earliest_date,
        'end_month' : latest_date,
        'sum' : total_sum,
        'unit' : Unit,
        'currency': to_currency_code,
        'text_interpretation' : interpretation,
        'dark_mode': dark_mode,

    }
    current_path = request.path
    return render(request, 'timeline.html', {'data': data, 'current_path': current_path}) 


#Forecasting View Code ##########
@login_required
def prevision_view(request):
   
    return render(request, 'rtl.html') 

from django.http import JsonResponse

@login_required
def profile_view(request):
    account = request.user.account  # Assuming there's a one-to-one relationship between User and Account
    username1 = request.user.username
    unit = account.units
    currency = account.currency
    dark_mode = account.dark_mode
    if request.method == 'POST':
        # First, handle the form submission for updating unit or currency
        if 'unit' in request.POST:
            form = UnitForm(request.POST, instance=account)
            if form.is_valid():
                account.units = form.cleaned_data['unit']
                account.save()
                # Return JSON response if it's an AJAX request
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': True})
                else:
                    return redirect('profile')  # Redirect for non-AJAX requests
        elif 'currency' in request.POST:
            form = CurrencyForm(request.POST, instance=account)
            if form.is_valid():
                account.currency = form.cleaned_data['currency']
                account.save()
                # Return JSON response if it's an AJAX request
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': True})
                else:
                    return redirect('profile')  # Redirect for non-AJAX requests
        
        # If the above conditions didn't match, it means it's a form submission for updating user profile
        uname = request.POST.get('name1')
        email = request.POST.get('email1')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        data = {
                'dark_mode': dark_mode,
                'unit': unit,
                'currency': currency,
                'username': username1,
            }
        
        if uname == "" or email == "" or password1 == "" or password2 == "":
            error_msg = 'Please fill all fields'
            return render(request, 'profile.html', {'error': error_msg,'data': data})

        if password1 != password2:
            error_msg = 'Passwords do not match.'
            return render(request, 'profile.html', {'error': error_msg,'data': data})

        if User.objects.filter(email=email).exists():
            error_msg = 'Email is already in use.'
            return render(request, 'profile.html', {'error': error_msg,'data': data})

        if User.objects.filter(username=uname).exists():
            error_msg = 'Username is already in use.'
            return render(request, 'profile.html', {'error': error_msg, 'data': data})

        # Create User object
        my_user = User.objects.create_user(uname, email, password1, last_name="LT")

        # Create associated Account object
        account = Account.objects.create(user=my_user)

        # Set the unit to "LT" for the newly created account
        account.units = "LT"
        account.currency = "TND"
        account.geography_global_selection = 1
        account.suppliers_global_selection = 1
        account.dark_mode = 1
        account.time_global_selection = 1
        account.time_by_filter = 1
        account.time_chart_type = 1 
        account.geography_filter_id = 1
        account.aircraft_chart_type = 1
        account.supplier_name_filter = "WORLD FUEL SERVICES"
        account.save()
        current_path = request.path

        # Pass the created username and password to the template
        return render(request, 'profile.html', {'success': True, 'username': uname, 'password': password1,'data': data,'current_path': current_path})
    else:
        form = UnitForm(instance=account)

    current_path = request.path
    data = {
        'dark_mode': dark_mode,
        'unit': unit,
        'currency': currency,
    }
    return render(request, 'profile.html', {'data': data, 'form': form,'current_path': current_path})

@login_required
def submit_rate_and_notes(request):
    account = request.user.account  # Assuming there's a one-to-one relationship between User and Account
    username = request.user.username  # Get the username
    unit = account.units
    currency = account.currency
    dark_mode = account.dark_mode

    if request.method == 'POST':
        rates = request.POST.get('rates')
        notes = request.POST.get('notes')
        user_account = Account.objects.get(user=request.user)
        user_account.rates = rates
        user_account.notes = notes
        user_account.save()
        success_message = "Rates and notes submitted successfully!"
        
        data = {
            'username': username,
            'dark_mode': dark_mode,
            'unit': unit,
            'currency': currency,
        }
        return render(request, 'profile.html', {'success_message': success_message, 'data': data})

    data = {
        'username': username,
        'dark_mode': dark_mode,
        'unit': unit,
        'currency': currency,
    }
    return render(request, 'profile.html', {'data': data})

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            print(f"Session data: {request.session.items()}")
            return redirect('profile')  # Change this to your profile URL
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profile.html', {'form': form, 'errors': form.errors})
def handle_ajax_request(request):
    # Handle the AJAX request here
    if request.method == 'POST':
        # Process the AJAX request
        # For demonstration, let's just return a JsonResponse
        return JsonResponse({'success': True})

# aircrafts View Code
@login_required
def aircrafts_view(request):
    username1 = None  # Default value if user is not authenticated
    if request.user.is_authenticated:
        account = request.user.account   
        to_unit_code = account.units
        username1 = request.user.username
        dark_mode = int(account.dark_mode)
        aircraft_chartType = account.aircraft_chart_type
        
    dv = DeliveryOrder.objects.all()
    # Extract data from objects DeliveryOrder
    x1 = [c.StartOperation for c in dv]
    x2 = [float(c.Quantity) for c in dv]
    x3 = [c.UnitCode for c in dv]
    x4 = [c.AircraftCode for c in dv]
    x5 = [c.Aircraft for c in dv]
    
    # Convert the Fuel unit DeliveryOrder
    x2_in_liters = []
    for quantity, unit_code in zip(x2, x3):
        converted_quantity = convert_quantity(quantity, unit_code, to_unit_code)
        x2_in_liters.append(converted_quantity)

    # Store delivery_orders_data into dataframe : df
    df = pd.DataFrame({'Date': x1, 'Data': x2_in_liters, 'Aircraft': x5})
    
    # Group by 'Countries' and sum the 'Data' for each provider from deliveryOrders
    sum_by_aircraft = df.groupby('Aircraft')['Data'].sum()
    
    # Sort Countries by fuel quantities in descending order
    sorted_aircrafts = sum_by_aircraft.sort_values(ascending=False)
    
    # Extract sorted provider names and fuel quantities
    aircraft_names_sorted = sorted_aircrafts.index.tolist()
    aircraft_fuel_quantities_sorted = sorted_aircrafts.tolist()
    
    most_provided_provider = aircraft_names_sorted[0]

    formatted_data = []
    # Iterate over sorted providers and format the data
    for aircraft, quantity in sorted_aircrafts.items():
        formatted_quantity = quantity  # Round to the nearest integer
        formatted_data.append([aircraft, formatted_quantity])
                    
    unit_name = from_unitcode_to_unitname(to_unit_code)
    current_path = request.path
    data = {
        'username': username1,
        'dark_mode' : dark_mode,
        'formatted_data': formatted_data,
        'unit': unit_name,
        'chart_type' : aircraft_chartType,
        'top_aircraft' : most_provided_provider,
        'aircraft_names': aircraft_names_sorted,
        'aircraft_fuel_quantities': aircraft_fuel_quantities_sorted,

    }
    return render(request, 'aircrafts.html', {'data': data, 'current_path': current_path})

import pickle 
import joblib
import logging

logger = logging.getLogger(__name__)
# Load the trained model outside the view function
model = joblib.load('C:/Users/HICHEM BEN/Desktop/ml models/ExchangeRatesModelV-Final.joblib')
invoice_model = joblib.load('C:/Users/HICHEM BEN/Desktop/ml models/Try3_expenses.joblib')
deliveryorders_model = joblib.load('C:/Users/HICHEM BEN/Desktop/ml models/Try2.joblib')

@login_required
@csrf_exempt
def forecasting_view(request):
    if request.user.is_authenticated:
        account = request.user.account
        username1 = request.user.username
        dark_mode = int(account.dark_mode)
        
    predicted_value = 'Fill Fields'
    predicted_values = 'Fill Fields'
    predicted_valuess = 'Fill Fields'
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'sample_prediction':
            year = request.POST.get('Year')  
            month = request.POST.get('Month')  
            day = request.POST.get('Day')  
            From = request.POST.get('From')  
            To = request.POST.get('To')  

            sample_data = pd.DataFrame({
                'Year': [year],
                'Month': [month],
                'Day': [day],
                'ExchangeRateSourceId': [From],
                'FromCurrencyId': [To]
            })

            predicted_ratios = model.predict(sample_data)
            predicted_value = predicted_ratios[0]
            print(predicted_value)
        
        elif form_type == 'invoice_prediction':
            year = request.POST.get('Year1')  
            month = request.POST.get('Month1')  
            day = request.POST.get('Day1')  
            From = request.POST.get('Quantity')  
            To = request.POST.get('Taxes')  

            for_prediction = pd.DataFrame({
                'StartYear': [year],
                'StartMonth': [month],
                'StartDay': [day],
                'TotalQuantity': [From],  
                'TaxesAmount': [To],         
            })

            predicted_ratioss = invoice_model.predict(for_prediction)
            predicted_values = predicted_ratioss[0]
            print(predicted_values)
        
        elif form_type == 'delivery_prediction':
            year = request.POST.get('Year2')  
            month = request.POST.get('Month2')  
            day = request.POST.get('Day2')  
            price = request.POST.get('Price')  

            for_predictiona = pd.DataFrame({
                'StartYear': [year],
                'StartMonth': [month],
                'StartDay': [day],
                'Price': [price],  
            })

            predicted_ratiosss = deliveryorders_model.predict(for_predictiona)
            predicted_valuess = predicted_ratiosss[0]
            print(predicted_valuess)
                          
    current_path = request.path
    data = {
        'username': username1,
        'dark_mode': dark_mode,
        'predicted_value': predicted_value,
        'predicted_values': predicted_values,
        'predicted_valuess': predicted_valuess,
    }
    return render(request, 'forecasting.html', {'data': data, 'current_path': current_path})


def logout_view(request):
    logout(request)
    return redirect('landingpage')

def landingpage_view(request):
    return render(request, 'landingpage.html')

from django.shortcuts import render

#Country-Details
def country_details(request):
    if request.user.is_authenticated:
        account = request.user.account
        to_unit_code = account.units
        currency = account.currency
        username1 = request.user.username
        filter_code = account.geography_global_selection
        dark_mode = int(account.dark_mode)

    country_code = request.GET.get('country', '')
    
    deliv_orders = DeliveryOrder.objects.filter(CountryCode=country_code)
    
    quantities = []
    units = []
    towns = []
    stopovers = []
    country_names = []
    
    for order in deliv_orders:
        quantities.append(float(order.Quantity))
        units.append(order.UnitCode)
        towns.append(order.Town)
        stopovers.append(order.StopOver)
        country_names.append(order.Country)
    
    quantities_in_liters = [convert_quantity(qty, unit, to_unit_code) for qty, unit in zip(quantities, units)]
    town_sum_df = pd.DataFrame({
        'Quantity': quantities_in_liters,
        'UnitCode': units,
        'Town': towns,
        'StopOver': stopovers,
        'CountryCode': country_names
    })
    town_sum = town_sum_df.groupby('Town')['Quantity'].sum().reset_index()
    stopover_sum = town_sum_df.groupby('StopOver')['Quantity'].sum().reset_index()
    
    top_town = town_sum_df.loc[town_sum_df['Quantity'].idxmax(), 'Town']
    top_stopover = town_sum_df.loc[town_sum_df['Quantity'].idxmax(), 'StopOver']

    country_name = country_names[0]
    print(town_sum.values.tolist())
    print(filter_code)
    data = {
        'towns': town_sum.values.tolist(),
        'stopover': stopover_sum.values.tolist(),
        'dark_mode' : dark_mode,
        'username' : username1,
        'country_code': country_code,
        'country_name': country_name,
        'town_max_quantity':top_town,
        'stopover_max_quantity':top_stopover,
        'unit' : to_unit_code,
        'currency' : currency,
        'selection_filter_code': filter_code,
    }
    
    return render(request, 'country_details.html', {'data': data})

@login_required
def about_view(request): 
    if request.user.is_authenticated:
        account = request.user.account 
        username1 = request.user.username
        dark_mode = int(account.dark_mode)
        
    current_path = request.path
    data = {
        'username' : username1,
        'dark_mode' : dark_mode
    }
    return render(request, 'about.html',{'data':data,'current_path': current_path})