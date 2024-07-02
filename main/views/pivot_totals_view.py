from django.shortcuts import render , redirect
from main.models import Monthly_ite_totals, Yearly_ite_totals, StationStng, ItemCategories, \
Daily_item_catID_totals, CashBook, InterestBook, WeeklyBook
from datetime import datetime, timedelta
from .  global_views import GlobalVariables
from django.contrib import messages


global_variables = GlobalVariables()
#getting a set of all categories that we have
ITEM_CATEGORIES_SET = ItemCategories.objects.all()

#getting a set of all stations that we have
STATIONS_SET  = StationStng.objects.all()

class PivotTotals():

    def set_totay_totals(self, request, stationID, item_catID, inc_exp_status, inc_amount, exp_amount):
                
        if not (request.session["current_stationID"]):
            return redirect('main:index')

        #initializing year, month, and day vairables    
        today = datetime.today()
        year= today.year
        month = today.month
        day = today.day

        #calling to pivot interest book
        self.pivot_for_interest_book(request, stationID,  year, month, day)

    

    def pivot_for_interest_book(self, request, stationID, year, month, day):
        #this function pivots the interest_book into the weekly book

                
        if request.POST.get("interest-id"):
            #make date values for edit value
             interestID = request.POST.get("interest-id")
             this_interest_book = InterestBook.objects.get(id=interestID)
             item = CashBook.objects.get(interest_bookID = this_interest_book)
             item_record_date = item.record_date
             year = item_record_date.year
             month = item_record_date.month
             day = item_record_date.day
        
        date_str_stationID = str(year)+"-"+str(month)+"-"+str(day)+"-"+str(stationID.id)

        date1 = datetime.strptime(str(year)+"-"+str(month)+"-"+str(day)+ " 00:00:00+00:00","%Y-%m-%d %H:%M:%S%z")
        date2 = date1 + timedelta(days=1)


        try:
            weekly = WeeklyBook.objects.get(date_str_stationID = date_str_stationID)
        except:
             weekly = WeeklyBook()
             weekly.fines = 0
             weekly.borrowers_book  = 0
             weekly.loan_processing_fee = 0
             weekly.interest_paid = 0
             weekly.total = 0
             weekly.date_str_stationID = date_str_stationID
             weekly.stationID = stationID
             weekly.save()

        if True:
            
            interest_book_list = InterestBook.objects.filter(record_date__gte = date1,
                                                             record_date__lte=date2, stationID=stationID)
            fines=0
            record_book=0
            interest_paid=0
            processing_fee=0
            total=0
            for book in interest_book_list: 
                fines += book.fines
                record_book += book.borrowers_book
                interest_paid += book.interest_paid 
                processing_fee += book.processing_fee
            total = fines +  record_book + interest_paid + processing_fee

            weekly.fines = fines
            weekly.borrowers_book  = record_book
            weekly.loan_processing_fee = processing_fee
            weekly.interest_paid = interest_paid
            weekly.total = total
            weekly.save()

           
       
       # except:
        #    pass

            





    def view_report(request):

        try: 
            user_station = request.session["current_stationID"]
            user_station = None
        except: 
            return redirect('main:index')         

        pivots_day = ""
        pivots_month=""
        pivots_year=""

        if not request.POST:
            
                today = datetime.today()
                year= today.year
                month = today.month
                day = today.day

                date_item= str(year)+"-"+str(month)+"-"+str(day)
                day_month= str(year)+"-"+str(month)
                year= today.year
 
                if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                   pivot_weekly = WeeklyBook.objects.filter(date_str_stationID__icontains = \
                                                        date_item).order_by("stationID")
                else:
                    stationID = StationStng.objects.get(id = int(request.session["current_stationID"]))
                    pivot_weekly = WeeklyBook.objects.filter(date_str_stationID__icontains = \
                                                        date_item,
                                                        stationID = stationID).order_by("stationID")

    
                
        if request.POST.get("date1") and request.POST.get("date2"):
                today = datetime.today()
                year= today.year
                month = today.month
                day = today.day
                   
                month_year= str(year)+"-"+str(month)
                year= today.year

                date_item= str(year)+"-"+str(month)+"-"+str(day)
                day_month= str(year)+"-"+str(month)
                year= today.year
                
                date1 =  request.POST.get("date1")
                date2_str = datetime.strptime(request.POST.get("date2"), '%Y-%m-%d')+ timedelta(days=1)
                date2_obj = str(date2_str).split("-")
                date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2]  
                

                if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                    if request.POST.get("station-id") and not (request.POST.get("station-id")== 0 )\
                    and not(request.POST.get("station-id")=="0"):
                        station = StationStng.objects.get(id=request.POST.get("station-id"))                 
    
                        pivot_weekly = WeeklyBook.objects.filter(record_date__gte=date1, record_date__lte=date2, \
                                                                stationID= station).order_by("stationID")

                    else:

                        pivot_weekly = WeeklyBook.objects.filter \
                        (record_date__gte=date1, record_date__lte=date2).order_by("stationID")
                else:
                    stationID = StationStng.objects.get(id = int(request.session["current_stationID"]))
                    pivot_weekly = WeeklyBook.objects.filter \
                                   (record_date__gte=date1, record_date__lte=date2,
                                    stationID = stationID).order_by("stationID")



        #Getting weekly sums
        total_fines = 0
        total_on_books = 0
        total_processing = 0
        total_interest = 0
        totally = 0
        for week in pivot_weekly:
            total_fines += week.fines
            total_on_books+=week.borrowers_book
            total_processing += week.loan_processing_fee
            total_interest += week.interest_paid
            totally += week.total

 
        return render(request, template_name ="main/pivot_totals.html", context={
                "get_global_db_objects":global_variables.get_global_db_objects(request),
                "total_fines":total_fines, "total_on_books":total_on_books,
                "total_processing":total_processing, "total_interest":total_interest,
                "totally":totally,
                "pivot_weekly":pivot_weekly,
            })













     
     






