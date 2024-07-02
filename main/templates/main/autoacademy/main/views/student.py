
from django.shortcuts import render, redirect
from django.contrib import messages
from main.models import Parent, Student, Employee, StudentParent, StudentType, \
                        Class, Stream, Term, Requirements, StudentRequirementsPerTerm, CashBook, Level, \
                        YearClass, YearClassTerm
from django.db.models import Q
from datetime import datetime, timedelta
from . global_views import GlobalViews
from .requirements_per_term import RequirementsPerTermActions
from . year_class_views import YearClassViews
from  . year_class_term_views import YearClassTermViews


GLOBAL_VARIABLES = GlobalViews()


class StudentViews:

    def add_student(request):

        #check if user is logged in or redirect to login page 
        if request.user.is_authenticated:
            pass
        else:
            return redirect("index")
        
        #redirecting not logged in users to loging page
        GLOBAL_VARIABLES.redirect_not_logged_in_user(request)

        current_employee= GLOBAL_VARIABLES.get_current_employee_info(request)
        STUDENT_TYPES = StudentType.objects.filter(campusID = current_employee.campusID)
        ALL_CLASSES = Class.objects.filter(campusID = current_employee.campusID)
        ALL_STREAMS = Stream.objects.filter(campusID = current_employee.campusID)
        ALL_TERMS =   Term.objects.filter(campusID = current_employee.campusID)


        if request.POST.get("status")=="NA":
          messages.warning(request, "Please choose correct status")
          return redirect("add-student")

        if request.POST.get("class")=="NA":
          messages.warning(request, "Please choose correct class")
          return redirect("add-student")

        if request.POST.get("tremID")=="NA":
          messages.warning(request, "Please choose correct class")
          return redirect("add-student")

        if request.POST.get("add-student"):
        #saving student class details
        #==========================================================================
        
            classID = Class.objects.get(settings_name = request.POST.get("class"), 
                                        campusID = current_employee.campusID)

            streamID = Stream.objects.get(settings_name = request.POST.get("strem-name"),
                                          campusID = current_employee.campusID,)

            student_typeID = StudentType.objects.get(
                                                 settings_name = request.POST.get("status"),
                                                 campusID = current_employee.campusID,
                                                 )

            termID = Term.objects.get(id = int(request.POST.get("termID")), 
                                      campusID = current_employee.campusID)

            current_requirements = Requirements.objects.filter(Q(
                                                              gender = "Both",
                                                              campusID = current_employee.campusID,
                                                              classID = classID,
                                                              student_typeID = student_typeID,
                                                              ) |
                                                              Q(
                                                              gender =  request.POST.get("gender"),
                                                              campusID = current_employee.campusID,
                                                              classID = classID,
                                                              student_typeID = student_typeID,
                                                              )
                                                              )  
            #check whether school fees has been set 
            # also pick fees vaule
            #=========================================================================
            try:                                                
              current_fees = Requirements.objects.get(
                                                        campusID = current_employee.campusID,
                                                        classID = classID,
                                                        student_typeID = student_typeID, 
                                                        is_school_fees = True, 
                                                        )  
            except:
               messages.warning(request, "Please set school fees for this class first")
               return redirect("add-student")



        #
        # Actual addding class
        # ==================================================================
        if request.POST.get("add-student"):  
           new_student = Student()
           new_student.surname = request.POST.get("surname").upper() 
           new_student.firstname = request.POST.get("firstname").upper() 
           new_student.othernames = request.POST.get("othernames").upper() 
           new_student.gender = request.POST.get("gender")
           new_student.student_NO = request.POST.get("student-no")

           if request.FILES.get("student-image"):
              new_student.student_image = request.FILES.get("student-image")

           #obtaining student type, i.e day or boarding
           student_type = StudentType.objects.get(
                                                 settings_name = request.POST.get("status"),
                                                 campusID = current_employee.campusID
                                                 )
           

           new_student.student_typeID = student_type
           new_student.date_of_birth = request.POST.get("dob")

           #obtaining current_user details and current user campua
           
           new_student.campusID = current_employee.campusID
           new_student.businessID = current_employee.businessID
           new_student.userID = request.user
           new_student.save()

           if True:
           #Saving Father
           #========================================================
              new_father = Parent()
              new_father.surname = request.POST.get("father-surname").upper() 
              new_father.firstname = request.POST.get("father-firstname").upper() 
              new_father.contacts = request.POST.get("father-contacts")
              new_father.save() 


              new_student_father = StudentParent()
              new_student_father.studentID = new_student
              new_student_father.parentID = new_father
              new_student_father.relation_to_student = "FATHER"
              new_student_father.save()

          
           if True:
             #Saving Mother
             #========================================================
              new_mother = Parent()
              new_mother.surname = request.POST.get("mother-surname").upper() 
              new_mother.firstname = request.POST.get("mother-firstname").upper() 
              new_mother.contacts = request.POST.get("mother-contacts")
              new_mother.save() 

              new_student_mother = StudentParent()
              new_student_mother.studentID = new_student
              new_student_mother.parentID = new_mother
              new_student_mother.relation_to_student = "MOTHER"
              new_student_mother.save()


           if True:
           #Saving Guardian
           #========================================================
              new_guardian = Parent()
              new_guardian.surname = request.POST.get("guardian-surname").upper() 
              new_guardian.firstname = request.POST.get("guardian-firstname").upper() 
              new_guardian.contacts = request.POST.get("guardian-contacts")
              new_guardian.save() 

              new_student_guardian = StudentParent()
              new_student_guardian.studentID = new_student
              new_student_guardian.parentID = new_guardian
              new_student_guardian.relation_to_student = "GUARDIAN"
              new_student_guardian.save()

          

           #get current year
           current_year = datetime.now().year 

          #below we add class and term for the student
          #===============================================================================
           new_year_class_obj = YearClassViews()
           new_year_class = new_year_class_obj.add_year_class(request, current_employee, 
                                 new_student, classID, streamID, current_year)

           new_year_class_term_obj = YearClassTermViews()
           new_year_class_term = new_year_class_term_obj.add_year_class_term(request, current_employee, 
                                 new_student, classID, new_year_class, streamID, termID, student_typeID, current_fees, current_year)
           
           #save balance into database
           #============================================================================
           update_std_term_details = UpdateOherStudentDetails()
           update_std_term_details.update_student_term_details(
                                                             new_student, 
                                                             new_year_class, 
                                                             termID, 
                                                             student_typeID,
                                                             streamID)


           #addding student requirments
           #=========================================================================
           for rqt in current_requirements:
              add_rqt = RequirementsPerTermActions()
              add_rqt.add_requiremt_to_student(request, current_employee, new_student, classID,
                                streamID, new_year_class, new_year_class_term, rqt, current_year)


           GLOBAL_VARIABLES.set_current_student(request, new_student)
           messages.info(request, "Success, record saved")
           return redirect("bursar-dashboard")
         
         #secirty
        return render(
                     request, 
                     template_name="main/add_student.html",
                     context ={
                       "STUDENT_TYPES":STUDENT_TYPES,
                       "ALL_CLASSES":ALL_CLASSES,
                       "ALL_STREAMS":ALL_STREAMS,
                       "ALL_TERMS":ALL_TERMS,
                     }
                     )




    def edit_student(request):

        if request.user.is_authenticated:
          pass
        else:
          return redirect("index")

        try:
          x = request.session["current_student_id"]
        except:
          messages.warning(request, "Please first load student into window")
          return redirect("index")

        #redirecting not logged in users to loging page
        GLOBAL_VARIABLES.redirect_not_logged_in_user(request)

        STUDENT_TYPES = None
        current_student = None
        date_of_birth = ""
        student_parents = None

        current_employee= GLOBAL_VARIABLES.get_current_employee_info(request)
        STUDENT_TYPES = StudentType.objects.all()
        ALL_CLASSES = Class.objects.all()

        
        #get current student details
        current_student = Student.objects.get(id = int(request.session["current_student_id"])) 

        if request.POST.get("surname"):
           current_student.surname = request.POST.get("surname").upper() 
           current_student.firstname = request.POST.get("firstname").upper() 
           current_student.othernames = request.POST.get("othernames").upper() 
           current_student.gender = request.POST.get("gender") 
           current_student.student_NO  = request.POST.get("student-no")

           #obtaining student type, i.e day or boarding
           student_type = StudentType.objects.get(settings_name = request.POST.get("status"), campusID = current_employee.campusID)

           current_student.student_typeID = student_type
           current_student.date_of_birth = request.POST.get("dob")

           #saving student image
           if request.FILES.get("student-image"):
              current_student.student_image = request.FILES.get("student-image")

           current_student.save()   

        #formating student date of birth to saveable date
        date_of_birth = str(current_student.date_of_birth).split(" ")[0]

        #getiing all the parents of this student
        student_parents = StudentParent.objects.filter(studentID = current_student)
        

        if request.POST.get("posted-parentID"):

          posted_parent_id = request.POST.get("posted-parentID")
          currnet_parent = Parent.objects.get(id = int(posted_parent_id))

          currnet_parent.surname = request.POST.get("parent-surname").upper() 
          currnet_parent.firstname = request.POST.get("parent-firstname").upper() 
          currnet_parent.contacts = request.POST.get("parent-contacts")
          
          currnet_parent.save()

                
        return render(
                     request, 
                     template_name="main/edit_student.html",
                     context ={
                       "STUDENT_TYPES":STUDENT_TYPES,
                       "current_student":current_student,
                       "date_of_birth": date_of_birth,
                       "student_parents":student_parents,
                     }
                     )



class UpdateOherStudentDetails:

   def update_student_term_details(self, student, year_class, termID, student_typeID, streamID):
        student.year_class = year_class.year_class 
        student.term_name =  termID.term_name
        student.stream_name = streamID.stream_name
        student.student_typeID = student_typeID
        student.save()
    