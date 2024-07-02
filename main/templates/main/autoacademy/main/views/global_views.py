from django.shortcuts import redirect
from  main . models import Employee, SystemRoles, Rights, CashBook, YearClass, YearClassTerm, MoneySource, StudentRequirementsPerTerm
from datetime import datetime, timedelta
from django.contrib import messages


class GlobalViews:


    def set_date2(self, second_date):
        date2_str = datetime.strptime(second_date, '%Y-%m-%d')+ timedelta(days=1)
        date2_obj = str(date2_str).split("-")
        date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2]
        return date2 

    def get_current_employee_info(self, request):
        current_employee = Employee.objects.get(userID = request.user)
        return current_employee

    def redirect_not_logged_in_user(self, request):
        if not(request.user.is_authenticated):
            return redirect("user-login")

    def set_current_student(self, request, student):
        this_std_terms = YearClassTerm.objects.filter(studentID = student)

        #set max year_class and year_class_term for this student
        last_current_year_class = YearClass.objects.filter(studentID = student).order_by("-id")[0]
        self.set_current_year_class(request, last_current_year_class)
        last_current_year_class_term = YearClassTerm.objects.filter(year_classID = last_current_year_class).order_by("-id")[0]
        self.set_current_year_class_term(request, last_current_year_class_term)

        

        #now reset this students current balance
        #===========================================================
        balance = 0
        for term in this_std_terms:

            term_balance = 0
            term_original_fees = 0
            term_amount_paid = 0

            rqt_list = StudentRequirementsPerTerm.objects.filter(yearclass_termID = term)
            term.balance = 0
            for rqt in rqt_list:
                if rqt.is_school_fees == True:
                    term.balance += rqt.balance  
                    orig_amount = rqt.amount_required
            
            balance += term.balance
            term.original_fees = orig_amount
            #messages.info(request, str(orig_amount))
            term.save()  

        student.balance = balance
        student.save()
       
       
        term.amount_paid = orig_amount - term.balance
        term.save()

        request.session["current_student_id"] = student.id



    
    def set_current_year_class(self, request, year_class):
        request.session["current_year_classID"] = year_class.id
        last_class_year_term = YearClassTerm.objects.filter(year_classID = year_class).order_by("-id")[0]
        self.set_current_year_class_term(request, last_class_year_term)
        

    def set_current_year_class_term(self, request, year_class_term):
        request.session["current_year_class_termID"] = year_class_term.id

    
    def check_current_user_roles(self, request, right_name):

        right = Rights.objects.get(settings_name = right_name)
        current_employee = Employee.objects.get(userID = request.user)

        allow_to_pass = False

        
        try:
            check_right = SystemRoles.objects.get(rightID = right, roleID=current_employee.roleID)
            allow_to_pass = True
        except:
            messages.info(request, "Sorry, you have no right to perform this action")


        if current_employee.roleID.settings_name == "administrator":
            #allows administrator to access every place
             allow_to_pass = True

        return allow_to_pass



    def running_total(self, request):

        current_employee = Employee.objects.get(userID = request.user)
        cash_money_source = MoneySource.objects.get(settings_name="cash")
        bank_money_source = MoneySource.objects.get(settings_name="bank")


        
        last_cashbook = CashBook.objects.filter(#last cashbook entry
                                                campusID = current_employee.campusID,
                                                businessID = current_employee.businessID,
                                                ).order_by("-id")[0]




        if last_cashbook.money_sourceID.settings_name == "bank": 
            
            prev_cashbook = CashBook.objects.filter(#second las cashbook entry with money_source = bank
                                                campusID = current_employee.campusID,
                                                businessID = current_employee.businessID,
                                                money_sourceID = bank_money_source
                                                ).order_by("-id")[1]
        else:
            prev_cashbook = CashBook.objects.filter(#second las cashbook entry with money source = cash
                                                campusID = current_employee.campusID,
                                                businessID = current_employee.businessID,
                                                money_sourceID = cash_money_source
                                                ).order_by("-id")[1]

        
        if prev_cashbook == None:
           last_cashbook.running_total = 0 + \
                                      last_cashbook.income_received - last_cashbook.expense_made
        else:
           last_cashbook.running_total = prev_cashbook.running_total + \
                                      last_cashbook.income_received - last_cashbook.expense_made
        last_cashbook.save()