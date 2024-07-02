
from django.shortcuts import render, redirect
from main.models import InterestBook, StationStng, Track_auto_item_adds
from datetime import datetime, timedelta
from . global_views import GlobalVariables
from django.contrib import messages
from django.db.models import Q

#initialixing the global object
global_variables = GlobalVariables()


class WeeklyReportDetailsView():

    #This class reports shows details from the interset book by giving the report about each item

    def view_borrowers_book(request):
        '''
        This function lists books sold betwwen date and date2
        '''
        
        try: 
            user_station = request.session["current_stationID"]
            user_station = None
        except: 
            return redirect('main:index')

        details_list = None
        detail_count = 0
        detail_total_amount = 0
        station = None
          
        if request.POST.get('date1') and request.POST.get('date2'):
            
            date1  = request.POST.get("date1")
            date2_str = datetime.strptime(request.POST.get("date2"), '%Y-%m-%d')+ timedelta(days=1)
            date2_obj = str(date2_str).split("-")
            date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2] 

            if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":

                 if request.POST.get("station-id") and not(request.POST.get("station-id")=='0') \
                                                      and not(request.POST.get("station-id")==0):

                        station = StationStng.objects.get(id= int(request.POST.get("station-id")))
                        details_list  = InterestBook.objects.filter(                                               
                                                record_date__gte=date1, 
                                                record_date__lte=date2,
                                                stationID = station,
                                                borrowers_book__gt=1,
                                                ).order_by("record_date", "stationID")
                        
                 else:
                        details_list  = InterestBook.objects.filter(
                                                record_date__gte=date1,
                                                record_date__lte=date2,
                                                borrowers_book__gt=1,
                                                ).order_by("record_date", "stationID")
                                                
            else:

                station = StationStng.objects.get(id = int(request.session["current_stationID"]))
                details_list  = InterestBook.objects.filter(
                                                record_date__gte=date1,
                                                record_date__lte=date2,
                                                stationID = station,
                                                borrowers_book__gt=1,
                                                ).order_by("record_date", "stationID")

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

            
           
            if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                #view all staions if you have the rights
                #by deafult a person with rights will view all records from their station
                details_list  = InterestBook.objects.filter(
                                                record_date__gte=date1, 
                                                record_date__lte=date2,
                                                borrowers_book__gt=1,
                                                ).order_by("record_date", "stationID")
                 #details_list  = InterestBook.objects.all()
                                           
            else:
                   #by deafult a person will view only records from their station
                station = StationStng.objects.get(id = int(request.session["current_stationID"]))
                details_list  = InterestBook.objects.filter(
                                                record_date__gte=date1,
                                                record_date__lte=date2,
                                                borrowers_book__gt=1,
                                                stationID = station,
                                                ).order_by("record_date", "stationID")
        
            #except:
            #pass
        detail_count = 0
        detail_total_amount = 0
        for counter in details_list:
                detail_count += 1
                try:
                   detail_total_amount += counter.borrowers_book
                except:
                    detail_total_amount += 0


        return render(request, template_name="main/detail_borrowers_book.html",
                       context={"details_list": details_list,
                       "detail_count":detail_count, "detail_total_amount":detail_total_amount,
                       "date1":date1,"date2":date2,
                       "get_global_db_objects":global_variables.get_global_db_objects(request),})#context edns here





    def view_processing_fee(request):

        '''
         This function lists the the interest paid between date 1 and date2 
        '''

        try: 
            user_station = request.session["current_stationID"]
            user_station = None
        except: 
            return redirect('main:index')

        details_list = None
        detail_count = 0
        detail_total_amount = 0
        station = None
          
        if request.POST.get('date1') and request.POST.get('date2'):
            
            date1  = request.POST.get("date1")
            date2_str = datetime.strptime(request.POST.get("date2"), '%Y-%m-%d')+ timedelta(days=1)
            date2_obj = str(date2_str).split("-")
            date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2] 

            if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":

                if request.POST.get("station-id") and not(request.POST.get("station-id")=='0') \
                                                      and not(request.POST.get("station-id")==0):

                        station = StationStng.objects.get(id= int(request.POST.get("station-id")))
                        details_list  = InterestBook.objects.filter(
                                                record_date__gte=date1, 
                                                record_date__lte=date2,
                                                processing_fee__gt = 0,
                                                stationID = station,
                                                ).order_by("record_date", "stationID")
                else:
                        details_list  = InterestBook.objects.filter(
                                                record_date__gte=date1,
                                                record_date__lte=date2,
                                                processing_fee__gt = 0,
                                                ).order_by("record_date", "stationID")
            else:

                station = StationStng.objects.get(id = int(request.session["current_stationID"]))
                details_list  = InterestBook.objects.filter(
                                                record_date__gte=date1,
                                                record_date__lte=date2,
                                                processing_fee__gt = 0,
                                                stationID = station,
                                                ).order_by("record_date", "stationID")

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

            
           
            if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                #view all staions if you have the rights
                #by deafult a person with rights will view all records from their station
                details_list  = InterestBook.objects.filter(
                                                record_date__gte=date1, 
                                                record_date__lte=date2,
                                                processing_fee__gt = 0,
                                                ).order_by("record_date", "stationID")
                        #details_list  = InterestBook.objects.all()                 
                        
            else:
                   #by deafult a person will view only records from their station
                station = StationStng.objects.get(id = int(request.session["current_stationID"]))
                details_list  = InterestBook.objects.filter(
                                                record_date__gte=date1,
                                                record_date__lte=date2,
                                                processing_fee__gt = 0,
                                                stationID = station,
                                                ).order_by("record_date", "stationID")
        
            #except:
            #pass
        detail_count = 0
        detail_total_amount = 0
        for counter in details_list:
                detail_count += 1
                detail_total_amount += counter.processing_fee




        return render(request, template_name="main/detail_processing_fee.html",
                       context={"details_list": details_list,
                       "detail_count":detail_count, "detail_total_amount":detail_total_amount,
                       "date1":date1,"date2":date2,
                       "get_global_db_objects":global_variables.get_global_db_objects(request),})#context edns here




    def view_interest_paid(request):

        '''
         This function lists the the interest paid between date 1 and date2 
        '''

        try: 
            user_station = request.session["current_stationID"]
            user_station = None
        except: 
            return redirect('main:index')

        details_list = None
        detail_count = 0
        detail_total_amount = 0
        station = None
          
        if request.POST.get('date1') and request.POST.get('date2'):
            
            date1  = request.POST.get("date1")
            date2_str = datetime.strptime(request.POST.get("date2"), '%Y-%m-%d')+ timedelta(days=1)
            date2_obj = str(date2_str).split("-")
            date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2] 

            if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":

                if request.POST.get("station-id") and not(request.POST.get("station-id")=='0') \
                                                      and not(request.POST.get("station-id")==0):

                    station = StationStng.objects.get(id= int(request.POST.get("station-id")))
                    details_list  = InterestBook.objects.filter(
                                                record_date__gte=date1, 
                                                record_date__lte=date2,
                                                interest_paid__gt = 0,
                                                stationID = station,
                                                ).order_by("record_date", "stationID")

                else:
                    details_list  = InterestBook.objects.filter(
                                                record_date__gte=date1,
                                                record_date__lte=date2,
                                                interest_paid__gt = 0,
                                                ).order_by("record_date", "stationID")
            else:

                station = StationStng.objects.get(id = int(request.session["current_stationID"]))
                details_list  = InterestBook.objects.filter(
                                                record_date__gte=date1,
                                                record_date__lte=date2,
                                                interest_paid__gt = 0,
                                                stationID = station,
                                                ).order_by("record_date", "stationID")

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

            
           
            if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                 #view all staions if you have the rights
                    if request.POST.get("station-id") and not(request.POST.get("station-id")=='0') \
                                                      and not(request.POST.get("station-id")==0):

                        station = StationStng.objects.get(id= int(request.POST.get("station-id")))
                        details_list  = InterestBook.objects.filter(
                                                record_date__gte=date1, 
                                                record_date__lte=date2,
                                                interest_paid__gt = 0,
                                                stationID = station,
                                                ).order_by("record_date", "stationID")
                        
                    else:
                        #by deafult a person with rights will view all records from their station
                        details_list  = InterestBook.objects.filter(
                                                record_date__gte=date1, 
                                                record_date__lte=date2,
                                                interest_paid__gt = 0,
                                                ).order_by("record_date", "stationID")
                        #details_list  = InterestBook.objects.all()                 

                        
            else:
                   #by deafult a person will view only records from their station
                station = StationStng.objects.get(id = int(request.session["current_stationID"]))
                details_list  = InterestBook.objects.filter(
                                                record_date__gte=date1,
                                                record_date__lte=date2,
                                                interest_paid__gt = 0,
                                                stationID = station,
                                                ).order_by("record_date", "stationID")

        
            #except:
            #pass
        detail_count = 0
        detail_total_amount = 0
        for counter in details_list:
                detail_count += 1
                detail_total_amount += counter.interest_paid



        return render(request, template_name="main/detail_interest_paid.html",
                       context={"details_list": details_list,
                       "detail_count":detail_count, "detail_total_amount":detail_total_amount,
                       "date1":date1,"date2":date2,
                       "get_global_db_objects":global_variables.get_global_db_objects(request),})#context edns here





    def view_detail_fines(request):

        '''
         This function lists the the interest paid between date 1 and date2 
        '''

        try: 
            user_station = request.session["current_stationID"]
            user_station = None
        except: 
            return redirect('main:index')

        details_list = None
        detail_count = 0
        detail_total_amount = 0
        station = None
          
        if request.POST.get('date1') and request.POST.get('date2'):
            
            date1  = request.POST.get("date1")
            date2_str = datetime.strptime(request.POST.get("date2"), '%Y-%m-%d')+ timedelta(days=1)
            date2_obj = str(date2_str).split("-")
            date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2] 

            if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                
                
                if request.POST.get("station-id") and not(request.POST.get("station-id")=='0') \
                                                      and not(request.POST.get("station-id")==0):
                    station = StationStng.objects.get(id= int(request.POST.get("station-id")))
                    details_list  = InterestBook.objects.filter(
                                                record_date__gte=date1, 
                                                record_date__lte=date2,
                                                fines__gt = 0,
                                                stationID = station,
                                                ).order_by("record_date", "stationID")
                        
                else:
                    details_list  = InterestBook.objects.filter(
                                                record_date__gte=date1,
                                                record_date__lte=date2,
                                                fines__gt = 0,
                                                ).order_by("record_date", "stationID")
            else:

                station = StationStng.objects.get(id = int(request.session["current_stationID"]))
                details_list  = InterestBook.objects.filter(
                                                record_date__gte=date1,
                                                record_date__lte=date2,
                                                fines__gt = 0,
                                                stationID = station,
                                                ).order_by("record_date", "stationID")

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

            
           
            if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                 #view all staions if you have the rights
                        #by deafult a person with rights will view all records from their station
                details_list  = InterestBook.objects.filter(
                                                record_date__gte=date1, 
                                                record_date__lte=date2,
                                                fines__gt = 0,
                                                ).order_by("record_date", "stationID")
                #details_list  = InterestBook.objects.all()          
            else:
                #by deafult a person will view only records from their station
                station = StationStng.objects.get(id = int(request.session["current_stationID"]))
                details_list  = InterestBook.objects.filter(
                                                record_date__gte=date1,
                                                record_date__lte=date2,
                                                fines__gt = 0,
                                                stationID = station,
                                                ).order_by("record_date", "stationID")
       
            #except:
            #pass
        detail_count = 0
        detail_total_amount = 0
        for counter in details_list:
                detail_count += 1
                detail_total_amount += counter.fines


        return render(request, template_name="main/detail_fines.html",
                       context={"details_list": details_list,
                       "detail_count":detail_count, "detail_total_amount":detail_total_amount,
                       "date1":date1,"date2":date2,
                       "get_global_db_objects":global_variables.get_global_db_objects(request),})#context edns here






    def view_detail_loan_recovered(request):

        '''
         This function lists the the interest paid between date 1 and date2 
        '''
        try: 
            user_station = request.session["current_stationID"]
            user_station = None
        except: 
            return redirect('main:index')

        details_list = None
        detail_count = 0
        detail_total_amount = 0
        station = None
          
        if request.POST.get('date1') and request.POST.get('date2'):
            
            date1  = request.POST.get("date1")
            date2_str = datetime.strptime(request.POST.get("date2"), '%Y-%m-%d')+ timedelta(days=1)
            date2_obj = str(date2_str).split("-")
            date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2] 

            if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                
                
                if request.POST.get("station-id") and not(request.POST.get("station-id")=='0') \
                                                      and not(request.POST.get("station-id")==0):
                    station = StationStng.objects.get(id= int(request.POST.get("station-id")))
                    details_list  = InterestBook.objects.filter(
                                                record_date__gte=date1, 
                                                record_date__lte=date2,
                                                loan_recovered__gt = 0,
                                                stationID = station,
                                                ).order_by("record_date", "stationID")
                        
                else:
                    details_list  = InterestBook.objects.filter(
                                                record_date__gte=date1,
                                                record_date__lte=date2,
                                                loan_recovered__gt = 0,
                                                ).order_by("record_date", "stationID")
            else:

                station = StationStng.objects.get(id = int(request.session["current_stationID"]))
                details_list  = InterestBook.objects.filter(
                                                record_date__gte=date1,
                                                record_date__lte=date2,
                                                loan_recovered__gt = 0,
                                                stationID = station,
                                                ).order_by("record_date", "stationID")

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

            
           
            if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                 #view all staions if you have the rights
                        #by deafult a person with rights will view all records from their station
                details_list  = InterestBook.objects.filter(
                                                record_date__gte=date1, 
                                                record_date__lte=date2,
                                                loan_recovered__gt = 0,
                                                ).order_by("record_date", "stationID")
                #details_list  = InterestBook.objects.all()          
            else:
                #by deafult a person will view only records from their station
                station = StationStng.objects.get(id = int(request.session["current_stationID"]))
                details_list  = InterestBook.objects.filter(
                                                record_date__gte=date1,
                                                record_date__lte=date2,
                                                loan_recovered__gt = 0,
                                                stationID = station,
                                                ).order_by("record_date", "stationID")
       
            #except:
            #pass
        detail_count = 0
        detail_total_amount = 0
        for counter in details_list:
                detail_count += 1
                detail_total_amount += counter.loan_recovered


        return render(request, template_name="main/detail_loan_recovered.html",
                       context={"details_list": details_list,
                       "detail_count":detail_count, "detail_total_amount":detail_total_amount,
                       "date1":date1,"date2":date2,
                       "get_global_db_objects":global_variables.get_global_db_objects(request),})#context edns here
