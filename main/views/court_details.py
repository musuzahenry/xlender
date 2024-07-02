from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import  HttpResponseRedirect
from . global_views import *
from . income_expense_view import *
from main.models import  CourtQueue, CashBook, ItemCategories, OtherPayments
from datetime import datetime, timedelta


#loading global objects abd variables
global_variables = GlobalVariables() #initiating a global variable object
#instantiating expense and income class 
new_inc_exp = IncomeExpense()

class CourtDetails():
   def set_court_details(request, id):

        try: 
            user_station = request.session["current_stationID"]
            user_station = None
        except: 
            return redirect('main:index')   
               
        #the sourcecode bloww helps in adding incomes and expenses due to the court and this client
        #we use the inc_exp_module
        if request.POST.get("add-court-inc-exp"):
            courtID = CourtQueue.objects.get(id=request.POST.get("court-id"))
            station = StationStng.objects.get(id=int(request.session["current_stationID"]))
            make_payment = OtherPayments()
            make_payment.stationID = station
            make_payment.courtID = courtID
            make_payment.fullname = request.POST.get("client-name")
            make_payment.description = request.POST.get("description")
            pay_methodID=request.POST.get("pay-methodID")
            pay_method = Paymethod.objects.get(id= int(pay_methodID))
            make_payment.pay_methodID = pay_method
            make_payment.pay_medium =  request.POST.get("pay-medium")
            make_payment.pay_identification = request.POST.get("pay-identification")
            if request.POST.get("court-inc"):
               make_payment.debit = request.POST.get("amount")
               make_payment.credit= 0
            elif request.POST.get("court-exp"):
               make_payment.debit = 0
               make_payment.credit= request.POST.get("amount")
            else:
               pass
            make_payment.userID = request.user
            make_payment.save()

        #setting expenses
        exp_name = "court_expense_to_client"
        inc_name = "court_payment"
        item_category_exp_cat = ItemCategories.objects.get(item_category_name=exp_name)
        item_category_exp = item_category_exp_cat.item_category_name
        item_category_inc_cat = ItemCategories.objects.get(item_category_name=inc_name)
        item_category_inc = item_category_inc_cat.item_category_name
        
        #Loading global objects
        get_global_db_objects = global_variables.get_global_db_objects(request)

        court_id = id
        court_payments = None



        court_item = CourtQueue.objects.get(id=court_id)
        
        
        try:
           court_payments = OtherPayments.objects.filter(courtID= court_item)
        except:
           pass
        
        #lets set court details
        try:
           loan = court_item.loanID
           client = court_item.loanID.clientID
           court_item.gender = client.gender
           court_item.address = client.physical_address
           court_item.contacts = client.contact_numbers
           court_item.national_identification_number = client.national_identification_number
           court_item.dob = client.date_of_birth
           court_item.save()

           global_variables.set_client_typeID(request, int(str(client.client_typeID.id)))
           global_variables.set_current_client(request,client)
           global_variables.set_current_loan(request,loan)
        except:
           pass

        
        if request.POST.get("edit-court-queue"):
           court_item.full_name =  request.POST.get("fullname")
           court_item.gender =  request.POST.get("gender")
           court_item.age =  request.POST.get("age")
           court_item.demand_notice = request.POST.get("demand-notice")
           court_item.contacts =  request.POST.get("contacts")
           court_item.address =  request.POST.get("address")
           court_item.national_identification_number =  request.POST.get("nin")
           court_item.loan_record_date =  request.POST.get("loan-record-date")
           court_item.loan_principle =  request.POST.get("principle")
           court_item.loan_debt =  request.POST.get("loan-debt")
           court_item.notes =  request.POST.get("details")
           court_item.userID = request.user
           court_item.save()


        if isinstance(court_item.loan_record_date, str):
           loan_record_datex=court_item.loan_record_date
        else:
           loan_record_datex = str(court_item.loan_record_date.year) +"-"+ \
           str(court_item.loan_record_date.month) +"-"+ str(court_item.loan_record_date.day)

        total_spent =0
        total_paid = 0
        client_diff = 0
        for cashitem in court_payments:
            total_spent += cashitem.credit
            total_paid += cashitem.debit

        client_diff = total_spent - total_paid




        return render(request, template_name="main/court_details.html", 
                            context={"court_item": court_item,
                                     "court_id":court_id,
                                     "loan_record_date":loan_record_datex,
                                     "court_payments":court_payments,
                                     "item_category_exp":item_category_exp,
                                     "item_category_inc":item_category_inc,
                                     "get_global_db_objects":get_global_db_objects,
                                     "total_spent":total_spent, 
                                     "total_paid":total_paid,
                                     "client_diff":client_diff,
                                     "title":"Court Details",})
      

    
    
        

