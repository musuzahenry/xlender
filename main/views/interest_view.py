from django.shortcuts import render, redirect
from main.models import Interest, StationStng, DailyPayBacksInterest
from . global_views import GlobalVariables
from . loan_view import LoanView
from datetime import datetime, timedelta
from django.contrib import messages

#initialixing the global object
global_variables = GlobalVariables()

class InterestViews():


    def adjust_fines(self, request):

        try: 
            user_station = request.session["current_stationID"]
            user_station = None
        except: 
            return redirect('main:index')

        if global_variables.user_rights(request.user, "allow_to_adjust_fines")=="Yes":
            pass
        else:
            messages.info(request, 'Sorry, you have no rights to adjust this value')
            return redirect('main:index')

        
        fines = Interest.objects.get(id = int(request.POST.get('interest-to-adjust')) )

        fines.loanID.current_balance += (int(request.POST.get('amount')) - int(fines.amount))
        
        if (fines.loanID.total_fines +(int(request.POST.get('amount')) - int(fines.amount)) ) >=0:
           fines.loanID.total_fines += (int(request.POST.get('amount')) - int(fines.amount)) 
        else:
            fines.loanID.total_fines = 0

        fines.loanID.save()
        fines.loanID.clientID.current_total_balance += (int(request.POST.get('amount')) - int(fines.amount))
        fines.loanID.clientID.save()

        fines.amount = int(request.POST.get('amount'))
        fines.save()

        global_variables.set_current_loan(request, fines.loanID)
        global_variables.set_current_client(request, fines.loanID.clientID)
        return redirect('main:index')




    def del_fines(self, request):

        try: 
            user_station = request.session["current_stationID"]
            user_station = None
        except: 
            return redirect('main:index')
        
        if global_variables.user_rights(request.user, "allow_to_adjust_fines")=="Yes":
            pass
        else:
            messages.info(request, 'Sorry, you have no rights to adjust this value')
            return redirect('main:index')

        
        fines = Interest.objects.get(id = int(request.POST.get('del-fineID')) )

        fines.loanID.current_balance -=  int(fines.amount)

        if (fines.loanID.total_fines -  int(fines.amount)) >=0:
           fines.loanID.total_fines -=  int(fines.amount)
        else:
            fines.loanID.total_fines = 0
            
        fines.loanID.save()
        fines.loanID.clientID.current_total_balance -= int(fines.amount)
        fines.loanID.clientID.save()

        #finally delete the fine
        fines.delete()

        global_variables.set_current_loan(request, fines.loanID)
        global_variables.set_current_client(request, fines.loanID.clientID)
        return redirect('main:index')    




    
    def view_interest(request):

        try: 
            user_station = request.session["current_stationID"]
            user_station = None
        except: 
            return redirect('main:index')

        #there is redired
        #there is redired
        #there is redired
        #there is redired
        #there is redired
        return redirect("main:index")
        daily_pay_back_interest_set = None
        interest_set = None
        total_iterest=0

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
                      StationStng.objects.get(id=request.POST.get("station-id"))
                      interest_set = Interest.objects.filter(
                                                            record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            ).order_by("-record_date", "stationID")
                      
                      daily_pay_back_interest_set = DailyPayBacksInterest.objects.filter(
                                                            record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            ).order_by("-record_date", "stationID")
                          
                   else:
                       station = StationStng.objects.get(id=request.session["current_stationID"])
                       interest_set = Interest.objects.filter(
                                                            record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            stationID = station,
                                                           ).order_by("-record_date", "stationID")
                       
                       daily_pay_back_interest_set = DailyPayBacksInterest.objects.filter(
                                                            record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            stationID = station,
                                                            ).order_by("-record_date", "stationID")
                                                           
                   total_iterest =0
                   for interest in interest_set:
                       total_iterest+=interest.amount
                    
                   for interest in daily_pay_back_interest_set:
                       total_iterest+=interest.interest_added
                       
                #except:
                #    pass
        
        if request.POST.get("date1") and request.POST.get("date2"):
                if global_variables.user_rights(request.user, "allow_to_back_date")=="Yes":
                    date1  = request.POST.get("date1")
                    date2_str = datetime.strptime(request.POST.get("date2"), '%Y-%m-%d')+ timedelta(days=1)
                    date2_obj = str(date2_str).split("-")
                    date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2]

                if global_variables.user_rights(request.user, "allow_to_back_date")=="Yes":
                   if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                      
                      if request.POST.get("station-id") and not request.POST.get("station-id")=="0" and \
                         not request.POST.get("station-id")==0:
                         station = StationStng.objects.get(id=request.POST.get("station-id"))
                         interest_set = Interest.objects.filter(
                                                            record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            stationID = station,
                                                            ).order_by("-record_date", "stationID")
                      
                         daily_pay_back_interest_set = DailyPayBacksInterest.objects.filter(
                                                            record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            stationID = station,
                                                            ).order_by("-record_date", "stationID")
                      else:
                         interest_set = Interest.objects.filter(
                                                            record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            ).order_by("-record_date", "stationID")
                      
                         daily_pay_back_interest_set = DailyPayBacksInterest.objects.filter(
                                                            record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            ).order_by("-record_date", "stationID")
                          
                   else:
                       station = StationStng.objects.get(id=request.session["current_stationID"])
                       interest_set = Interest.objects.filter(
                                                            record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            stationID = station,
                                                           ).order_by("-record_date", "stationID")
                       
                       daily_pay_back_interest_set = DailyPayBacksInterest.objects.filter(
                                                            record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            stationID = station,
                                                            ).order_by("-record_date", "stationID")
                                                           
                   total_iterest =0
                   for interest in interest_set:
                       total_iterest+=interest.amount
                    
                   for interest in daily_pay_back_interest_set:
                       total_iterest+=interest.interest_added
                       
                #except:
                #    pass
                            
        return render(request, template_name="main/view_interest.html", 
                            context={"interest_set":interest_set, 
                                     "daily_pay_back_interest_set":daily_pay_back_interest_set,
                                     "total_incamount":total_iterest, 
                            "get_global_db_objects":global_variables.get_global_db_objects(request),"title":"Interest",})
        
            