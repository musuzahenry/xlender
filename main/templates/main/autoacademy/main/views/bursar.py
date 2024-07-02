from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from main.models import Parent, Student, Employee, StudentParent, StudentType, YearClass, YearClassTerm, \
                         StudentRequirementsPerTerm, StudentRequirementsPerTermBrought, CashBook, Class, \
                        Term, Stream, Requirements, PaymentMethod, Item, MoneySource, RefundedItens
from datetime import datetime
from .global_views import GlobalViews
from .requirements_per_term import RequirementsPerTermActions
from . year_class_views import YearClassViews
from  . year_class_term_views import YearClassTermViews
from . student import UpdateOherStudentDetails
from . cashbook import CahBookActions



GLOBAL_VARIABLES = GlobalViews()


class BursarViews:
    
    def bursar_dashboard(request):


        #check if user is logged in or redirect to login page 
        if request.user.is_authenticated:
            pass
        else:
            return redirect("index")

        #initialise vairables
        #================================================================
        bursar_action = BursarActions()

        current_employee = GLOBAL_VARIABLES.get_current_employee_info(request)
    
        STUDENT_TYPES = StudentType.objects.filter(campusID = current_employee.campusID)
        ALL_CLASSES = Class.objects.filter(campusID = current_employee.campusID)
        ALL_STREAMS = Stream.objects.filter(campusID = current_employee.campusID)
        ALL_TERMS =   Term.objects.filter(campusID = current_employee.campusID)
        ALL_PAYMENT_METHODS = PaymentMethod.objects.all()

        current_student = None 

        try:
          #set current student
          #==================================================================
           current_student = Student.objects.get(id = int(request.session["current_student_id"]))
        except:
            pass

  

        current_student_classes = YearClass.objects.filter(studentID = current_student).order_by("-id")

        #current_class, current_year_class_terms, current_requirements_upnaid, current_items_brought

        try:
           current_class = YearClass.objects.get(id = int(request.session["current_year_classID"]))
        except:
            current_class = None
        try:
           current_year_term = YearClassTerm.objects.get(id = int(request.session["current_year_class_termID"]))
        except:
           current_year_term = None
        try:
           current_year_class_terms =  YearClassTerm.objects.filter(year_classID = current_class)
           
        except:
            pass 

        #obtain requirements for current class year term
        try:
           all_requirements = Item.objects.filter(
                                                campusID =  current_employee.campusID,
                                                is_requirement = True,
                                            ).order_by("item_name")
            
        except:
           all_requirements = None
           

        

        #
        # ===================================================================================
        # below are bursar actions
        #====================================================================================  

        if request.POST.get("del-rqtID"):
            bursar_action.bursar_del_rqt_unpaid(request, request.POST.get("del-rqtID"))
            return redirect("bursar-dashboard")

        if request.POST.get("del-broughtID"):
            #refund a requiremt
            rqt = StudentRequirementsPerTermBrought.objects.get(id =int(request.POST.get("del-broughtID")))
            reason = request.POST.get("reason")
            bursar_action.bursar_del_brought_requiremnts(request, current_employee, rqt, reason)
            return redirect("bursar-dashboard")

   
        if request.POST.get("add-class") and (current_student):
           #Adding new class
           #===============================================================================      
          bursar_action.bursar_add_year_class(request, current_employee, current_student)  
          return redirect("bursar-dashboard")           
        elif request.POST.get("add-class") and not (current_student):
            messages.warning(request, "Please first load student into window")
            return redirect("bursar-dashboard")
        else:
            pass


        if request.POST.get("add-term") and (current_student):
            #adding new term
            #============================================================================
            bursar_action.bursar_add_year_class_term(request, current_employee, current_student) 
            return redirect("bursar-dashboard")   

        elif request.POST.get("add-term") and not (current_student):
            messages.warning(request, "Please first load student into window")
            return redirect("bursar-dashboard")
        else:
            pass


        if request.POST.get("rqtID") and (current_year_term):
            if request.POST.get("rqtID") == "NA":
                messages.warning(request, "Please choose an item")
                return redirect("bursar-dashboard")
            bursar_action.bursar_add_add_requiremt_to_student(request, current_employee, current_student, 
                                                              current_year_term)
            return redirect("bursar-dashboard")

        elif request.POST.get("rqtID") and not (current_year_term):
            messages.warning(request, "Please first load student into window")
            return redirect("bursar-dashboard")
        else:
            pass




        #getting current term and requirements
        #=================================================================================================
        current_requirements_upnaid = StudentRequirementsPerTerm.objects.filter(
                                                                       yearclass_termID 
                                                                       = current_year_term
                                                                        )
        current_items_brought = StudentRequirementsPerTermBrought.objects.filter(
                                                                                #we use term not year since we are looking
                                                                                #at items brought per term
                                                                                 yearclass_termID = current_year_term  ,
                                                                                 is_deleted = False,
                                                                               ).order_by("-id")

        if request.POST.get("pay-rqt-id"):

            current_pay_rqt = StudentRequirementsPerTerm.objects.get(id = int(request.POST.get("pay-rqt-id")))

            if float(request.POST.get("amount-qty-recieived")) -  float(current_pay_rqt.balance) > 0:
                messages.warning(request, "Amount entered cannot be greater than balance")
            else:
                #add payment to requirements brought
                rqt_brought = StudentRequirementsPerTermBrought()
                rqt_brought.businessID = current_employee.businessID
                rqt_brought.campusID = current_employee.campusID
                rqt_brought.categoryID = current_pay_rqt.categoryID
                rqt_brought.classID = current_pay_rqt.classID
                rqt_brought.levelID = current_pay_rqt.levelID
                rqt_brought.rqt_requiredID = current_pay_rqt
                rqt_brought.streamID = current_pay_rqt.streamID
                rqt_brought.yearclassID = current_pay_rqt.yearclassID
                rqt_brought.yearclass_termID = current_year_term
                rqt_brought.class_name =  current_pay_rqt.class_name
                rqt_brought.stream_name =  current_year_term.term_name
                rqt_brought.year_class = current_pay_rqt.year_class
                rqt_brought.year_class_term = current_pay_rqt.year_class_term
                rqt_brought.studentID = current_pay_rqt.studentID
                rqt_brought.student_name = current_pay_rqt.student_name
                rqt_brought.is_school_fees = current_pay_rqt.is_school_fees
                rqt_brought.itemID = current_pay_rqt.itemID
                rqt_brought.item_name = current_pay_rqt.item_name
                rqt_brought.is_monetary = current_pay_rqt.is_monetary

                if  current_pay_rqt.is_monetary:
                    rqt_brought.amount_brought = float((request.POST.get("amount-qty-recieived")))
                else:
                     rqt_brought.quantity_brought = float((request.POST.get("amount-qty-recieived")))

                rqt_brought.userID = request.user
                rqt_brought.user_fullname = current_employee.surname+" "+current_employee.firstname+" "+current_employee.othername
                rqt_brought.save()

                
                if  current_pay_rqt.is_monetary:
                #saving to cashboo
                #==============================================================

                #obtaining paymeny details
                    pay_methodID = PaymentMethod.objects.get(settings_name = request.POST.get("paymethodID"))
                    pay_methodID_NO = request.POST.get("pay-number")
                    
                    if pay_methodID.settings_name == "bank_deposit" or pay_methodID.settings_name == "bank_transfer":
                        money_sourceID = MoneySource.objects.get(settings_name = "bank")
                    else:
                       money_sourceID = MoneySource.objects.get(settings_name = "cash")
                    
                    rqt_cashbook = CashBook()
                    rqt_cashbook.businessID = current_employee.businessID
                    rqt_cashbook.campusID = current_employee.campusID
                    rqt_cashbook.categoryID = rqt_brought.categoryID
                    rqt_cashbook.classID = rqt_brought.classID
                    rqt_cashbook.levelID = rqt_brought.levelID
                    rqt_cashbook.streamID = rqt_brought.streamID
                    rqt_cashbook.yearclassID = rqt_brought.yearclassID
                    rqt_cashbook.yearclass_termID = rqt_brought.yearclass_termID
                    rqt_cashbook.rqt_broughtID = rqt_brought
                    rqt_cashbook.pay_methodID = pay_methodID
                    rqt_cashbook.money_sourceID = money_sourceID
                    rqt_cashbook.payID_NO = pay_methodID_NO
                    rqt_cashbook.class_name =  rqt_brought.class_name
                    rqt_cashbook.stream_name =  rqt_brought.stream_name
                    rqt_cashbook.year_class = rqt_brought.year_class
                    rqt_cashbook.year_class_term = rqt_brought.year_class_term
                    rqt_cashbook.studentID = rqt_brought.studentID
                    #rqt_cashbook.student_name = rqt_brought.student_name
                    rqt_cashbook.particulars = rqt_brought.student_name
                    rqt_cashbook.itemID = rqt_brought.itemID
                    rqt_cashbook.item_name = rqt_brought.item_name
                    rqt_cashbook.is_school_fees = rqt_brought.is_school_fees
                    rqt_cashbook.is_income = True
                    rqt_cashbook.unit_cost = 0
                    rqt_cashbook.unit_price = 0

                    rqt_cashbook.quantity = 1
                    rqt_cashbook.income_received = rqt_brought.amount_brought
                    rqt_cashbook.expense_made = 0
                    rqt_cashbook.net = rqt_brought.amount_brought

                    rqt_cashbook.approved = True

                    rqt_cashbook.userID = request.user
                    rqt_cashbook.user_fullname = rqt_brought.user_fullname

                    rqt_cashbook.save()
                    GLOBAL_VARIABLES.running_total(request)

                     
                #updating balance
                #=======================================================================================================

                if current_pay_rqt.is_school_fees == True:
                    #updating school fees balance
                    current_pay_rqt.studentID.balance = float(current_pay_rqt.studentID.balance) - float(request.POST.get("amount-qty-recieived"))
                    current_pay_rqt.studentID.save()

                current_pay_rqt.balance = float(current_pay_rqt.balance) - float(request.POST.get("amount-qty-recieived"))
                current_pay_rqt.save()

                messages.info(request, "Success, record saved")
                return redirect("bursar-dashboard")




        return render(request, template_name = "main/bursar_dashboard.html",
                                context={
                                    "STUDENT_TYPES":STUDENT_TYPES,
                                    "current_student":current_student,
                                    "current_student_classes":current_student_classes,
                                    "current_year_class_terms":current_year_class_terms,
                                    "current_requirements":current_requirements_upnaid,
                                    "current_class":current_class,
                                    "current_year_term":current_year_term,
                                    "current_items_brought":current_items_brought,
                                    "STUDENT_TYPES":STUDENT_TYPES,
                                    "ALL_CLASSES":ALL_CLASSES,
                                    "ALL_STREAMS":ALL_STREAMS,
                                    "ALL_TERMS":ALL_TERMS,
                                    "ALL_PAYMENT_METHODS":ALL_PAYMENT_METHODS,
                                    "all_requirements":all_requirements,
                                })





class BursarActions:
    def bursar_add_year_class(self, request, current_employee, current_student):


           current_year = datetime.now().year  #get current year
           
           classID = Class.objects.get(
                                       settings_name = request.POST.get("class"), 
                                      campusID = current_employee.campusID,
                                      ) #getiing class e.h p.1
           streamID = Stream.objects.get(
                                         settings_name = request.POST.get("strem-name"),
                                         campusID = current_employee.campusID,
                                         )#getting stream e.g sharp
           
           student_typeID = StudentType.objects.get(                                     
                                            settings_name = request.POST.get("status"),
                                            campusID = current_employee.campusID,
                                            )#getting student type e.g boarding or day, that is, status

           termID = Term.objects.get(
                                    id = int(request.POST.get("termID")), 
                                    campusID = current_employee.campusID,
                                    )#getting term, e.g, term I
           
           current_fees = Requirements.objects.get(
                                                        campusID = current_employee.campusID,
                                                        classID = classID,
                                                        student_typeID = student_typeID, 
                                                        is_school_fees = True, 
                                                        )  



           new_year_class_obj = YearClassViews()
           new_year_class = new_year_class_obj.add_year_class(request, current_employee, 
                                 current_student, classID, streamID, current_year)

           new_year_class_term_obj = YearClassTermViews()
           new_year_class_term = new_year_class_term_obj.add_year_class_term(
                                 request, 
                                 current_employee, 
                                 current_student, classID, new_year_class, 
                                 streamID, termID, student_typeID,
                                 current_fees, current_year)
           
           #
           #update other student details
           #============================================================================
           update_std_term_details = UpdateOherStudentDetails()
           update_std_term_details.update_student_term_details(
                                                            current_student, 
                                                            new_year_class, 
                                                            termID, 
                                                            student_typeID,
                                                            streamID)

           
           #addding student requirments
           #=========================================================================
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
           for rqt in current_requirements:
              add_rqt = RequirementsPerTermActions()
              add_rqt.add_requiremt_to_student(request, current_employee, current_student, classID,
                                streamID, new_year_class, new_year_class_term, rqt, current_year)


           GLOBAL_VARIABLES.set_current_student(request, current_student)


    


    def bursar_add_year_class_term(self, request, current_employee, current_student):
           current_year = datetime.now().year  #get current year
           

           current_year_classID = YearClass.objects.get(id = int(request.session["current_year_classID"]))


           
           student_typeID = StudentType.objects.get(                                     
                                            settings_name = request.POST.get("status"),
                                            campusID = current_employee.campusID,
                                            )#getting student type e.g boarding or day, that is, status

           termID = Term.objects.get(
                                    id = int(request.POST.get("termID")), 
                                    campusID = current_employee.campusID,
                                    )#getting term, e.g, term I

           streamID = Stream.objects.get(
                                         settings_name = request.POST.get("strem-name"),
                                         campusID = current_employee.campusID,
                                         )#getting stream e.g sharp
           
           current_fees = Requirements.objects.get(
                                                        campusID = current_employee.campusID,
                                                        classID = current_year_classID.classID,
                                                        student_typeID = student_typeID, 
                                                        is_school_fees = True, 
                                                        )  

           new_year_class_term_obj = YearClassTermViews()
           new_year_class_term = new_year_class_term_obj.add_year_class_term(request, current_employee, 
                                 current_student, current_year_classID.classID, current_year_classID, 
                                 streamID, termID,student_typeID, current_fees, current_year)
           



           #
           #update other student details
           #============================================================================
           update_std_term_details = UpdateOherStudentDetails()
           update_std_term_details.update_student_term_details(
                                                            current_student, 
                                                            current_year_classID, 
                                                            termID, 
                                                            student_typeID,
                                                            streamID)

           #addding student requirments
           #=========================================================================
           current_requirements = Requirements.objects.filter(Q(
                                                              gender = "Both",
                                                              campusID = current_employee.campusID,
                                                              classID = current_year_classID.classID,
                                                              student_typeID = student_typeID,
                                                              ) |
                                                              Q(
                                                              gender =  request.POST.get("gender"),
                                                              campusID = current_employee.campusID,
                                                              classID = current_year_classID.classID,
                                                              student_typeID = student_typeID,
                                                              )
                                                              )
           for rqt in current_requirements:
              add_rqt = RequirementsPerTermActions()
              add_rqt.add_requiremt_to_student(request, current_employee, current_student, 
                                                current_year_classID.classID, streamID, current_year_classID,
                                                new_year_class_term, rqt, current_year)


           GLOBAL_VARIABLES.set_current_student(request, current_student)
           

    

    def bursar_add_add_requiremt_to_student(self, request, current_employee, current_student, current_year_term):
            add_rqt = RequirementsPerTermActions()
            classID = current_year_term.classID
            streamID = current_year_term.streamID
            year_class = current_year_term.year_classID
            current_year = datetime.now().year  #get current year
            
            rqt = Item.objects.get(id = int(request.POST.get("rqtID")))

            add_rqt.add_requiremt_to_student(request, current_employee, current_student, classID,
                                streamID, year_class, current_year_term, rqt, current_year)



    def bursar_del_brought_requiremnts(self, request, current_employee, rqt, reason):

        refunded_item = RefundedItens()
        refunded_item.rqt_broughtID = rqt
        refunded_item.item_name = rqt.item_name

        if rqt.is_monetary == True:
           refunded_item.amount_refunded = rqt.amount_brought + rqt.quantity_brought
        else:
            refunded_item.amount_refunded = rqt.quantity_brought

        if rqt.is_deleted == True:
            messages.info(request, "Item already refunded")
            return redirect("index")

        refunded_item.reason = reason
        refunded_item.userID = request.user
        refunded_item.user_fullname = str(current_employee.surname) +" "+ str(current_employee.firstname)+" "+str(current_employee.othername)
        
        

        if rqt.is_monetary == True:
            refund_list = CashBook.objects.filter(rqt_broughtID= rqt)
            for refund in refund_list:
                cashbook_actions = CahBookActions()
                cashbook_actions.refund_cashbook(request, current_employee, refund)

        refunded_item.save()
        rqt.is_deleted = True


        if rqt.rqt_requiredID.is_school_fees == True:
            rqt.rqt_requiredID.studentID.balance += rqt.amount_brought
            rqt.rqt_requiredID.studentID.save()
        
        rqt.rqt_requiredID.balance += rqt.quantity_brought + rqt.amount_brought
        rqt.rqt_requiredID.save()

        rqt.save()
        messages.info(request, "Success, item returned")


    

    def bursar_del_rqt_unpaid(self, request, id):

        del_rqt = StudentRequirementsPerTerm.objects.get(id=int(id))
        check_items_count = StudentRequirementsPerTermBrought.objects.filter(rqt_requiredID = del_rqt, is_deleted=False).count()

        if (check_items_count > 0 ):
            messages.warning(request, "Item cannot be deleted, first refund what has been brought by the student")
            return redirect("bursar-dashboard")
        
        del_rqt.delete()
        messages.info(request, "Success item deleted")


            


    


        



    