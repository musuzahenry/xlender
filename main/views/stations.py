from django.shortcuts import render
from django.contrib import messages
from main.models import  StationStng, AutoItemAdds, LoanTypeStng, ItemCategories
from datetime import datetime, timedelta
from django.utils import timezone
from .global_views import *
from . income_expense_view import *
from .pivot_totals_view import PivotTotals


#initialixing the global object
global_variables = GlobalVariables()
#initializing pivots and totals
pivot_totals = PivotTotals()

class StationsView():
    ''' 
    This class hold views for editing station settings from the front end
    '''
    def view_stations(request):
        
        try:
            x = request.session["current_stationID"]
            x = None
        except:
            return redirect("main:index")

        if request.POST.get("pay-rent-id"):
            #the sourcecode bloww helps in adding trent to incomes and expenses
            #we use the inc_exp_module 
            IncomeExpense.manage_incomes_and_expenses(request)
         
        stations = None
        if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
            stations = StationStng.objects.all().order_by("station_name")
        else:
            stations = StationStng.objects.filter(id= int(request.session["current_stationID"])).order_by("station_name")
        
        return render(request, template_name="main/view_stations.html", context={"stations":stations,"title":"Stations"})

        
        
        
        
    def stations_loan_seetings(request):

        try:
            x = request.session["current_stationID"]
            x = None
        except:
            return redirect("main:index")
   
        stations = None
        #check if user is alllowed to change interest settings
        if global_variables.user_rights(request.user, "allow_to_change_loan_interest_settings")=="Yes":
            if request.POST.get("station-id"):
                change_station = StationStng.objects.get(id= int(request.POST.get("station-id")))
                change_station.daily_percent = int(request.POST.get("daily-interest"))
                change_station.monthly_percent = int(request.POST.get("monthly-interest"))
                change_station.defaulters_percent = int(request.POST.get("daily-defaulters-interest"))
                change_station.monthly_defaulters_percent = int(request.POST.get("monthly-defaulters-interest"))
                change_station.save()
                #notify te user that the change was successful
                messages.info(request, "Succes!, settings updated")
            
        #check if user is allowed to view all stations
        if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
            stations = StationStng.objects.all().order_by("station_name")
        #else just view your station
        else:
            stations = StationStng.objects.filter(id= int(request.session["current_stationID"]))
   
        return render(request, template_name="main/view_stations_loan_settings.html", context={"stations":stations,"title":"Stations"})
   



    def stations_book_settings(request):

        try:
            x = request.session["current_stationID"]
            x = None
        except:
            return redirect("main:index")
   
        auto_items = None
        #check if user is alllowed to change interest settings
        if global_variables.user_rights(request.user, "allow_to_change_loan_interest_settings")=="Yes":
            

            #Add a record book
            if request.POST.get("book-fee") and request.POST.get("station-id"):

                try:
                   station_add = StationStng.objects.get(id = int(request.POST.get("station-id")))
                except:
                    messages.info(request, "Error!, please choose a station")
                    return redirect("main:book-settings")

                try:
                    loan_type = LoanTypeStng.objects.get(id = int(request.POST.get("loan-typeID")))
                except:
                    messages.info(request, "Error!, please choose correct loan type")
                    return redirect("main:book-settings")

                try:
                  add_item = AutoItemAdds.objects.get(item_name = 'borrowers_book', 
                                                      loan_typeID = loan_type,
                                                       stationID = station_add)
                  messages.info(request, "Error!, book already exists")
                except:
                    borrowers_book_category = ItemCategories.objects.get(item_category_name ="borrowers_book")
                    add_item = AutoItemAdds()
                    add_item.item_catID = borrowers_book_category
                    add_item.loan_typeID = loan_type
                    add_item.item_name = "borrowers_book"
                    add_item.unit_price = int(request.POST.get("book-fee"))
                    add_item.user_friendly_name = "Record Book"
                    add_item.stationID = station_add
                    add_item.save()
                    messages.info(request, "Success!, book added")


            if request.POST.get("item-id"):
                item = AutoItemAdds.objects.get(id= int( request.POST.get("item-id")))
                item.unit_price = int(request.POST.get('unit-price'))
                item.save()
                #notify te user that the change was successful
                messages.info(request, "Succes!, book settings updated")
         
        if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
        #check if user is allowed to view all stations
            auto_items = AutoItemAdds.objects.filter(item_name = 'borrowers_book').order_by("stationID")
        
        else:
        #else just view your station
            station = StationStng.objects.get(id= int(request.session["current_stationID"]))
            auto_items = AutoItemAdds.objects.filter(stationID= station, item_name='borrowers_book')
  
        return render(request, template_name="main/book_settings.html", context={"auto_items":auto_items,
                                             "get_global_db_objects":global_variables.get_global_db_objects(request),})



    
    def stations_processing_fee(request):

        try:
            x = request.session["current_stationID"]
            x = None
        except:
            return redirect("main:index")
   
        auto_items = None
        #check if user is alllowed to change interest settings
        if global_variables.user_rights(request.user, "allow_to_change_loan_interest_settings")=="Yes":
            

            #Add a record book
            if request.POST.get("unit-price") and request.POST.get("station-id"):

                try:
                   station_add = StationStng.objects.get(id = int(request.POST.get("station-id")))
                except:
                    messages.info(request, "Error!, please choose a station")
                    return redirect("main:processing-fee-settings")

                try:
                    loan_type = LoanTypeStng.objects.get(id = int(request.POST.get("loan-typeID")))
                except:
                    messages.info(request, "Error!, please choose correct loan type")
                    return redirect("main:processing-fee-settings")
          
                if True: 
                    #then lets add processing fee
                    processing_fee_category = ItemCategories.objects.get(item_category_name ="processing_fee")
                    add_item = AutoItemAdds()
                    add_item.item_catID = processing_fee_category
                    add_item.item_name = "processing_fee"
                    add_item.loan_typeID = loan_type
                    add_item.lower_limit = request.POST.get("lower-limit")
                    add_item.upper_limit = request.POST.get("upper-limit")
                    add_item.unit_price = int(request.POST.get("unit-price"))
                    add_item.stationID = station_add
                    add_item.save()



            if request.POST.get("item-id"):
                item = AutoItemAdds.objects.get(id= int( request.POST.get("item-id")))
                item.lower_limit = int(request.POST.get("lower-limit"))
                item.upper_limit = int(request.POST.get("upper-limit")) 
                item.unit_price = int(request.POST.get('unit-price'))
                item.save()
                #notify te user that the change was successful
                messages.info(request, "Succes!, processing fee settings updated")
         
        if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
        #check if user is allowed to view all stations
            if request.POST.get("station-id") and not(request.POST.get("station-id")=='0') \
                                                      and not(request.POST.get("station-id")==0):
               
               station = StationStng.objects.get(id= int(request.POST["station-id"]))
               auto_items = AutoItemAdds.objects.filter(item_name = 'processing_fee', stationID=station).order_by("lower_limit")
            else:
               auto_items = AutoItemAdds.objects.filter(item_name = 'processing_fee').order_by("stationID", "lower_limit")
        
        else:
        #else just view your station
            station = StationStng.objects.get(id= int(request.session["current_stationID"]))
            auto_items = AutoItemAdds.objects.filter(stationID= station, item_name='processing_fee')
  
        return render(request, template_name="main/processing_fee_settings.html", context={"auto_items":auto_items,
                                             "get_global_db_objects":global_variables.get_global_db_objects(request),})

