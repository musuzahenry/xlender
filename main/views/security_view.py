from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from main.models import Security, Loan
from .global_views import GlobalVariables


#getting our module varaibles

global_variable = GlobalVariables()

class SecurityView():

    #lists all the securitiess on a given loan
    @login_required(login_url="/")
    def list_security(request):
        loan = Loan.objects.get(id = request.session["current_loanID"])
        security_list = Security.objects.filter(loanID = loan)
        return render(request, template_name="main/security_view_list_security.html", 
                      context={"security_list":security_list})
    


    #sets the current loan when a user clicks the security list
    @login_required(login_url="/")
    def set_security_from_list(request, id):
        global_variable.set_current_security(request, id)
        return redirect("main:edit-security")
    


    @login_required(login_url="/")
    def add_security(request):
        """Adds new security with loan and client foreign key"""
        
        security_name = ""
        security_address = ""
        estimated_value = ""
        image = ""
        securityID = None

        
       
        loan = Loan.objects.get(id=request.session["current_loanID"])       
        if request.POST.get("add-security"):
                security_name = request.POST.get("security-name")
                security_address = request.POST.get("security-address")
                estimated_value = float(request.POST.get("estimated-value") or 0)

                security = Security()
                security.loanID = loan
                security.userID = request.user
                security.clientID = loan.clientID
                security.fullname = loan.full_name
                security.security_name = security_name
                security.security_address = security_address
                security.estimated_value = estimated_value                     

                #Finally saving everything
                security.save()

                if security.id is not None:
                    global_variable.set_current_security(request, security.id)
                    security.save()
                    return redirect("main:edit-security")
    


        return render(request, template_name="main/security_view_add.html", 
                      context={"securityID":securityID, "security_name":security_name, "image":str(image),
                               "security_address":security_address, "estimated_value":estimated_value,})
    




    @login_required(login_url="/")
    def edit_security(request):

        if request.GET.get("id"):
            global_variable.set_current_security(request, security.id)
 
        security = Security.objects.get(id = request.session["current_securityID"])    
        securityID = security.id
        security_name = security.security_name
        security_address = security.security_address
        estimated_value = security.estimated_value
        image = security.image
        
        if request.POST.get("edit-security"):
            security_name = request.POST.get("security-name")
            security_address = request.POST.get("security-address")
            estimated_value = float(request.POST.get("estimated-value"))

            
            security.security_name = security_name
            security.security_address = security_address
            security.estimated_value = estimated_value
            
            #Finally saving everything
            security.save()
            return redirect("main:edit-security")


        return render(request, template_name="main/security_edit.html", 
                      context={"securityID":securityID, "security_name":security_name, "image":str(image),
                               "security_address":security_address, "estimated_value":estimated_value,})
    








        



        
