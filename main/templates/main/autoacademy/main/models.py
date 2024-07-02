from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

GENDER_CHOICES = (("Male",'Male'), ("Female",'Female'))

#custom functions
#=======================================================
from django.conf import settings
import os


  
class Business(models.Model):
    busniness_name = models.CharField(max_length=150)
    logo = models.ImageField(null=True, blank=True, upload_to ="logo")
    contact_numbers = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    motto = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    website = models.CharField(max_length=80, null=True, blank=True)
    custom_header = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.busniness_name
#================================================================================================



class Campus(models.Model):
    campus_name = models.CharField(max_length=150)
    logo = models.ImageField(null=True, blank=True, upload_to ="logo")
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    contact_numbers = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    motto = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    website = models.CharField(max_length=80, null=True, blank=True)
    custom_header = models.TextField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.campus_name



class Parent(models.Model):
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    surname = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50, default="")
    othernames = models.CharField(max_length=50, null=True, blank=True, default="")
    NIN = models.CharField(max_length=50, null=True, blank=True)
    userID = models.ForeignKey(User, null=True, blank=True,  on_delete = models.CASCADE)
    gender = models.CharField(max_length=7, null=True, choices = GENDER_CHOICES)
    contacts = models.CharField(max_length=50)
    search_string = models.CharField(max_length=120, null=True, blank=True)
    address = models.CharField(max_length = 100, null=True, blank=True)
    parent_image = models.ImageField(null=True, blank=True, upload_to ="images")

    def __str__(self):
        return str(self.surname)+" "+str(self.firstname)+" "+str(self.othernames)

    def save(self, *args,**kwargs):
        self.search_string = str(self.surname)+" "+ \
                             str(self.firstname)+" "+str(self.othernames)+" "+ \
                             str(self.NIN)+" "+  str(self.contacts)
        super(Parent, self).save(*args, **kwargs)
 
    class Meta:
       indexes = [ 
         models.Index(fields=["search_string",]), 
         models.Index(fields=["NIN",]),       
       ]



class StudentType(models.Model):
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    settings_name = models.CharField(max_length=50)
    student_type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.student_type_name
    class Meta:
       indexes = [ 
         models.Index(fields=["settings_name",]),       
       ]
    

class Student(models.Model):
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    student_typeID = models.ForeignKey(StudentType, on_delete = models.CASCADE, null=True, blank=True)
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    surname = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50, default="")
    othernames = models.CharField(max_length=50, null=True, blank=True, default="")
    fullname = models.CharField(max_length=80, null=True, blank=True)
    NIN = models.CharField(max_length=50, null=True, blank=True)
    student_NO = models.CharField(max_length=50, null=True, blank=True)
    AST_NO = models.CharField(max_length=50, null=True, blank=True, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    userID = models.ForeignKey(User, null=True, blank=True,  on_delete = models.CASCADE)
    user_fullname = models.CharField(max_length=80, null=True, blank=True)
    gender = models.CharField(max_length=7, null=True, choices = GENDER_CHOICES)
    contacts = models.CharField(max_length=50)
    search_string = models.CharField(max_length=120, null=True, blank=True)
    address = models.CharField(max_length = 100, null=True, blank=True)
    student_image = models.ImageField(null=True, blank=True, upload_to ="images")
    #speed optimization
    year_class = models.CharField(max_length = 40, default="")
    term_name  = models.CharField(max_length = 40, default="")
    stream_name = models.CharField(max_length = 50, default="")
    original_fees = models.FloatField(default=0, null=True, blank=True)
    amount_paid  = models.FloatField(default=0, null=True, blank=True)
    balance  = models.FloatField(default=0, null=True, blank=True)
    record_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.id)+": "+str(self.surname)+" "+str(self.firstname)+" "+str(self.othernames)

    def save(self, *args,**kwargs):
        self.search_string = str(self.surname)+" "+str(self.firstname)+" "+str(self.othernames)+" "+str(self.NIN)+" "+str(self.contacts)
        self.fullname = str(self.surname)+" "+str(self.firstname)+" "+str(self.othernames)
        super(Student, self).save(*args, **kwargs)
 
    class Meta:
       indexes = [ 
        models.Index(fields=["search_string",]), 
        models.Index(fields=["year_class",]), 
        models.Index(fields=["term_name",]),
        models.Index(fields=["stream_name",]), 
        models.Index(fields=["balance",]), 
        models.Index(fields=["record_date",]),  
        models.Index(fields=["student_NO",]), 
        models.Index(fields=["NIN",]),
       ]




class StudentParent(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    studentID = models.ForeignKey(Student, on_delete = models.CASCADE)
    parentID = models.ForeignKey(Parent, on_delete = models.CASCADE)
    relation_to_student = models.CharField(max_length=50, default="")

    def __str__(self):
        return str(self.studentID) +": "+ str(self.parentID)



class Category(models.Model):
        businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
        campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
        settings_name = models.CharField(max_length=50)
        category_name = models.CharField(max_length=50)

        def __str__(self):
            return self.category_name
        class Meta:
           indexes = [ 
             models.Index(fields=["settings_name",]),
           ]




class Level(models.Model):
        businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
        campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
        categoryID = models.ForeignKey(Category, on_delete = models.CASCADE)
        settings_name = models.CharField(max_length=50,)
        level_name = models.CharField(max_length=50)

        def __str__(self):
            return self.level_name
        
        class Meta:
           indexes = [ 
             models.Index(fields=["settings_name",]),
           ]


class Class(models.Model):
        businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
        campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
        categoryID = models.ForeignKey(Category, on_delete = models.CASCADE)
        levelID = models.ForeignKey(Level, on_delete = models.CASCADE)
        settings_name = models.CharField(max_length=50,)
        class_name = models.CharField(max_length=50)

        def __str__(self):
            return self.class_name
        
        class Meta:
           indexes = [ 
             models.Index(fields=["settings_name",]),
           ]





class Stream(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    settings_name = models.CharField(max_length=50)
    stream_name = models.CharField(max_length=50)

    def __str__(self):
        return  self.stream_name

    class Meta:
       indexes = [ 
         models.Index(fields=["settings_name",]),            
       ]




class Department(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    department_name = models.CharField(max_length = 80)
    module_settings = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.department_name
    class Meta:
       indexes = [ 
         models.Index(fields=["department_name",]),
         models.Index(fields=["module_settings",]),
       ]






class Position(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    settings_name = models.CharField(max_length = 80, null=True, blank=True)
    position_name = models.CharField(max_length=80, null=True, blank=True)
    mandatory = models.BooleanField(default=False, null=True, blank=True)
  
    def __str__(self):
        return self.position_name
    class Meta:
       indexes = [ 
         models.Index(fields=["settings_name",]),
       ]



class SystemRoles(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    role_name = models.CharField(max_length=80)
    module_settings = models.CharField(max_length=50, null=True, blank=True)
    user_friendly_name = models.CharField(max_length=100)
    deleted = models.BooleanField(default=False, null=True, blank=True)


    def __str__(self):
        return self.user_friendly_name
    
    class Meta:
       indexes = [ 
         models.Index(fields=["role_name",]),
         models.Index(fields=["module_settings",]),
         models.Index(fields=["deleted",]),
       ]




class Rights(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    settings_name = models.CharField(max_length = 50, null=True, blank=True,)
    right_name = models.CharField(max_length = 80, null=True, blank=True)
    description = models.CharField(max_length = 120, null=True, blank=True)
    mandatory = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.right_name

    class Meta:
       indexes = [ 
         models.Index(fields=["settings_name",]),
         models.Index(fields=["mandatory",]),
       ]





class RoleRights(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    roleID = models.ForeignKey(SystemRoles, on_delete=models.CASCADE)
    rightID = models.ForeignKey(Rights, on_delete=models.CASCADE)
    mandatory = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
      return str(self.rightID)
         
    class Meta:
       indexes = [ 
         models.Index(fields=["mandatory",]),
       ]




class EmployeeType(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    employee_type_name = models.CharField(max_length=80)
    user_friendly_name = models.CharField(max_length=100)
    class Meta:
       indexes = [ 
         models.Index(fields=["employee_type_name",]),
       ]





class Employee(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    firstname = models.CharField(max_length = 80, default="")
    surname = models.CharField(max_length=80, default="")
    othername = models.CharField(max_length=80, default="", null=True, blank=True)
    employee_image = models.ImageField(null=True, blank=True, upload_to="employees")
    gender = models.CharField(max_length=7, choices = GENDER_CHOICES)
    date_of_birth = models.DateField()
    NIN = models.CharField(max_length=40, default="")
    employee_typeID = models.ForeignKey(EmployeeType, on_delete = models.CASCADE, null=True, blank=True)
    positionID  = models.ForeignKey(Position, on_delete = models.CASCADE, null=True, blank=True)
    system_roleID = models.ForeignKey(SystemRoles, on_delete = models.CASCADE, null=True, blank=True)
    is_system_user = models.BooleanField(default=False, null=True, blank=True)
    deleted = models.BooleanField(default=False, null=True, blank=True)
    date_of_hire = models.DateField(null=True, blank=True)
    employee_title = models.CharField(max_length=80, null=True, blank=True, default="")
    qualifications = models.CharField(max_length=80, null=True, blank=True, default="")
    academic_documents_upload = models.FileField(upload_to ="emp_docs", blank=True, default="")
    NSSF_NO = models.CharField(max_length=80, null=True, blank=True, default="")

    phone_contacts = models.CharField(max_length=50, null=True, blank=True, default="")
    email_address = models.CharField(max_length=50, null=True, blank=True, default="")
    address = models.CharField(max_length=40, null=True, blank=True, default="")
    bank_name = models.CharField(max_length=80, null=True, blank=True, default="")
    bank_account_no = models.CharField(max_length=40, null=True, blank=True, default="")

    net_salary = models.FloatField(default=0, null=True, blank=True)
    nssf =   models.FloatField(default=0, null=True, blank=True)
    PAYE =   models.FloatField(default=0, null=True, blank=True)
    userID = models.ForeignKey(User, on_delete = models.CASCADE, null=True, blank=True)

    next_of_kin_names = models.CharField(max_length=50, null=True, blank=True, default="")
    next_of_kin_contacts = models.CharField(max_length=50, null=True, blank=True, default="")
    next_of_kin_address = models.CharField(max_length=40, null=True, blank=True, default="")
    
    def __str__(self):
      return str(self.surname)+" "+ str(self.firstname)+" "+ str(self.othername)
       
    class Meta:
       indexes = [ 
         models.Index(fields=["is_system_user",]),
         models.Index(fields=["NIN",]),
         models.Index(fields=["NSSF_NO",]),
         models.Index(fields=["deleted",]),
       ]




class YearClass(models.Model):
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    categoryID = models.ForeignKey(Category, on_delete = models.CASCADE)
    classID = models.ForeignKey(Class, on_delete = models.CASCADE)
    levelID = models.ForeignKey(Level, on_delete = models.CASCADE)
    streamID = models.ForeignKey(Stream, on_delete = models.CASCADE)
    studentID = models.ForeignKey(Student, on_delete = models.CASCADE)
    year = models.IntegerField()
    class_name = models.CharField(max_length =40)# capturing class name e.g p.1, p.2, s.3
    year_class = models.CharField(max_length = 40) #e.g 2024-S.2
    stream_name  = models.CharField(max_length = 40)
    student_number = models.CharField(max_length = 40)
    student_name = models.CharField(max_length = 80)

    def save(self, *args,**kwargs):
        self.year_class = str(self.year)+"-"+self.class_name #e.g 2024-S.3
        super(YearClass, self).save(*args, **kwargs)

    class Meta:
       indexes = [ 
         models.Index(fields=["year_class",]), 
         models.Index(fields=["student_name",]),
         models.Index(fields=["stream_name",]),            
       ]




class Term(models.Model):
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    term_name = models.CharField(max_length=40)




class YearClassTerm(models.Model):
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    categoryID = models.ForeignKey(Category, on_delete = models.CASCADE)
    classID = models.ForeignKey(Class, on_delete = models.CASCADE)
    levelID = models.ForeignKey(Level, on_delete = models.CASCADE)
    streamID = models.ForeignKey(Stream, on_delete = models.CASCADE)
    student_typeID = models.ForeignKey(StudentType, on_delete = models.CASCADE, null=True, blank=True)
    studentID = models.ForeignKey(Student, on_delete = models.CASCADE)
    year_classID= models.ForeignKey(YearClass, on_delete = models.CASCADE, null=True, blank=True)
    year = models.IntegerField()
    class_name = models.CharField(max_length =40)# capturing class name e.g p.1, p.2, s.3
    term_name  = models.CharField(max_length =40)
    year_class = models.CharField(max_length = 40, null=True, blank=True) #e.g 2024-S.2
    year_class_term = models.CharField(max_length = 40) #e.g 2024-S.2
    stream_name  = models.CharField(max_length = 40)
    student_number = models.CharField(max_length = 40)
    student_name = models.CharField(max_length = 80)
    fees = models.FloatField()
    original_fees = models.FloatField(default=0, null=True, blank=True)
    amount_paid  = models.FloatField(default=0, null=True, blank=True)
    balance  = models.FloatField(default=0, null=True, blank=True)


    def save(self, *args,**kwargs):
        self.year_class = str(self.year)+"-"+self.class_name #e.g 2024-S.3
        self.year_class_term = str(self.year)+"-"+str(self.class_name)+"-"+str(self.term_name) #e.g 2024-S.3
        super(YearClassTerm, self).save(*args, **kwargs)

    class Meta:
       indexes = [ 
         models.Index(fields=["year_class",]), 
         models.Index(fields=["year_class_term",]), 
         models.Index(fields=["student_name",]),
         models.Index(fields=["stream_name",]),
         models.Index(fields=["term_name",]),
         models.Index(fields=["balance",]),            
       ]




class ItemType(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    item_type_name = models.CharField(max_length =80,)
    settings_name = models.CharField(max_length =80, null=True, blank=True)
    is_income = models.BooleanField()
    
    class Meta:
       indexes = [ 
         models.Index(fields=["is_income",]),
         models.Index(fields=["settings_name",]),
         ]
    def __str__(self):
        return self.item_type_name

    class Meta:
           indexes = [ 
             models.Index(fields=["item_type_name",]),
           ]


class ItemCategory(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    settings_name= models.CharField(max_length =80,  null=True, blank=True)
    category_name = models.CharField(max_length =80, null=True, blank=True)

    def __str__(self):
        return self.category_name
    
    class Meta:
           indexes = [ 
             models.Index(fields=["settings_name",]),
             models.Index(fields=["category_name",]),
           ]




class Item(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    item_typeID = models.ForeignKey(ItemType, on_delete = models.CASCADE)
    item_categoryID = models.ForeignKey(ItemCategory, on_delete = models.CASCADE, null=True, blank=True)
    item_name = models.CharField(max_length =80,)
    unit_cost = models.FloatField(default=0, null=True, blank=True)
    unit_price = models.FloatField(default=0, null=True, blank=True)
    unit_measure = models.CharField(max_length=20, default="", null=True, blank=True)
    is_income = models.BooleanField()
    is_school_fees = models.BooleanField(default=False, null=True, blank=True)
    is_monetary = models.BooleanField(default=False, null=True, blank=True)
    is_requirement = models.BooleanField(default=False, null=True, blank=True)
    #is_monetary = 
    
     
    class Meta:
       indexes = [ 
         models.Index(fields=["is_income",]),
         models.Index(fields=["item_name",]),
         models.Index(fields=["is_monetary",]),
         models.Index(fields=["is_school_fees",]),
         models.Index(fields=["is_requirement",]),
         ]
    
    def __str__(self):
        return str(self.item_typeID) +" "+str(self.item_name)




class Requirements(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    categoryID = models.ForeignKey(Category, on_delete = models.CASCADE)
    itemID =  models.ForeignKey(Item, on_delete = models.CASCADE, null=True, blank=True)
    student_typeID = models.ForeignKey(StudentType, on_delete=models.CASCADE, null=True, blank=True)
    classID = models.ForeignKey(Class, on_delete = models.CASCADE)
    levelID = models.ForeignKey(Level, on_delete = models.CASCADE)
    class_name =  models.CharField(max_length = 40)
    gender = models.CharField(max_length=10, default="Both", choices = (("Both", "Required For Both"),("M",'Male'), ("F",'Female')))
    item_name = models.CharField(max_length=80)
    unit_measure = models.CharField(max_length=40, null=True, blank=True)
    quantity_required = models.FloatField(default=0, null=True, blank = True)
    amount_required = models.FloatField(default=0, null=True, blank = True)
    is_monetary = models.BooleanField(default=False, blank=True, null=True)
    is_school_fees = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.item_name
        
    class Meta:
       indexes = [ 
         models.Index(fields=["is_monetary",]),
         models.Index(fields=["is_school_fees",]),
         models.Index(fields=["gender",]),
         ]




class ClassTermRequirements(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    categoryID = models.ForeignKey(Category, on_delete = models.CASCADE)
    classID = models.ForeignKey(Class, on_delete = models.CASCADE)
    levelID = models.ForeignKey(Level, on_delete = models.CASCADE)
    streamID = models.ForeignKey(Stream, on_delete = models.CASCADE)
    class_name =  models.CharField(max_length = 40)
    year_class = models.CharField(max_length = 40)
    year_class_term = models.CharField(max_length = 40,)
    item_name = models.CharField(max_length=80)
    unit_measure = models.CharField(max_length=40, null=True, blank=True)
    quantity_required = models.FloatField(default=0, null=True, blank = True)
    amount_required = models.FloatField(default=0, null=True, blank = True)
    is_monetary = models.BooleanField()

    def __str__(self):
        return self.item_name
    
    class Meta:
       indexes = [ 
         models.Index(fields=["is_monetary",]),
         models.Index(fields=["item_name",]),
         models.Index(fields=["year_class_term",]),
         ]




class StudentRequirementsPerTerm(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    categoryID = models.ForeignKey(Category, on_delete = models.CASCADE)
    classID = models.ForeignKey(Class, on_delete = models.CASCADE)
    levelID = models.ForeignKey(Level, on_delete = models.CASCADE)
    streamID = models.ForeignKey(Stream, on_delete = models.CASCADE)
    yearclassID = models.ForeignKey(YearClass, on_delete = models.CASCADE, null=True, blank=True)
    yearclass_termID = models.ForeignKey(YearClassTerm, on_delete = models.CASCADE,  null=True, blank=True)
    class_name =  models.CharField(max_length = 40)
    stream_name =  models.CharField(max_length = 40)
    year_class = models.CharField(max_length = 40)
    year_class_term = models.CharField(max_length = 40)
    studentID = models.ForeignKey(Student, on_delete = models.CASCADE)
    student_name = models.CharField(max_length=80) #index
    itemID = models.ForeignKey(Item, on_delete = models.CASCADE)
    item_name = models.CharField(max_length=80)
    is_monetary = models.BooleanField(default=False, blank=True, null=True)
    is_school_fees = models.BooleanField(default=False, blank=True, null=True)
    unit_measure = models.CharField(max_length=40, null=True, blank=True)
    quantity_required = models.FloatField(default=0, null=True, blank = True)
    amount_required = models.FloatField(default=0, null=True, blank = True)
    balance = models.FloatField(default=0, null=True, blank = True)
    userID = models.ForeignKey(User, on_delete = models.CASCADE)
    user_fullname = models.CharField(max_length=80)
    record_date = models.DateTimeField(auto_now_add = True)
    refund_bg_color = models.CharField(max_length=20, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return str(self.record_date)+": "+self.student_name+ " "+self.item_name 
    
    class Meta:
       indexes = [ 
         models.Index(fields=["is_monetary",]),
         models.Index(fields=["is_school_fees",]),
         models.Index(fields=["record_date",]),
         models.Index(fields=["student_name",]),
         models.Index(fields=["is_deleted",]),
         models.Index(fields=["year_class_term",]),
         models.Index(fields=["stream_name",]),
         models.Index(fields=["balance",]),
         ]




class StudentRequirementsPerTermBrought(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    categoryID = models.ForeignKey(Category, on_delete = models.CASCADE)
    classID = models.ForeignKey(Class, on_delete = models.CASCADE)
    rqt_requiredID = models.ForeignKey(StudentRequirementsPerTerm, on_delete = models.CASCADE, null=True, blank=True)
    levelID = models.ForeignKey(Level, on_delete = models.CASCADE)
    streamID = models.ForeignKey(Stream, on_delete = models.CASCADE)
    yearclassID = models.ForeignKey(YearClass, on_delete = models.CASCADE, null=True, blank=True)
    yearclass_termID = models.ForeignKey(YearClassTerm, on_delete = models.CASCADE,  null=True, blank=True)
    class_name =  models.CharField(max_length = 40)
    stream_name =  models.CharField(max_length = 40)
    year_class = models.CharField(max_length = 40)
    year_class_term = models.CharField(max_length = 45)
    studentID = models.ForeignKey(Student, on_delete = models.CASCADE)
    student_name = models.CharField(max_length=80) #index
    itemID = models.ForeignKey(Item, on_delete = models.CASCADE)
    item_name = models.CharField(max_length=80)
    is_monetary = models.BooleanField()
    is_school_fees = models.BooleanField(default=False, blank=True, null=True)
    quantity_brought = models.FloatField(default=0, null=True, blank = True)
    amount_brought = models.FloatField(default=0, null=True, blank = True)
    userID = models.ForeignKey(User, on_delete = models.CASCADE)
    user_fullname = models.CharField(max_length=80)
    record_date = models.DateTimeField(auto_now_add = True)
    is_deleted = models.BooleanField(default=False)
    refund_bg_color = models.CharField(max_length=10, null=True, blank=True)
    

    def __str__(self):
        return str(self.record_date)+": "+self.student_name+ " "+self.item_name
    
    class Meta:
       indexes = [ 
         models.Index(fields=["is_monetary",]),
         models.Index(fields=["record_date",]),
         models.Index(fields=["student_name",]),
         models.Index(fields=["is_deleted",]),
         models.Index(fields=["year_class_term",]),
         models.Index(fields=["stream_name",]),
         models.Index(fields=["is_school_fees",]),
         ]




class ItemBroughtBack(models.Model):
    rqt_broughtID = models.ForeignKey(StudentRequirementsPerTermBrought, on_delete = models.CASCADE,  null=True, blank=True)
    item_name = models.CharField(max_length=80, null=True, blank=True)
    amount_brought = models.FloatField(default=0, null=True, blank = True)
    reason = models.CharField(max_length=80, null=True, blank=True)
    userID = models.ForeignKey(User, on_delete = models.CASCADE)
    user_fullname = models.CharField(max_length=80)
    record_date = models.DateTimeField(auto_now_add = True)
    


  
class PaymentMethod(models.Model):
    settings_name = models.CharField(max_length=20,)
    pay_method_name = models.CharField(max_length=20)
    class Meta:
       indexes = [ 
         models.Index(fields=["settings_name",]),
       ]
    def __str__(self):
      return self.pay_method_name




class MoneySource(models.Model):
    settings_name = models.CharField(max_length=20,)
    money_source_name = models.CharField(max_length=20)

    def __str__(self):
      return self.money_source_name




class CashBook(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    categoryID = models.ForeignKey(Category, on_delete = models.CASCADE, null=True, blank=True)
    classID = models.ForeignKey(Class, on_delete = models.CASCADE, null=True, blank=True)
    money_sourceID = models.ForeignKey(MoneySource, on_delete = models.CASCADE, null=True, blank=True)
    paid_employeeID = models.ForeignKey(Employee, on_delete = models.CASCADE, null=True, blank=True)
    pay_methodID = models.ForeignKey(PaymentMethod, on_delete = models.CASCADE, null=True, blank=True)
    levelID = models.ForeignKey(Level, on_delete = models.CASCADE, null=True, blank=True)
    streamID = models.ForeignKey(Stream, on_delete = models.CASCADE, null=True, blank=True)
    yearclassID = models.ForeignKey(YearClass, on_delete = models.CASCADE, null=True, blank=True)
    yearclass_termID = models.ForeignKey(YearClassTerm, on_delete = models.CASCADE,  null=True, blank=True)
    rqt_broughtID = models.ForeignKey(StudentRequirementsPerTermBrought, on_delete = models.CASCADE,  null=True, blank=True)
    class_name =  models.CharField(max_length = 40, null=True, blank=True)
    stream_name =  models.CharField(max_length = 40, null=True, blank=True)
    year_class = models.CharField(max_length = 40, null=True, blank=True)
    year_class_term = models.CharField(max_length = 40, null=True, blank=True)
    studentID = models.ForeignKey(Student, on_delete = models.CASCADE, null=True, blank=True)
    student_name = models.CharField(max_length=80, default="", null=True, blank=True) #index
    particulars = models.CharField(max_length=80, default="", null=True, blank=True) #index
    itemID = models.ForeignKey(Item, on_delete = models.CASCADE, null=True, blank=True)
    item_name = models.CharField(max_length=80, null=True, blank=True)
    payID_NO = models.CharField(max_length = 40, null=True, blank=True)
    is_school_fees = models.BooleanField(default =True, null=True, blank=True)
    is_income = models.BooleanField(default=True, null=True, blank=True)
    unit_cost = models.FloatField(default=0, null=True, blank=True)
    unit_price = models.FloatField(default=0, null=True, blank=True)

    quantity = models.FloatField(default=0, null=True, blank=True) #2.5
    income_received = models.FloatField(default=0, null=True, blank=True)
    expense_made = models.FloatField(default=0, null=True, blank=True)
    net = models.FloatField(default=0, null=True, blank=True)

    approved = models.BooleanField(default=False, null=True, blank=True)

    userID = models.ForeignKey(User, on_delete = models.CASCADE, null=True, blank=True)
    user_fullname = models.CharField(max_length=80, null=True, blank=True)
    record_date = models.DateTimeField(auto_now_add = True, null=True, blank=True)
    refund_date = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False, null=True, blank=True)
    refund_bg_color = models.CharField(max_length=10, null=True, blank=True)
    running_total = models.FloatField(default=0, null=True, blank=True)


    def __str__(self):
        return str(self.record_date)+": "
        +str(self.item_name)+": Quantity: "+str(self.quantity)
        +" Income Received: "+str(self.income_received)
        +" Expense Made: "+str(self.expense_made)

    
    class Meta:
       indexes = [ 
         models.Index(fields=["is_income",]),
         models.Index(fields=["is_school_fees",]),
         models.Index(fields=["record_date",]),
         models.Index(fields=["refund_date",]),
         models.Index(fields=["is_deleted",]),
         models.Index(fields=["year_class",]),
         models.Index(fields=["year_class_term",]),
         models.Index(fields=["stream_name",]),
         ]




class RefundedItens(models.Model):
    rqt_broughtID = models.ForeignKey(StudentRequirementsPerTermBrought, on_delete = models.CASCADE,  null=True, blank=True)
    cashbookID = models.ForeignKey(CashBook, on_delete = models.CASCADE,  null=True, blank=True)
    item_name = models.CharField(max_length=80, null=True, blank=True)
    amount_refunded = models.FloatField(default=0, null=True, blank = True)
    reason = models.CharField(max_length=80, null=True, blank=True)
    userID = models.ForeignKey(User, on_delete = models.CASCADE)
    user_fullname = models.CharField(max_length=80)
    record_date = models.DateTimeField(auto_now_add = True)





class Subject(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    levelID = models.ForeignKey(Level, on_delete = models.CASCADE, null=True, blank=True)
    subject_name = models.CharField(max_length=80, null=True, blank=True)
    deleted = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
      return self.subject_name


class Paper(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    subjectID = models.ForeignKey(Subject, on_delete = models.CASCADE, null=True, blank=True)
    subject_name = models.CharField(max_length=80, null=True, blank=True)
    paper_name = models.CharField(max_length=80, null=True, blank=True)
    deleted = models.BooleanField(default=False, null=True, blank=True)
    
    def __str__(self):
      return self.paper_name




class ScoreDescription(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    lower_mark = models.FloatField(null=True, blank=True, default=0)
    upper_mark = models.FloatField(null=True, blank=True, default=0)
    identifier = models.IntegerField(null=True, blank=True)
    identifier = models.IntegerField(null=True, blank=True)

    

class GradeSettings(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    grade_name = models.CharField(max_length=50, null=True, blank=True)



class DivisionSettings(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    levelID = models.ForeignKey(Level, on_delete = models.CASCADE, null=True, blank=True)
    division_name = models.CharField(max_length=50, null=True, blank=True)

class ReportCardType(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    levelID = models.ForeignKey(Level, on_delete = models.CASCADE, null=True, blank=True)
    report_card_type_name = models.CharField(max_length=50, null=True, blank=True)

class Grading(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    levelID = models.ForeignKey(Level, on_delete = models.CASCADE, null=True, blank=True)
    subjectID = models.ForeignKey(Subject, on_delete = models.CASCADE, null=True, blank=True)
    subject_name = models.CharField(max_length=80, null=True, blank=True)
    lower_figure = models.FloatField(default=0, null=True, blank=True)
    upper_figure = models.FloatField(default=0, null=True, blank=True)
    grade_name = models.CharField(max_length=50, null=True, blank=True)
    gradeID = models.ForeignKey(GradeSettings, on_delete = models.CASCADE, null=True, blank=True)
    points = models.FloatField(default=0, null=True, blank=True)
    general_remarks = models.CharField(max_length=80, null=True, blank=True)

    class Meta:
       indexes = [ 
         models.Index(fields=["lower_figure",]),
         models.Index(fields=["upper_figure",]),
         ]




class PaperComments(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    levelID = models.ForeignKey(Level, on_delete = models.CASCADE, null=True, blank=True)
    subjectID = models.ForeignKey(Subject, on_delete = models.CASCADE, null=True, blank=True)
    employeeID = models.ForeignKey(Employee, on_delete = models.CASCADE, null=True, blank=True)
    gradeID = models.ForeignKey(Grading, on_delete = models.CASCADE, null=True, blank=True)
    grade_name_and_marks_range = models.CharField(max_length=70, null=True, blank=True)
    subject_name = models.CharField(max_length=80, null=True, blank=True) 
    remarks = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
      return str(self.employeeID) +" " + sstr(elf.subject_name)



class GeneralSettings(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    lower_figure = models.FloatField(default=0, null=True, blank=True)
    upper_figure = models.FloatField(default=0, null=True, blank=True)
    settings_name = models.CharField(max_length=50, null=True, blank=True)
    user_friendly_name = models.CharField(max_length=80, null=True, blank=True)
    settings_value = models.CharField(max_length=120, null=True, blank=True)
    class Meta:
       indexes = [ 
         models.Index(fields=["settings_name",]),
         models.Index(fields=["lower_figure",]),
         models.Index(fields=["upper_figure",]),
         ]


class ReportCardMarksLabels(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    levelID = models.ForeignKey(Level, on_delete = models.CASCADE, null=True, blank=True)
    mark1 = models.CharField(max_length=40, null=True, blank=True)
    mark2 = models.CharField(max_length=40, null=True, blank=True)
    mark3 = models.CharField(max_length=40, null=True, blank=True)
    mark4 = models.CharField(max_length=40, null=True, blank=True)
    mark5 = models.CharField(max_length=40, null=True, blank=True)
    mark6 = models.CharField(max_length=40, null=True, blank=True)
    final_mark = models.CharField(max_length=40, null=True, blank=True)

    class Meta:
       indexes = [ 
         models.Index(fields=["mark1",]),
         models.Index(fields=["mark2",]),
         models.Index(fields=["mark3",]),
         models.Index(fields=["mark4",]),
         models.Index(fields=["mark5",]),
         models.Index(fields=["mark6",]),
         models.Index(fields=["final_mark",]),
         ]



class Division(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    levelID = models.ForeignKey(Level, on_delete = models.CASCADE, null=True, blank=True)
    lower_figure = models.FloatField(default=0, null=True, blank=True)
    upper_figure = models.FloatField(default=0, null=True, blank=True)
    division_settingsID = models.ForeignKey(DivisionSettings, on_delete = models.CASCADE, null=True, blank=True)
    division_name = models.CharField(max_length=20, null=True, blank=True)
    gereral_remarks = models.CharField(max_length=80, null=True, blank=True)


    def __str__(self):
      return self.division_name





class GeneralReportCardRemarks(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    levelID = models.ForeignKey(Level, on_delete = models.CASCADE, null=True, blank=True)
    divisionID = models.ForeignKey(Division, on_delete = models.CASCADE, null=True, blank=True)
    division_name_and_range= models.CharField(max_length=60, null=True, blank=True)
    remarks = models.CharField(max_length=120, null=True, blank=True)


    

class PaperTeacherClass(models.Model):
  #assins a subject in a certain class to a teacher
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    levelID = models.ForeignKey(Level, on_delete = models.CASCADE, null=True, blank=True)
    paperID = models.ForeignKey(Paper, on_delete = models.CASCADE, null=True, blank=True)
    employeeID = models.ForeignKey(Employee, on_delete = models.CASCADE, null=True, blank=True)
    classID = models.ForeignKey(Class, on_delete = models.CASCADE, null=True, blank=True)
    class_name = models.CharField(max_length=30, null=True, blank=True)
    paper_name = models.CharField(max_length=80, null=True, blank=True)
    lower_figure = models.FloatField(default=0, null=True, blank=True)
    deleted = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
       indexes = [ 
         models.Index(fields=["deleted",]),
         ]




class SubjectDone(models.Model):
  #assins a subject in a certain class to a teacher
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    levelID = models.ForeignKey(Level, on_delete = models.CASCADE, null=True, blank=True)

    classID = models.ForeignKey(Class, on_delete = models.CASCADE, null=True, blank=True)
    class_name = models.CharField(max_length=30, null=True, blank=True)
    year_class= models.CharField(max_length=30, null=True, blank=True)
    termID = models.ForeignKey(Term, on_delete = models.CASCADE, null=True, blank=True)
    year_class_term = models.CharField(max_length=30, null=True, blank=True)

    subjectID = models.ForeignKey(Subject, on_delete = models.CASCADE, null=True, blank=True)
    subject_name = models.CharField(max_length=80, null=True, blank=True)

    mark1 = models.FloatField(default=0, null=True, blank=True)
    mark2 = models.FloatField(default=0, null=True, blank=True)
    mark3 = models.FloatField(default=0, null=True, blank=True)
    mark4 = models.FloatField(default=0, null=True, blank=True)
    mark5 = models.FloatField(default=0, null=True, blank=True)
    mark6 = models.FloatField(default=0, null=True, blank=True)
    final_mark = models.FloatField(default=0, null=True, blank=True)
    
    points = models.FloatField(default=0, null=True, blank=True)
    grade_name = models.CharField(max_length=50, null=True, blank=True)

    teacherID = models.ForeignKey(Employee, on_delete = models.CASCADE, null=True, blank=True)
    teacher_name = models.CharField(max_length=80, null=True, blank=True)

    userID = models.ForeignKey(User, on_delete = models.CASCADE, null=True, blank=True)
    user_fullname = models.CharField(max_length=80, null=True, blank=True)
    record_date = models.DateTimeField(auto_now_add = True, null=True, blank=True)

    class Meta:
       indexes = [ 
         models.Index(fields=["record_date",]),
         ]




class PaperDone(models.Model):
  #assins a subject in a certain class to a teacher
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    campusID = models.ForeignKey(Campus, on_delete = models.CASCADE, null=True, blank=True)
    levelID = models.ForeignKey(Level, on_delete = models.CASCADE, null=True, blank=True)

    classID = models.ForeignKey(Class, on_delete = models.CASCADE, null=True, blank=True)
    class_name = models.CharField(max_length=30, null=True, blank=True)
    year_class= models.CharField(max_length=30, null=True, blank=True)
    termID = models.ForeignKey(Term, on_delete = models.CASCADE, null=True, blank=True)
    year_class_term = models.CharField(max_length=30, null=True, blank=True)


    subject_doneID = models.ForeignKey(SubjectDone, on_delete = models.CASCADE, null=True, blank=True)
    subjectID = models.ForeignKey(Subject, on_delete = models.CASCADE, null=True, blank=True)
    subject_name = models.CharField(max_length=80, null=True, blank=True)
    paperID = models.ForeignKey(Paper, on_delete = models.CASCADE, null=True, blank=True)
    paper_name = models.CharField(max_length=80, null=True, blank=True)

    mark1 = models.FloatField(default=0, null=True, blank=True)
    mark2 = models.FloatField(default=0, null=True, blank=True)
    mark3 = models.FloatField(default=0, null=True, blank=True)
    mark4 = models.FloatField(default=0, null=True, blank=True)
    mark5 = models.FloatField(default=0, null=True, blank=True)
    mark6 = models.FloatField(default=0, null=True, blank=True)
    final_mark = models.FloatField(default=0, null=True, blank=True)
    
    points = models.FloatField(default=0, null=True, blank=True)
    grade_name = models.CharField(max_length=50, null=True, blank=True)

    teacherID = models.ForeignKey(Employee, on_delete = models.CASCADE, null=True, blank=True)
    teacher_name = models.CharField(max_length=80, null=True, blank=True)

    userID = models.ForeignKey(User, on_delete = models.CASCADE, null=True, blank=True)
    user_fullname = models.CharField(max_length=80, null=True, blank=True)
    record_date = models.DateTimeField(auto_now_add = True, null=True, blank=True)

    class Meta:
       indexes = [ 
         models.Index(fields=["record_date",]),
         ]