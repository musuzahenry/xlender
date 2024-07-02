from main . models import Requirements, StudentType, Class, Item, ItemType, StudentRequirementsPerTerm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from . global_views import GlobalViews


GLOBAL_VARIABLES = GlobalViews()

class RequirementsViews:

    def list_requirements(request):
        if request.user.is_authenticated:
            pass
        else:
            return redirect("index")

        current_employee = GLOBAL_VARIABLES.get_current_employee_info(request)
        material_item_type= ItemType.objects.get(settings_name= "material")
        monetary_item_type= ItemType.objects.get(settings_name= "monetary")

        add_items = Item.objects.filter(
                                        campusID = current_employee.campusID,
                                        businessID = current_employee.businessID,
                                        is_requirement = True,
                                      )
        classesx = Class.objects.filter(
                                        campusID = current_employee.campusID,
                                        businessID = current_employee.businessID
                                      )
        current_employee = GLOBAL_VARIABLES.get_current_employee_info(request)
        typeds = StudentType.objects.filter(
                                        campusID = current_employee.campusID,
                                        businessID = current_employee.businessID
                                      )
        try:
            classID = Class.objects.get(id = int(request.session["class_settingsID"]))
        except:
            classID = None

        try:
            student_typeID = StudentType.objects.get(id = int(request.session["student_type_settingsID"]))
        except:
            student_typeID = None




        if request.POST.get("add-requirements"):
            requirement_action = RequirementsActions()


            requirement_action.add_requiremt(
                                            request, 
                                            request.session["class_settingsID"],
                                            request.session["student_type_settingsID"]
                                            )

            return redirect("list-requirements")



        
        if request.POST.get("del-requirementID"):
            requirement_action = RequirementsActions()
            requirement_action.del_requiremnt(request)





        current_employee = GLOBAL_VARIABLES.get_current_employee_info(request)

        current_student_typeID = StudentType.objects.filter(
                                            id = int(request.session["student_type_settingsID"]),
                                            campusID =  current_employee.campusID,
                                            businessID= current_employee.businessID,
                                            )


                                            
       
        ALL_CLASSES = Class.objects.filter(
                                            campusID =  current_employee.campusID,
                                            businessID= current_employee.businessID,
                                            ) 

        
        #get requiremets, either filtered or unfiltered

        if classID or student_typeID: #if a class has been chosen to load this apge

            if classID and student_typeID:
                      
               all_requirements = Requirements.objects.filter(
                                                campusID =  current_employee.campusID,
                                                businessID= current_employee.businessID,
                                                classID = classID,
                                                student_typeID = student_typeID,
                                                ).order_by("student_typeID")

            elif not(classID) and student_typeID:
                               all_requirements = Requirements.objects.filter(
                                                campusID =  current_employee.campusID,
                                                businessID= current_employee.businessID,
                                                classID__isnull = True,
                                                student_typeID = student_typeID,
                                                ).order_by("student_typeID")
            else:
                pass

        else:
            pass

        #list items
        #===================================================

        already_added_items = []
        
        for this_item in all_requirements:
           already_added_items.append(this_item.itemID.id)

        monetary_items = Item.objects.filter(
                                        ~Q(pk__in = already_added_items),
                                        campusID =  current_employee.campusID,
                                        businessID= current_employee.businessID,
                                        item_typeID = monetary_item_type,
                                        is_requirement = True,
                                        )
        
        material_items = Item.objects.filter(
                                        ~Q(pk__in = already_added_items),
                                        campusID =  current_employee.campusID,
                                        businessID= current_employee.businessID,
                                        item_typeID = material_item_type,
                                        is_requirement = True,
                                        )

        return render(
                     request, 
                     template_name="main/list_requirements.html",
                     context ={
                       "current_class":classID,
                       "current_student_type":student_typeID,
                       "monetary_items":monetary_items,
                       "material_items":material_items,
                       "all_requirements":all_requirements, 
                       "ALL_CLASSES":ALL_CLASSES,  
                     }
                     )





class RequirementsActions:

    def add_requiremt(self, request, class_settingsID, student_type_settingsID):

        if request.POST.get("itemID") == "NA":
            messages.warning(request, "Please choose correct value for item")
            return redirect("list-requirements")
   

        current_employee = GLOBAL_VARIABLES.get_current_employee_info(request)
        current_class = Class.objects.get(id = int(class_settingsID))
        student_typeID = StudentType.objects.get(id = int(student_type_settingsID))

                
        if request.POST.get("add-fees"):

            try:
                check_fees = Requirements.objects.get(
                                                campusID =  current_employee.campusID,
                                                businessID= current_employee.businessID,
                                                classID = current_class,
                                                student_typeID = student_typeID,
                                                is_school_fees = True,
                                                )
                messages.warning(request, "Fees is already added, you can't add second time")
                return redirect("list-requirements")
            except:
                pass


            current_item = Item.objects.get(
                                            campusID =  current_employee.campusID,
                                            businessID= current_employee.businessID,
                                            is_school_fees = True,)
        else:
           current_item = Item.objects.get(id = int(request.POST.get("itemID")))

            

        new_requirement = Requirements()
        new_requirement.businessID = current_employee.businessID
        new_requirement.campusID = current_employee.campusID
        new_requirement.itemID = current_item 
        new_requirement.item_name = current_item.item_name
        
        if request.POST.get("add-fees"):
            new_requirement.is_school_fees = True
        new_requirement.classID = current_class
        new_requirement.levelID = current_class .levelID
        new_requirement.student_typeID = student_typeID
        new_requirement.class_name = current_class.class_name
        

        if request.POST.get("qty-required"):
             new_requirement.quantity_required = float(request.POST.get("qty-required"))
             new_requirement.is_monetary = False
        else: 
            new_requirement.quantity_required = 0
        
        if request.POST.get("amount-requiredx"):
            new_requirement.amount_required = float(request.POST.get("amount-requiredx"))
            new_requirement.is_monetary = True
        else:
            new_requirement.amount_required = 0

        new_requirement.gender = request.POST.get("gender")



    
        new_requirement.save()
        messages.info(request, "Success, item saved")


    def del_requiremnt(self, request):
        deleted_requirement = Requirements.objects.get(id = int(request.POST.get("del-requirementID")))
        deleted_requirement.delete()
        messages.info(request,"Success, item deleted")
        return redirect("list-requirements")


    def add_requiremt_to_student(self, request, current_employee, student, classID,
                                streamID, year_classID, year_class_termID, rqt, current_year):

        std_req_debts = StudentRequirementsPerTerm()
        std_req_debts.businessID = current_employee.businessID
        std_req_debts.campusID = current_employee.campusID
        std_req_debts.categoryID = classID.categoryID
        std_req_debts.classID = classID
        std_req_debts.levelID = classID.levelID
        std_req_debts.streamID = streamID
        std_req_debts.yearclassID = year_classID
        std_req_debts.yearclass_termID = year_class_termID
        std_req_debts.class_name = classID.class_name
        std_req_debts.stream_name = streamID.stream_name
        std_req_debts.year_class = str(current_year)+"-"+classID.class_name
        std_req_debts.year_class_term = str(current_year)+"-"+classID.class_name+"-"+streamID.stream_name
        std_req_debts.studentID = student
        std_req_debts.student_name = student.fullname
        std_req_debts.itemID = rqt.itemID
        std_req_debts.item_name = rqt.item_name
        std_req_debts.is_monetary = rqt.is_monetary
        std_req_debts.is_school_fees = rqt.is_school_fees
        std_req_debts.quantity_required = rqt.quantity_required
        std_req_debts.amount_required = rqt.amount_required
        std_req_debts.balance = rqt.quantity_required + rqt.amount_required
        std_req_debts.userID = request.user
        #std_req_debts.user_fullname
        std_req_debts.save()

        messages.info(request, "Success, record saved!")
       

           



