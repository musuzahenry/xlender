from django.shortcuts import render
from django.contrib import messages
from main.models import  StationStng, Employee, CashBook
from datetime import datetime, timedelta
from django.utils import timezone
from .global_views import *
from . pivot_totals_view import PivotTotals
from . income_expense_view   import IncomeExpense

#initialixing the global object
global_variables = GlobalVariables()
#initializing pivots and totals
pivot_totals = PivotTotals()

class EmployeeView():

    def paid_salaries(request):
        
        try: 
            user_station = request.session["current_stationID"]
            user_station = None
        except: 
            return redirect('main:index')

        paid_set = None
  
        if not request.POST:
            paid_set = None
            today = datetime.today()
            year= today.year
            month = today.month
            day = today.day
            date1 = str(year)+"-"+str(month)+"-"+str(day)
            date2_str = today + timedelta(days=1)
            date2_obj = str(date2_str).split("-")
            date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2]
            if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes" \
            and global_variables.user_rights(request.user, "allow_to_view_salary_payments") == "Yes":
                    paid_set = CashBook.objects.filter(
                                                           record_date__gte=date1,
                                                           record_date__lte=date2,
                                                           employeeID__isnull=False,
                                                           )                       
            elif global_variables.user_rights(request.user, "allow_to_view_salary_payments") == "Yes":
                    station = StationStng.objects.get(id= int(request.session["current_stationID"]))
                    paid_set = CashBook.objects.filter(stationID=station,
                                                           record_date__gte=date1,
                                                           record_date__lte=date2,
                                                          employeeID__isnull=False,
                                                           )
            else:
                station = StationStng.objects.get(id= int(request.session["current_stationID"]))
                this_employee = Employee.objects.get(user_accountID = request.user)
                paid_set = CashBook.objects.filter(stationID=station,
                                                   record_date__gte=date1,
                                                   record_date__lte=date2,
                                                   employeeID=this_employee,
                                                    )
                 
                                                           
                    
                    

        if request.POST.get("date1") and request.POST.get("date2"):
                date1  = request.POST.get("date1")
                date2_str = datetime.strptime(request.POST.get("date2"), '%Y-%m-%d')+ timedelta(days=1)
                date2_obj = str(date2_str).split("-")
                date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2]
                
                if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                    if not (request.POST.get("station-id") ==0 or request.POST.get("station-id")=="0"):

                        station = StationStng.objects.get(id= int(request.POST.get("station-id")))
                        paid_set = CashBook.objects.filter(
                                                           stationID=station,
                                                           record_date__gte=date1,
                                                           record_date__lte=date2,
                                                           employeeID__isnull=False,
                                                           )                        
                    else:   
                        paid_set = CashBook.objects.filter(                                                          
                                                           record_date__gte=date1,
                                                           record_date__lte=date2,
                                                           employeeID__isnull=False,
                                                           )
                else:
                        station = StationStng.objects.get(id= int(request.session["current_stationID"]))
                        paid_set = CashBook.objects.filter(
                                                           stationID=station,
                                                           record_date__gte=date1,
                                                           record_date__lte=date2,
                                                           employeeID__isnull=False,
                                                           )
              
        return render(request, template_name="main/paid_salaries.html",context={"paid_set":paid_set, 
                    "get_global_db_objects":global_variables.get_global_db_objects(request),
                    "title":"Salary Payments",})




    def  view_employees(request):

        try: 
            user_station = request.session["current_stationID"]
            user_station = None
        except: 
            return redirect('main:index')

        #retriving employee lists
        try:
            station = StationStng.objects.get(id= int(request.session["current_stationID"]))
        except:
            return redirect("main:index")
          
        if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":

            if request.POST.get("station-id"):
                station = StationStng.objects.get(id= int(request.POST.get("station-id")))
                employees = Employee.objects.filter(stationID = station, is_active=True,)
            else:
               employees = Employee.objects.filter(is_active=True,)
        else:
            employees = Employee.objects.filter(stationID = station, is_active=True,)

        #making payments

        if request.POST.get("pay-salary-id"):
            #the sourcecode bloww helps pay salaries
            #we use the inc_exp_module
            if True:
               IncomeExpense.manage_incomes_and_expenses(request)

        #deactivating and employee
        if request.POST.get("emp-del-id"):
             if global_variables.user_rights(request.user, "allow_to_delete_employees")=="Yes":
                deleted_emp = Employee.objects.get(id=int(request.POST.get("emp-del-id")))
                deleted_emp.is_active = False
                deleted_emp.user_accountID.is_active = False
                deleted_emp.save()
                deleted_emp.user_accountID.save()
                messages.info(request, "Success, employee deleted")

                return redirect("main:view-employees")


        return render(request, template_name="main/employee_list.html",context={"employees":employees, 
                    "get_global_db_objects":global_variables.get_global_db_objects(request),
                    "title":"Employee List",})
    



    def view_deleted_employees(request):
    
        try: 
            user_station = request.session["current_stationID"]
            user_station = None
        except: 
            return redirect('main:index')

        employees= None

        if request.POST.get("restore-emp-del-id"):
            if global_variables.user_rights(request.user, "allow_to_restore_deleted_employees")=="Yes":
                restored_emp = Employee.objects.get(id=int(request.POST.get("restore-emp-del-id")))
                restored_emp.user_accountID.is_active = True
                restored_emp.user_accountID.save()
                restored_emp.is_active=True
                restored_emp.save()

            messages.info(request, "Success, employee restored")
            return redirect("main:view-deleted-employees")
         
        if global_variables.user_rights(request.user, "allow_to_restore_deleted_employees")=="Yes":
            if request.POST.get("station-id"):
                station = StationStng.objects.get(id=int(request.POST.get("station-id")))
                employees = Employee.objects.filter(is_active=False, stationID = station).order_by("-id")
            else:
                employees = Employee.objects.filter(is_active=False,).order_by("-id")
        else:
             employees= None        

             
        return render(request, template_name="main/employee_deleted_list.html",context={"employees":employees, 
                    "get_global_db_objects":global_variables.get_global_db_objects(request),
                    "title":"Deleted Employees",})
         
    

    



   