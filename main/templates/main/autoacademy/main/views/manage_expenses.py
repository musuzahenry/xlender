from main.models import CashBook, Item, ItemCategory, CashBook, PaymentMethod, MoneySource
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



class ManageExpense:

    def expenses(request):

        if request.user.is_authenticated:
                pass
        else: 
                return redirect("index")

        date1 = today_date
        date2 = tomorrow_date
        #get all expenses
        ALL_PAYMENT_METHODS = PaymentMethod.objects.all()
        ALL_MONEY_SOURCES = MoneySource.objects.all()
        current_employee = GLOBAL_VARIABLES.get_current_employee_info(request)

        
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



        expense_list = CashBook.objects.filter(
                                                   businessID = current_employee.businessID,
                                                   campusID = current_employee.campusID,
                                                   record_date__gte = date1,
                                                   record_date__lte = date2,
                                                   is_income=False,
                                                    ).order_by("id")



        expense_categoryID = ItemCategory.objects.get(
                                                      settings_name = "expense",
                                                      businessID = current_employee.businessID,
                                                      campusID = current_employee.campusID,
                                                      )
        item_expense_list = Item.objects.filter(
                                                item_categoryID = expense_categoryID,
                                                businessID = current_employee.businessID,
                                                campusID = current_employee.campusID,
                                                is_requirement = False,
                                                )
        expenses = Item.objects.all()

        if  request.POST.get("itemID"):
            expense_action = ExpenseActions()
            description = request.POST.get("description")
            expense_action.add_expense(request, current_employee, request.POST.get("itemID"), description )

            messages.info(request, "Success, record saved")
            return redirect("expenses")

        total = 0
        for item in expense_list:
            total += float(item.expense_made)
        
        return render(
                     request,
                     template_name="main/expenses.html",
                     context ={
                        "item_expense_list":item_expense_list,
                        "expense_list":expense_list,  
                        "total":total, 
                        "ALL_MONEY_SOURCES":ALL_MONEY_SOURCES,                  }
                     )


class ExpenseActions:

    def add_expense(self, request, current_employee, id, description):

            if request.user.is_authenticated:
                pass
            else: 
                return redirect("index")

            cash = CashBook()
            cash.businessID = current_employee.businessID
            cash.campusID = current_employee.campusID
            
            money_sourceID = MoneySource.objects.get(settings_name = request.POST.get("money-sourceID"))

            itemID = Item.objects.get(id = int(id))
         
            cash.itemID = itemID
            cash.particulars = itemID.item_categoryID.category_name
            cash.is_income = False
            cash.money_sourceID = money_sourceID
            cash.payID_NO = str(request.POST.get("pay-number"))

            cash.item_name = itemID.item_name +" :" + description

            cash.expense_made = request.POST.get("amount")

            cash.userID = request.user
            cash.user_fullname = current_employee.surname +" "+current_employee.firstname +" "+ current_employee.othername

            cash.save()
            GLOBAL_VARIABLES.running_total(request)






                     