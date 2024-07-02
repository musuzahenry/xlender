from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.utils import timezone
from ckeditor.fields import RichTextField
from image_optimizer.fields import OptimizedImageField



# Create your models here.

#listing user right settings


RIGHTS = (("allow_user_to_choose_loan_type",'Allow To Choose Loan Type'), 
          ("allow_user_to_choose_client_type", "Allow To Choose Client Type"),
          ("allow_choose_station",'Allow To Choose Station'),
          ("allow_to_refund_payment",'Allow To Refund Payment'),
          ("allow_to_add_custom_loan_interest",'Allow To Add Custom Loan Interest'),
          ("allow_to_change_loan_duration",'Allow To Change Loan Duration'),
          ("allow_to_approve_loan",'Allow To Approve Loans'),
          ("allow_to_delete_from_cashbook",'Allow To Delete From Cash Book'),
          ("allow_to_back_date",'Allow To Back Date'),
          ("allow_to_view_other_stations",'Allow View Other Stations'),
          ("allow_to_view_other_reports",'Allow View Other Reports'),
          ("allow_to_set_opening_balance", "Allow To Set Opening Balance"),
          ("allow_to_correct_interest_book", "Allow To Change Interest Book"),
          ("allow_to_delete_from_court_queue", "Allow To Delete From Court Queue"),
          ("allow_to_pay_salaries", "Allow To Pay Salaries"),
          ("allow_to_pay_all_salaries", "Allow To Pay All Salaries"),
          ("allow_to_pay_rent", "Allow To Pay Rent"),
          ("allow_to_delete_employees", "Allow To Delete Employees"),
          ("allow_to_restore_deleted_employees", "Allow To Restore Deleted Employees"),
          ("allow_to_view_salary_payments", "Allow To View Salary Payments"),
          ("allow_to_adjust_fines", "Allow To Adjust Fines"),
          ("allow_to_view_visited_loans", "Allow To View Visited Loans"),
          ("allow_to_adjust_loan_balance", "Allow To Adjust Loan Balance"),
          ("allow_to_edit_total_fines", "Allow To Edit Total Fines"),
          ("allow_to_change_loan_interest_settings", "Allow To Change Loan Interest Settings"),
          ("allow_to_edit_loan_date", "Allow to edit loan date"),
          ("allow_to_stop_auto_loan_fines", "Allow to stop auto loan fines"),
          )
'''
Below are models for settings ad they have the key word stng
===============================================================================
'''

class BusinessStng(models.Model):
    """
    A store is a branch, forxample, a business may have many branches(stores) in diffrent areas, so 
    our app is a chain store app
    """
    business_name = models.CharField(max_length=150, null=True, blank=True)
    contact_numbers = models.CharField(max_length=50, null=True, blank=True)
    physical_adress = models.CharField(max_length=150, null=True, blank=True)
    email_address = models.CharField(max_length=50, null=True, blank=True)
    tag_line = models.CharField(max_length=50, null=True, blank=True)
    logo = OptimizedImageField(upload_to="logo/",null=True, blank=True,
                               optimized_image_output_size=(400, 400),
                               optimized_image_resize_method="cover"  #  "crop", "cover", "contain", "width", "height", "thumbnail" or None
                                 )
    reports_header = models.TextField(blank=True, null=True)

    def image_preview(self):
        return mark_safe(f'<img src="images/logo/{self.logo}" width="300">')
    image_preview.short_description = "Image"
    
    def __str__(self):
        return self.business_name
    class Meta:
        verbose_name = "Business Info"



class LoanTypeStng(models.Model):
    loan_type_name = models.CharField(max_length=80, blank=True, null=True)
    loan_duration = models.IntegerField(blank=True, default=0, null=True, verbose_name="Duration in Days")
    how_often_intreest_added = models.IntegerField(blank=True, null=True, default=0, 
                                                 verbose_name="How Often Interest Added(in Days)")
    loan_type_description = models.TextField(blank=True, null=True, default=0, )

    def __str__(self):
        return (self.loan_type_name or "")
    class Meta:
        verbose_name = "Loan Types"




class StationStng(models.Model):
    """
    A store is a branch, forxample, a business may have many branches(stores) in diffrent areas, so 
    our app is a chain store app
    """
    station_name = models.CharField(max_length=150, null=True, blank=True, unique=True)
    loan_typeID=models.ForeignKey(LoanTypeStng, on_delete=models.CASCADE, 
                                  null=True, blank=True,  verbose_name="Default Loan Scheme")
    station_head = models.CharField(max_length=80, null=True, blank=True)
    contact_numbers = models.CharField(max_length=50, null=True, blank=True)
    physical_adress = models.CharField(max_length=150, null=True, blank=True)
    rent = models.FloatField(default=0, null=True, blank=True)
    day_for_rent_payment =  models.CharField(max_length=50, null=True, blank=True)
    duration =  models.CharField(max_length=50, null=True, blank=True)
    rent_period = models.CharField(max_length=100, null=True, blank=True)
    email_address = models.CharField(max_length=50, null=True, blank=True)
    daily_percent = models.FloatField(default=0, null=True, blank=True)
    monthly_percent = models.FloatField(default=0, null=True, blank=True)
    defaulters_percent = models.FloatField(default=0, null=True, blank=True)
    monthly_defaulters_percent = models.FloatField(default=0, null=True, blank=True)
    
    def __str__(self):
        return self.station_name
    class Meta:
        verbose_name = "Station"




class SystemCustomSettings(models.Model):
    BOOLEAN_CHOICES = ((True,"Yes"), (False,"No"))
    stationID = models.ForeignKey(StationStng, on_delete=models.CASCADE, null=True, blank=True)
    settings_name  = models.CharField(max_length=50, null=True, blank=True, unique=True)
    user_friendly_name  = models.CharField(max_length=120, null=True, blank=True)
    settings_value  = models.CharField(max_length=40, null=True, blank=True)
    date_value = models.DateTimeField(null=True, blank=True)
    boolean_value = models.BooleanField(default=True, verbose_name="Allow", choices=BOOLEAN_CHOICES, )


    def __str__(self):
        return self.user_friendly_name+ " | " +str(self.settings_value)+" | "+ str(self.boolean_value)
       
    class Meta:
       
       indexes = [
         models.Index(fields=["settings_name",]),
       ]




class ClientTypeStng(models.Model):
    client_type_name = models.CharField(max_length=150, unique=True)
    interest_rate = models.FloatField(default=0, null=True, blank=True)
    def __str__(self):
        return str(self.id)+"-"+self.client_type_name




class ReportTypeStng(models.Model):
    report_name = models.CharField(max_length=150, unique=True, null=True, blank=True)
    def __str__(self):
        return self.report_name




class ItemType(models.Model):
    '''
    We have 1. incomes  and 2. expenses  
    '''
    item_type_name= models.CharField(max_length=50, unique=True, null=True, blank=True)
    def __str__(self):
        return self.item_type_name



class ItemCategories(models.Model):
    item_category_name= models.CharField(max_length=50, unique=True, null=True, blank=True)
    user_friendly_name = models.CharField(max_length=80, null=True, blank=True)
    item_typeID = models.ForeignKey(ItemType, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.user_friendly_name




class Paymethod(models.Model):
    pay_method_name= models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return str(self.id)+": "+ self.pay_method_name




class Custom_user_rights_settings(models.Model):
    user_right_name = models.CharField(max_length=50, blank=True, null=True, unique=True)
    user_friendly_name = models.CharField(max_length=120, null=True, blank=True)
    def __str__(self):
        return self.user_friendly_name




class Custom_user_rights(models.Model):
    userID=models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True)
    user_rightID=models.ForeignKey(Custom_user_rights_settings,  on_delete=models.CASCADE, blank=True, null=True)
    user_right = models.CharField(max_length=100, null=True, blank=True, choices=RIGHTS)
    def __str__(self):
        return str(self.userID)+" | "+ str(self.user_right)
    class Meta:
        ordering = ["userID",]
        indexes = [
          models.Index(fields=["user_rightID",]),
        ]

class Windows(models.Model):
    windows_name = models.CharField(max_length=80,null=True, blank=True, unique=True)
    user_friendly_name= models.CharField(max_length=120,null=True, blank=True)



class ReportTemplate(models.Model):
    report_typeID=models.ForeignKey(ReportTypeStng, on_delete=models.CASCADE, blank=True, null=True)
    windowID=models.ForeignKey(Windows, on_delete=models.CASCADE, blank=True, null=True)
    template_name = models.CharField(max_length=150, null=True, blank=True)
    template_report = RichTextField(null=True, blank=True)
    def __str__(self):
        self.template_name




class AutoItemAdds(models.Model):
    '''For items automatically added at a certain level, e.g processing fees, processing books
     admission fees, etc '''
    item_catID = models.ForeignKey(ItemCategories, on_delete=models.CASCADE, blank=True, null=True)
    loan_typeID = models.ForeignKey(LoanTypeStng, on_delete=models.CASCADE, blank=True, null=True)
    stationID= models.ForeignKey(StationStng, on_delete=models.CASCADE, blank=True, null=True)
    window= models.ForeignKey(Windows, on_delete=models.CASCADE, blank=True, null=True)
    item_name = models.CharField(max_length=80,null=True, blank=True)
    user_friendly_name = models.CharField(max_length=80,null=True, blank=True)
    unit_cost = models.FloatField(default=0,  blank=True, null=True)
    unit_price = models.FloatField(default=0,  blank=True, null=True)
    lower_limit = models.IntegerField(default=0, null=True, blank=True)
    upper_limit = models.IntegerField(default=0, null=True, blank=True)
    allow_auto_add= models.BooleanField(default=True, null=True, blank=True)
    per_unit_measure = models.CharField(max_length=70, null=True, blank=True)
    max_allowed_value = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
       ordering = ["-id",]
       indexes = [
         models.Index(fields=["item_name",]),
         models.Index(fields=["lower_limit",]),
         models.Index(fields=["upper_limit",]),
       ]
    def __str__(self):
        return str(self.stationID)+"-"+str(self.id)+"-"+(self.item_catID.item_typeID.item_type_name or "") +" | "+ (str(self.user_friendly_name) or "") + ": " + (str(self.lower_limit)or "") \
              + "-" +  (str(self.upper_limit) or "") + " | " +(str(self.unit_price) or "")




class ProcessingFeeStgn(models.Model):
    item_name = models.CharField(max_length=100, null=True, blank=True)

    amount = models.FloatField(null=True, blank=True)




class Employee(models.Model):
    GENDER_CHOICES = (("M",'Male'), ("F",'Female'))
    user_accountID=models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True)
    
    stationID = models.ForeignKey(StationStng, on_delete=models.CASCADE, null=True, blank=True)
    qualifications = models.CharField(max_length=100,blank=True, null=True)
    academic_docs = models.FileField(null=True, blank=True, upload_to ="employees/")
    hire_date = models.DateTimeField(null=True, blank=True)
    emp_title = models.CharField(max_length=80, blank=True, null=True)
    national_identification_number = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    surname = models.CharField(max_length=50, blank=True, null=True)
    other_names= models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=1, null=True, choices = GENDER_CHOICES)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    physical_address = models.CharField(max_length=150, blank=True, null=True)
    contact_numbers = models.CharField(max_length=50, blank=True, null=True)
    email_address = models.CharField(max_length=100, blank=True, null=True)
    monthly_pay = models.FloatField(default=0, blank=True, null=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    emp_img = OptimizedImageField(null=True, blank=True, upload_to ="employees/",
                                  optimized_image_output_size=(400, 400),
                                  optimized_image_resize_method="cover"  #  "crop", "cover", "contain", "width", "height", "thumbnail" or None
                                  )

    #Banking 
    bank_name = models.CharField(max_length=60, null=True, blank=True)
    accountNo = models.CharField(max_length=40, null=True, blank=True)
    net_pay = models.FloatField(default=0,  blank=True, null=True)
    nssf = models.FloatField(default=0,  blank=True, null=True)
    payee = models.FloatField(default=0,  blank=True, null=True)
    
    #Next of Kin info
    next_of_kin1 =models.CharField(max_length=80, blank=True, null=True) 
    next_of_kin1_contacts =models.CharField(max_length=50, blank=True, null=True) 
    next_of_kin1_address =models.CharField(max_length=120, blank=True, null=True) 
    next_of_kin1_img = OptimizedImageField(null=True, blank=True, upload_to ="employees/",
                                  optimized_image_output_size=(400, 400),
                                  optimized_image_resize_method="cover"  #  "crop", "cover", "contain", "width", "height", "thumbnail" or None
                                  )   
 
    next_of_kin2 =models.CharField(max_length=80, blank=True, null=True) 
    next_of_kin2_contacts =models.CharField(max_length=50, blank=True, null=True) 
    next_of_kin2_address =models.CharField(max_length=120, blank=True, null=True)  
    next_of_kin2_img =OptimizedImageField(null=True, blank=True, upload_to ="employees/",
                                  optimized_image_output_size=(400, 400),
                                  optimized_image_resize_method="cover"  #  "crop", "cover", "contain", "width", "height", "thumbnail" or None
                                  )   

    #Other important information
    district = models.CharField(max_length=100, null=True, blank=True)
    sub_county = models.CharField(max_length=100, null=True, blank=True)
    lc1_village = models.CharField(max_length=100, null=True, blank=True)

    record_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    notes = models.TextField(max_length=255, null=True, blank=True)
    deleted =  models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
       return (str(self.user_accountID) or "")+": " +(self.first_name or "") +" "+ (self.surname or "")

    class Meta:
       ordering = ["first_name",]
       indexes = [
         models.Index(fields=["first_name",]),
         models.Index(fields=["surname",]),
         models.Index(fields=["other_names",]),
         models.Index(fields=["contact_numbers",]),
         models.Index(fields=["deleted",]),
         models.Index(fields=["is_active",]),
       ]




class UserStationDetailsVew(models.Model):
    userID=models.ForeignKey(User,  on_delete=models.CASCADE)
    stationID = models.ForeignKey(StationStng, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.userID) or " " + " "+ str(self.stationID) or " "



class Client(models.Model):
    GENDER_CHOICES = (("M",'Male'), ("F",'Female'))

    userID=models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True)
    user_accountID=models.IntegerField(default=0,blank=True, null=True)#Just incase the client is a system user
    stationID = models.ForeignKey(StationStng, on_delete=models.CASCADE, null=True, blank=True)
    client_typeID=models.ForeignKey(ClientTypeStng, default=1, on_delete=models.CASCADE, null=True, blank=True)
    national_identification_number = models.CharField(max_length=50, db_index=True, blank=True, null=True)
    client_national_id = OptimizedImageField(null=True, blank=True, upload_to ="client_files/",
                                  optimized_image_output_size=(400, 400),
                                  optimized_image_resize_method="cover"  #  "crop", "cover", "contain", "width", "height", "thumbnail" or None
                                  ) 
    first_name = models.CharField(max_length=50, blank=True, null=True)
    surname = models.CharField(max_length=50, blank=True, null=True)
    other_names= models.CharField(max_length=50, blank=True, null=True, default="")
    full_name = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True, choices = GENDER_CHOICES)
    date_of_birth = models.CharField(max_length=50, blank=True, null=True)
    physical_address = models.CharField(max_length=150, blank=True, null=True)
    contact_numbers = models.CharField(max_length=50, blank=True, null=True)
    email_address = models.CharField(max_length=100, blank=True, null=True)
    client_img = OptimizedImageField(null=True, blank=True, upload_to ="clients/",
                                  optimized_image_output_size=(400, 400),
                                  optimized_image_resize_method="cover"  #  "crop", "cover", "contain", "width", "height", "thumbnail" or None
                                  )   

    current_total_balance = models.FloatField(default=0, null=True, blank=True)

    #auto add items
    borrowers_book_record = models.IntegerField(default=0, null=True, blank=True)

    #Banking and occuptaion
    occupation = models.CharField(max_length=120, blank=True, null=True) 
    bank_name = models.CharField(max_length=60, null=True, blank=True)
    accountNo = models.CharField(max_length=40, null=True, blank=True)
    ATM_NO = models.CharField(max_length=40, null=True, blank=True)
    ATM_PIN = models.CharField(max_length=5, null=True, blank=True)
    employer = models.CharField(max_length=120, blank=True, null=True)
    employer_address = models.CharField(max_length=120, blank=True, null=True)

    #Next of Kin info
    next_of_kin1 =models.CharField(max_length=80, blank=True, null=True) 
    next_of_kin1_contacts =models.CharField(max_length=50, blank=True, null=True) 
    next_of_kin1_address =models.CharField(max_length=120, blank=True, null=True)   
    next_of_kin2 =models.CharField(max_length=80, blank=True, null=True) 
    next_of_kin2_contacts =models.CharField(max_length=50, blank=True, null=True) 
    next_of_kin2_address =models.CharField(max_length=120, blank=True, null=True)    

    #Other important information
    district = models.CharField(max_length=100, null=True, blank=True)
    sub_county = models.CharField(max_length=100, null=True, blank=True)
    lc1_village = models.CharField(max_length=100, null=True, blank=True)

    record_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    deleted =  models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return str(self.id)+ ": | "+ str(self.surname) or "" +" "+ str(self.first_name) or ""



    class Meta:
       indexes = [
         models.Index(fields=["first_name",]),
         models.Index(fields=["surname",]),
         models.Index(fields=["other_names",]),
         models.Index(fields=["full_name",]),
         models.Index(fields=["contact_numbers",]),
         models.Index(fields=["current_total_balance",]),
         models.Index(fields=["deleted",]),
         models.Index(fields=["record_date",]),
         models.Index(fields=["user_accountID",]),
         models.Index(fields=["userID",]),
         models.Index(fields=["national_identification_number",]),
       ]

    def return_fullname(self):

       fullname= (str(self.surname) or "") + " " + (str(self.first_name) or "") + " " +(str(self.other_names) or "")
              
       return fullname
    

    def save(self, *args,**kwargs):
        self.full_name = self.return_fullname()
        super(Client, self).save(*args, **kwargs)

            

    
class Loan(models.Model):
    '''Loans Model'''
    clientID = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(StationStng, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=80, null=True, blank=True)
    loan_typeID=models.ForeignKey(LoanTypeStng, on_delete=models.CASCADE, null=True, 
                                  verbose_name="Loan Scheme", blank=True, default=1)
    allow_get_loan_without_processing_book = models.BooleanField(default=False, null=True, blank=True)
    allow_pay_loan_without_processing_book = models.BooleanField(default=False, null=True, blank=True)
    allow_casual_payments = models.BooleanField(default=False, null=True, blank=True)
    stop_loan_counting= models.BooleanField(default=False, null=True, blank=True)
    dont_add_to_court_queue = models.BooleanField(default=False, null=True, blank=True)
    sent_to_court = models.BooleanField(default=False, null=True, blank=True)
    
    principle = models.FloatField(default=0, null=True, blank=True)
    current_principle = models.FloatField(default=0, null=True, blank=True)
    original_interest = models.FloatField(default=0, null=True, blank=True)
    current_interest = models.FloatField(default=0, null=True, blank=True)
    total_loan_interest = models.FloatField(default=0, null=True, blank=True)
    current_balance = models.FloatField(default=0, null=True, blank=True)
    loan_total_paid  = models.FloatField(default=0, null=True, blank=True)
    total_fines = models.FloatField(default=0, null=True, blank=True)

    #Disbursement
    processing_fee = models.FloatField(default=0, null=True, blank=True)
    borrowers_book_fee = models.FloatField(default=0, null=True, blank=True)
    disbursing_officerID = models.IntegerField(default=0, null=True, blank=True)
    disbursing_officer = models.CharField(max_length=80, blank=True, null=True)  
    pay_methodID =models.ForeignKey(Paymethod, on_delete=models.CASCADE, null=True, blank=True, default=1)
    pay_medium = models.CharField(max_length=30, blank=True, null=True)  
    pay_identification = models.CharField(max_length=40, blank=True, null=True) 
    approve_status = models.BooleanField(default=False, blank=True, null=True)
    disburse_status = models.BooleanField(default=False, blank=True, null=True)
    approved_byID=models.IntegerField(default=0,  blank=True, null=True)
    approved_by_name =  models.CharField(max_length=80, null=True, blank=True)
    received_by = models.CharField(max_length=80, null=True, blank=True)
    loan_disbursement_file =OptimizedImageField(null=True, blank=True, upload_to ="client_files/",
                                  optimized_image_output_size=(420, 594),
                                  optimized_image_resize_method="cover"  #  "crop", "cover", "contain", "width", "height", "thumbnail" or None
                                  ) 
    loan_agreement_file =OptimizedImageField(null=True, blank=True, upload_to ="client_files/",
                                  optimized_image_output_size=(420, 594),
                                  optimized_image_resize_method="cover"  #  "crop", "cover", "contain", "width", "height", "thumbnail" or None
                                  ) 
    #Other details
    date_given = models.DateTimeField(null=True, blank=True)
    loan_duration = models.IntegerField(default=0, blank=True, null=True)
    expected_clearance_date = models.DateTimeField(null=True, blank=True)
    userID=models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True)
    prepared_by_name =  models.CharField(max_length=80, blank=True, null=True) 
    record_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    deleled =  models.BooleanField(default=False, null=True, blank=True)


  

    class Meta:
       ordering = ["record_date",]
       indexes = [
         models.Index(fields=["full_name"]),  
         models.Index(fields=["current_balance"]),
         models.Index(fields=["approve_status"]),
         models.Index(fields=["disburse_status"]),
         models.Index(fields=["record_date",]),
         models.Index(fields=["approved_byID",]),
         models.Index(fields=["deleled",]),
         models.Index(fields=["stop_loan_counting",]),
         models.Index(fields=["dont_add_to_court_queue",]),
         models.Index(fields=["sent_to_court",]),
       ]
    
    def __str__(self):
        return (str(self.id) or "") +" "+(str(self.full_name) or "")+": Balance: "+ (f"{self.current_balance:,}" or"")




class AgreementFile(models.Model):
    clientID = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(StationStng, on_delete=models.CASCADE, null=True, blank=True)
    loanID = models.ForeignKey(Loan, on_delete=models.CASCADE, null=True, blank=True)
    page_name = models.CharField(max_length=20, null=True, blank=True)
    agreement_file =OptimizedImageField(null=True, blank=True, upload_to ="client_files/",
                                  optimized_image_output_size=(420, 594),
                                  optimized_image_resize_method="cover"  #  "crop", "cover", "contain", "width", "height", "thumbnail" or None
                                  )
    userID=models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True)
    record_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.id)+ ": " + str(self.clientID)+ " -:"+ (str(self.page_name) or "")
                                   






class DisbursementFile(models.Model):
    clientID = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(StationStng, on_delete=models.CASCADE, null=True, blank=True)
    loanID = models.ForeignKey(Loan, on_delete=models.CASCADE, null=True, blank=True)
    page_name = models.CharField(max_length=20, null=True, blank=True)
    disbursement_file =OptimizedImageField(null=True, blank=True, upload_to ="client_files/",
                                  optimized_image_output_size=(420, 594),
                                  optimized_image_resize_method="cover"  #  "crop", "cover", "contain", "width", "height", "thumbnail" or None
                                  )
    userID=models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True)
    record_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    def __str__(self):
        return str(self.clientID)
                                   



class InterestBook(models.Model):
    clientID = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(StationStng, on_delete=models.CASCADE, null=True, blank=True)
    loanID = models.ForeignKey(Loan, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=80, blank=True, null=True)
    original_principle = models.FloatField(default=0, null=True, blank=True)
    loan_recovered = models.FloatField(default=0, null=True, blank=True)
    interest_paid = models.FloatField(default=0, null=True, blank=True)
    loan_disbursed = models.FloatField(default=0, null=True, blank=True)
    fines = models.FloatField(default=0, null=True, blank=True)
    processing_fee = models.FloatField(default=0, null=True, blank=True)
    borrowers_book = models.FloatField(default=0, null=True, blank=True)
    userID=models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True)
    record_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    deleled =  models.BooleanField(default=False, null=True, blank=True)
    
    def __str__(self):
        return str(self.stationID)+" "+ (str(self.full_name) or "")
    
    class Meta:
        indexes = [
            models.Index(fields=["record_date"]),  
            models.Index(fields=["full_name"]),
            models.Index(fields=["loan_recovered"]),
            models.Index(fields=["interest_paid"]),
            models.Index(fields=["fines"]),
            models.Index(fields=["processing_fee"]),
            models.Index(fields=["borrowers_book"]),
        ]
    

   

class Guarantor(models.Model):
    GENDER_CHOICES = (("M",'Male'), ("F",'Female'))
    #Just incase the client is a system user
    loanID = models.ForeignKey(Loan, on_delete=models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(StationStng, on_delete=models.CASCADE, null=True, blank=True)
    national_identification_number = models.CharField(max_length=50, db_index=True, null=True, blank=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    surnane = models.CharField(max_length=50, blank=True, null=True)
    other_names= models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=1,  choices = GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    physical_address = models.CharField(max_length=150, blank=True, null=True)
    contact_numbers = models.CharField(max_length=50, blank=True, null=True)
    email_address = models.CharField(max_length=100, blank=True, null=True)
    occupation = models.CharField(max_length=120, blank=True, null=True)
    guarantor_img = OptimizedImageField(null=True, blank=True, upload_to ="guarantors/",
                                  optimized_image_output_size=(400, 400),
                                  optimized_image_resize_method="cover"  #  "crop", "cover", "contain", "width", "height", "thumbnail" or None
                                  )   

    userID=models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True)
    record_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    deleled =  models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
       return (str(self.first_name) or "") +" "+ (str(self.surnane) or "")

    class Meta:
       indexes = [
         models.Index(fields=["deleled",]),
       ]




class Security(models.Model):
    GENDER_CHOICES = (("M",'Male'), ("F",'Female'))
    
    #Just incase the client is a system user
    clientID = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(StationStng, on_delete=models.CASCADE, null=True, blank=True)
    loanID = models.ForeignKey(Loan, on_delete=models.CASCADE, null=True, blank=True)
    fullname=models.CharField(max_length=100, null=True, blank=True)
    security_name = models.CharField(max_length=150, null=True, blank=True)
    security_address = models.CharField(max_length=150, blank=True, null=True)
    estimated_value = models.FloatField(default=0, null=True, blank=True)
    image = OptimizedImageField(null=True, blank=True, upload_to ="security/",
                                  optimized_image_output_size=(400, 400),
                                  optimized_image_resize_method="cover"  #  "crop", "cover", "contain", "width", "height", "thumbnail" or None
                                  )   

    userID=models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True)
    record_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    deleled =  models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
       return (self.security_name or "")
    
    class Meta:
       indexes = [
         models.Index(fields=["record_date",]),
         models.Index(fields=["deleled",]),        
       ]




class DailyPayBack(models.Model):
    clientID = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(StationStng, on_delete=models.CASCADE, null=True, blank=True)
    loanID = models.ForeignKey(Loan, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=80, blank=True, null=True)
    original_principle = models.FloatField(default=0, null=True, blank=True)
    principle_day_pay_back = models.FloatField(default=0, null=True, blank=True)
    original_interest_day_pay_back = models.FloatField(default=0, null=True, blank=True)
    interest_day_pay_back = models.FloatField(default=0, null=True, blank=True)
    total_day_debt =  models.FloatField(default=0, null=True, blank=True)
    total_day_paid= models.FloatField(default=0, null=True, blank=True)
    total_day_balance = models.FloatField(default=0, null=True, blank=True)
    no_of_days_past = models.IntegerField(default=0, null=True, blank=True)
    expected_pay_date =models.DateTimeField(null=True, blank=True)
    bg_color = models.CharField(max_length=20, blank=True, null=True)
    text_color = models.CharField(max_length=20, blank=True, null=True)
    pay_date = models.DateTimeField(null=True, blank=True)
    last_date_updated = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    record_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
       return (self.loanID.stationID.station_name)+": "+self.full_name + "Loan: "+ str(self.loanID)
      
    class Meta:
       ordering = ["-id",]
       indexes = [
         models.Index(fields=["full_name",]),
         models.Index(fields=["pay_date",]),
         models.Index(fields=["expected_pay_date"]),
         models.Index(fields=["record_date",]),
         models.Index(fields=["last_date_updated",]),  
         models.Index(fields=["total_day_balance",]),       
       ]




class Interest(models.Model):
    clientID = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(StationStng, on_delete=models.CASCADE, null=True, blank=True)
    loanID = models.ForeignKey(Loan, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    original_principle = models.FloatField(default=0, null=True, blank=True)
    current_principle = models.FloatField(default=0, null=True, blank=True)
    original_interest = models.FloatField(default=0, null=True, blank=True)
    amount = models.FloatField(default=0, null=True, blank=True)
    userID=models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True)
    record_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    deleled =  models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
       return self.full_name

    class Meta:
       indexes = [
         models.Index(fields=["full_name",]),
         models.Index(fields=["record_date",]),
         models.Index(fields=["deleled",]),         
       ]


class VisitedLoans(models.Model):
    clientID = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(StationStng, on_delete=models.CASCADE, null=True, blank=True)
    loanID = models.ForeignKey(Loan, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    loan_record_date = models.DateTimeField(null=True, blank=True)
    loan_last_pay_date =models.DateTimeField(null=True, blank=True)
    loan_current_debt_then = models.FloatField(default=0, null=True, blank=True)
    record_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    userID=models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.full_name



class cashBookMain(models.Model):
    date_stationID = models.CharField(max_length=50, unique=True, null=True, blank=True)
    started= models.BooleanField(default=False, null=True, blank=True)
    opening_balance = models.FloatField(default=0, null=True, blank=True)
    stationID = models.ForeignKey(StationStng, on_delete=models.CASCADE, null=True, blank=True)
    closing_balance= models.FloatField(default=0, null=True, blank=True)
    userID=models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True)
    record_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    class Meta:
       indexes = [
         models.Index(fields=["started",]),
         models.Index(fields=["record_date",]),        
       ]
    def __str__(self):
        return str(self.stationID)




class CourtQueue(models.Model):
    GENDER_CHOICES = (("M",'Male'), ("F",'Female'))
    clientID = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(StationStng, on_delete=models.CASCADE, null=True, blank=True)
    loanID = models.ForeignKey(Loan, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=80, blank=True, null=True)
    gender = models.CharField(max_length=1, null=True, choices = GENDER_CHOICES)
    dob = models.DateTimeField(null=True, blank=True)
    age = models.IntegerField(default=0, null=True, blank=True)
    contacts= models.CharField(max_length=80, blank=True, null=True)
    national_identification_number = models.CharField(max_length=50, db_index=True, blank=True, null=True)
    address= models.CharField(max_length=140, blank=True, null=True)
    loan_record_date= models.DateTimeField(null=True, blank=True)
    loan_expected_pay_date = models.DateTimeField(null=True, blank=True)
    loan_principle =  models.FloatField(default=0, null=True, blank=True)
    loan_debt =  models.FloatField(default=0, null=True, blank=True)
    total_court_expense =  models.FloatField(default=0, null=True, blank=True)
    total_paid =  models.FloatField(default=0, null=True, blank=True)
    demand_notice = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(max_length=255, null=True, blank=True)
    del_notes=models.TextField(max_length=255, null=True, blank=True)
    userID=models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True)
    remove_from_court_queue = models.BooleanField(default=False, null=True, blank=True)
    record_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.full_name
    
    class Meta:
       indexes = [
         models.Index(fields=["loan_expected_pay_date",]),  
         models.Index(fields=["record_date",]),    
         models.Index(fields=["full_name"]),
         models.Index(fields=["remove_from_court_queue"]),
       ]




class CashBook(models.Model):
    cashbooktmainID = models.ForeignKey(cashBookMain, on_delete=models.CASCADE, null=True, blank=True) 
    clientID = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True) 
    courtID = models.ForeignKey(CourtQueue, on_delete=models.CASCADE, null=True, blank=True) 
    stationID = models.ForeignKey(StationStng, on_delete=models.CASCADE, null=True, blank=True)
    employeeID = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    interest_bookID =  models.ForeignKey(InterestBook, on_delete=models.CASCADE, null=True, blank=True)
    loanID = models.ForeignKey(Loan, on_delete=models.CASCADE, null=True, blank=True)
    full_name =models.CharField(max_length=100, blank=True, null=True) #takes up client name in case of loan payment, otherwise itam name for others
    item_name = models.CharField(max_length=100, blank=True, null=True) #takes names such as loan given, proessing fee, etc
    item_catID = models.ForeignKey(ItemCategories, on_delete=models.CASCADE, null=True, blank=True)
    daily_pay_backID = models.ForeignKey(DailyPayBack, on_delete=models.CASCADE, null=True, blank=True)
    inc_exp_status=models.BooleanField(default=True, null=True, blank=True) #True means income
    pay_methodID =models.ForeignKey(Paymethod,  on_delete=models.CASCADE, null=True, blank=True, default=1)
    pay_medium = models.CharField(max_length=30, blank=True, null=True)  
    pay_identification = models.CharField(max_length=40, blank=True, null=True) 
    quantity = models.FloatField(default=1, null=True, blank=True)
    unit_cost = models.FloatField(default=0, null=True, blank=True)
    unit_price = models.FloatField(default=0, null=True, blank=True) 
    inc_amount = models.FloatField(default=0, null=True, blank=True)
    cost_amount = models.FloatField(default=0, null=True, blank=True)
    exp_amount = models.FloatField(default=0, null=True, blank=True)
    balance = models.FloatField(default=0, null=True, blank=True)
    balance_str = models.CharField(max_length=100, null=True, blank=True)
    userID=models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True)
    record_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    deleled =  models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.item_name
    class Meta:
       indexes = [ 
         models.Index(fields=["record_date",]),
         models.Index(fields=["deleled",]), 
         models.Index(fields=["item_name",]),
         models.Index(fields=["inc_exp_status",]),        
       ]

    def return_balance_str(self):
        if float(self.balance) < 0:
            results = "("+ f"{-1*self.balance:,}" +")"
        else:
            results = str(self.balance) 
        return results

    def save(self, *args,**kwargs):
        self.balance_str = self.return_balance_str()
        super(CashBook, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.stationID) + " | " +str(self.full_name or "") +" | "+ str(self.item_name or "")
        



class OtherPayments(models.Model):
    stationID = models.ForeignKey(StationStng, on_delete=models.CASCADE, null=True, blank=True)
    courtID = models.ForeignKey(CourtQueue, on_delete=models.CASCADE, null=True, blank=True) 
    fullname = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    pay_methodID =models.ForeignKey(Paymethod,  on_delete=models.CASCADE, null=True, blank=True, default=1)
    pay_medium = models.CharField(max_length=30, blank=True, null=True)  
    pay_identification = models.CharField(max_length=40, blank=True, null=True) 
    debit = models.FloatField(default=0, null=True, blank=True)
    credit = models.FloatField(default=0, null=True, blank=True) 
    userID=models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True)
    record_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return str(self.record_date) + " " + str(self.stationID) + self.fullname




class Track_auto_item_adds(models.Model):
    clientID = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(StationStng, on_delete=models.CASCADE, null=True, blank=True)
    loanID = models.ForeignKey(Loan, on_delete=models.CASCADE, null=True, blank=True )
    AutoItemAddsID = models.ForeignKey(AutoItemAdds, on_delete=models.CASCADE, null=True, blank=True)
    item_name = models.CharField(max_length=80, null=True, blank=True)
    cashbookID = models.ForeignKey(CashBook, on_delete=models.CASCADE, null=True, blank=True)
    tracking_number=models.IntegerField(default=0, null=True, blank=True)
    closed = models.BooleanField(default=False, null=True, blank=True)
    userID=models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True)
    record_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):

        this_date=""
        try:
            this_datex = str(self.record_date)
        except:
            pass

        this_date = this_datex.split(" ")
        return (this_date[0] or "")+" | Client "+ (str(self.clientID) or"")

    class Meta:
       indexes = [
         models.Index(fields=["tracking_number",]),
         models.Index(fields=["closed",]),  
         models.Index(fields=["item_name",]),     
       ]




class StationDeposits(models.Model):
    stationID = models.ForeignKey(StationStng, on_delete=models.CASCADE, null=True, blank=True)
    amount=models.FloatField(default=0, null=True, blank=True)
    userID=models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True)
    record_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
       indexes = [
         models.Index(fields=["record_date",]),     
       ]



class DailyPayBacksInterest(models.Model):
    clientID = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(StationStng, on_delete=models.CASCADE, null=True, blank=True)
    loanID = models.ForeignKey(Loan, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=80, blank=True, null=True)
    pay_date = models.DateTimeField(null=True, blank=True)
    old_total_debt =  models.FloatField(default=0, null=True, blank=True)
    total_day_debt =  models.FloatField(default=0, null=True, blank=True)
    total_day_balance = models.FloatField(default=0, null=True, blank=True)
    interest_added = models.FloatField(default=0, null=True, blank=True)
    userID=models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True)
    record_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
       indexes = [ 
         models.Index(fields=["record_date",]),     
       ]




class Report(models.Model):
    report_typeID = models.ForeignKey(ReportTypeStng, on_delete=models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(StationStng, on_delete=models.CASCADE, null=True, blank=True)
    courtID = models.ForeignKey(CourtQueue, on_delete=models.CASCADE, null=True, blank=True)
    relatedID= models.IntegerField(default=0, null=True)
    clientID = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    loanID = models.ForeignKey(Loan, on_delete=models.CASCADE, null=True, blank=True)
    report_text = RichTextField(null=True)
    userID=models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True)
    record_date = models.DateTimeField(auto_now_add=True)
    deleled =  models.BooleanField(default=False, null=True, blank=True)
    class Meta:
        verbose_name ="Reports"
        indexes = [
         models.Index(fields=["relatedID",]),
         models.Index(fields=["record_date",]),
         models.Index(fields=["deleled",]),
        ]
    def __str__(self):
        record_date = str(self.record_date).split(' ')
        return str(record_date[0])+" "+str(self.stationID) +" "+str(self.clientID)
        


class WeeklyBook(models.Model):
            stationID = models.ForeignKey(StationStng, on_delete=models.CASCADE, null=True, blank=True)
            fines = models.FloatField(blank=True, default=0, null=True)
            borrowers_book = models.FloatField(blank=True, default=0, null=True)
            loan_processing_fee = models.FloatField(blank=True, default=0, null=True)
            interest_paid = models.FloatField(blank=True, default=0, null=True)
            total = models.FloatField(blank=True, default=0, null=True)
            date_str_stationID = models.CharField(blank=True, max_length=40, null=True, unique=True)
            record_date= models.DateTimeField(auto_now_add=True, null=True)

            def __str__(self):
                date_str = str(self.record_date).split(" ")
                return str(self.stationID.station_name) +": "+ date_str[0]
            
            class Meta:
                ordering = ["record_date","stationID"]
                indexes = [ 
                    models.Index(fields=["record_date",]),     
                ]




class Daily_item_catID_totals(models.Model):
    item_catID = models.ForeignKey(ItemCategories, on_delete=models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(StationStng, on_delete=models.CASCADE, null=True, blank=True)
    date_item_catID_stationID  = models.CharField(max_length=40, unique=True,  null=True, blank=True)
    year_week_item_catID_stationID = models.CharField(max_length=40, null=True, blank=True)
    exp_amount = models.FloatField(default=0, null=True, blank=True)
    inc_amount = models.FloatField(default=0, null=True, blank=True)
    net_amount = models.FloatField(default=0, null=True, blank=True)
    net_amount_str = models.CharField(max_length=100, null=True, blank=True)
    date_str = models.CharField(max_length=40, null=True, blank=True)
    record_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
       verbose_name ="Daily Totals"
       indexes = [
         models.Index(fields=["record_date",]),
         models.Index(fields=["year_week_item_catID_stationID"]), 
         models.Index(fields=["date_str",]),     
       ]

    def return_date_value(self):
        datetime_str = str(self.record_date)
        datetime_obj = datetime_str.split(" ")
        return datetime_obj[0]
       
    def return_net_amount_str(self):
        if float(self.net_amount) < 0:
            results = "("+ f"{-1*self.net_amount:,}" +")"
        else:
            results = str(self.net_amount) 
        return results 

    def save(self, *args,**kwargs):
        self.net_amount_str = self.return_net_amount_str()
        self.date_str = self.return_date_value()
        super(Daily_item_catID_totals, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.stationID)+" | " + self.item_catID.item_category_name



class Monthly_ite_totals(models.Model):
    item_catID = models.ForeignKey(ItemCategories, on_delete=models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(StationStng, on_delete=models.CASCADE, null=True, blank=True)
    month_item_catID_stationID = models.CharField(max_length=25, unique=True,  null=True, blank=True)
    inc_amount = models.FloatField(default=0, null=True, blank=True)
    exp_amount = models.FloatField(default=0, null=True, blank=True)
    net_amount = models.FloatField(default=0, null=True, blank=True)
    net_amount_str = models.CharField(max_length=100, null=True, blank=True)
    date_str = models.CharField(max_length=40, null=True, blank=True)
    record_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
       verbose_name ="Monthly Totals"
       indexes = [
         models.Index(fields=["record_date",]),  
         models.Index(fields=["date_str",]),      
       ]
    
    def return_net_amount_str(self):
        if float(self.net_amount) < 0:
            results = "("+ f"{-1*self.net_amount:,}" +")"
        else:
            results = str(self.net_amount) 
        return results
    
    def return_date_value(self):
        datetime_str = str(self.record_date)
        datetime_obj = datetime_str.split(" ")
        return datetime_obj[0]

    def save(self, *args,**kwargs):
        self.net_amount_str = self.return_net_amount_str()
        self.date_str = self.return_date_value()
        super(Monthly_ite_totals, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.stationID)+" | " + self.item_catID.item_category_name




class Yearly_ite_totals(models.Model):
    item_catID = models.ForeignKey(ItemCategories, on_delete=models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(StationStng, on_delete=models.CASCADE, null=True, blank=True)
    year_item_catID_stationID = models.CharField(max_length=25, unique=True,  null=True, blank=True)
    inc_amount = models.FloatField(default=0, null=True, blank=True)
    exp_amount = models.FloatField(default=0, null=True, blank=True)
    net_amount = models.FloatField(default=0, null=True, blank=True)
    net_amount_str = models.CharField(max_length=100, null=True, blank=True)
    date_str = models.CharField(max_length=40, null=True, blank=True)
    record_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        record_date = self.record_date
        year = str(record_date.year)
        return str(year) +": "+ str("Income: ") +str(self.inc_amount) + \
              " Expense: "+str(self.exp_amount)

    class Meta:
       verbose_name ="Yearly Totals"
       indexes = [
         models.Index(fields=["record_date",]), 
         models.Index(fields=["date_str",]),       
       ]

    def return_net_amount_str(self):
        if float(self.net_amount) < 0:
            results = "("+ f"{-1*self.net_amount:,}" +")"
        else:
            results = str(self.net_amount) 
        return results
    
    def return_date_value(self):
        datetime_str = str(self.record_date)
        datetime_obj = datetime_str.split(" ")
        return datetime_obj[0]

    def save(self, *args,**kwargs):
        self.net_amount_str = self.return_net_amount_str()
        self.date_str = self.return_date_value()
        super(Yearly_ite_totals, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.stationID)+" | " + self.item_catID.item_category_name





class Tbl_trigger_checker(models.Model):
     """
     This table flags off the trigger status with value =1 to indicate that that days' 
     automation is done already
     """
     triger_status = models.IntegerField(default=0, null=True, blank=True)
     stationID = models.ForeignKey(StationStng, on_delete=models.CASCADE, null=True, blank=True)
     date_stationID = models.CharField(max_length=30, unique=True,  null=True, blank=True)
     record_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

     class Meta:
       indexes = [
         models.Index(fields=["record_date",]), 
         models.Index(fields=["triger_status",]),       
       ]




class DeletedItems(models.Model):
    deleted_item_catID = models.IntegerField(null=True, blank=True, default=0)
    stationID= models.ForeignKey(StationStng, on_delete=models.CASCADE, blank=True, null=True)
    item_record_date=models.DateTimeField(null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    reason = models.CharField(max_length=200, null=True, blank=True)
    amount=models.FloatField(null=True, blank=True, default=0)
    exp_amount=models.FloatField(null=True, blank=True, default=0)
    item_catID = models.ForeignKey(ItemCategories, on_delete=models.CASCADE, blank=True, null=True)
    userID=models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True)
    record_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.record_date)+": "+ str(self.userID or "") +" "+ str(self.description or "")
    

