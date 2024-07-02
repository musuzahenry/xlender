from django.shortcuts import render, redirect
from main . models import Class, StudentType
from . global_views import GlobalViews



GLOBAL_VARIABLES = GlobalViews()
class ClassSettings:

    def list_all_classes(request):
        if request.user.is_authenticated:
            pass
        else:
           return redirect("index")
        
        current_employee = GLOBAL_VARIABLES.get_current_employee_info(request)
        all_classes = Class.objects.filter(
                                           businessID = current_employee.businessID,
                                           campusID = current_employee.campusID,)
        
        ALL_STUDENT_TYPES = StudentType.objects.filter(
                                            campusID =  current_employee.campusID,
                                            businessID= current_employee.businessID,
                                            )

        if request.POST.get("classID"):
            request.session["class_settingsID"] = request.POST.get("classID")
            request.session["student_type_settingsID"] =  request.POST.get("student-typeID")
            return redirect("list-requirements")

        if request.POST.get("student-typeID") and not(request.POST.get("classID")):
            request.session["class_settingsID"] = "NA"
            request.session["student_type_settingsID"] =  request.POST.get("student-typeID")
            return redirect("list-requirements")

        return render(
                    request, 
                    template_name="main/class_settings.html",
                    context = {"all_classes": all_classes,
                    "ALL_STUDENT_TYPES": ALL_STUDENT_TYPES,
                    "no_of_types":ALL_STUDENT_TYPES.__len__(),
                    }
                   )