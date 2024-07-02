from django.shortcuts import redirect
from  main.models import Employee, SystemRoles, Rights, CashBook, Student
from datetime import datetime, timedelta

from . global_views import *



GLOBAL_VARIABLES = GlobalViews()

class GlobalViewsByClick:

 
    def set_current_student_by_click(request, id):
        student = Student.objects.get(id = int(id))
        GLOBAL_VARIABLES.set_current_student(request, student)
        return redirect("index") #redirect user to appropriate dashboard using the index_views

    
    def set_current_year_class_by_click(request, id):
        year_class = YearClass.objects.get(id = int(id))
        GLOBAL_VARIABLES.set_current_year_class(request, year_class)
        return redirect("index") #redirect user to appropriate dashboard using the index_views

    def set_current_year_class_term_by_click(request, id):
        year_class_term = YearClassTerm.objects.get(id = int(id))
        GLOBAL_VARIABLES.set_current_year_class_term(request, year_class_term)
        return redirect("index") #redirect user to appropriate dashboard using the index_views





