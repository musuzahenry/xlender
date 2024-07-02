from django .shortcuts import  redirect, render
from main.models import CashBook, cashBookMain, StationStng, ItemCategories
from datetime import datetime, timedelta
from . global_views import GlobalVariables
from .pivot_totals_view import PivotTotals
from django.contrib import messages


#initialixing the global object
global_variables = GlobalVariables()
#initializing pivots and totals
pivot_totals = PivotTotals()

class CashBookMainView():

    def set_opening_balance(self, request):
        
        cashbook_mainID = request.POST.get("cashbook-main-id")   
        new_opening_balance_main = float(request.POST.get("opening-balance"))
                
        if True:
            cashbook_main_today = cashBookMain.objects.get(id=cashbook_mainID)  
            station = cashbook_main_today.stationID
            this_opening_balance = cashbook_main_today.opening_balance          
            cashbook_main_today.opening_balance = new_opening_balance_main

            try:
                cashbook_list = CashBook.objects.filter(cashbooktmainID = cashbook_main_today)
                n = 0

                first_cashbook = CashBook.objects.filter(cashbooktmainID = cashbook_main_today,
                                                       stationID= station).order_by("id")[0]
                first_cashbook.balance = first_cashbook.inc_amount - first_cashbook.exp_amount + \
                                          new_opening_balance_main
                first_cashbook.save()

                prev_cashbook_val = first_cashbook.inc_amount - first_cashbook.exp_amount + new_opening_balance_main
                
                for cashbook_item in cashbook_list:
                    if cashbook_item.id != first_cashbook.id:                  
                        cashbook_item.balance = cashbook_item.inc_amount - cashbook_item.exp_amount + \
                                                + prev_cashbook_val 
                        old_cashbook_val = cashbook_item.inc_amount - cashbook_item.exp_amount + \
                                                + prev_cashbook_val 
                        prev_cashbook_val = old_cashbook_val
                        cashbook_item.save()

                last_cashbook_list = CashBook.objects.filter(cashbooktmainID = cashbook_main_today).order_by("-id")[0]
                cashbook_main_today.closing_balance =last_cashbook_list.balance
                
                cashbook_main_today.save()
            except:
                cashbook_main_today.closing_balance = new_opening_balance_main
            
            cashbook_main_today.save()

        else:
            messages.info(request, "You are not allowed to set opening balance")

        return redirect("main:view-cashbook")

   
    def get_cash_book_main(self, request):
    
        today = datetime.today()
        year= today.year
        month = today.month
        day = today.day

        date1 = str(year)+"-"+str(month)+"-"+str(day)          
        date2_str = today + timedelta(days=1)
        date2_obj = str(date2_str).split("-")
        date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2]
        
        if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":

            if request.POST.get("station-id") and not request.POST.get("station-id")==0 \
                and not request.POST.get("station-id") == "0":
                station = StationStng.objects.get(id = request.POST.get("station-id"))
                cashbook_main_today = cashBookMain.objects.filter(record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            stationID = station)
            else:
                cashbook_main_today = cashBookMain.objects.filter(record_date__gte = date1,
                                                            record_date__lte = date2)
                                                            
        else:
            station = StationStng.objects.get(id = request.session["current_stationID"])
            cashbook_main_today = cashBookMain.objects.filter(record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            stationID = station) 
        return cashbook_main_today
    


    def check_for_cashbook(self, request):
    
        today = datetime.today()
        year= today.year
        month = today.month
        day = today.day
        try:   
            station = StationStng.objects.get(id = request.session["current_stationID"])
            date_stationID = str(year)+"-"+str(month)+"-"+str(day)+"-"+str(station.id)          
            cashbook_main_today_add = cashBookMain.objects.get(date_stationID = date_stationID)
            return True
        except:
            return False
        

    def get_current_main_cashbook(self, station):

        today = datetime.today()
        year= today.year
        month = today.month
        day = today.day
        try:   
            date_stationID = str(year)+"-"+str(month)+"-"+str(day)+"-"+str(station.id)          
            cashbook_main_today_add = cashBookMain.objects.get(date_stationID = date_stationID)
            return cashbook_main_today_add
        except:
            return None


    def inititialize_cash_book(self, request):


        if self.check_for_cashbook(request) == True:
                return redirect("main:index")
        
        today = datetime.today()
        year= today.year
        month = today.month
        day = today.day
        date1 = str(year)+"-"+str(month)+"-"+str(day)

        date2_str = today + timedelta(days= -1)
        date2_obj = str(date2_str).split("-")
        date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2]

        try:
            station = StationStng.objects.get(id=request.session["current_stationID"])
            last_main_cashbook_last = cashBookMain.objects.filter(stationID= station).order_by("-id")[0]
            last_closing_balance = last_main_cashbook_last.closing_balance
            mew_main_cashbook = cashBookMain()
            mew_main_cashbook.opening_balance = last_closing_balance
            mew_main_cashbook.stationID = station
            mew_main_cashbook.date_stationID = date1+"-"+str(station.id)
            mew_main_cashbook.closing_balance = last_closing_balance
            mew_main_cashbook.save()
        except:
            station = StationStng.objects.get(id=request.session["current_stationID"])
            mew_main_cashbook = cashBookMain()
            mew_main_cashbook.stationID = station
            mew_main_cashbook.opening_balance = 0
            mew_main_cashbook.closing_balance = 0           
            mew_main_cashbook.date_stationID = date1+"-"+str(station.id)            
            mew_main_cashbook.save()
            









        