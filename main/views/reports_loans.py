from django.shortcuts import render, redirect
from main.models import Loan, StationStng, VisitedLoans
from datetime import datetime, timedelta
from . global_views import GlobalVariables

global_variables = GlobalVariables()

class ReportLoans():

    def approve_loans(request):
                
        try: 
            user_station = request.session["current_stationID"]
            user_station = None
        except: 
            return redirect('main:index')

        today = datetime.today()
        year= today.year
        month = today.month
        day = today.day

        date1= str(year)+"-"+str(month)+"-"+str(day)
        date2_str = today + timedelta(days=1)
        date2_obj = str(date2_str).split("-")
        date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2]

        approve_loans_set =None
        total_principle = 0
        station = StationStng.objects.get(id=request.session["current_stationID"])

        if True:
            if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":    
               approve_loans_set = Loan.objects.filter(approve_status=False,
                                                    record_date__gte = date1, 
                                                    record_date__lte = date2,
                                                    ).order_by("-record_date", "stationID")
            else:
                approve_loans_set = Loan.objects.filter(approve_status=False,
                                                    record_date__gte = date1, 
                                                    record_date__lte = date2,
                                                    stationID = station,
                                                    ).order_by("-record_date", "stationID")
            for loan in approve_loans_set:
                 total_principle += loan.principle

            
        
        #except:
        #   pass
        
           
        return render(request, template_name="main/loan_report.html", 
                         context={"approve_loans_set":approve_loans_set,"total_principle":total_principle,
                                  "title":"Approve Loans"})
        


    def approved_loans(request):
            
        try: 
            user_station = request.session["current_stationID"]
            user_station = None
        except: 
            return redirect('main:index')

        today = datetime.today()
        year= today.year
        month = today.month
        day = today.day

        today = datetime.today()
        year= today.year
        month = today.month
        day = today.day

        date1= str(year)+"-"+str(month)+"-"+str(day)
        date2_str = today + timedelta(days=1)
        date2_obj = str(date2_str).split("-")
        date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2]

        approve_loans_set =None
        total_principle=0
        station = StationStng.objects.get(id=request.session["current_stationID"])

        if True:
            if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":    
               approve_loans_set = Loan.objects.filter(approve_status=True,
                                                       disburse_status=False,
                                                       record_date__gte = date1, 
                                                       record_date__lte = date2,
                                                    ).order_by("-record_date", "stationID")
            else:
                approve_loans_set = Loan.objects.filter(approve_status=True,
                                                        disburse_status=False,
                                                        record_date__gte = date1, 
                                                        record_date__lte = date2,
                                                        stationID = station,
                                                    ).order_by("-record_date", "stationID")
            for loan in approve_loans_set:
                 total_principle += loan.principle

            
        #except:
        #   pass
           

        return render(request, template_name="main/loan_report.html", 
                         context={"approve_loans_set":approve_loans_set, "total_principle":total_principle,
                                  "title":"Loans For Disburse ",})
    

    def  disbursed_loans(request):
           
        try: 
            user_station = request.session["current_stationID"]
            user_station = None
        except: 
            return redirect('main:index')
 
        total_principle=0
        disbursed_loans_set = None

        if request.POST.get("station-id") and not request.POST.get("station-id")==0 \
                                 and not request.POST.get("station-id")=="0":
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
                   disbursed_loans_set = Loan.objects.filter(disburse_status=True,
                                                        record_date__gte = date1, 
                                                        record_date__lte = date2,
                                                        ).order_by("-record_date", "stationID")
               else:
                   disbursed_loans_set = Loan.objects.filter(disburse_status=True,
                                                        record_date__gte = date1, 
                                                        record_date__lte = date2,
                                                        stationID = station,
                                                        ).order_by("-record_date", "stationID")
               for loan in disbursed_loans_set:
                    total_principle += loan.principle
            #except:
            #   pass


        if request.POST.get("date1") and request.POST.get("date2"):
            date1  = request.POST.get("date1")
            date2_str = datetime.strptime(request.POST.get("date2"), '%Y-%m-%d')+ timedelta(days=1)
            date2_obj = str(date2_str).split("-")
            date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2] 

            if global_variables.user_rights(request.user, "allow_to_back_date")=="Yes":
               if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes": 
                    if request.POST.get("station-id") and not request.POST.get("station-id")==0 \
                                                        and not request.POST.get("station-id")=="0":
                       disbursed_loans_set = Loan.objects.filter(disburse_status=True,
                                                        record_date__gte = date1, 
                                                        record_date__lte = date2,
                                                        stationID = station,
                                                        ).order_by("-record_date", "stationID")
                    else:
                        disbursed_loans_set = Loan.objects.filter(disburse_status=True,
                                                        record_date__gte = date1, 
                                                        record_date__lte = date2,
                                                        ).order_by("-record_date", "stationID")
                        
               else:
                   disbursed_loans_set = Loan.objects.filter(disburse_status=True,
                                                        record_date__gte = date1, 
                                                        record_date__lte = date2,
                                                        stationID = station,
                                                        ).order_by("-record_date", "stationID")
               for loan in disbursed_loans_set:
                    total_principle += loan.principle
            #except:
            #   pass


        return render(request, template_name="main/loans_disbursed.html", 
                         context={"disbursed_loans_set":disbursed_loans_set, "total_principle":total_principle,
                                  "get_global_db_objects":global_variables.get_global_db_objects(request) ,"title":"Loan List",})




    def  loan_debts(request):

            try: 
                user_station = request.session["current_stationID"]
                user_station = None
            except: 
                return redirect('main:index')

            total_principle=0
            total_debts=0
            loan_debts_set = None

            if request.POST.get("station-id") and not request.POST.get("station-id")==0 \
                                          and not request.POST.get("station-id")=="0":
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
                       loan_debts_set = Loan.objects.filter(disburse_status=True,
                                                            record_date__gte = date1, 
                                                            record_date__lte = date2,
                                                            current_balance__gt= 0,
                                                            ).order_by("-record_date", "stationID")
                   else:                     
                      loan_debts_set = Loan.objects.filter(disburse_status=True,
                                                            record_date__gte = date1, 
                                                            record_date__lte = date2,
                                                            stationID = station,
                                                            current_balance__gt= 0,
                                                            ).order_by("-record_date", "stationID")
                   for loan in loan_debts_set:
                        total_principle += loan.principle
                        total_debts += loan.current_balance
                #except:
                #    pass


            if request.POST.get("date1") and request.POST.get("date2"):
                date1  = request.POST.get("date1")
                date2_str = datetime.strptime(request.POST.get("date2"), '%Y-%m-%d')+ timedelta(days=1)
                date2_obj = str(date2_str).split("-")
                date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2] 


                if True:
                   if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes": 
                        if request.POST.get("station-id") and not request.POST.get("station-id")==0 \
                                                         and not request.POST.get("station-id")=="0":
                           loan_debts_set = Loan.objects.filter(disburse_status=True,
                                                            record_date__gte = date1, 
                                                            record_date__lte = date2,
                                                            stationID = station,
                                                            current_balance__gt= 0,
                                                            ).order_by("-record_date", "stationID")
                        else:
                           loan_debts_set = Loan.objects.filter(disburse_status=True,
                                                            record_date__gte = date1, 
                                                            record_date__lte = date2,
                                                            current_balance__gt= 0,
                                                            ).order_by("-record_date", "stationID")
                   else:   
                                     
                      loan_debts_set = Loan.objects.filter(disburse_status=True,
                                                            record_date__gte = date1, 
                                                            record_date__lte = date2,
                                                            stationID = station,
                                                            current_balance__gt= 0,
                                                            ).order_by("-record_date", "stationID")
                   for loan in loan_debts_set:
                        total_principle += loan.principle
                        total_debts += loan.current_balance

                        
               # except:
                #    pass
            

            return render(request, template_name="main/loan_debts.html", 
                            context={"loan_debts_set":loan_debts_set, "total_principle":total_principle,
                                    "total_debts":total_debts , 
                                    "get_global_db_objects":global_variables.get_global_db_objects(request) ,"title":"Loan Debts",})




    def visited_loans(request): 
           
        try: 
            user_station = request.session["current_stationID"]
            user_station = None
        except: 
            return redirect('main:index')

        if global_variables.user_rights(request.user, "allow_to_view_visited_loans")=="Yes":
            pass
        else:
            return redirect('main:index')
            
        #instantiaring visited loans
        visited_loan_list = None
        
            
        if request.POST.get('date1') and request.POST.get('date2'):
            date1  = request.POST.get("date1")
            date2_str = datetime.strptime(request.POST.get("date2"), '%Y-%m-%d')+ timedelta(days=1)
            date2_obj = str(date2_str).split("-")
            date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2] 
        else:
            #by default, todays data is immediately loaded
            today = datetime.today()
            year= today.year
            month = today.month
            day = today.day
            date1 = str(year)+"-"+str(month)+"-"+str(day)               
            date2_str = today + timedelta(days=1)
            date2_obj = str(date2_str).split("-")
            date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2]
         
            
            #Selecting from database

        
        if request.POST.get("station-id") and not(request.POST.get("station-id")=='0') \
                                               and not(request.POST.get("station-id")==0):

            station = StationStng.objects.get(id= int(request.POST.get("station-id")))
            visited_loan_list  = VisitedLoans.objects.filter(
                                                    record_date__gte=date1, 
                                                    record_date__lte=date2,
                                                    stationID = station,
                                                    ).order_by("record_date", "stationID")
        else:
            visited_loan_list  = VisitedLoans.objects.filter(
                                                    record_date__gte=date1, 
                                                    record_date__lte=date2,
                                                    ).order_by("record_date", "stationID") 
                     

        return render(request, template_name="main/visited_loan.html",
                        context={"visited_loan_list":visited_loan_list, "date1":date1, "date2":date2,
                        "get_global_db_objects":global_variables.get_global_db_objects(request),})#context edns here





