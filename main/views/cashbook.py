
from django.shortcuts import render, redirect
from main.models import CashBook, StationStng, cashBookMain, DeletedItems, ItemCategories, Loan, Client
from datetime import datetime, timedelta
from . global_views import GlobalVariables
from . cashbook_main import CashBookMainView
from . pivot_totals_view import PivotTotals
from django.contrib import messages
from django.db.models import Q

#initialixing the global object
global_variables = GlobalVariables()
#initializing pivots and totals
pivot_totals = PivotTotals()
#main cashbook
cashbook_main = CashBookMainView()




class CashBookView():

    
    def view_cashbook(request):
        
            try: 
                user_station = request.session["current_stationID"]
                user_station = None
            except: 
                return redirect('main:index')


            #setting opening balance
            if request.POST.get("opening-balance"):
                cashbook_main.set_opening_balance(request)
            

            #obtaining todays openng balance:
            cashbook_main_today = None
            total_incamount=0
            total_expamount=0
            total_netamount=0
            cashbook_set = None

            if request.POST.get("station-id") and not request.POST.get("station-id")=="0" \
               and not request.POST.get("station-id")==0:
                station = StationStng.objects.get(id=request.POST.get("station-id"))
            else:
                station = StationStng.objects.get(id=request.session["current_stationID"])


            if not request.POST:
                cashbook_main_today = cashbook_main.get_cash_book_main(request)
                today = datetime.today()
                year= today.year
                month = today.month
                day = today.day

                date1 = str(year)+"-"+str(month)+"-"+str(day)
                
                date2_str = today + timedelta(days=1)
                date2_obj = str(date2_str).split("-")
                date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2]

                if True:
                   if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                      cashbook_set = CashBook.objects.filter(
                                                           record_date__gte = date1,
                                                           record_date__lte = date2,                                                         
                                                            ).order_by("record_date", "stationID")
                   else:
                       cashbook_set = CashBook.objects.filter(
                                                           record_date__gte = date1,
                                                           record_date__lte = date2,
                                                           stationID = station,
                                                            ).order_by("record_date", "stationID")
                   for cashbook in cashbook_set:
                       if cashbook.inc_amount >0:
                           total_incamount += cashbook.inc_amount
                       if cashbook.exp_amount > 0:
                           total_expamount += cashbook.exp_amount
                   
                   if total_incamount >= total_expamount:
                       total_netamount = total_incamount - total_expamount
                   else:
                       total_netamount = "("+str((total_expamount - total_incamount)) +")"

                #except:
                 #   pass

                
            if request.POST.get("date1"):
                if True:

                    date1  = request.POST.get("date1")
                    date2_str = datetime.strptime(request.POST.get("date1"), '%Y-%m-%d')+ timedelta(days=1)
                    date2_obj = str(date2_str).split("-")
                    date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2]  

                else:
                    today = datetime.today()
                    year= today.year
                    month = today.month
                    day = today.day
                    date1 = str(year)+"-"+str(month)+"-"+str(day)
                    date2_str = today + timedelta(days=1)
                    date2_obj = str(date2_str).split("-")
                    date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2]

                if True:
                   if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                        if not request.POST.get("station-id")=="0" and not request.POST.get("station-id")==0:
                         cashbook_set = CashBook.objects.filter(
                                                           record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            stationID = station,
                                                            ).order_by("record_date", "stationID")
                         
                         cashbook_main_today = cashBookMain.objects.filter(
                                                           record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            stationID = station,
                                                            ).order_by("record_date", "stationID")
                        else:
                         cashbook_set = CashBook.objects.filter(
                                                            record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            ).order_by("record_date", "stationID")
                         
                         cashbook_main_today = cashBookMain.objects.filter(
                                                           record_date__gte = date1,
                                                            record_date__lte = date2
                                                            ).order_by("record_date", "stationID")

                   else:
                       cashbook_set = CashBook.objects.filter(
                                                           record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            stationID = station,
                                                            ).order_by("record_date", "stationID")
                       cashbook_main_today = cashBookMain.objects.filter(
                                                           record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            stationID = station,
                                                            ).order_by("record_date", "stationID")
                   for cashbook in cashbook_set:
                       if cashbook.inc_amount >0:
                           total_incamount += cashbook.inc_amount
                       if cashbook.exp_amount > 0:
                           total_expamount += cashbook.exp_amount
                   
                   if total_incamount >= total_expamount:
                       total_netamount = total_incamount - total_expamount
                   else:
                       total_netamount = "("+str((total_expamount - total_incamount)) +")"

                #except:
                   # pass
            

            #deleting items
            if request.POST.get("del-cashbookID") and \
             global_variables.user_rights(request.user, "allow_to_delete_from_cashbook")=="Yes":
                

                item = CashBook.objects.get(id=request.POST.get("del-cashbookID"))
    
                if item.item_catID.item_category_name == "loan":
                    try:
                        loan_items = CashBook.objects.filter(loanID = item.loanID) 

                        for loan_item in loan_items:
                            if not(loan_item.item_catID.item_category_name =="loan"):
                                messages.info(request, "Please first delete any items related to this loan")
                                return redirect("main:view-cashbook")
                        
                    except:
                        pass  
                if True:
                   cashbook_list = CashBook.objects.filter(id__gt=item.id, cashbooktmainID = item.cashbooktmainID)
                   for item2 in cashbook_list:
                       item2.balance +=item.exp_amount - item.inc_amount 
                       item2.save()

                #reducing values from cashbook main
                cashbooktmainID=item.cashbooktmainID
                cashbooktmainID.closing_balance+= (item.exp_amount - item.inc_amount)
                cashbooktmainID.save()


                if item.inc_exp_status == True: #if the item is an income
                    
                    if item.item_catID.item_category_name =="loan_payment":
                        #catering for loan recovered and interste paid
                        loan_recovered_category = ItemCategories.objects.get(item_category_name = "loan_recovered")
                        itenrest_paid_category = ItemCategories.objects.get(item_category_name = "interest_paid")

                        loan_recovered = ((float(request.session["daily_principle_pay_percent"])/100)*(item.inc_amount))
                        interest_paid = ((100-float(request.session["daily_principle_pay_percent"]))/100)*(item.inc_amount)

                        pivot_totals.set_totay_totals(request, item.stationID, loan_recovered_category, 
                                                      True, -1*loan_recovered, 0)
                        pivot_totals.set_totay_totals(request, item.stationID, itenrest_paid_category, 
                                                      True, -1*interest_paid, 0)

                    else:         
                        pivot_totals.set_totay_totals(request, item.stationID, item.item_catID, 
                                                      True, (-1*(float(item.inc_amount))), 0)
                else: #if the intem is an expense
                    
                    #Then if item is a loan
                    if item.item_catID.item_category_name == "loan":#i.e loan disbursement
                        this_loan = item.loanID
                        #loan principle
                        pivot_totals.set_totay_totals(request, item.stationID, item.item_catID, 
                                                      False,0, (-1*(float(this_loan.principle))))
                        
                        processing_fee_category= ItemCategories.objects.get(item_category_name= "processing_fee")
                        borrower_book_category = ItemCategories.objects.get(item_category_name= "borrowers_book")
                        #processing fee
                        pivot_totals.set_totay_totals(request, item.stationID, processing_fee_category, 
                                                      True,(-1*(float(this_loan.processing_fee))), 0)
                        #borrowers book
                        pivot_totals.set_totay_totals(request, item.stationID, borrower_book_category, 
                                                      True,(-1*(float(this_loan.borrowers_book_fee))), 0)
                        #now reducing client total
                        this_loan.clientID.current_total_balance -= this_loan.principle
                        this_loan.clientID.save()  
 
                    else:
                       #then if item is not a loan
                       pivot_totals.set_totay_totals(request, item.stationID, item.item_catID, 
                                                      False,0, (-1*(float(item.exp_amount))))
                                     
                       
                        
                #item categrory 2 =-loan payment
                #subtracting a cashnook
                
                if item.item_catID.item_category_name == "loan_payment":
                    loan = item.loanID
                    loan.loan_total_paid -= float(item.inc_amount)
                    loan.current_balance += float(item.inc_amount)
                    loan.save()
                    client = loan.clientID
                    client.borrowers_book_record-=1
                    client.current_total_balance += float(item.inc_amount)
                    client.save()

                #deleting the item
                deleted_item3 = DeletedItems()
                deleted_item3.stationID = item.stationID
                deleted_item3.reason = request.POST.get("reason") +" | Recorded by: "+ item.userID.username
                deleted_item3.description = (item.full_name or "") +" | "+(item.item_name or "") 
                deleted_item3.item_record_date = item.record_date
                deleted_item3.item_catID = item.item_catID
                deleted_item3.amount = item.inc_amount
                deleted_item3.exp_amount = item.exp_amount
                deleted_item3.userID = request.user
                deleted_item3.save()

                cashbooktmainID = item.cashbooktmainID

                
                try:
                    #clear items from interest book
                    item.interest_bookID.delete()
                except:
                    pass


                station = item.stationID
                record_date =item.record_date
                item.delete()


                if True:              
                   year = record_date.year
                   month = record_date.month
                   day = record_date.day
                   pivot_totals.pivot_for_interest_book(request, station, year, month, day)

        
                #delete main cashbook if there is just one item and 
                #this is done to clean out any opening balance in the opening table                               
                return redirect("main:view-cashbook")

                
            return render(request, template_name="main/view_cashbook.html", 
                            context={"cashbook_main_today": cashbook_main_today,
                                "cashbook_set":cashbook_set, "total_incamount":total_incamount, 
                                "total_expamount":total_expamount, "total_netamount":total_netamount,
                                "get_global_db_objects":global_variables.get_global_db_objects(request),"title":"CashBook",})
        
            
            

    def set_balance(self, request, station, inc_value, exp_value):
       
        new_balance_add = 0
           
        today = datetime.today()
        year= today.year
        month = today.month
        day = today.day

        #picking up the last cashbook_main_today_add     
        date_stationID = str(year)+"-"+str(month)+"-"+str(day)+"-"+str(station.id)  
        cashbook_main_today_add = cashBookMain.objects.get(date_stationID = date_stationID) 

        if cashbook_main_today_add.started == False:

            #pick opening balance
            opening_balance = cashbook_main_today_add.opening_balance
            net_value = float(inc_value) - float(exp_value)
            new_balance_add = opening_balance + net_value
                      
            #Flagging off the main cashbook since it needs to be added just once a day
            #the rest of the day it is just updated
            cashbook_main_today_add.started = True
            cashbook_main_today_add.save()
                        
        else:
            try:  
               last_cashbook = CashBook.objects.filter(cashbooktmainID = cashbook_main_today_add,
                                                       stationID= station).order_by("-id")[0]
               new_balance_add = last_cashbook.balance + (float(inc_value) - float(exp_value))
            except:
               new_balance_add = 0

        return new_balance_add




    def view_other_incomes_and_expenses(request):
            try: 
                user_station = request.session["current_stationID"]
                user_station = None
            except: 
                return redirect('main:index')

 

            #obtaining todays openng balance:
            cashbook_main_today = None
            total_incamount=0
            total_expamount=0
            total_netamount=0
            cashbook_set = None

            if request.POST.get("station-id") and not request.POST.get("station-id")=="0" \
               and not request.POST.get("station-id")==0:
                station = StationStng.objects.get(id=request.POST.get("station-id"))
            else:
                station = StationStng.objects.get(id=request.session["current_stationID"])


            if not request.POST:
                today = datetime.today()
                year= today.year
                month = today.month
                day = today.day

                date1 = str(year)+"-"+str(month)+"-"+str(day)
                
                date2_str = today + timedelta(days=1)
                date2_obj = str(date2_str).split("-")
                date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2]

                if True:
                   if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                      cashbook_set = CashBook.objects.filter(
                                                           record_date__gte = date1,
                                                           record_date__lte = date2,                                                         
                                                            ).order_by("record_date", "stationID")
                   else:
                       cashbook_set = CashBook.objects.filter(
                                                           record_date__gte = date1,
                                                           record_date__lte = date2,
                                                           stationID = station,
                                                            ).order_by("record_date", "stationID")
                   for cashbook in cashbook_set:
                       if cashbook.inc_amount >0:
                           total_incamount += cashbook.inc_amount
                       if cashbook.exp_amount > 0:
                           total_expamount += cashbook.exp_amount
                   
                   if total_incamount >= total_expamount:
                       total_netamount = total_incamount - total_expamount
                   else:
                       total_netamount = "("+str((total_expamount - total_incamount)) +")"

                #except:
                 #   pass

                
            if request.POST.get("date1"):
                if True:

                    date1  = request.POST.get("date1")
                    date2_str = datetime.strptime(request.POST.get("date2"), '%Y-%m-%d')+ timedelta(days=1)
                    date2_obj = str(date2_str).split("-")
                    date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2]  



                if True:
                   if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                        if not request.POST.get("station-id")=="0" and not request.POST.get("station-id")==0:
                         cashbook_set = CashBook.objects.filter(
                                                           record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            stationID = station,
                                                            ).order_by("record_date", "stationID")

                        else:
                         cashbook_set = CashBook.objects.filter(
                                                            record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            ).order_by("record_date", "stationID")


                   else:
                       cashbook_set = CashBook.objects.filter(
                                                           record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            stationID = station,
                                                            ).order_by("record_date", "stationID")

                   for cashbook in cashbook_set:
                       if cashbook.inc_amount >0:
                           total_incamount += cashbook.inc_amount
                       if cashbook.exp_amount > 0:
                           total_expamount += cashbook.exp_amount
                   
                   if total_incamount >= total_expamount:
                       total_netamount = total_incamount - total_expamount
                   else:
                       total_netamount = "("+str((total_expamount - total_incamount)) +")"


                
            return render(request, template_name="main/view_other_inc_exp.html", 
                            context={"cashbook_main_today": cashbook_main_today,
                                "cashbook_set":cashbook_set, "total_incamount":total_incamount, 
                                "total_expamount":total_expamount, "total_netamount":total_netamount,
                                "get_global_db_objects":global_variables.get_global_db_objects(request),"title":"CashBook",})
        
            
            

    def set_balance(self, request, station, inc_value, exp_value):
       
        new_balance_add = 0
           
        today = datetime.today()
        year= today.year
        month = today.month
        day = today.day

        #picking up the last cashbook_main_today_add     
        date_stationID = str(year)+"-"+str(month)+"-"+str(day)+"-"+str(station.id)  
        cashbook_main_today_add = cashBookMain.objects.get(date_stationID = date_stationID) 

        if cashbook_main_today_add.started == False:

            #pick opening balance
            opening_balance = cashbook_main_today_add.opening_balance
            net_value = float(inc_value) - float(exp_value)
            new_balance_add = opening_balance + net_value
                      
            #Flagging off the main cashbook since it needs to be added just once a day
            #the rest of the day it is just updated
            cashbook_main_today_add.started = True
            cashbook_main_today_add.save()
                        
        else:
            try:  
               last_cashbook = CashBook.objects.filter(cashbooktmainID = cashbook_main_today_add,
                                                       stationID= station).order_by("-id")[0]
               new_balance_add = last_cashbook.balance + (float(inc_value) - float(exp_value))
            except:
               new_balance_add = 0

        return new_balance_add





       




    