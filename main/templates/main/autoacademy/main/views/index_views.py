
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from . global_views import GlobalViews
from main.models import Business, Student


#settong global constants
GLOBAL_VARIABLES = GlobalViews()


class IndexViews:
    
    def index(request):
          
        if not(request.user.is_authenticated):
            
                return redirect("user-login")

        else:
            #get current user details
            #rediect to appropriate dashboard
            current_employee = GLOBAL_VARIABLES.get_current_employee_info(request)
            request.session["current_user_fullname"] = str(current_employee.firstname) + \
                                                       str(current_employee.surname) + str(current_employee.othername) 
            request.session["current_campusID"] = current_employee.campusID.id
            request.session["current_campus_name"] = current_employee.campusID.campus_name
            return redirect(current_employee.system_roleID.module_settings)

        return render(request, template_name="main/index.html", context={"title": "Home"})
        
    


    def user_logout(request):
        #logout view
        #====================================================================
        logout(request)
        return redirect("index")



    def user_login(request):
        #login view
        #================================================================
        business = Business.objects.get(id=2)

        if request.POST.get("username") and request.POST.get("password"):
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)
           
            if user is None:
                messages.info(request, "Wrong username or password")
                return redirect("user-login")
            else:
                #reiredt to index views after succesful login
                messages.info(request, "You are now looged in as "+ str(user).upper())
                login(request, user)
                return redirect("index")
        
        return render(request, template_name="main/login.html", context={"business":business,})
        


        