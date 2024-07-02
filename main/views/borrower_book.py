from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .global_views import *
from main.models import Loan, Track_auto_item_adds,  AutoItemAdds, StationStng,  \
            ItemCategories, InterestBook, CashBook
from .pivot_totals_view import PivotTotals
from . cashbook import CashBookView
from . cashbook_main import CashBookMainView

#initializing records
#initialixing the global object

global_variables = GlobalVariables()
globla_variables = GlobalVariables()
pivot_totals = PivotTotals()
cashbook_main = CashBookMainView()
cashbook_balance = CashBookView()



class BorrowerBook():
    
    @login_required(login_url="/")
    def add_borrower_book(request):
        
        station = StationStng.objects.get(id = request.session["current_stationID"])
        loan = Loan.objects.get(id=request.session["current_loanID"])
        get_global_db_objects = globla_variables.get_global_db_objects(request)
        borrower_book = AutoItemAdds.objects.get(item_name = "borrowers_book",loan_typeID=loan.loan_typeID,
                                                  stationID = station)
        tracking_number = borrower_book.id
        book_fee = borrower_book.unit_price
        item_name =borrower_book.item_name
        item_catID = borrower_book.item_catID
        info_message = ""

        
        #checking whether we have any existent book
        add_book = True

        
        if request.POST.get("add-borrower-book") and add_book == True:

            book = Track_auto_item_adds()
            #saving book details  
            #the book is saved into tracking items since it has to be tracked
            #we can follow from the cashbook since the cashbook is also saved into this record
            book.loanID = loan
            book.clientID = loan.clientID
            book.item_name = item_name
            book.stationID = loan.stationID
            book.tracking_number = tracking_number #obtained from as Tracking_items_foreign key
            book.userID = request.user
            book.save()


            #saving borrowers book to loan
            loan.borrowers_book_fee = book_fee
            loan.save()

            #Finally resetting borrower record counter in the clients record
            loan.clientID.borrowers_book_record =0
            loan.clientID.save()


            globla_variables.set_current_client(request, loan.clientID)
            globla_variables.set_current_loan(request, loan)

            info_message = "Book added"

            #check if borrowers book has been added cashbook or interest book
                                    #pivoting the borrowers book
            
            if True:
                try :
                    x=request.session["add_book"] 
                    #this means the book hasnt been posted to pivotals yet
                    borrowers_book_category = ItemCategories.objects.get(item_category_name ="borrowers_book")
                                     
                    interest_book_i = InterestBook()
                    interest_book_i.stationID = station
                    interest_book_i.clientID = loan.clientID
                    interest_book_i.loanID = loan    
                    interest_book_i.full_name = loan.full_name
                    interest_book_i.original_principle = loan.principle
                    interest_book_i.borrowers_book = book_fee
                    interest_book_i.userID = request.user
                    interest_book_i.save()

                    cashbook = CashBook()
                    cashbook.interest_bookID = interest_book_i
                    cashbook.loanID = loan
                    cashbook.clientID = loan.clientID
                    cashbook.stationID = station
                    cashbook.full_name = loan.full_name
                    
                    try:
                       cashbook.pay_methodID = Paymethod.objects.get(id=int(request.POST.get("pay-methodID")))
                    except:
                        pass
                
                    cashbook.pay_medium = request.POST.get("pay-medium")
                    cashbook.pay_identification = request.POST.get("pay-identification")
                    cashbook.inc_exp_status = True #Because loan payment is an income
                    #picking loan payment category 
                    cashbook.item_catID = borrowers_book_category
                    cashbook.item_name = borrowers_book_category.user_friendly_name
                    cashbook.quantity = 1
                    cashbook.unit_price = book_fee
                    cashbook.inc_amount = book_fee
                    cashbook.balance = cashbook_balance.set_balance(request, station,
                                                book_fee, 0) 
                    cashbook.cashbooktmainID = cashbook_main.get_current_main_cashbook(station)         
                    cashbook.userID = request.user
                    cashbook.save()

                    cashbook.cashbooktmainID.closing_balance += book_fee
                    cashbook.cashbooktmainID.save()

                    #pivoting after adding book
                    pivot_totals.set_totay_totals(request, station, borrowers_book_category, 
                                                            True, float(loan.borrowers_book_fee),0) 
                except:
                   pass

            #redirect to prevent multiple entries
            return redirect("main:index")

                       


        return render(request, template_name="main/borrower_book_add.html",
                      context={"get_global_db_objects":get_global_db_objects,  
                      "book_fee":book_fee, "info_message":info_message,})
    


    def manually_add_book(request):
        

        try:
            station = StationStng.objects.get(id=int(request.session["current_stationID"]))
        except:
            return redirect("main:index")
        
        try:
            loan = Loan.objects.get(id=request.session["current_loanID"])
        except:
            return redirect("main:index")  
        
        station = loan.stationID
        borrower_book = AutoItemAdds.objects.get(item_name = "borrowers_book", stationID = station)
        book_fee = borrower_book.unit_price


        if request.POST.get("add-book-manual"):
                                                                                                                     
            borrowers_book_category = ItemCategories.objects.get(item_category_name ="borrowers_book")          

            #saving book into loan
            loan.borrowers_book_fee = 0
            loan.save()

            #Finally resetting borrower record counter in the clients record
            loan.clientID.borrowers_book_record =0
            loan.clientID.save()


            globla_variables.set_current_client(request, loan.clientID)
            globla_variables.set_current_loan(request, loan)
            

            interest_book_i = InterestBook()
            interest_book_i.stationID = station
            interest_book_i.clientID = loan.clientID
            interest_book_i.loanID = loan    
            interest_book_i.full_name = loan.full_name
            interest_book_i.original_principle = loan.principle
            interest_book_i.borrowers_book = book_fee
            interest_book_i.userID = request.user
            interest_book_i.save()


            #saving into the cashbook
            cashbook = CashBook()
            cashbook.interest_bookID = interest_book_i
            cashbook.loanID = loan
            cashbook.clientID = loan.clientID
            cashbook.stationID = station
            cashbook.full_name = loan.full_name      
            cashbook.pay_medium = request.POST.get("pay-medium")
            cashbook.pay_identification = request.POST.get("pay-identification")
            cashbook.inc_exp_status = True #Because loan payment is an income
            #picking loan payment category 
            try:
                cashbook.pay_methodID = Paymethod.objects.get(id=int(request.POST.get("pay-methodID")))
            except:
                pass
            cashbook.item_catID = borrowers_book_category
            cashbook.item_name = borrowers_book_category.user_friendly_name
            cashbook.quantity = 1
            cashbook.unit_price = book_fee
            cashbook.inc_amount = book_fee
            cashbook.balance = cashbook_balance.set_balance(request, station,
                                                    book_fee, 0) 
            cashbook.cashbooktmainID = cashbook_main.get_current_main_cashbook(station)         
            cashbook.userID = request.user
            cashbook.save()

            cashbook.cashbooktmainID.closing_balance += book_fee
            cashbook.cashbooktmainID.save()


            #Adding AutoItem adds
            try:
                track_book = Track_auto_item_adds.objects.get(clientID = loan.clientID,
                                                            item_name="borrowers_book")
            except:
                track_book = Track_auto_item_adds()
                track_book.clientID = loan.clientID
                track_book.cashbookID = cashbook
                track_book.loanID = loan
                track_book.item_name="borrowers_book"
                track_book.closed = False
                track_book.stationID = station
                track_book.save()

            #pivoting after adding book       
            pivot_totals.set_totay_totals(request, station, borrowers_book_category, 
                                                                True, float(book_fee),0) 
            
            messages.warning(request, "Book Added, please let client clear book")
            return redirect("main:index")
        
        return render(request, template_name="main/borrower_book_add_manually.html", 
                            context={"book_fee": book_fee,
                            "get_global_db_objects": global_variables.get_global_db_objects(request)})



    

        
    




        
        



            


    

    