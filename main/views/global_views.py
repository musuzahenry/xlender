from django.shortcuts import redirect
import base64
from django.core.files.base import ContentFile
from main.models import BusinessStng, Employee, ClientTypeStng, LoanTypeStng, StationStng, \
SystemCustomSettings,  Custom_user_rights, Client, Loan, Paymethod, VisitedLoans
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.dateparse import parse_date

class GlobalVariables():
   """
   This class sets our apps global variables and scope
   """

   def set_global_sessions(self,request):
      """
      Thie function gets values for:
      => business_name, business_logo, business_tagline
      => System user types
      => Logged in user StaionID, Staion Name, Loan Scheme for that Station
      => 
      """

      #Geting business basic info sunch that it is viewable before logging in
      business = BusinessStng.objects.get(id=1)

           
      
      #obtaining business info 
      request.session["business_name"] = business.business_name
      request.session["business_logo"] = str(business.logo)#images are not serializable so we changed this to a string
      request.session["business_tagline"] = business.tag_line



      #obtaining business info when person with cashier role logs in
      if request.user.is_authenticated:
         if request.POST.get("username") and request.POST.get("password"):
            client_typeID = SystemCustomSettings.objects.get(settings_name = "default_client_typeID")
            daily_interest_increment = SystemCustomSettings.objects.get(settings_name = "daily_interest_increment")
            allow_daily_partial_payments = SystemCustomSettings.objects.get(settings_name = "allow_daily_partial_payments")
            default_loan_interest_percent= SystemCustomSettings.objects.get(settings_name = "loan_interest_percent")
            default_loan_duration= SystemCustomSettings.objects.get(settings_name = "loan_duration")
            max_court_days = SystemCustomSettings.objects.get(settings_name = "max_court_days")
            daily_principle_pay_percent =SystemCustomSettings.objects.get(settings_name ="daily_principle_pay_percent")
            records_in_borrowers_book =SystemCustomSettings.objects.get(settings_name ="records_in_borrowers_book")

            #system custom settings 
            request.session["default_client_typeID"] = client_typeID.settings_value
            request.session["daily_interest_increment"] = daily_interest_increment.settings_value
            request.session["default_loan_duration"] = default_loan_duration.settings_value
            request.session["allow_daily_partial_payments"] = allow_daily_partial_payments.boolean_value
            request.session["default_loan_interest_percent"] = default_loan_interest_percent.settings_value
            request.session["max_court_days"] = max_court_days.boolean_value
            request.session["daily_principle_pay_percent"] = daily_principle_pay_percent.settings_value
            request.session["records_in_borrowers_book"] = records_in_borrowers_book.settings_value

            #getting current station for current user
            this_employee = Employee.objects.get(user_accountID = request.user)
            #station =  StationStng.objects.get(id=this_employee.stationID)
            station =  this_employee.stationID
            station_str =  str(station)
            request.session["current_station"] = station_str
            request.session["current_stationID"] = station.id
            request.session["current_loan_typeID"] = station.loan_typeID.id
            request.session["current_loan_type_name"] = station.loan_typeID.loan_type_name
                    
          


   #this entire function is passed as it is, it returns a dictionary
   def get_global_db_objects(self, request): 

      """This functio returns all the current user rights"""
      client_types = None
      loan_types = None
      stations = None    
      pay_methods = None  

      #Getting pay methods
      pay_methods = Paymethod.objects.all()

      #getting user rights from database 
      def get_user_right(user_right):
         try:
            current_user_rights=Custom_user_rights.objects.get(userID=request.user, user_right=user_right)
         except:
            current_user_rights = None 
         return current_user_rights
  
      if get_user_right("allow_user_to_choose_loan_type"):
         loan_types = LoanTypeStng.objects.all()
      else:
         loan_types = LoanTypeStng.objects.all()

      if not get_user_right("allow_user_to_choose_client_type") == None:
         client_types= ClientTypeStng.objects.all()
      else:
          client_types={}

      if not get_user_right("allow_choose_station")==None:
         stations =  StationStng.objects.all()
      else:
         stations = {}

      if not get_user_right("allow_to_add_custom_loan_interest")==None:
         allow_to_add_custom_loan_interest= request.session["allow_to_add_custom_loan_interest"] = None
      else:
         allow_to_add_custom_loan_interest= request.session["allow_to_add_custom_loan_interest"] = "Disabled"

      if not get_user_right("allow_to_change_loan_duration")==None:
         allow_to_change_loan_duration= request.session["allow_to_change_loan_duration"] = None
      else:
         allow_to_change_loan_duration = request.session["allow_to_change_loan_duration"] = "Disabled"
         
      if not get_user_right("allow_to_approve_loan")==None:
         request.session["allow_to_approve_loan"] = True
      else:
         request.session["allow_to_approve_loan"] = False




      global_objects={
         "client_types" : client_types, 
         "loan_types"   : loan_types,
         "stations"     : stations,
         "pay_methods"  : pay_methods,
         "allow_to_change_loan_duration": allow_to_change_loan_duration,
         "allow_to_add_custom_loan_interest": allow_to_add_custom_loan_interest,
      }
      return global_objects
   


   
   def set_client_typeID(self, request, client_typeID):

      request.session["client_typeID"] = client_typeID



   def set_current_client(self, request, client):

      """This function sets current client variables"""  
      client_fullname = client.full_name
      current_client_balance = client.current_total_balance
      #settting client globale variables
      request.session["current_clientID"] = client.id
      request.session["client_typeID"] = client.client_typeID.id
      request.session["current_borrowers_book_record"] =client.borrowers_book_record
      request.session["current_client_fullname"] = client_fullname
      request.session["current_client_balance"] = current_client_balance
 



   def set_current_loan(self, request, loan):

      if not (request.session["current_stationID"]):
            return redirect('main:index')
      if loan is not None:
         
         #record_visted load
         self.record_visited_loan(request, loan)

         #if loan is not none then set these variables        
         record_date = str(loan.record_date).split(" ")
         principle  = loan.principle 
         original_balance = loan.principle + loan.original_interest
         loan_total_paid  = loan.loan_total_paid
         current_balance=loan.current_balance
         loan_typeID= loan.loan_typeID.id
         total_fines = loan.total_fines

         if loan.stop_loan_counting == True:
            auto_fines = "No"
         else:
            auto_fines = "Yes"

          
         #Current loan status flags
         if loan.approve_status == True:
             approve_status = "Yes"
         else:
            approve_status = "No"

         if loan.disburse_status == True:
            disburse_status = "Yes"
         else:
            disburse_status = "No"
       
         request.session["principle"] = principle 
         request.session["approve_status"] = approve_status
         request.session["disburse_status"] = disburse_status 
         request.session["current_balance"] = current_balance
         request.session["loan_total_paid"] = loan_total_paid 
         request.session["total_fines"] = total_fines
         request.session["loan_type_name"] = loan.loan_typeID.loan_type_name
         request.session["current_loanID"] = loan.id
         request.session["loan_typeID"] = loan_typeID
         request.session["original_balance"] =  original_balance
         request.session["loan_record_date"] = record_date[0]
         request.session["auto_fines"] =  auto_fines

      else:
         loan=None
         list_of_current_loans =""
         request.session["principle"] =None
         request.session["current_balance"] = None
         request.session["current_loanID"] = None
         request.session["loan_typeID"] = None
         request.session["loan_record_date"] = None


   def record_visited_loan(self, request, loan):
           #recording a visited_loan
         try:
            today = today = timezone.now()
            loan_record_date = loan.record_date
            date_diff = today - loan_record_date

            station = StationStng.objects.get(id = int(request.session['current_stationID']))

            if date_diff.days >= 21:
               visited_loan = VisitedLoans()
               visited_loan.loanID = loan
               visited_loan.clientID = loan.clientID
               visited_loan.stationID = station
               visited_loan.full_name = loan.full_name
               visited_loan.loan_record_date = loan.record_date
               visited_loan.loan_current_debt_then = loan.current_balance
               visited_loan.userID = request.user
               visited_loan.save()
         except:
            pass
            





#Security Global variable
   def set_current_security(self, request, securityID):
        request.session["current_securityID"] = securityID

   


   
#Guarantor Global variable
   def set_current_guarantor(self, request, guarantorID):
        request.session["current_guarantorID"] = guarantorID



   #check current_user_right
   def user_rights(self, user, user_right):
      '''Takes the user and right in question'''
      check_right = None
      try:
         check_right = Custom_user_rights.objects.get(userID = user, user_right=user_right)
      except:
         check_right = None

      if check_right:
         return "Yes"
      else:
         return "No"
      


   def image_base64_to_jpg(self, base64_img):
      format, base64img = base64_img.split(';base64,') 
      ext = format.split('/')[-1]
      img_jpg = ContentFile(base64.b64decode(base64img ), name='temp.' + ext) # You can save this as file instance.
      return img_jpg







   

