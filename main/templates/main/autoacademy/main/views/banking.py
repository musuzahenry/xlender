
from main.models import CashBook, MoneySource
from django.shortcuts import render, redirect
from django.contrib import messages
from . global_views import GlobalViews
from datetime import datetime, timedelta




GLOBAL_VARIABLES = GlobalViews()
today = datetime.today()
year= today.year
month = today.month
day = today.day
today_date = datetime.strptime(str(year)+"-"+str(month)+"-"+str(day)+ " 00:00:00+03:00","%Y-%m-%d %H:%M:%S%z")
tomorrow_date = today_date + timedelta(days = 1)


class BankViews:
    

    def list_bank(request):

        if request.user.is_authenticated:
            pass
        else:
            return redirect("index")
        
        #get current employee
        current_employee= GLOBAL_VARIABLES.get_current_employee_info(request)
        bank_money_source = MoneySource.objects.get(settings_name = "bank")

        if request.POST.get("bank-amount"):
           bank_actions = BankActions()
           bank_actions.edit_cash_at_bank(request, current_employee, bank_money_source,
            request.POST.get("bank-amount"), request.POST.get("reason"))

        
        opening_balance = 0
        closing_balance = 0
        opening_balance_set = ""
        closing_balance_set = ""

        date1 = today_date
        date2 = tomorrow_date
        
        if not request.POST:
            date1 = today_date
            date2 = tomorrow_date
            orig_date1 = str(today_date).split(" ")[0]
            orig_date2 = str(today_date).split(" ")[0]
        elif request.POST.get("date1") and request.POST.get("date2"): 
            date1 = request.POST.get("date1")
            date2 = GLOBAL_VARIABLES.set_date2(request.POST.get("date2"))
            orig_date1 = str(request.POST.get("date1")).split(" ")[0]
            orig_date2 = str(request.POST.get("date2")).split(" ")[0]
        else:
            date1 = today_date
            date2 = tomorrow_date
            orig_date1 = str(today_date).split(" ")[0]
            orig_date2 = str(today_date).split(" ")[0]



        try:   
            opening_balance = CashBook.objects.filter(
                                                  businessID = current_employee.businessID,
                                                  campusID = current_employee.campusID,
                                                  money_sourceID = bank_money_source,
                                                  record_date__lt = date1,
                                                  ).order_by("-id")[0].running_total
        except:
           opening_balance_set = "Not set"




        try:
            closing_balance = CashBook.objects.filter(
                                                  businessID = current_employee.businessID,
                                                  campusID = current_employee.campusID,
                                                  money_sourceID = bank_money_source,
                                                  record_date__gte = date1,
                                                  record_date__lte = date2,
                                                  ).order_by("-id")[0].running_total
        except:
            closing_balance_set = "Not set"



        bank_list = CashBook.objects.filter(
                                                   businessID = current_employee.businessID,
                                                   campusID = current_employee.campusID,
                                                   money_sourceID = bank_money_source,
                                                   record_date__gte = date1,
                                                   record_date__lte = date2,
                                                    ).order_by("id")
        total_debit=0
        total_credit =0
        net = 0
        count = 0
        for item in bank_list:
            total_debit += item.income_received
            total_credit += item.expense_made
            net += (item.income_received - item.expense_made)
            
            count +=1
    
        return render(
                      request, 
                    template_name ="main/list_bank.html",
                    context={
                        "bank_list":bank_list,
                        "orig_date1":orig_date1,
                        "orig_date2":orig_date2,
                        "total_debit":total_debit,
                        "total_credit":total_credit,
                        "net":net,
                        "count":count,
                        "opening_balance":opening_balance,
                        "closing_balance":closing_balance,
                        "opening_balance_set":opening_balance_set,
                        "closing_balance_set":closing_balance_set,

                    })


class BankActions:
    def edit_cash_at_bank(self, request, current_employee, bank_money_source, amount, reason):
        
        edit_bank = CashBook()
        edit_bank.campusID = current_employee.campusID
        edit_bank.businessID = current_employee.businessID
        edit_bank.running_total = int(amount)
        edit_bank.money_sourceID = bank_money_source
        edit_bank.particulars = "Manually Fix Cash At Bank"
        edit_bank.item_name = reason
        edit_bank.userID = request.user
        edit_bank.user_fullname = str(current_employee.firstname)+" "+str(current_employee.firstname) +" "+str(current_employee.othername)
        edit_bank.save()
        messages.info(request, "Success record saved!")


        



