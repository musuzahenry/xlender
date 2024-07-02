from django.shortcuts import render
from django.contrib import messages
from main.models import CourtQueue, StationStng, CashBook, cashBookMain, OtherPayments
from datetime import datetime, timedelta
from django.utils import timezone
from .global_views import *

global_variables = GlobalVariables()

class CourtQueueView():

    def manually_add_court_queue(request):
        
        try: 
            user_station = request.session["current_stationID"]
            user_station = None
        except: 
            return redirect('main:index')   
               
        if request.POST.get("add-to-court-queue"):

            station = StationStng.objects.get(id=int(request.session["current_stationID"]))

            court = CourtQueue()
            court.stationID = station
            court.full_name =  request.POST.get("surname").upper() + " "+  request.POST.get("othernames").upper()
            court.gender = request.POST.get("gender")        
            court.contacts = request.POST.get("contacts")
            court.demand_notice = request.POST.get("demand-notice")
            court.address = request.POST.get("address").upper() 
            court.loan_record_date = request.POST.get("loan-record-date")
            court.record_date = timezone.now
            court.loan_debt = request.POST.get("balance")
            court.loan_principle = request.POST.get("principle")
            court.notes = request.POST.get("details")
            court.userID = request.user
            court.save()

            return redirect("main:view-court-queue")


    def  view_court_queue(request):

        try: 
            user_station = request.session["current_stationID"]
            user_station = None
        except: 
            return redirect('main:index')  
               
        court_set = None
        total_balance=0
        total_principle=0

        #deleting from cour queue
        if request.POST.get("del-court-id"):
                del_item = CourtQueue.objects.get(id = int(request.POST.get("del-court-id")))
                del_item.del_notes = request.POST.get("details") + "  \n " + \
                "\n ========================================================== \n " + \
                "Removed by: " + str(request.user)
                del_item.remove_from_court_queue = True
                del_item.save()
                return redirect("main:view-court-queue")
   
        if request.POST.get("name-seach"):
                name_search = request.POST.get("name-seach")
                try:
                   if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                      court_set = CourtQueue.objects.filter(full_name__icontains = name_search
                                                            ).order_by("-id", "stationID")
                 
                   else:
                       station = StationStng.objects.get(id=request.session["current_stationID"])
                       court_set = CourtQueue.objects.filter(full_name__icontains = name_search,
                                                             stationID = station,
                                                           ).order_by("-id", "stationID")
                except:
                    pass


        if not request.POST:

                today = datetime.today()
                year= today.year
                month = today.month
                day = today.day

                date1 = str(year)+"-"+str(month)+"-"+str(day)
                
                date2_str = today + timedelta(days=1)
                date2_obj = str(date2_str).split("-")
                date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2]
                

                try:
                   if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                      court_set = CourtQueue.objects.filter(remove_from_court_queue= False,).order_by("-id", "stationID")
                 
                   else:
                       station = StationStng.objects.get(id=request.session["current_stationID"])
                       court_set = CourtQueue.objects.filter(stationID = station,
                                                            remove_from_court_queue= False,
                                                           ).order_by("-id", "stationID")
                except:
                    pass


               
        
        if request.POST.get("date1") and request.POST.get("date2"):
                if True:
                    date1  = request.POST.get("date1")
                    date2_str = datetime.strptime(request.POST.get("date2"), '%Y-%m-%d')+ timedelta(days=1)
                    date2_obj = str(date2_str).split("-")
                    date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2] 

                try:
                   if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                      if request.POST.get("station-id") and not request.POST.get("station-id")==0 and \
                       not request.POST.get("station-id")=="0":
                         station = StationStng.objects.get(id=request.POST.get("station-id"))
                         court_set = CourtQueue.objects.filter(
                                                            record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            stationID = station,
                                                            remove_from_court_queue= False,
                                                            ).order_by("-record_date", "stationID")
                      else:
                         court_set = CourtQueue.objects.filter(
                                                            record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            remove_from_court_queue= False,
                                                            ).order_by("-record_date", "stationID")

                      
                          
                   else:
                       station = StationStng.objects.get(id=request.session["current_stationID"])
                       court_set = CourtQueue.objects.filter(
                                                            record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            stationID = station,
                                                            remove_from_court_queue= False,
                                                           ).order_by("-record_date", "stationID")
                                       
                except:
                    pass

        try:
            for court in court_set:
                total_balance +=court.loan_debt
                total_principle+=court.loan_principle

        except:
            pass
                      
        return render(request, template_name="main/court_queue.html", 
                            context={"court_set":court_set, 
                                     "total_balance":total_balance, "total_principle":total_principle,
                            "get_global_db_objects":global_variables.get_global_db_objects(request),"title":"Court Queue",})
        
    
    def court_transactions(request):

            try: 
                user_station = request.session["current_stationID"]
                user_station = None
            except: 
                return redirect('main:index')
                    
            if not request.POST:        
                today = datetime.today()
                year= today.year
                month = today.month
                day = today.day

                date1 = str(year)+"-"+str(month)+"-"+str(day)
                    
                date2_str = today + timedelta(days=1)
                date2_obj = str(date2_str).split("-")
                date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2]
                    

                try:
                    if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                       transaction_set = OtherPayments.objects.filter(record_date__gte = date1,
                                                                record_date__lte = date2,
                                                                courtID__isnull = False,
                                                                ).order_by("-id", "stationID")
                    
                    else:
                        station = StationStng.objects.get(id=request.session["current_stationID"])
                        transaction_set = OtherPayments.objects.filter(record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            stationID = station,
                                                            courtID__isnull = False,
                                                            ).order_by("-id", "stationID")
                except:
                        pass


                
            
            if request.POST.get("date1") and request.POST.get("date2"):
                if True:
                        date1  = request.POST.get("date1")
                        date2_str = datetime.strptime(request.POST.get("date2"), '%Y-%m-%d')+ timedelta(days=1)
                        date2_obj = str(date2_str).split("-")
                        date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2] 

                try:
                    if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                        if request.POST.get("station-id") and not request.POST.get("station-id")==0 and \
                        not request.POST.get("station-id")=="0":
                            station = StationStng.objects.get(id=request.POST.get("station-id"))
                            transaction_set = OtherPayments.objects.filter(
                                                                record_date__gte = date1,
                                                                record_date__lte = date2,
                                                                stationID = station,
                                                                courtID__isnull = False,
                                                                ).order_by("-record_date", "stationID")
                        else:
                            transaction_set = OtherPayments.objects.filter(
                                                                record_date__gte = date1,
                                                                record_date__lte = date2,
                                                                courtID__isnull = False,
                                                                ).order_by("-record_date", "stationID")

                        
                            
                    else:
                        station = StationStng.objects.get(id=request.session["current_stationID"])
                        transaction_set = OtherPayments.objects.filter(
                                                                record_date__gte = date1,
                                                                record_date__lte = date2,
                                                                stationID = station,
                                                            ).order_by("-record_date", "stationID")
                                        
                except:
                    pass
            
            total_spent =0
            total_paid = 0
            for cashitem in transaction_set:
                total_spent += cashitem.credit
                total_paid += cashitem.debit

            all_diff = total_spent - total_paid
            if all_diff<0:
                all_diff = "("+ f"{-1*all_diff:,}" +")"

            return render(request, template_name="main/court_transactions.html", 
                                context={"transaction_set":transaction_set, 
                                        "all_diff":all_diff,
                                        "total_spent":total_spent,
                                        "total_paid":total_paid,
                                        "get_global_db_objects":global_variables.get_global_db_objects(request),
                                        "title":"Court Transactions",})






class CourtQueueActions():

    def add_client_to_court(self, request, client, loan, current_total_balance, total_court_expenses, demand_notice, more_notes):

        new_court_case = CourtQueue()
        new_court_case.clientID = client
        
        new_court_case.stationID = loan.stationID
        new_court_case.loanID =loan
        new_court_case.full_name =loan.full_name
        new_court_case.gender = client.gender
        new_court_case.dob = client.date_of_birth
        new_court_case.contacts= client.contact_numbers
        new_court_case.national_identification_number = client.national_identification_number
        new_court_case.address= client.physical_address
        new_court_case.loan_record_date= loan.record_date
        new_court_case.loan_expected_pay_date = loan.expected_clearance_date
        new_court_case.loan_principle =  loan.principle
        new_court_case.loan_debt = current_total_balance
        new_court_case.total_court_expense =  total_court_expenses
        new_court_case.total_paid =  loan.loan_total_paid
        new_court_case.demand_notice = demand_notice
        new_court_case.notes = more_notes
        new_court_case.userID=request.user
        new_court_case.save()
        
        #now let system know that client is already in court
        loan.sent_to_court = True
        loan.save()

            