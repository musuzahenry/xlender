from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from datetime import date, datetime, timedelta
from .global_views import *
from .pivot_totals_view import PivotTotals
from main.views.processing_fee import ProcessingFee
from main.views.client_view import ClientView
from main.models import Client, StationStng, DailyPayBack, Loan, LoanTypeStng, CashBook, \
            ItemCategories, Track_auto_item_adds, AutoItemAdds, InterestBook, AgreementFile

from . cashbook_main import CashBookMainView
from . cashbook import CashBookView


#ininitalizing our objects
global_variables = GlobalVariables()
pivot_totals = PivotTotals()
cashbook_main = CashBookMainView()
cashbook_balance = CashBookView()


class LoanView():
    
    @login_required(login_url="/")
    def pay_loan(request):
        if request.POST.get("pay-old-loansx") and 9==7:        
            today = datetime.today()
            yesterday = today + timedelta(days=-1)

            deccription= request.POST.get("description")
            amount = int(request.POST.get("amount"))

            station = StationStng.objects.get(id=int(request.session["current_stationID"]))
            item_catID = ItemCategories.objects.get(item_category_name= request.POST.get("item-catID"))
            
            #saing loan to interset book
            interest_book = InterestBook()
            interest_book.stationID = station  
            interest_book.full_name = deccription

            if item_catID.item_category_name =="paying_existing_loan":                           
                interest_book.loan_recovered = (amount*((float(request.session["daily_principle_pay_percent"]))/100))
                interest_book.interest_paid = (amount*((100-float(request.session["daily_principle_pay_percent"]))/100))
            if item_catID.item_category_name =="fines":
                interest_book.fines = amount
      
            interest_book.userID = request.user
            interest_book.save()
            interest_book2 = InterestBook.objects.get(id=interest_book.id)
            interest_book2.record_date = yesterday
            interest_book2.save(update_fields=['record_date'])

            return redirect("main:manage-incomes-and-expenses")
        return render (request, template_name="main/income_expense_view_history.html")
        
                           


    @login_required(login_url="/")
    def add_loan(request):

        if cashbook_main.check_for_cashbook(request) == False:
            return render (request, template_name="main/view_cashbook.html", 
                           context={"err_message":"Please first enter Opening balance"
            })
                
        if not request.method == "POST":
            return redirect("main:index")

        #getting the station
        if request.POST.get("stationID") and not ( request.POST.get("stationID") ==0 
                                          or request.POST.get("stationID")=="0" ):
            stationID = request.POST.get("stationID")
            if not stationID == 0 and not stationID == "0":
                      stationID = request.POST.get("stationID") 
            else:
                   stationID = request.session["current_stationID"]
        else:
            stationID = request.session["current_stationID"]
        

        #getting loan_typeID
        
        if request.POST.get("loan-typeID"):
                loan_typeID = request.POST.get("loan-typeID")
                if not (loan_typeID == "NA"):                
                      loan_typeID = request.POST.get("loan-typeID")     
                else:
                   station = StationStng.objects.get(id=int(request.session["current_stationID"]))
                   loan_typeID=station.loan_typeID.id
        else:
             loan_typeID = request.session["current_loan_typeID"]
           
        
        if request.POST.get("actual-add-loan"):
                try:
                    x_client = request.session["current_clientID"]
                    x_client = None
                except:
                    messages.info(request, "Please first load client")
                    return redirect('main:index')

                                
                #setting values
                loan = Loan()
                
                client = Client.objects.get(id=request.session["current_clientID"])               
                client_fullname = request.session["current_client_fullname"]
                loan_typeID = LoanTypeStng.objects.get(id=int(request.POST.get("loan-typeID")))
                stationID = StationStng.objects.get(id=int(request.POST.get("stationID")))
                prepared_by= Employee.objects.get(user_accountID  = request.user)
                prepared_by_name = (prepared_by.surname or "") + " "+ \
                (prepared_by.first_name or "") + " "+\
                (prepared_by.other_names or "")


                principle = float(request.POST.get("principle"))

                if request.POST.get("interest-rate"):
                   original_interest = (float(request.POST.get("interest-rate"))/100) * float(principle)
                else:
                    if loan_typeID.id == 1:                   
                        if int(stationID.daily_percent)  > 0:
                            original_interest = (int(stationID.daily_percent)/100) * int(request.POST.get("principle"))
                        else:
                            original_interest = (int(request.session["default_loan_interest_percent"])/100) * int(request.POST.get("principle"))
                    else:
                        if int(stationID.monthly_percent)  > 0:
                            original_interest = (int(stationID.monthly_percent)/100) * int(request.POST.get("principle"))
                        else:
                            original_interest = (int(request.session["default_loan_interest_percent"])/100) * int(request.POST.get("principle"))            
                
                current_interest = original_interest
                total_loan_interest = original_interest
                current_balance = principle + original_interest

                #getting pay method
                pay_methodID=request.POST.get("pay-methodID")
                pay_method = Paymethod.objects.get(id= int(pay_methodID))

                pay_medium =  request.POST.get("pay-medium")
                pay_identification =  request.POST.get("pay-identification")
                if  request.POST.get("loan-duration"):
                    loan_duration = int(request.POST.get("loan-duration"))
                else:
                    loan_duration =  int(request.session["default_loan_duration"])

                expected_clearance_date = datetime.today() + timedelta(days=loan_duration)

                loan.clientID = client
                loan.full_name  = client_fullname
                loan.principle = principle
                loan.current_principle = principle
                loan.original_interest = original_interest
                loan.current_interest =current_interest
                loan.total_loan_interest = total_loan_interest
                loan.current_balance = current_balance
                loan.prepared_by_name = prepared_by_name
                loan.pay_medium = pay_medium
                loan.pay_identification = pay_identification
                loan.loan_duration = loan_duration
                loan.expected_clearance_date = expected_clearance_date
                
                loan.userID= request.user
                loan.pay_methodID = pay_method
                loan.stationID = stationID
                loan.loan_typeID = loan_typeID

                #passing ids again
                loan_typeIDx = loan_typeID
                stationIDx = stationID
             
                loan.save()

                if True: #This code block wont execute
                    if loan.loan_typeID.id == 1:

                        #Appending to daily payment
                        #==================================================================
                        
                        #we use current balance 
                        #daily_pay = None                 
                        for day in range(30):
                            daily_pay  = DailyPayBack()
                            expected_pay_date = datetime.today() + timedelta(day + 1)
                            daily_pay.expected_pay_date = expected_pay_date                  
                            daily_pay.loanID = loan
                            daily_pay.clientID = loan.clientID
                            daily_pay.stationID = loan.stationID
                            daily_pay.full_name = loan.full_name
                            daily_total_pay_back = (current_balance / loan_duration)
                            daily_principle_pay_back= daily_total_pay_back*(float(request.session["daily_principle_pay_percent"])/100)
                            daily_interest_pay_back =daily_total_pay_back*((100-float(request.session["daily_principle_pay_percent"]))/100)

                            daily_pay.original_principle = principle
                            daily_pay.total_day_debt = daily_total_pay_back
                            daily_pay.principle_day_pay_back = daily_principle_pay_back
                            daily_pay.interest_day_pay_back = daily_interest_pay_back
                            daily_pay.total_day_balance = daily_total_pay_back
                            daily_pay.save()


                #passing variables to next session
                loan_typeID = loan_typeIDx.id #for redundancy, not so necessary but important
                stationID = stationIDx.id #for redundancy, not so necessary but important
                global_variables.set_current_loan(request, loan)
                
                return redirect("/edit-loan")
        

        interest_percent =0

        this_station = StationStng.objects.get(id = int(stationID))

        if int(loan_typeID) == 1 and this_station.daily_percent > 0 and not (this_station.daily_percent is None) :
            interest_percent = this_station.daily_percent
        elif int(loan_typeID) == 2 and this_station.monthly_percent > 0 and not (this_station.monthly_percent is None) :
            interest_percent = this_station.monthly_percent
        else:
            interest_percent = request.session["default_loan_interest_percent"]

        
        return render(request, template_name="main/loan_view_create_form.html", 
                      context={"stationID":stationID,"loan_typeID":loan_typeID, 
                               "interest_percent":interest_percent,
                               "get_global_db_objects":global_variables.get_global_db_objects(request)})
    
            




    @login_required(login_url="/")
    def edit_loan(request):
        
        warning_message ="" #displayed if one tries to change an approved loan
        loan_editable = None # is set to disabled once loan is approved
        loan = None
        
        try:
           loan = Loan.objects.get(id = request.session["current_loanID"])
        except:
           loan = None

        #redirecting if no loan has been loaded
        if loan is None:
            return redirect("main:index")
        

        #approving loan
        if request.POST.get("approve-loan"):
            loan.approved_byID = request.user.id
            #getting approvers full name
            if True:
            #checking if the user has approve rights
               if loan.disburse_status==False:
                  emp = Employee.objects.get(user_accountID = request.user)
                  fullname = (emp.surname or " ")+" "+(emp.first_name or " ")+" "+(emp.other_names or " ")
                  loan.approved_by_name = fullname
                  if request.POST.get("allow-loan-without-book") =="yes" and (loan.loan_typeID.id==1):
                      loan.allow_get_loan_without_processing_book = True
                      if not (int(request.POST.get("no-of-rows")) == 0):
                         
                        #updating clinet total balance and tracking book
                        borrower_book_tracker = Track_auto_item_adds()
                        borrower_book_tracker.clientID = loan.clientID
                        borrower_book_tracker.stationID = loan.stationID
                        borrower_book_tracker.item_name = "borrowers_book"
                        borrower_book_tracker.closed = False
                        borrower_book_tracker.loanID =loan
                        borrower_book_tracker.save()

                        loan.clientID.borrowers_book_record = int(request.session["records_in_borrowers_book"])-int(request.POST.get("no-of-rows"))

                        #lets record record book bypass
                        client_view = ClientView()
                        client_view.edit_book(request)

                        global_variables.set_current_client(request, loan.clientID)
                  else:
                      loan.allow_get_loan_without_processing_book = False  

                  loan.approve_status = True

                  try:
                      #delete unapproved loans for this client
                      del_loan_list = Loan.objects.filter(clientID = loan.clientID, id__lt = loan.id,
                                                      approve_status=False)
                      for loanx in del_loan_list:
                          loanx.delete()
                  except:
                      pass
                  
                  #approving the loan
                  warning_message ="Loan approved!"
                  loan.save()
               else:
                    if request.POST.get("record-date"):
                        if global_variables.user_rights(request.user, "allow_to_edit_loan_date")=="Yes":
                            loan.record_date = request.POST.get("record-date")
                            loan.save(update_fields=["record_date"])
                            record_date = str(loan.record_date).split(" ")
                            request.session["loan_record_date"] = record_date[0]
                            warning_message ="Date Updated"
                   

                    
                    if request.POST.get("count-status"):
                        if global_variables.user_rights(request.user, "allow_to_stop_auto_loan_fines") == "Yes":   
                            
                            if request.POST.get("count-status") == "Yes":
                                warning_message ="Monthly Automatic Fines Stopped yesssssssssss"
                            else:
                                loan.stop_loan_counting = True
                                loan.save(update_fields=["stop_loan_counting"])
                                warning_message ="Monthly Automatic Fines Stopped"
                                request.session["auto_fines"] = True

                         
                    warning_message ="Loan already disbursed"
                             
            else:
                warning_message ="You are not allwed to approve loans"


        #disbursing loan
        if request.POST.get("disburse-loan"):
            
            if ((request.POST.get("no-of-rows") == "0" or request.POST.get("no-of-rows") == 0) \
            and request.POST.get("allow-loan-without-book") == "yes") and loan.loan_typeID.id==1:
                
                warning_message ="Please enter how much of the book has been used"
                return redirect("main:edit-loan")

            if not request.session["current_stationID"]:
                return redirect("main:index")
            if loan.approve_status == True:
                if loan.disburse_status == False:
                    emp = Employee.objects.get(user_accountID = request.user)
                    fullname = (emp.surname or " ")+" "+(emp.first_name or " ")+" "+(emp.other_names or " ")
                    loan.disbursing_officerID = request.user.id
                    loan.disbursing_officer = fullname
                    loan.received_by = request.POST.get("received-by")

                    processing_fee = request.POST.get("processing-fee")

                    #working on disbursinf form
                    loan_disbursement_file=request.FILES.get("loan-disbursement-file-rc")
                    if request.FILES.get("loan-disbursement-file-rc"):
                        loan.loan_disbursement_file = loan_disbursement_file                   
                    loan.disburse_status = True
                    warning_message ="Loan disbursed!, please let the client pay all the added fees"
                    
                    #Other objects for saving into cashbook
                    station = StationStng.objects.get(id=request.session["current_stationID"])
                    item_category = ItemCategories.objects.get(item_category_name = "loan")

                  
                    #getting new borrower track book / record book
                    book_fee = 0
                    if (loan.loan_typeID.id == 1):
                        #Adding book fee to loan

                        borrowers_book_category = ItemCategories.objects.get(item_category_name ="borrowers_book")
                        no_of_books_ever_sold = CashBook.objects.filter(clientID = loan.clientID, \
                            item_catID = borrowers_book_category).count()

                        if ((  ( #new loan and new client whose book is not bypassed
                                (loan.allow_get_loan_without_processing_book == False) #book not bypassed
                                and (no_of_books_ever_sold==0 and loan.borrowers_book_fee == 0) #new client status
                                ) 
                            or ( #for an old client getting another loan, book lines over  and book not bypassed
                                (loan.allow_get_loan_without_processing_book == False) #book not bypassed
                                and (int(request.session['current_borrowers_book_record']) \
                                >= int(request.session['records_in_borrowers_book'])) #book lines over                            
                             ) )) :
                               
                               #pick book fee price                              
                               borrower_book = AutoItemAdds.objects.get(item_name = "borrowers_book", stationID = station)
                               #Adding to track auto add items
                               borrower_book = AutoItemAdds.objects.get(item_name = "borrowers_book",loan_typeID=loan.loan_typeID,
                                                  stationID = station)

                               #obtaining book fee
                               book_fee = borrower_book.unit_price
                               
                               book = Track_auto_item_adds()
                               #saving book details  
                               #we can follow from the cashbook since the cashbook is also saved into this record
                               book.loanID = loan
                               book.clientID = loan.clientID
                               book.item_name = borrower_book.item_name
                               book.stationID = loan.stationID
                               book.tracking_number = borrower_book.id #obtained from as Tracking_items_foreign key
                               book.userID = request.user
                               book.save()


                               #add notification that a book has been added
                               messages.info(request, "Record book has also been added")
                   
                    #Check if borrower has a borrowers book or prompt to buy
                    #or otherwise loan_type is not 1
                    #or client allowed to borrow without a book
                    #actual disbusing loan
                    #check if borrower's book is full or current loan given bypass or
                    if (loan.allow_get_loan_without_processing_book==True 
                            and loan.clientID.borrowers_book_record ==0): 
                            
                            request.session['dont_save_borrower_book_on_disburse'] = True
                            messages.warning(request, "Please enter number of rows for record book")
                            return redirect("main:edit-loan")
                    

                    loan.borrowers_book_fee = book_fee  
                    loan.processing_fee = processing_fee
                    loan.save()    
                    loan.clientID.current_total_balance+=loan.current_balance or 0
                    loan.clientID.save()
                    global_variables.set_current_client(request, loan.clientID)                
                       
                        #The code below runs pivots each time a loan is disbursed
                        #pivots for principle, processing fee and borrowers book are run
                        #========================================================================
                        #obtaining categories for piboting
                    loan_disbirse_category = ItemCategories.objects.get(item_category_name ="loan")
                    processing_fee_category = ItemCategories.objects.get(item_category_name ="processing_fee")
                    borrowers_book_category = ItemCategories.objects.get(item_category_name ="borrowers_book")


                    #saving processing fee
                    process_fee = ProcessingFee()
                    process_fee.add_processing_fee(request)


                    #saing loan to interset book
                    #This happens for only daily loan
                    interest_book = InterestBook()
                    interest_book.stationID = station
                    interest_book.clientID = loan.clientID
                    interest_book.loanID = loan    
                    interest_book.full_name = loan.full_name
                    interest_book.original_principle = loan.principle
                    interest_book.loan_disbursed = loan.principle
                    interest_book.processing_fee = processing_fee
                    if loan.loan_typeID.id==1:
                       interest_book.borrowers_book = loan.borrowers_book_fee
                    interest_book.userID = request.user
                    interest_book.save()

                    #saving into the cashbook
                    cashbook = CashBook()
                    cashbook.loanID = loan
                    cashbook.full_name = loan.full_name
                    cashbook.clientID = loan.clientID
                    if loan.loan_typeID.id==1:
                       #adding interest_book to only daily loan
                       cashbook.interest_bookID =interest_book
                    cashbook.inc_exp_status = False #false = expense, True=income


                    cashbook.inc_amount=(float(processing_fee) + loan.borrowers_book_fee)
                    cashbook.exp_amount = loan.principle #because loan is expense
                    cashbook.pay_identification = loan.pay_identification
                    cashbook.pay_medium = loan.pay_medium
                    cashbook.userID = request.user
                    #dealing with item cat
                    cashbook.item_catID = item_category
                    cashbook.item_name = item_category.user_friendly_name
                    #saving cashbook into station
                    cashbook.stationID = station
                    cashbook.balance = cashbook_balance.set_balance(request, station, 
                                        (float(processing_fee) + loan.borrowers_book_fee), loan.principle)
                    cashbook.cashbooktmainID = cashbook_main.get_current_main_cashbook(station)
                    cashbook.save() 
                    
                    #saving cloging balance
                    cashbook.cashbooktmainID.closing_balance += (float(processing_fee) 
                                                                 + loan.borrowers_book_fee 
                                                                 - loan.principle)
                    cashbook.cashbooktmainID.save()


                     #pivoting the loan disbursed at the very end
                    pivot_totals.set_totay_totals(request, station, loan_disbirse_category, 
                                                      False, 0, float(loan.principle))  
                        #pivoting the processing fee
                    pivot_totals.set_totay_totals(request, station, processing_fee_category, 
                                                      True, float(loan.processing_fee),0)
                        #pivoting the borrowers book
                    pivot_totals.set_totay_totals(request, station, borrowers_book_category, 
                                                      True, float(loan.borrowers_book_fee),0) 
 
                        #The finally we set current loan and client variables 
                        #==================================================================
                    global_variables.set_current_client(request, loan.clientID)
                    global_variables.set_current_loan(request, loan)
     
                else:    
                    loan.record_date = request.POST.get("record-date")
                    loan.save(update_fields=["record_date"])
                    warning_message ="Loan already disbursed"
            else:
                warning_message ="Loan not yet approved"
             
        



        
        if request.POST.get("actual-edit-loan") and loan is not None:
                if not request.session["current_loanID"]:
                   return redirect("main:index")
        
                principle=request.POST.get("principle")        
                current_principle = request.POST.get("current-principle")
                current_interest  = request.POST.get("current-interest")
                current_principle = request.POST.get("current-principle")
                total_loan_interest = request.POST.get("total-loan-interest")
                current_balance = request.POST.get("current-balance")
                pay_medium = request.POST.get("pay-medium")
                pay_identification = request.POST.get("pay-identification")
                loan_agreement_file =  request.FILES.get("loan-agreement-file")
                loan_disbursement_file =  request.FILES.get("loan-disbursement-file")
                
                pay_method_id =  request.POST.get("pay-method-id")
                stationID =  request.POST.get("stationID")
                loan_typeID = request.POST.get("loan-typeID")


                #setting dates and setting expctecd total pay baclk date
                if  not(loan.loan_duration == request.POST.get("loan-duration")):
                    loan_duration = int(request.POST.get("loan-duration"))
                    expected_clearance_date = datetime.today() + timedelta(days=loan_duration)
                    #saving into loan object
                    loan.loan_duration = loan_duration
                    loan.expected_clearance_date = expected_clearance_date

                #safely picking original interest
                if request.POST.get("interest-rate") \
                   and not(request.session["allow_to_add_custom_loan_interest"] =="Disabled") \
                   and not(loan.original_interest == request.POST.get("original-interest")):
                     #working on original interest
                     original_interest = (float(request.POST.get("interest-rate"))/100) * float(principle)
                     loan.original_interest = original_interest
                 
                #obtaining pay method id
                pay_method = Paymethod.objects.get(id=pay_method_id)
                loan.pay_medium = pay_medium


                #saving more fields into loan object
                loan.principle = float(principle)
                loan.current_principle = float(principle)
                loan.original_interest = float(original_interest)
                loan.current_interest = float(original_interest)
                loan.total_loan_interest = float(original_interest)
                loan.current_balance = float(principle) + original_interest
                loan.pay_methodID = pay_method
                
                loan.pay_identification = pay_identification


                if request.FILES.get("loan-agreement-file"):
                    loan.loan_agreement_file = loan_agreement_file
                if request.FILES.get("loan-disbursement-file"):
                    loan.loan_disbursement_file = loan_disbursement_file
                
                #pay_methodID = Paymethod.objects.get(id=pay_method_id)
                station = StationStng.objects.get(id=stationID)
                loan.stationID = station
                loan_type = LoanTypeStng.objects.get(id=loan_typeID)
                loan.loan_typeID = loan_type
                
                
                #actually saving loan info before approval takes place
                #and also change the daily pay values
                if request.POST.get("approve-status") =="No":
                   loan.save()
                   #and also change the daily pay values
                                        
                else:
                    if request.POST.get("record-date"):
                        if global_variables.user_rights(request.user, "allow_to_edit_loan_date")=="Yes":
                            loan.record_date = request.POST.get("record-date")
                            loan.save(update_fields=["record_date"])
                            request.session["loan_record_date"] = request.POST.get("record-date")
                            warning_message ="Record date Updated"                                                  
                    else:
                        warning_message ="Loan already approved, cannot be changed"
                                            
                    if request.POST.get("count-status") and not (request.POST.get("record-date")):
                        if global_variables.user_rights(request.user, "allow_to_stop_auto_loan_fines") == "Yes":   
                            
                            if request.POST.get("count-status") == "yes":
                                loan.stop_loan_counting = False
                                loan.save(update_fields=["stop_loan_counting"])
                                request.session["auto_fines"] = "Yes"
                            elif request.POST.get("count-status") == "no":
                                loan.stop_loan_counting = True
                                loan.save(update_fields=["stop_loan_counting"])
                                warning_message ="Monthly Automatic Fines Stopped"
                                request.session["auto_fines"] = "No"
                            else:
                                pass



        loanID = loan.id
        record_date = loan.record_date
        principle= loan.principle
        current_principle= loan.current_principle
        original_interest = loan.original_interest
        current_interest=loan.current_interest
        total_loan_interest  = loan.total_loan_interest
        current_balance = loan.current_balance 
        approved_by_name=loan.approved_by_name
        prepared_by_name = loan.prepared_by_name
        pay_medium = loan.pay_medium
        pay_identification = loan.pay_identification
        loan_duration = loan.loan_duration
        expected_clearance_date = loan.expected_clearance_date

        received_by = loan.received_by
        approve_status = loan.approve_status
        disburse_status = loan.disburse_status


        loan_agreement_file = loan.loan_agreement_file
        loan_disbursement_file = loan.loan_disbursement_file
            

        #other variables
        pay_method_id = loan.pay_methodID.id
        pay_method_name = loan.pay_methodID.pay_method_name

        stationID = loan.stationID.id 
        loan_station_name = loan.stationID.station_name
            
        loan_typeID = loan.loan_typeID
        loan_type_id = loan_typeID.id
        current_loan_type_name = loan_typeID.loan_type_name

        #setting loan approval and disbursement    
        prepared_by_name = loan.prepared_by_name
        approved_by_name = loan.approved_by_name
        disbursing_officer = loan.disbursing_officer
            
        approve_status_boolean ="No"
        if approve_status == True:
            loan_editable = "Disabled"  #disable submit button if loan is approved
            approve_status_boolean = "Yes"
        else:
            approve_status = "No"
            
        disburse_status_boolean = "No"
        if disburse_status ==True:
            disburse_status_boolean = "Yes"
        else:
            disburse_status = "No"
        #Getting record date
        record_date = loan.record_date
        #Interest Percent
        interest_percent = (float(original_interest)/float(principle))*100


    
        #getting processing fee value to be added to loan edit form
        processing_fee_count = AutoItemAdds.objects.filter(item_name = "processing_fee",
                     stationID = loan.stationID,
                     loan_typeID=loan.loan_typeID, lower_limit__lte=principle, 
                     upper_limit__gte=principle).count()
        
        if processing_fee_count > 1:
            messages.info(request, "Error!, 2 values of processing fee exist because the fee ranges are not set right. Please contact the system admin to help fix this problem")
            return redirect("main:index")


        processing = AutoItemAdds.objects.get(item_name = "processing_fee",stationID = loan.stationID,
                    loan_typeID=loan.loan_typeID, lower_limit__lte=principle, upper_limit__gte=principle)
        processing_fee = processing.unit_price

        if loan.allow_get_loan_without_processing_book ==True:
            borrower_book_yes="Yes"
        else:
            borrower_book_yes=None

        #Agreement file

        if True:
            agree_files = AgreementFile.objects.filter(loanID = loan)
        #except:
         #   pass
        


        return render(request, template_name="main/loan_view_edit_form.html", 
                     context={"loanID":loanID,"record_date":record_date,"principle":principle, "borrowersbook":loan.clientID.borrowers_book_record,
                        "current_principle":current_principle,"original_interest":original_interest,
                        "current_interest":current_interest, "total_loan_interest":total_loan_interest,
                        "current_balance":current_balance, "disbursing_officer":disbursing_officer,
                        "approved_by_name":approved_by_name , "prepared_by_name":prepared_by_name, 
                        "pay_medium":pay_medium, "pay_identification":pay_identification, 
                        "loan_duration":loan_duration, "expected_clearance_date":expected_clearance_date,
                        "received_by":received_by,"loan_editable":loan_editable,
                        "approve_status":approve_status,"disburse_status":disburse_status,
                        "approve_status_boolean":approve_status_boolean,"disburse_status_boolean":disburse_status_boolean,
                        "loan_disbursement_file":loan_disbursement_file,
                        "loan_agreement_file":loan_agreement_file, "pay_method_id":pay_method_id,"pay_method_name":pay_method_name,
                        "stationID":stationID,"loan_station_name":loan_station_name, "loan_type_id":loan_type_id, 
                        "current_loan_type_name":current_loan_type_name,"warning_message":warning_message,
                        "record_date":record_date,"interest_percent":interest_percent,"processing_fee":processing_fee,
                        "borrower_book_yes":borrower_book_yes, "agree_files": agree_files,
                        "get_global_db_objects":global_variables.get_global_db_objects(request)})
 

    

    @login_required(login_url="/")
    def set_list_of_current_loans(request, loan):
        """Here we get list of all current loans"""
        client = loan.clientID
        station = loan.stationID
        #the loans must be from that station
        if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
            list_of_loans = Loan.objects.filter(clientID = client)
        else:
           list_of_loans = Loan.objects.filter(clientID = client, stationID = station)
        
        total_debt = 0
        for loan_item in list_of_loans:
            if loan_item.disburse_status == True:
               total_debt += loan_item.current_balance

        client.current_total_balance = total_debt
        request.session["current_client_balance"] = total_debt
        client.save()

        return list_of_loans




    @login_required(login_url="/")
    def set_loan_by_click(request, id):
        """This sets the loan when one clicks"""

        if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
           loan = Loan.objects.get(id=id)
        else:
           station = StationStng.objects.get(id=request.session["current_stationID"])
           loan = Loan.objects.get(id=id, stationID = station)

        global_variables.set_current_loan(request, loan)
        return redirect("main:index")






    @login_required(login_url="/")
    def set_prev_loan(request):
        station = StationStng.objects.get(id= request.session["current_stationID"])
 
        try:
           if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
               client = Client.objects.get(id=request.session["current_clientID"])
               loan = Loan.objects.filter(id__lt= request.session["current_loanID"], \
                                            clientID = client).order_by("-id")[0]
           else:
               client = Client.objects.get(id=request.session["current_clientID"], stationID = station)
               loan = Loan.objects.filter(id__lt= request.session["current_loanID"], \
                                            stationID=station, clientID = client).order_by("-id")[0]
           try:
               global_variables.set_current_loan(request, loan)
           except:
               pass
           
        except:
             pass

        return redirect("main:index")
    


    @login_required(login_url="/")
    def set_next_loan(request):

        station = StationStng.objects.get(id=request.session["current_stationID"])
        try:
           if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
              client = Client.objects.get(id=request.session["current_clientID"])
              loan = Loan.objects.filter(id__gt= request.session["current_loanID"],  
                                           clientID = client).order_by("id")[0]
           else:
              client = Client.objects.get(id=request.session["current_clientID"], stationID = station)
              loan = Loan.objects.filter(id__gt= request.session["current_loanID"],  
                                       stationID=station, clientID = client).order_by("id")[0]
           try:
               global_variables.set_current_loan(request, loan)
           except:
               pass
        except:
            pass


        return redirect("main:index")
  


    
    #Daily points
    def pay_daily(request):
       pass




    def monthly_loan_payment(request):   
        
        if not (request.session["current_stationID"]):
            return redirect('main:index')

        if cashbook_main.check_for_cashbook(request) == False:
            return render (request, template_name="main/view_cashbook.html", 
                           context={"err_message":"Please first enter Opening balance"
            })

        loan = None
        try:
           loan = Loan.objects.get(id = request.session["current_loanID"])
        except:
           pass

        if request.POST.get("monthly-pay") and loan is not None:

            stationID = request.session["current_stationID"]
            station = StationStng.objects.get(id=stationID)
            
            #lets get the item payment categories now
            fines_category = ItemCategories.objects.get(item_category_name = "fines")
            loan_recovered_category = ItemCategories.objects.get(item_category_name = "loan_recovered")
            itenrest_paid_category = ItemCategories.objects.get(item_category_name = "interest_paid")

            amount_paid = float(request.POST.get("amount-paid"))
            pay_medium = request.POST.get("amount-paid")
            pay_identification = request.POST.get("pay-identification")
            pay_method_id = request.POST.get("pay-method-id")
            pay_methodID = Paymethod.objects.get(id=pay_method_id)
              
            #checking if amount entered is not very big
            if loan.current_balance - amount_paid <0:
                messages.warning(request, "Error! Amount paid cannot be greater than balance")
                return redirect("main:index")
            

             #saving to the client
            #===================================================
            client = loan.clientID

            if loan.disburse_status == False:
                        messages.warning(request, "Please disburse loan first")
                        return redirect("main:index")
            
            request.session["add_book"] = False
             #then we close the book just in case it has reached the maximum number of records                    
            if loan.clientID.borrowers_book_record >= int(request.session["records_in_borrowers_book"]) \
                and  (loan.loan_typeID.id==1):
                 request.session["add_book"] = True
                 return redirect("main:add-borrower-book")


            if loan.clientID.borrowers_book_record < int(request.session["records_in_borrowers_book"]) \
                and not (loan.loan_typeID.id==2):
                       #prevent getting more records than required records
                       loan.clientID.borrowers_book_record+=1 #adding a record to the borrower's book
                       
            else:
                pass
                    
            #lets pick previous balance before updating everything
            previous_loan_total_paid = loan.loan_total_paid
            previous_balance = loan.current_balance
       
            
            interest_book_i = InterestBook()
            interest_book_i.stationID = station
            interest_book_i.clientID = loan.clientID
            interest_book_i.loanID = loan    
            interest_book_i.full_name = loan.full_name
            interest_book_i.original_principle = loan.principle

            fines_paid = 0
            loan_recovered = 0
            interest_paid = 0


            if loan.loan_typeID.id==1:
                #work on daily loans
                #======================================================
                interest_book_i.loan_recovered = round(amount_paid*((float(request.session["daily_principle_pay_percent"]))/100))
                interest_book_i.interest_paid = round(amount_paid*((100-float(request.session["daily_principle_pay_percent"]))/100))

                if  (float(loan.total_fines)) >0: 

                    if float(loan.total_fines) - float(amount_paid) >=0:
                        fines_paid = float(amount_paid)
                        loan_recovered = 0
                        interest_paid = 0
                    else:
                        fines_paid = loan.total_fines
                        remainder = float(amount_paid) - float(loan.total_fines)
                        loan_recovered = (remainder*((float(request.session["daily_principle_pay_percent"]))/100))
                        interest_paid = (remainder*((100-float(request.session["daily_principle_pay_percent"]))/100))

                    interest_book_i.fines = fines_paid
                    interest_book_i.loan_recovered = loan_recovered
                    interest_book_i.interest_paid = interest_paid              
                else:
                    #we just pivot for loan recovered and interest paid
                    #lets pick categories now
                    #here since loan_balance - amount_paid >= 0, means all money goes tp loan recored and intest paid
                    #we are going to use the entire amount paid for this purpose
                    loan_recovered = (amount_paid*((float(request.session["daily_principle_pay_percent"]))/100))
                    interest_paid = (amount_paid*((100-float(request.session["daily_principle_pay_percent"]))/100))
                    interest_book_i.loan_recovered = loan_recovered
                    interest_book_i.interest_paid = interest_paid
                    
            if loan.loan_typeID.id == 2:
                #work on monthly loans
                if int(loan.current_balance) <= int(loan.principle):
                    loan.total_fines = 0
                    interest_book_i.loan_recovered = amount_paid
                    interest_book_i.interest_paid  = 0

                else:
                    if int(loan.current_balance) - int(amount_paid) >= int(loan.principle):
                        interest_book_i.loan_recovered = 0                 
                        interest_book_i.interest_paid = int(amount_paid)

                    else:
                        interest_book_i.interest_paid = int(loan.current_balance) - int(loan.principle)
                        interest_book_i.loan_recovered = int(amount_paid) - (int(loan.current_balance) 
                                                            -  int(loan.principle))

                        
            #finally save the interest book
            interest_book_i.userID = request.user

            #save interestbook for only daily loans
            interest_book_i.save()



            #saving into the cashbook
            item_category = ItemCategories.objects.get(item_category_name = "loan_payment")

            cashbook = CashBook()
            cashbook.interest_bookID = interest_book_i
            cashbook.loanID = loan
            cashbook.clientID = client
            cashbook.stationID = station
            cashbook.full_name = loan.full_name
            cashbook.pay_methodID = pay_methodID
            cashbook.pay_medium = pay_medium
            cashbook.pay_identification = pay_identification
            cashbook.inc_exp_status = True #Because loan payment is an income
            #picking loan payment category 
            cashbook.item_catID = item_category
            cashbook.item_name = item_category.user_friendly_name
            cashbook.quantity = 1
            cashbook.unit_price = amount_paid
            cashbook.inc_amount = amount_paid
            cashbook.balance = cashbook_balance.set_balance(request, station,
                                         amount_paid, 0) 
            cashbook.cashbooktmainID = cashbook_main.get_current_main_cashbook(station)         
            cashbook.userID = request.user
            cashbook.save()

            cashbook.cashbooktmainID.closing_balance += amount_paid
            cashbook.cashbooktmainID.save()



            #saving intp the loan
            loan.current_balance -= amount_paid
            loan.loan_total_paid += amount_paid
            loan.pay_medium = pay_methodID
            loan.pay_medium = pay_medium
            loan.pay_identification = pay_identification
            loan.userID = request.user
            loan.stationID = station   
            
            #setting loan fines balance
            if loan.loan_typeID.id==1:
               loan.total_fines -= fines_paid
            loan.save()
            loan.clientID.current_total_balance -=amount_paid
            loan.clientID.save()#reducing client balance 
            

            #Below we run pivots for loan recoverd, interest paid, and fines
            #=======================================================================
            if  fines_paid>0:   #amount_paid is the actual posted value

                pivot_totals.set_totay_totals(request, station, loan_recovered_category, 
                                                      True, loan_recovered, 0)
                pivot_totals.set_totay_totals(request, station, itenrest_paid_category, 
                                                      True, interest_paid, 0)             
                pivot_totals.set_totay_totals(request, station, fines_category, 
                                                      True, fines_paid, 0)
            else:
                
                pivot_totals.set_totay_totals(request, station, loan_recovered_category, 
                                                      True, loan_recovered, 0)
                pivot_totals.set_totay_totals(request, station, itenrest_paid_category, 
                                                      True, interest_paid, 0)
             
            
      


            #now updating session variables
            global_variables.set_current_client(request, client)
            global_variables.set_current_loan(request, loan)

            #sening success message
            messages.add_message(request, messages.INFO, "Payment successful")

            #then finally redirect back to index page with all values updated and refreshed
            return redirect("main:index")
        
        #return to index page if nothing was done
        return redirect("main:index")
    



    def delete_yesterday_undisbursed_loand(request):

        if not (request.session["current_stationID"]):
            return redirect('main:index')

        """
        This function is called on login to delete on loans that were not disbursed before close 
        of the day yesterday
        """

        today = datetime.today()
        year= today.year
        month = today.month
        day = today.day
        yesterday = str(year)+"-"+str(month)+"-"+str(str(day))

        undisbursed_loans = Loan.objects.filter(record_date__lte = yesterday, disburse_status=False)

        undisbursed_loans.delete()
        return undisbursed_loans
    



    def old_loan(request):
        try: 
            user_station = request.session["current_stationID"]
            user_station = None
        except: 
            return redirect('main:index')

        
        if request.POST.get("old-loan-edit"):             

            client = Client()
            try:
               client_name = (request.POST.get("full-names")).split(" ")
               client.surname = client_name[0]
               client.first_name = client_name[1]
            except:
               client.surname = (request.POST.get("full-names"))
               client.first_name ="NONE"

            client.contact_numbers = request.POST.get("contacts")
            client.current_total_balance = int(request.POST.get("current-balance"))
            client.stationID = StationStng.objects.get(id = int(request.session["current_stationID"]))
            client.save()

            loan = Loan()         
            loan.clientID = client              
            loan.full_name = client.full_name
            this_station = StationStng.objects.get(id = int(request.session["current_stationID"]))
            loan.stationID = this_station

            try:
               loan.loan_typeID = LoanTypeStng.objects.get(id = int(request.POST.get("loan-typeID")))
            except:
                messages.info(request, "Please choose correct loan type")
                return redirect("main:index")
            loan.record_date = request.POST.get("record-date")
            loan.principle = int(request.POST.get("principle"))


            if int(this_station.daily_percent)  > 0:
                loan.original_interest = (int(this_station.daily_percent)/100) * int(request.POST.get("principle"))
            else:
               loan.original_interest = (int(request.session["default_loan_interest_percent"])/100) * int(request.POST.get("principle"))
            
            loan.current_balance = int(request.POST.get("current-balance"))
            loan.total_fines = int(request.POST.get("total-fines"))
            loan.loan_total_paid =int(request.POST.get("total-paid"))
            loan.approve_status=True
            loan.disburse_status = True
            
            if request.POST.get("count-status") == "No":
               loan.stop_loan_counting = False

            if request.POST.get("count-status") == "Yes":
               loan.stop_loan_counting = True

            loan.save()  
            loan.record_date = request.POST.get("record-date")
            loan.save(update_fields=["record_date"])


            global_variables.set_current_loan(request, loan)
            global_variables.set_current_client(request, loan.clientID)
            return redirect("main:index")
  
        return render(request, template_name="main/loan_view_add_old_loan.html", 
                     context={"get_global_db_objects":global_variables.get_global_db_objects(request)})
    




    def delete_loan(request,id):
        
         if not (request.session["current_stationID"]):
            return redirect('main:index')

         del_loan = Loan.objects.get(id=id)
         client = del_loan.clientID


         try:
             item_category = ItemCategories.objects.get(item_category_name = "loan_payment")
             loan_list = CashBook.objects.filter(loanID = del_loan, item_catID = item_category)
             if len(loan_list) == 0:
                    del_loan.clientID.current_total_balance -= del_loan.current_balance
                    del_loan.clientID.save()
                    del_loan.delete()
             else:
                messages.info(request, "Error! Loan has payments, can't be deleted")
         except:
                loan_list = CashBook.objects.filter(loanID = del_loan)
                if del_loan.disburse_status==True:
                    del_loan.clientID.current_total_balance -= del_loan.current_balance
                    del_loan.clientID.save()

                del_loan.delete()
                messages.info(request, "Success, Loan Deleted")


         global_variables.set_current_loan(request, del_loan)
         global_variables.set_current_client(request, client)
         return redirect("main:index")



    def adjust_loan_balance(self, request):

        if not (request.session["current_stationID"]):
            return redirect('main:index')

        if global_variables.user_rights(request.user, "allow_to_adjust_loan_balance")=="Yes":
            pass
        else:
            return redirect('main:index')   
        
        loan = Loan.objects.get(id = int(request.POST.get('loan-id')))
        loan.current_balance  = int(request.POST.get('loan-balance'))
        loan.loan_total_paid = int(loan.principle) + int(loan.original_interest) + \
                                    int(loan.total_fines) - int(request.POST.get('loan-balance')) 
        
        loan_old_balance_str = request.POST.get('loan-current-balance').split('.')
        loan.clientID.current_total_balance += int(request.POST.get('loan-balance')) - \
                                                int(loan_old_balance_str[0])
        loan.clientID.save()          
        loan.save()

        

        global_variables.set_current_loan(request, loan)
        global_variables.set_current_client(request, loan.clientID)
        return redirect("main:index")




    def edit_total_fines(self, request): 

        try:
            x = request.session["current_stationID"]
            x = None
        except:
            return redirect('main:index')

        messages.info(request, "Success, value changed!")
        loan_edit = Loan.objects.get(id = int(request.POST.get("loan-id")))
        loan_edit.total_fines = int(request.POST.get("total-fines"))
        loan_edit.save()

        global_variables.set_current_loan(request, loan_edit)
        global_variables.set_current_client(request, loan_edit.clientID)

        


