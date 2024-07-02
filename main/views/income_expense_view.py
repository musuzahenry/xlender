
from django.db.models import Q
from django.contrib import messages
from django.http import  HttpResponseRedirect
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from main.models import  StationStng,  ItemCategories, ItemType, CashBook, InterestBook, CourtQueue, Employee
from .global_views import *
from .pivot_totals_view import PivotTotals
from . cashbook_main import CashBookMainView
from . cashbook import CashBookView


#initializing objects
cashbook_main = CashBookMainView()
pivot_totals = PivotTotals()
cashbook_balance = CashBookView()
            

global_variables = GlobalVariables() #initiating a global variable object

class IncomeExpense():
    
    def manage_incomes_and_expenses(request):
        
        try: 
            user_station = request.session["current_stationID"]
            user_station = None
        except: 
            return redirect('main:index')

        #obtaining global db objects
        get_global_db_objects = global_variables.get_global_db_objects(request)
        

        if request.POST.get("inc-exp-add") or request.POST.get("court-inc-exp-add") or \
                                              request.POST.get("pay-salary-id"):
            if cashbook_main.check_for_cashbook(request) == False:
                return render (request, template_name="main/view_cashbook.html", 
                           context={"err_message":"Please first enter Opening balance"
            })
            
            item_typeID = int(request.POST.get("supper-typeID"))
            item_category_name = request.POST.get("cat-name")
            decsription = request.POST.get("decsription")
            amount = request.POST.get("amount")

            
            pay_methodID = int(request.POST.get("pay-method-id"))
            pay_method = Paymethod.objects.get(id=pay_methodID)
              
            pay_medium = request.POST.get("pay-medium")
            pay_identification = request.POST.get("pay-identification")


            item_type = ItemType.objects.get(id=item_typeID)
            item_category = ItemCategories.objects.get(item_category_name=item_category_name)

            station = StationStng.objects.get(id= int(request.session["current_stationID"]))


            itemx_name = item_category.user_friendly_name


            #saving into the cashbook
            cashbook = CashBook()
             #saving into the cashbook
            cashbook.pay_methodID = pay_method #pay method
            cashbook.pay_medium = pay_medium
            cashbook.pay_identification = pay_identification
            cashbook.stationID = station

            #saving court to cashbook 
            if request.POST.get("court-inc-exp-add") or request.POST.get("court-inc-add"):
                court_item = CourtQueue.objects.get(id= int(request.POST.get("court-id"))) 
                amount = request.POST.get("amount")              
                cashbook.courtID = court_item
                cashbook.full_name = request.POST.get("client-name") 
                cashbook.item_name = request.POST.get("decsription")
            elif request.POST.get("pay-salary-id"):
                paid_emp = Employee.objects.get(id=int(request.POST.get("pay-salary-id")))
                amount= int(request.POST.get("amount"))
                cashbook.employeeID = paid_emp
                cashbook.full_name = (str(paid_emp.surname) or "") + \
                " "+ (str(paid_emp.first_name) or "")
                cashbook.item_name = itemx_name 
            elif request.POST.get("pay-rent-id"):
                station_paid = StationStng.objects.get(id= int(request.POST.get("pay-rent-id")))
                amount= request.POST.get("amount")   
                cashbook.full_name = station_paid.station_name
                cashbook.item_name = itemx_name
                messages.info(request,"Payment Successful")  
                
            else:
                cashbook.full_name = decsription
                cashbook.item_name = itemx_name 
            cashbook.item_catID =  item_category



            interest_book_i = InterestBook()
            if item_category.item_category_name =="paying_existing_loan":
                interest_book_i.stationID = station 
                interest_book_i.full_name = decsription               
                interest_book_i.loan_recovered = round(float(amount)*((float(request.session["daily_principle_pay_percent"]))/100))
                interest_book_i.interest_paid = round(float(amount)*((100-float(request.session["daily_principle_pay_percent"]))/100))
                interest_book_i.userID = request.user
                itemx_name = "Loan Payment"
                interest_book_i.save()

                cashbook.interest_bookID = interest_book_i
                
            if item_category.item_category_name =="fines":
                interest_book_i.stationID = station 
                interest_book_i.full_name = decsription               
                interest_book_i.fines = amount
                interest_book_i.userID = request.user
                itemx_name = "Fines"
                interest_book_i.save()

                cashbook.interest_bookID = interest_book_i
            
            if item_category.item_category_name =="borrowers_book":
                interest_book_i.stationID = station 
                interest_book_i.full_name = decsription               
                interest_book_i.borrowers_book = amount
                interest_book_i.userID = request.user
                itemx_name = "Record Book"
                interest_book_i.save()


                #Adding cashbook to interset book
                cashbook.interest_bookID = interest_book_i


           
            if item_typeID == 1:
               cashbook.inc_exp_status =  True # since 1 is an income
               cashbook.inc_amount = amount
            else:
                cashbook.inc_exp_status =  False # since 2 is an expense
                cashbook.exp_amount = amount

            cashbook.balance = cashbook_balance.set_balance(request, station, cashbook.inc_amount,
                                        cashbook.exp_amount)
            cashbook_main_obj = cashbook_main.get_current_main_cashbook(station)
            cashbook.cashbooktmainID = cashbook_main_obj
            cashbook.userID = request.user

            cashbook.save()

            #saving cloging balance
            cashbook_main_obj.closing_balance += (float(cashbook.inc_amount)-
                                                         float(cashbook.exp_amount))
            cashbook_main_obj.save()



            #setting cashbook balance
            
            #setting pivots and totals
            if cashbook.inc_exp_status ==  True:
               pivot_totals.set_totay_totals(request, station, item_category, 
                                                      True, int(amount), 0)
            if cashbook.inc_exp_status == False:
               pivot_totals.set_totay_totals(request, station, item_category, 
                                                      False, 0, int(amount))
               
            if request.POST.get("court-inc-exp-add") or request.POST.get("court-inc-add"):
               return HttpResponseRedirect("/court-details/"+ str(court_item.id))
            elif request.POST.get("pay-salary-id"):
                messages.info(request,"Payment Successful")  
            else:
               return redirect("main:manage-incomes-and-expenses")


            
        #obtaining acceptable income list
        income_super_type= ItemType.objects.get(id=1)
        expense_super_type= ItemType.objects.get(id=2)

        income_type_list = ItemCategories.objects.filter(
            ~Q(item_category_name ="loan_recovered"),
            ~Q(item_category_name ="loan_payment"),
            ~Q(item_category_name ="processing_fee"),
            ~Q(item_category_name ="monthly_loan_payment"),
            ~Q(item_category_name ="daily_interest_payment"),
            ~Q(item_category_name ="interest_paid"),
            ~Q(item_category_name ="court_payment"),
            ~Q(item_category_name ="paying_existing_loan"),
            ~Q(item_category_name ="borrowers_book"),
            ~Q(item_category_name ="fines"),
            item_typeID = income_super_type,
        )

        #obtaining expense list
        expense_type_list = ItemCategories.objects.filter(
            ~Q(item_category_name ="loan"),
            ~Q(item_category_name ="court_expense_to_client"),
            item_typeID  = expense_super_type,
        )


        #return list of incomes and expenses entered today for that station
        cashbook_today = None
        try:
           station = StationStng.objects.get(id= request.session["current_stationID"])
           cashbook_today = CashBook.objects.filter(record_date__gte=datetime.today().date(),
                                                    record_date__lte=datetime.today().date()+timedelta(1),
                                                    stationID = station, deleled=False).order_by("-id")
        except:
            pass

        total_income = 0
        total_expense = 0
        net = 0
        for item in cashbook_today:
            if item.inc_exp_status ==True:
                total_income+=item.inc_amount
            if item.inc_exp_status == False:
                total_expense+=item.exp_amount

        

        if  total_income >= total_expense:
            net = total_income - total_expense
        else:
            net = "("+str((total_expense - total_income))+")"

        

        return  render(request, template_name= "main/income_expense_view.html",
                       context={"income_type_list":income_type_list, 
                                "expense_type_list":expense_type_list,
                                "get_global_db_objects":get_global_db_objects,
                                "cashbook_today":cashbook_today,
                                "total_income":total_income, "total_expense":total_expense,
                                "net":net,})


    