from django.urls import path
from django.contrib.auth.views  import LogoutView
from .views import *


app_name="main"

urlpatterns =[
    #REST FRAMEWORK API USRLS
    path('api-login/', LoginAPIView.login, name='api-login'),
    #user view urls
    path("",index, name="index"),
    path("login/", login_request, name="login"),
    path("native-login/",native_login, name="native-login"),
    path("logout/", LogoutView.as_view(template_name ="user/logout.html"), name="logout"),
    path("change-password/", change_password, name="change-password"),

    #client management views
    path("add-client", ClientView.add_client, name="add-client"),
    path("edit-client", ClientView.edit_client, name="edit-client"),
    path("search-for-a-client", ClientView.search_for_a_client, name="search-for-a-client"),
    path("search-for-a-client/<int:id>", ClientView.set_search_for_a_client, name="set-search-for-a-client"),
    path("set-prev-client", ClientView.set_prev_client, name="set-prev-client"), 
    path("set-next-client", ClientView.set_next_client, name="set-next-client"), 
    path("client-list", ClientView.client_list, name="client-list"),
    #Book adjustments
    path("book-adjustment-report", ClientView.book_adjustment_report, name="book-adjustment-report"),
      
    #Loan management views
    path("add-loan", LoanView.add_loan, name="add-loan"),
    path("edit-loan",  LoanView.edit_loan, name="edit-loan"),
    path("set-prev-loan", LoanView.set_prev_loan, name="set-prev-loan"), 
    path("set-next-loan", LoanView.set_next_loan, name="set-next-loan"),
    path("pay-daily", LoanView.pay_daily, name="pay-daily"), #Daily payments
    path("monthly-loan-payment", LoanView.monthly_loan_payment , name="monthly-loan-payment"),#montlly loan payments
    path("pay-loan", LoanView.pay_loan , name="pay-loan"),#pay_loan
    path("old-loan", LoanView.old_loan, name="old-loan"),#old_loan
    path("edit-loan/<int:id>", LoanView.delete_loan, name="delete-loan"),

    #Images
    path("client-image", Image.client_image, name="client-image"),
    path("national-id", Image.nationaID_image, name="national-id"),
    path("agreement-image", Image.agreement_image, name="agreement-image"),
    path("disburse-iamge", Image.disburse_iamge, name="disburse-iamge"),
    path("security-image", Image.security_image, name="security-image"),
    path("guarantor-image", Image.guarantor_image, name="guarantor-image"),

    #Borrower book management
    path("add-borrower-book", BorrowerBook.add_borrower_book, name="add-borrower-book"),
    path("manually-add-book", BorrowerBook.manually_add_book, name="manually-add-book"),
    

    #Security management views
    path("list-security", SecurityView.list_security, name="list-security"),
    path("add-security", SecurityView.add_security, name="add-security"),
    path("edit-security", SecurityView.edit_security, name="edit-security"),
    path("edit-security/<int:id>", SecurityView.set_security_from_list, name="set-edit-security"),

    #Guarantor management
    path("guarantor-list", GuarantorView.guarantor_list, name="guarantor-list"),
    path("add-guarantor", GuarantorView.add_guarantor, name="add-guarantor"),
    path("edit-guarantor",GuarantorView.edit_guarantor, name="edit-guarantor"),
    path("edit-guarantor/<int:id>",GuarantorView.set_edit_from_list_guarantor, name="set-edit-guarantor"),

    #Loan Reports
    path("approve-loans",  ReportLoans.approve_loans, name="approve-loans"),
    path("approved-loans", ReportLoans.approved_loans, name="approved-loans"),
    path("disbursed-loans", ReportLoans.disbursed_loans, name="disbursed-loans"),
    path("loan-debts", ReportLoans.loan_debts, name="loan-debts"),
    path("visited-loans", ReportLoans.visited_loans, name="visited-loans"),
   
    #Other Incomes and expenses management
    path("manage-incomes-and-expenses", IncomeExpense.manage_incomes_and_expenses, name="manage-incomes-and-expenses"),
    
    #Cashbook 
    path("view-cashbook", CashBookView.view_cashbook, name="view-cashbook"),
    path("view-transactions", CashBookView.view_other_incomes_and_expenses, name="view-transactions"),
    

    #InterestBook 
    path("view-interest-book", InterestBookView.view_interest_book, name="view-interest-book"),

    #Added Interest   added-interest
    path("view-interest", InterestViews.view_interest, name="view-interest"),

    #Added Interest   added-interest
    path("view-interest", InterestViews.view_interest, name="view-interest"),

    #defaulters
    path("view-fines", FinesView.view_fines, name="view-fines"),
    
    #Court Queue
    path("view-court-queue", CourtQueueView.view_court_queue, name="view-court-queue"),
    path("court-transactions", CourtQueueView.court_transactions, name="court-transactions"),
    path("manually-add-court-queue", CourtQueueView.manually_add_court_queue, name="manually-add-court-queue"),
    path("court-details/<int:id>", CourtDetails.set_court_details, name="court-details"),

    
    #Court
    path("view-employees", EmployeeView.view_employees, name="view-employees"),
    path("view-deleted-employees", EmployeeView.view_deleted_employees, name="view-deleted-employees"),
    path("paid-salaries", EmployeeView.paid_salaries, name="paid-salaries"),

    #Pivot reports and Weekly Reports
    path("pivot-reports", PivotTotals.view_report, name="pivot-reports"),
    path("interest-paid-details", WeeklyReportDetailsView.view_interest_paid, name="interest-paid-details"),
    path("view-sold-books", WeeklyReportDetailsView.view_borrowers_book, name="view-sold-books"),
    path("view-processing-fee", WeeklyReportDetailsView.view_processing_fee, name="view-processing-fee"),
    path("detail-view-fines", WeeklyReportDetailsView.view_detail_fines, name="detail-view-fines"),
    path("detail-loan-recovered", WeeklyReportDetailsView.view_detail_loan_recovered, name="detail-loan-recovered"),

    #Stations
    path("view-station", StationsView.view_stations, name="view-stations"),
    path("view-stations-loan-settings", StationsView.stations_loan_seetings, name="view-stations-loan-settings"),
    path("book-settings", StationsView.stations_book_settings, name="book-settings"),
    path("processing-fee-settings", StationsView.stations_processing_fee, name="processing-fee-settings"),
    
    


    ]