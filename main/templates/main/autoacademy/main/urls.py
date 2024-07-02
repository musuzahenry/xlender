from django.urls import path
from . views import *


urlpatterns =[
    path("", IndexViews.index, name = "index"),
    path("user-login", IndexViews.user_login, name = "user-login"),
    path("user-logout", IndexViews.user_logout, name = "user-logout"),

    #set variables by click
    path("set-current-student-by-click<int:id>",GlobalViewsByClick.set_current_student_by_click, name="set-current-student-by-click"),
    path("set-current-year-class-by-click<int:id>",GlobalViewsByClick.set_current_year_class_by_click, name="set-current-year-class-by-click"),
    path("set-current-year-class-term-by-click<int:id>",GlobalViewsByClick.set_current_year_class_term_by_click, name="set-current-year-class-term-by-click"),
    

    #Bursar urls
    #==================================================================
    path("bursar-dashboard", BursarViews.bursar_dashboard, name="bursar-dashboard"),
    #Student Reuirements
    path("list-requirements", RequirementsViews.list_requirements, name="list-requirements"),

    #search for a student  
    path("search-for-a-student", SearchForStudent.search_for_a_student, name="search-for-a-student"),

    #class lists list-classes
    path("list-classes", classListsView.list_classes, name="list-classes"),

    #student views
    path("add-student", StudentViews.add_student, name="add-student"),
    path("edit-student", StudentViews.edit_student, name="edit-student"),

    #Expemses
    path("expenses", ManageExpense.expenses, name="expenses"),

    #cashbook views
    path("list-cashbook", CashBookViews.list_cashbook, name="list-cashbook"),

    #banking views
    path("list-bank", BankViews.list_bank, name="list-bank"),

    #class settings
    path("list-all-classes", ClassSettings.list_all_classes, name="list-all-classes"),

    ]


