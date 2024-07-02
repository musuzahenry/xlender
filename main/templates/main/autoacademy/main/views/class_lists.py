

from main.models import YearClass, YearClassTerm, Class, Stream, Term, Requirements, YearClassTerm
from django.shortcuts import render, redirect
from django.contrib import messages
from . global_views import GlobalViews
from datetime import datetime, timedelta

GLOBAL_VARIABLES = GlobalViews()
today = datetime.today()
year= today.year


class classListsView:


    def list_classes(request):
         
        if request.user.is_authenticated:
            pass
        else:
            return redirect("index")

        #get current employee
        current_employee= GLOBAL_VARIABLES.get_current_employee_info(request)
        ALL_CLASSES = Class.objects.filter(campusID = current_employee.campusID)
        ALL_STREAMS = Stream.objects.filter(campusID = current_employee.campusID)
        ALL_TERMS =   Term.objects.filter(campusID = current_employee.campusID)
        class_list = None

        if request.POST.get("year") and request.POST.get("class-name"):
            request.session["year"] = request.POST.get("year")
            request.session["class_name"] =  request.POST.get("class-name")
            request.session["stream_name"]= request.POST.get("stream-name")

            if request.session["stream_name"]=="all":
                class_list = YearClassTerm.objects.filter(
                                                    campusID = current_employee.campusID,
                                                    year_class = str(request.session["year"])+"-"+request.session["class_name"],
                                                    )
            else:
                class_list = YearClassTerm.objects.filter(
                                                    campusID = current_employee.campusID,
                                                    year_class = str(request.session["year"])+"-"+request.session["class_name"],
                                                    stream_name = request.session["stream_name"],
                                                    )
        
        elif request.POST.get("year") and request.POST.get("class-name") and request.POST.get("term-name"):
                request.session["year"] = request.POST.get("year")

                request.session["class_name"] =  request.POST.get("class-name")
                request.session["stream_name"]= request.POST.get("stream-name")
                request.session["term_name"] = request.POST.get("term-name")

                if request.session["stream_name"] == "all":
                    class_list = YearClassTerm.objects.filter(
                                                    campusID = current_employee.campusID,
                                                    year_class_term = str(request.session["year"])+"-"+request.session["class_name"]+"-"+request.session["term_name"],     
                                                    )
                else:
                    class_list = YearClassTerm.objects.filter(
                                                    campusID = current_employee.campusID,
                                                    year_class_term = str(request.session["year"])+"-"+request.session["class_name"]+"-"+request.session["term_name"],
                                                    stream_name = request.session["stream_name"],       
                                                    )
        else:
            class_list = None
        

        total_fees = 0
        total_paid = 0
        total_balance = 0
        count = 0

        try:
            for x in class_list :
                total_fees += int(x.original_fees)
                total_paid += int(x.amount_paid)
                total_balance += int(x.balance)
                count += 1
        except:
                total_fees = 0
                total_paid = 0
                total_balance = 0

        #class_list = YearClass.objects.all()
        return render(
                        request,
                        template_name = "main/class_lists.html",
                        context ={
                         "class_list":class_list,  
                        "ALL_CLASSES":ALL_CLASSES,
                        "ALL_STREAMS":ALL_STREAMS,
                        "ALL_TERMS":ALL_TERMS,
                        "total_fees":total_fees,
                        "total_paid":total_paid,
                        "total_balance":total_balance,
                        "count":count,
                        }
                        )