from main .models  import Loan, StationStng, Interest
from django.shortcuts import render
from datetime import datetime, timedelta
from .global_views import GlobalVariables

#initializing the global object
global_variables = GlobalVariables()

class FinesView():

    def view_fines(request):

        try: 
            user_station = request.session["current_stationID"]
            user_station = None
        except: 
            return redirect('main:index')
        
        total_fines=0
        fines_set = None

        if request.POST.get("station-id") and not request.POST.get("station-id")=="0" and not request.POST.get("station-id")==0:
           station = StationStng.objects.get(id=request.POST.get("station-id"))
        else:
           station = StationStng.objects.get(id=request.session["current_stationID"])

        if not request.POST:
            today = datetime.today()
            year= today.year
            month = today.month
            day = today.day
            total_paid = 0

            date1 = str(year)+"-"+str(month)+"-"+str(day)
            date2_str = today + timedelta(days=1)
            date2_obj = str(date2_str).split("-")
            date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2]

            if True:  
               if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                fines_set =Interest.objects.filter(record_date__gte = date1, 
                                                 record_date__lte = date2
                                                 ).order_by("record_date", "stationID")
               else:
                fines_set = Interest.objects.filter(record_date__gte = date1, 
                                                    record_date__lte = date2,
                                                   stationID = station
                                                   ).order_by("record_date", "stationID")


            #except:
            #    pass


        if request.POST.get("date1") and request.POST.get("date2"):
            date1  = request.POST.get("date1")
            date2_str = datetime.strptime(request.POST.get("date2"), '%Y-%m-%d')+ timedelta(days=1)
            date2_obj = str(date2_str).split("-")
            date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2]

            if True:
               if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                
                if not request.POST.get("station-id")=="0" and not request.POST.get("station-id")==0:                
                   fines_set = Interest.objects.filter(
                                                       record_date__gte = date1, 
                                                       record_date__lte = date2,
                                                       stationID = station
                                                        ).order_by("record_date", "stationID")
                else:
                    fines_set = Interest.objects.filter(
                                                       record_date__gte = date1, 
                                                       record_date__lte = date2,
                                                        ).order_by("record_date", "stationID")
                   
               else:
                fines_set = Loan.objects.filter(
                                                record_date__gte = date1, 
                                                record_date__lte = date2,
                                                stationID = station,
                                                ).order_by("record_date", "stationID")
        total_fines=0
        for fine in fines_set:
            total_fines += fine.amount


        return render(request, template_name="main/view_fines.html", 
                         context={"fines_set":fines_set, "total_fines":total_fines,
                                 "get_global_db_objects":global_variables.get_global_db_objects(request) ,"title":"Added Fines",})
