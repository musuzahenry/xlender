

from django.shortcuts import render, redirect
from django.contrib import messages
from main.models import Parent, Student

from . global_views import GlobalViews

GLOBAL_VARIABLES = GlobalViews()


class SearchForStudent:

    def search_for_a_student(request):


       current_employee= GLOBAL_VARIABLES.get_current_employee_info(request)
      
       if request.POST.get("search-str"):
            request.session["search_str"] =  request.POST.get("search-str")
            list_students = Student.objects.filter(
                                 campusID = current_employee.campusID,
                                 search_string__icontains = request.session["search_str"]
                                 )
       else:
            list_students = Student.objects.filter(
                                            campusID = current_employee.campusID,
                                            search_string__icontains = request.session["search_str"]
                                             )

       return render(
                     request, 
                     template_name="main/list_search_for_a_client.html",
                     context ={
                        "list_students":list_students,
                     }
                    )





