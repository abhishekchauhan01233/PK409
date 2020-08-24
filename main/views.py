from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import registrationdata, crop_farmer, farm_science_expert, machine_learning, feedback_model, contacts

from datetime import datetime, date, time
import requests, json 
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import smtplib
from email.mime.text import MIMEText as text

# Create your views here.
def home(request):
    user = request.user
    userid = user.id

    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin/')
        else:
            return redirect('/farmer/')

    else:
        if request.POST.get('usave'):
            return redirect('/signup/')

        elif request.POST.get('isave'):
            return redirect('/login/')

        elif request.POST.get('formsave'):
            lang = request.POST.get('language')
            if (lang == 'english'):
                return redirect('/')
            elif (lang == 'hindi'):
                return redirect('/h/')

        return render(request, 'main/index.html')

def signup(request):
    user = request.user
    userid = user.id

    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin/')
        else:
            return redirect('/farmer/')

    else:
        if request.method == 'POST':
            region = request.POST.get('region')
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            pass1 = request.POST.get('password1')
            pass2 = request.POST.get('password2')
            aadhar = request.POST.get('aadhar')
            phone = request.POST.get('phone')
            email = request.POST.get('email')

            if (pass1==pass2):
                if User.objects.filter(username=email).exists():
                    messages.error(request, "User with this Email already exists")
                    return redirect('/signup/')
                elif registrationdata.objects.filter(aadhar=aadhar).exists():
                    messages.error(request, "User with this Aadhar number already exists")
                    return redirect('/signup/')
                else:
                    s = smtplib.SMTP("smtp.gmail.com",  587)
                    s.starttls()
                    s.login('commontrivial13@gmail.com','Trivial@987')
                    message =  ''' Dear Farmer

Thank you for registring to our Crop yeild and Compensation 
web portal'''


                    m = text(message)
                    m['Subject'] = 'FARM X' 
                    m['From'] = 'commontrivial13@gmail.com'
                    m['To'] = email
                    s.sendmail("commontrivial13@gmail.com", email, m.as_string())
                    s.quit()
                    user = User.objects.create_user(username=email, password=pass1, email=email, first_name=firstname, last_name=lastname)
                    user.save()
                    farmer = registrationdata.objects.create(user=user,region=region, first_name=firstname, last_name=lastname, phone=phone, email=email, aadhar=aadhar)
                    farmer.save()
                    return redirect('/farmer/')

            messages.error(request, "Password1 and Password2 did not match")
            return redirect('/signup/')

        else:
            return render(request, 'main/signup.html')

def login(request):
    user = request.user
    userid = user.id

    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin/')
        else:
            return redirect('/farmer/')

    else:
        if request.method == "POST":
            role = request.POST.get('role')
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = auth.authenticate(username=email, password=password)

            if (role == 'Scientist'):
                if (email == 'scientist@gmail.com') and (password == 'chirag@123'):
                    auth.login(request, user)
                    return redirect('/scientist/')
                
                messages.error(request, "Invalid Credentials")
                return redirect('/login/')

            elif (role == 'Farmer'):
                if (email == 'weather@gmail.com') or (email == 'scientist@gmail.com'):
                    messages.error(request, "Invalid Credentials")
                    return redirect('/login/')

                else:
                    if user is not None:
                        auth.login(request, user)
                        return redirect('/farmer/')
                    else:
                        messages.error(request, "Invalid Credentials")
                        return redirect('/login/')

            messages.error(request, "Invalid Credentials")
            return redirect('/login/')

        else:
            return render(request, 'main/login.html')

def contact(request):
    data = contacts.objects.all()
    return render(request, 'main/contact.html', {'data':data})

@login_required(login_url='/login/')
def farmer(request):
    user = request.user
    userid = user.id
    today = date.today()

    data = registrationdata.objects.get(user_id=userid)
    year = today.year

    if request.POST.get('psave'):
        return redirect('/profile/')
    
    elif request.POST.get('csave'):
        return redirect('/claim/')
    
    elif request.POST.get('fsave'):
        return redirect('/feedback/')

    elif request.POST.get('lsave'):
        auth.logout(request)
        return redirect('/login/')

    return render(request, 'main/farmer.html', {'data':data})

@login_required(login_url='/login/')
def claim(request):
    user = request.user
    userid = user.id

    data = registrationdata.objects.get(user_id=userid)

    if request.POST.get('lsave'):
        auth.logout(request)
        return redirect('/login/')
    
    elif request.POST.get('success_save'):
        return redirect('/farmer/')
    
    elif request.POST.get('fail_save'):
        return redirect('/farmer/')
    
    elif request.POST.get('submit_save'):
        return redirect('/farmer/')

    elif request.POST.get('save'):
        region = data.region
        crop_type = request.POST.get('crop_type')
        crop_name = request.POST.get('crop_name').lower()
        seed_type = request.POST.get('seed_type')
        year = request.POST.get('year')
        month = request.POST.get('month')
        days = request.POST.get('days')
        area = int(request.POST.get('area'))
        irrigation = float(request.POST.get('irrigation'))
        fertilizers = request.POST.get('fertilizers')
        pesticides = request.POST.get('pesticides')
        cost = float(request.POST.get('cultivation_cost'))
        msp = float(request.POST.get('msp'))
        production = float(request.POST.get('production'))


        print('crop_type', crop_type)
        print(crop_name)
        print(area)
        print('year', year)
        print('month', month)
        print('days', days)
        print('msp' , msp)
        

        farm_expert = farm_science_expert.objects.all()
        for i in farm_expert:
            crop_name_ = i.crop_name.lower()
            if (i.region == region and crop_name_ == crop_name and i.seed_type == seed_type):
                if (area>0 and area<5000):
                    for j in range(0,5000):
                        if j == i.area:
                            farm_expert2 = farm_science_expert.objects.get(Q(region = i.region),Q(crop_name = i.crop_name), Q(seed_type = i.seed_type),Q(area=i.area))


                elif (area>5001 and area<10000):
                    for j in range(5001,10000):
                        if j == i.area:
                            farm_expert2 = farm_science_expert.objects.get(Q(region = i.region),Q(crop_name = i.crop_name), Q(seed_type = i.seed_type),Q(area=i.area))

                elif (area>10001 and area<15000):
                    for j in range(10001,15000):
                        if j == i.area:
                            farm_expert2 = farm_science_expert.objects.get(Q(region = i.region),Q(crop_name = i.crop_name), Q(seed_type = i.seed_type),Q(area=i.area))


                elif (area>15001 and area<20000):
                    for j in range(15001,20000):
                        if j == int(i.area):
                            print(i.area)
                            farm_expert2 = farm_science_expert.objects.get(Q(region = i.region),Q(crop_name = i.crop_name), Q(seed_type = i.seed_type),Q(area=i.area))


                elif (area>20001 and area<25000):
                    for j in range(20001,25000):
                        if j == i.area:
                            farm_expert2 = farm_science_expert.objects.get(Q(region = i.region),Q(crop_name = i.crop_name), Q(seed_type = i.seed_type),Q(area=i.area))

                elif (area>25001 and area<30000):
                    for j in range(25001,30000):
                        if j == i.area:
                            farm_expert2 = farm_science_expert.objects.get(Q(region = i.region),Q(crop_name = i.crop_name), Q(seed_type = i.seed_type),Q(area=i.area))


                elif (area>30001 and area<35000):
                    for j in range(30001,35000):
                        if j == i.area:
                            farm_expert2 = farm_science_expert.objects.get(Q(region = i.region),Q(crop_name = i.crop_name), Q(seed_type = i.seed_type),Q(area=i.area))


                elif (area>35001 and area<40000):
                    for j in range(35001,40000):
                        if j == i.area:
                            farm_expert2 = farm_science_expert.objects.get(Q(region = i.region),Q(crop_name = i.crop_name), Q(seed_type = i.seed_type),Q(area=i.area))


                elif (area>40001 and area<45000):
                    for j in range(40001,45000):
                        if j == i.area:
                            farm_expert2 = farm_science_expert.objects.get(Q(region = i.region),Q(crop_name = i.crop_name), Q(seed_type = i.seed_type),Q(area=i.area))


                elif (area>45001 and area<50000):
                    for j in range(45001,50000):
                         if j == i.area:
                            farm_expert2 = farm_science_expert.objects.get(Q(region = i.region),Q(crop_name = i.crop_name), Q(seed_type = i.seed_type),Q(area=i.area))


                elif (area>50001 and area<55000):
                    for j in range(50001,55000):
                        if j == i.area:
                            farm_expert2 = farm_science_expert.objects.get(Q(region = i.region),Q(crop_name = i.crop_name), Q(seed_type = i.seed_type),Q(area=i.area))


                elif (area>55001 and area<60000):
                    for j in range(55001,60000):
                        if j == i.area:
                            farm_expert2 = farm_science_expert.objects.get(Q(region = i.region),Q(crop_name = i.crop_name), Q(seed_type = i.seed_type),Q(area=i.area))

        context = {
            'farmer_region': region,
            'expert_region': farm_expert2.region,
            'farmer_area': area,
            'expert_area': farm_expert2.area,
            'farmer_name': crop_name,
            'expert_name': farm_expert2.crop_name,
            'farmer_irrigation': irrigation,
            'expert_irrigation': farm_expert2.irrigation,
            'farmer_fertilizers': fertilizers,
            'expert_fertilizers': farm_expert2.fertilizers,
            'farmer_pesticides': pesticides,
            'expert_pesticides': farm_expert2.pesticides,
        }

        if crop_farmer.objects.filter(email=data.email).exists():
            crop = crop_farmer.objects.filter(email=data.email)
            for i in crop:
                if i.crop_year == year:
                    messages.error(request, "You had already applied for the claim this year")
                    return redirect('/farmer/')
            
            else:
                machine_data = machine_learning.objects.all()

                for i in machine_data:
                    if (i.region==region) and (i.crop_year==year) and (i.month==month):
                        avg_temp = i.avg_temp
                        pressure = i.pressure
                        humidity = i.humidity
            
                        a = pd.DataFrame(list(machine_learning.objects.all().values()))
                        a.to_csv('csv/demo.csv', index=False)
                        Crop_data = pd.read_csv("csv/demo.csv")
                        Crop_data = Crop_data[['id','region','crop_type','crop_name','crop_year','month','area','avg_temp','pressure','humidity','production']]
                        Crop_data.drop(['id','region','crop_name'],axis=1,inplace= True)


                        year = float(year)
                        month = float(month)
                        area = float(area)

                        Crop_data = pd.get_dummies(Crop_data)

                        X = Crop_data.drop(['production'], 1)
                        Y = Crop_data['production']

                        reg = LinearRegression(normalize = True)

                        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)

                        reg.fit(X_train,y_train)

                        if crop_type == 'Kharif':
                            crop_type_Rabi = 0
                            crop_type_Kharif = 1
                        elif crop_type == 'Rabi':
                            crop_type_Rabi = 1
                            crop_type_Kharif = 0

                        print(X_test.head(5))

                        d = [[year,month,area,avg_temp,pressure,humidity,crop_type_Kharif,crop_type_Rabi]]

                        prediction = reg.predict(d)
                        score = reg.score(X_test,y_test)
                        score = score*100

                        print("Score: ", score)
                        print("Score2: ",reg.score(d,prediction))

                        for x in range(len(prediction)):
                            print('P: ',prediction[x], '  Data: ', d ,'  A: ', production)

                        x = (10*prediction[0])/100

                        new_prediction_ = prediction[0]+x

                        prediction = int(prediction[0])
                        new_prediction_ = int(new_prediction_)
                        
                        print("Production: ", production)
                        print("Prediction: ", prediction)
                        print("New Prediciton: ", new_prediction_)

                        year=int(year)
                        if (new_prediction_>production):
                            b = crop_farmer.objects.create(email=data.email, region=region, crop_type=crop_type, crop_name=crop_name, seed_type=seed_type, crop_year=year, area=area, days=days, irrigation=irrigation, fertilizers=fertilizers, pesticides=pesticides, avg_temp=avg_temp, cost=cost, msp=msp, production=production, approval_status='Approved')
                            b.save()
                            return render(request, 'main/thanks.html', context)

                        else:
                            b = crop_farmer.objects.create(email=data.email, region=region, crop_type=crop_type, crop_name=crop_name, seed_type=seed_type, crop_year=year, area=area, days=days, irrigation=irrigation, fertilizers=fertilizers, pesticides=pesticides, avg_temp=avg_temp, cost=cost, msp=msp, production=production, approval_status='Notapproved')
                            b.save()
                            return render(request, 'main/thanks.html', context)
            
                else:
                    messages.error(request, "Weather Data of this region or year is not availaible yet! Try after some time")
                    return redirect('/claim/')
        
        else:
            machine_data = machine_learning.objects.all()

            for i in machine_data:
                if (i.region==region) and (i.crop_year==year) and (i.month==month):
                    avg_temp = i.avg_temp
                    pressure = i.pressure
                    humidity = i.humidity
        
                    a = pd.DataFrame(list(machine_learning.objects.all().values()))
                    a.to_csv('csv/demo.csv', index=False)
                    Crop_data = pd.read_csv("csv/demo.csv")
                    Crop_data = Crop_data[['id','region','crop_type','crop_name','crop_year','month','area','avg_temp','pressure','humidity','production']]
                    Crop_data.drop(['id','region','crop_name'],axis=1,inplace= True)


                    year = float(year)
                    month = float(month)
                    area = float(area)

                    Crop_data = pd.get_dummies(Crop_data)

                    X = Crop_data.drop(['production'],1)
                    Y = Crop_data['production']

                    reg = LinearRegression(normalize = True)

                    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)

                    reg.fit(X_train,y_train)

                    if crop_type == 'Kharif':
                        crop_type_Rabi = 0
                        crop_type_Kharif = 1
                    elif crop_type == 'Rabi':
                        crop_type_Rabi = 1
                        crop_type_Kharif = 0

                    print(X_test.head(5))

                    d = [[year,month,area,avg_temp,pressure,humidity,crop_type_Kharif,crop_type_Rabi]]

                    prediction = reg.predict(d)
                    score = reg.score(X_test,y_test)
                    score = score*100


                    print("Score: ", score)
                    print("Score2: ",reg.score(d,prediction))

                    for x in range(len(prediction)):
                        print('P: ',prediction[x], '  Data: ', d ,'  A: ', production)

                    x = (10*prediction[0])/100

                    new_prediction = prediction[0]+x

                    prediction = int(prediction[0])
                    new_prediction = int(new_prediction)
                    
                    print("Production: ", production)
                    print("Prediction: ", prediction)
                    print("New Prediciton: ", new_prediction)

                    year=int(year)
                    if (new_prediction>production):
                        b = crop_farmer.objects.create(email=data.email, region=region, crop_type=crop_type, crop_name=crop_name, seed_type=seed_type, crop_year=year, area=area, days=days, irrigation=irrigation, fertilizers=fertilizers, pesticides=pesticides, avg_temp=avg_temp, cost=cost, msp=msp, production=production, approval_status='Approved')
                        b.save()
                        return render(request, 'main/thanks.html', context)

                    else:
                        b = crop_farmer.objects.create(email=data.email, region=region, crop_type=crop_type, crop_name=crop_name, seed_type=seed_type, crop_year=year, area=area, days=days, irrigation=irrigation, fertilizers=fertilizers, pesticides=pesticides, avg_temp=avg_temp, cost=cost, msp=msp, production=production, approval_status='Notapproved')
                        b.save()
                        return render(request, 'main/thanks.html', context)
            
            else:
                messages.error(request, "Weather Data of this region or year is not availaible yet! Try after some time")
                return redirect('/claim/')  

    return render(request, 'main/claim.html', {'data':data})

@login_required(login_url='/login/')
def profile(request):
    user = request.user
    userid = user.id

    data  = registrationdata.objects.get(user_id=userid)

    if request.POST.get('lsave'):
        auth.logout(request)
        return redirect('/login/')

    elif request.POST.get('bsave'):
        return redirect('/farmer/')

    elif request.POST.get('lsave'):
        auth.logout(request)
        return redirect('/login/')

    return render(request, 'main/profile.html', {'data':data})

@login_required(login_url='/login/')
def feedback(request):
    user = request.user
    userid = user.id

    data  = registrationdata.objects.get(user_id=userid)
        
    if request.POST.get('lsave'):
        auth.logout(request)
        return redirect('/login/')

    elif request.POST.get('save'):
        feed = request.POST.get('feedback')
        a = feedback_model.objects.create(first_name=data.first_name, aadhar=data.aadhar, phone=data.phone, email=data.email, feedback=feed)
        a.save()
        return redirect('/farmer/')

    return render(request, 'main/feedback.html', {'data':data})
 
@login_required(login_url='/login/')
def scientist(request):
    user = request.user
    userid = user.id
    today = date.today()

    year = today.year
    month = today.month

    data = User.objects.get(username='scientist@gmail.com')

    if request.POST.get('lsave'):
        auth.logout(request)
        return redirect('/login/')

    elif request.POST.get('save'):
        region = request.POST.get('region')
        area = request.POST.get('area')
        crop_type = request.POST.get('crop_type')
        crop_name = request.POST.get('crop_name')
        seed_type = request.POST.get('seed_type')
        days = request.POST.get('days')
        irrigation = float(request.POST.get('irrigation'))
        fertilizers = request.POST.get('fertilizers')
        pesticides = request.POST.get('pesticides')
        cost = float(request.POST.get('cultivation_cost'))
        production = float(request.POST.get('production'))

        api_key = "8aee5106eeed58e2a61679a2aeefb4af"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = region
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name 
        response = requests.get(complete_url) 
        x = response.json() 

        if x["cod"] != "404": 
            y = x["main"] 
            current_temperature = y["temp"] 
            avg_temp = current_temperature - 273.15
            pressure = y["pressure"] 
            humidity = y["humidity"] 
            z = x["weather"] 
            weather_description = z[0]["description"] 

        else: 
            print(" City Not Found ") 

        scientist_data = farm_science_expert.objects.all()

        for i in scientist_data:
            if (i.region == region) and (i.crop_type == crop_type) and (i.crop_name == crop_name): 
                messages.error(request, "You had already filled data of this crop still if you want to enter the data then first go to admin panel and delete the data of this crop")
                return redirect('/scientist/')

            else:
                a = farm_science_expert.objects.create(region=region, area=area,  crop_type=crop_type, crop_name=crop_name, seed_type=seed_type, days=days, irrigation=irrigation, fertilizers=fertilizers, pesticides=pesticides, cost=cost, production=production)
                a.save()
                b = machine_learning.objects.create(region=region, crop_type=crop_type, crop_name=crop_name, avg_temp=avg_temp, pressure=pressure, humidity=humidity, production=production, crop_year=year, month=month, area=area)
                b.save()
                return redirect('/scientist/')
    return render(request, 'main/scientist.html', {'data':data})

@login_required(login_url='/login/')
def thanks(request):
    if request.POST.get('submit_save'):
        return redirect('/farmer/')
    return render(request, 'main/thanks.html')

'''I am commenting this because we had replaced weather coordinator by weather API now weather data will be automatically updated'''

'''def weather(request):
    user = request.user
    userid = user.id

    data = User.objects.get(username='weather@gmail.com')

    if request.POST.get('lsave'):
        auth.logout(request)
        return redirect('/login/')

    elif request.POST.get('save'):
        region = request.POST.get('region')
        month = request.POST.get('month')
        crop_year = request.POST.get('crop_year')
        day_temp = float(request.POST.get('day_temp'))
        night_temp = float(request.POST.get('night_temp'))
        rainfall = float(request.POST.get('rainfall'))
        flood = request.POST.get('flood')
        drought = request.POST.get('drought')
        fire = request.POST.get('fire')

        avg_temp = float((day_temp + night_temp)/2)

        weather_data = weather_coordinator.objects.all()

        for i in weather_data:
            if (i.region == region) and (i.month == month) and (i.crop_year == crop_year):
                messages.error(request, "Weather Data of this region and year is already filled by you if still you want to enter then go to admin panel and delete the data of this region and year")
                return redirect('/weather/')
            else:
                None

        scientist_data = farm_science_expert.objects.all()
        
        for i in scientist_data:
            if(i.region==region):
                a = weather_coordinator.objects.create(region=region,month=month, crop_year=crop_year, day_temp=day_temp, night_temp=night_temp, rainfall=rainfall, flood=flood, drought=drought, fire=fire)
                a.save()
                b = machine_learning.objects.create(region=region, crop_type=i.crop_type, crop_name=i.crop_name, avg_temp=avg_temp, rainfall=rainfall,production=i.production, crop_year=crop_year, month=month, area=i.area)
                b.save()
                return redirect('/weather/')
        else:
            messages.error(request, "Crop data of this region is not filled by Farm Science Expert yet")
            return redirect('/weather/')
                   
    return render(request, 'main/weather.html', {'data':data})'''