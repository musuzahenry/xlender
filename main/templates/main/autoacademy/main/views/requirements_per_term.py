from main . models import Requirements, StudentType, Class, Item, ItemType, StudentRequirementsPerTerm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from . global_views import GlobalViews


GLOBAL_VARIABLES = GlobalViews()


class RequirementsPerTermActions:


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
        std_req_debts.year_class_term = str(current_year)+"-"+classID.class_name+"-"+ year_class_termID.term_name
        std_req_debts.studentID = student
        std_req_debts.student_name = student.fullname

        try:
           std_req_debts.itemID = rqt.itemID
        except:
            std_req_debts.itemID = rqt

        std_req_debts.item_name = rqt.item_name
        std_req_debts.is_monetary = rqt.is_monetary
        std_req_debts.is_school_fees = rqt.is_school_fees

        if request.POST.get("amount-qty"):

           if  rqt.is_monetary == True:
                std_req_debts.quantity_required = 0
                std_req_debts.amount_required = int(request.POST.get("amount-qty"))
                std_req_debts.balance = int(request.POST.get("amount-qty"))
           else:
                std_req_debts.quantity_required = int(request.POST.get("amount-qty"))
                std_req_debts.amount_required = 0
                std_req_debts.balance = int(request.POST.get("amount-qty"))
        else:
           std_req_debts.quantity_required = rqt.quantity_required
           std_req_debts.amount_required = rqt.amount_required
           std_req_debts.balance = rqt.quantity_required + rqt.amount_required

        
        std_req_debts.userID = request.user
        #std_req_debts.user_fullname
        std_req_debts.save()
       

           



