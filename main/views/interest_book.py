from django.shortcuts import render, redirect
from main.models import StationStng, InterestBook, CashBook, ItemCategories
from .global_views import GlobalVariables
from datetime import datetime, timedelta
from .pivot_totals_view import PivotTotals


global_variables = GlobalVariables()
pivot_totals = PivotTotals()



class InterestBookView():
    
    def view_interest_book(request):

        try: 
            user_station = request.session["current_stationID"]
            user_station = None
        except: 
            return redirect('main:index')

        interest_book_set = None
        total_iterest_paid =0
        total_loan_recovered=0
        total_loan_disbursed=0
        total_borrowers_book=0
        total_processing_fee =0
        total_fines_fee = 0


        if request.POST.get("interest-id"):
            #if global_variables.user_rights(request.user, "allow_to_correct_interest_book")=="Yes":
            if True:
                interestID = request.POST.get("interest-id")
                this_interest_book = InterestBook.objects.get(id=interestID)

                new_inc_amount = float(request.POST.get("record-book")) + float(request.POST.get("processing-fee"))
                
                #working on cashbook, balances main cashbook, closing balance and opening balance
                this_cashbook = CashBook.objects.get(interest_bookID = this_interest_book)
                cashbook_list = CashBook.objects.filter(cashbooktmainID = this_cashbook.cashbooktmainID,
                                                        id__gt = this_cashbook.id)
                this_cashbook.cashbooktmainID.closing_balance = this_cashbook.cashbooktmainID.closing_balance - \
                                                                this_cashbook.inc_amount + new_inc_amount
                this_cashbook.cashbooktmainID.save()

                for a_cashbook in cashbook_list:
                    a_cashbook.balance = a_cashbook.balance - this_cashbook.inc_amount + new_inc_amount
                    a_cashbook.save()
                
                #re-pivoting before saving this cashbook
                #we pivot 2 times, that is, remove th old values and then add new ones
                processing_fee_category = ItemCategories.objects.get(item_category_name ="processing_fee")
                borrowers_book_category = ItemCategories.objects.get(item_category_name ="borrowers_book")


                #saving everyithing before pivots can be done
                this_cashbook.balance = this_cashbook.balance  - this_cashbook.inc_amount + new_inc_amount
                this_cashbook.inc_amount = new_inc_amount
                this_cashbook.save()  
                this_interest_book.borrowers_book = float(request.POST.get("record-book"))
                this_interest_book.processing_fee= float(request.POST.get("processing-fee"))
                this_interest_book.save()

                pivot_totals.set_totay_totals(request, this_cashbook.stationID, borrowers_book_category, 
                                                        True, -1*(this_interest_book.borrowers_book), 0) 
                pivot_totals.set_totay_totals(request, this_cashbook.stationID, processing_fee_category, 
                                                        True,  -1*(this_interest_book.processing_fee), 0)

                pivot_totals.set_totay_totals(request, this_cashbook.stationID, borrowers_book_category, 
                                                        True, float(request.POST.get("record-book")), 0) 
                pivot_totals.set_totay_totals(request, this_cashbook.stationID, processing_fee_category, 
                                                        True, float(request.POST.get("processing-fee")), 0)



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
                      try:
                        station =  StationStng.objects.get(id=request.session["current_stationID"])
                      except:
                          return redirect("main:index")
                      interest_book_set = InterestBook.objects.filter(
                                                            record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            ).order_by("record_date", "stationID")                          
                   else:
                       station = StationStng.objects.get(id=request.session["current_stationID"])
                       interest_book_set = InterestBook.objects.filter(
                                                            record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            stationID = station,
                                                           ).order_by("record_date", "stationID")
                   
                   for interest in interest_book_set:
                        total_iterest_paid+=interest.interest_paid
                        total_loan_recovered+=interest.loan_recovered
                        total_loan_disbursed+=interest.loan_disbursed
                        total_borrowers_book+=interest.borrowers_book
                        total_processing_fee+=interest.processing_fee
                        total_fines_fee+=interest.fines
                                
                            #except:
                            #    pass
                                                           


        
        if request.POST.get("date1") and request.POST.get("date2"):
                #if global_variables.user_rights(request.user, "allow_to_back_date")=="Yes":
                if True:
                    date1  = request.POST.get("date1")
                    date2_str = datetime.strptime(request.POST.get("date2"), '%Y-%m-%d')+ timedelta(days=1)
                    date2_obj = str(date2_str).split("-")
                    date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2]

                #if global_variables.user_rights(request.user, "allow_to_back_date")=="Yes":
                if True:
                   if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                      
                      if request.POST.get("station-id") and not request.POST.get("station-id")=="0" and \
                         not request.POST.get("station-id")==0:
                         station = StationStng.objects.get(id=request.POST.get("station-id"))
                         interest_book_set = InterestBook.objects.filter(
                                                            record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            stationID = station,
                                                            ).order_by("-record_date", "stationID")
                      else:
                         interest_book_set = InterestBook.objects.filter(
                                                            record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            ).order_by("-record_date", "stationID")
                          
                   else:
                       station = StationStng.objects.get(id=request.session["current_stationID"])
                       interest_book_set = InterestBook.objects.filter(
                                                            record_date__gte = date1,
                                                            record_date__lte = date2,
                                                            stationID = station,
                                                           ).order_by("-record_date", "stationID") 
                else: 
                    return redirect("main:view-interest-book")                                                          
                                                           

                for interest in interest_book_set:
                    total_iterest_paid+=interest.interest_paid
                    total_loan_recovered+=interest.loan_recovered
                    total_loan_disbursed+=interest.loan_disbursed
                    total_borrowers_book+=interest.borrowers_book
                    total_processing_fee+=interest.processing_fee
                    total_fines_fee+=interest.fines
                            
                        #except:
                        #    pass
                            
        return render(request, template_name="main/view_interest_book.html", 
                            context={"interest_book_set":interest_book_set, 
                                     "total_loan_recovered":total_loan_recovered,
                                     "total_iterest_paid":total_iterest_paid, 
                                     "total_loan_disbursed":total_loan_disbursed,
                                     "total_borrowers_book":total_borrowers_book,
                                     "total_processing_fee": total_processing_fee,
                                     "total_fines_fee": total_fines_fee,                                    
                            "get_global_db_objects":global_variables.get_global_db_objects(request),"title":"Interest Book",})
        
            
