from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from datetime import datetime, timedelta
#importing models
from main.models import Loan, Client, StationStng, InterestBook, Interest, CashBook, CourtQueue
#importing global views
from .global_views import GlobalVariables
#importing loan view to help us pick some useful loan functions like list of all current loans
from .loan_view import LoanView
from .client_view import ClientView
from .cashbook_main import CashBookMainView
from .interest_view import InterestViews
from .court_queue import CourtQueueActions



#ninitializing the main cashbook object
cashbook_main = CashBookMainView()

def index(request):         
    
    """
    This function initialises the application, it does the followind
    1. Get basic business info for viewing on login page
    2. Load login form
    3. Handle login logic
    4. It sets initial variables for the loggedin user, these variables include
        >user staionID
        >It also sets an initial client and initial loan the station last worked on
        such that the logged in user sees this information immediately they login, that is,
        the last client worked on
    """ 

    #initializing variables and objects
    global_variables= GlobalVariables()
    global_variables.set_global_sessions(request) #sets and stores our sessions
    get_global_db_objects =  global_variables.get_global_db_objects(request) 
    message = ""

    if request.method=="POST" and request.POST.get("username"):

      
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")

                #Do some staff at successful login
                #set user global variables
                global_variables.set_global_sessions(request)
                #delete all past undisbursed loans
                undisbursed_loand = LoanView.delete_yesterday_undisbursed_loand(request)
                #then initialize the cashbook
                cashbook_main.inititialize_cash_book(request)

                return redirect("main:index")
            else:
                message ="Wrong username or password" 
                messages.error(request, "Invalid  username or password")
        else:
            message ="Wrong username or password"  
            messages.error(request, "Invalid username or password")
         
    form = AuthenticationForm()

    
    loan = None
    loan_list = None
    interest_book = None
    added_fines = None
    cash_book = None

    #setting current loan from front clicking
    if request.POST.get("set-loan-id"):
        loanID = request.POST.get("set-loan-id")
       
        if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
           loan = Loan.objects.get(id= loanID)
        else:
           station = StationStng.objects.get(id=request.session["current_stationID"])
           loan = Loan.objects.get(id= loanID, stationID = station)
        
        global_variables.set_current_client(request, loan.clientID)
        global_variables.set_current_loan(request, loan)
        return redirect("main:index")
    

    if True:
        #setting list of current loans for this client
        try:
           loan = Loan.objects.get(id = int(request.session["current_loanID"]))
           loan_list = LoanView.set_list_of_current_loans(request, loan)
        except:
            try:
                client_change = Client.objects.get(id = int(request.session["current_clientID"]))   
                client_change.current_total_balance =0
                request.session["current_client_balance"] = 0
                client_change.save()
            except:
                pass

        try:
            added_fines = Interest.objects.filter(loanID = loan).order_by("-id")
        except:
            pass

        try:
            #for daily loans
            if loan.loan_typeID.id ==1 or loan.loan_typeID.id ==2:
               interest_book = InterestBook.objects.filter(loanID = loan).order_by("-id")
        except:
            pass

        '''
        try:
            #for monthly loans
            if loan.loan_typeID.id ==2:
               cash_book = CashBook.objects.filter(loanID = loan).order_by("-id")
        except:
            pass
        '''

        #============================================================
        #Adjusting various values invoked from the index template
        #=============================================================
        if request.POST.get('edit-total-fines'):
            loan_edit_fines = LoanView()
            loan_edit_fines.edit_total_fines(request)

        if request.POST.get('interest-to-adjust'):
            interest = InterestViews()
            interest.adjust_fines(request)

        if request.POST.get('del-fineID'):
            interest = InterestViews()
            interest.del_fines(request)

        if request.POST.get("edit-client-rows"):
            book_client = ClientView()
            book_client.edit_book(request)

        if request.POST.get('adjust-loan-balance'):
            loan_edit_balance = LoanView()
            loan_edit_balance.adjust_loan_balance(request)

        if request.POST.get('all-balance'):
            client_edit_all_time_balance = ClientView
            client_edit_all_time_balance.set_client_all_time_balance(request)

        if request.POST.get("send-client-to-court"):
            if loan is None:
                messages.info(request, "Please first load client into window")
                return redirect("main:index")

            if loan.sent_to_court == True:
                messages.info(request, "Client already in court queue, please go to court queue for more details")
                return redirect("main:index")

            court = CourtQueueActions() 
            total_court_expenses = request.POST.get("total-court-expenses")
            demand_notice =  request.POST.get("demand-notice")
            more_notes =  request.POST.get("more-notes")
            current_total_balance = request.POST.get("current-total-balance")
            court.add_client_to_court(request, loan.clientID, loan, current_total_balance, total_court_expenses, demand_notice, more_notes)
            messages.info(request, "Success, client sent to court")
            return redirect("main:index")


    
    #setting loan_list
    return render(request=request, template_name="main/index.html", 
                  context = {"login_form":form,"get_global_db_objects": get_global_db_objects,
                             "message":message, "interest_book":interest_book, "loan_list":loan_list,
                             "added_fines":added_fines, "cash_book":cash_book, "loan":loan})




def login_request(request):

    if request.method=="POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect("main:index")
            else:
                pass
        else: 
            pass
               
    form = AuthenticationForm()
    
    return render(request=request, template_name="main/index.html", context = {"login_form":form})





@login_required(login_url="/")
def change_password(request):
    if request.method =="POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect ("main:logout")
        else:
            messages.error(request, "Please correct the error below")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "main/change_password.html", context={'form':form})



def native_login(request):
    username = request.GET.get("username")
    password = request.GET.get("password")

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        messages.info(request, f"You are now logged in as {username}")
        return redirect("main:index")

    messages.info(request, f"Wrong username or password, please try again")
    return redirect("main:index")





def transactional(request):
    pass