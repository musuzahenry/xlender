
from django.shortcuts import render, redirect
from . global_views import *
from main.models import Client, Loan, Guarantor, Security, StationStng
from main.forms.client_forms import ClientImageForm, NationalIDImageForm, AgreementImageForm, \
                    DisburseImageForm, GuarantorImageForm, SecurityImageForm



#setting vaules and objects
model=Client
client_typeID =0
stationID =0
global_variables = GlobalVariables()


class Image():

    def client_image(request):
        client = Client.objects.get(id=request.session["current_clientID"])
        form = ClientImageForm(request.POST, request.FILES or None, instance=client)
        if form.is_valid():
           form.save()
        return render(request, template_name="main/client_image.html", 
                    context={"client":client, "form":form})




    def nationaID_image(request):
        client = Client.objects.get(id=request.session["current_clientID"])
        form = NationalIDImageForm(request.POST, request.FILES or None, instance=client)
        if form.is_valid():
           form.save()
        return render(request, template_name="main/nationalID_image.html", 
                    context={"client":client, "form":form})
    
    

    def agreement_image(request):
        loan = Loan.objects.get(id=request.session["current_loanID"])
        form = AgreementImageForm(request.POST, request.FILES or None, instance=loan)
        if form.is_valid():
           form.save()
        return render(request, template_name="main/agreement_image.html", 
                    context={"loan":loan, "form":form})
    
    def disburse_iamge(request):
        loan = Loan.objects.get(id=request.session["current_loanID"])
        form = DisburseImageForm(request.POST, request.FILES or None, instance=loan)
        if form.is_valid():
           form.save()
        return render(request, template_name="main/disburse_image.html", 
                    context={"loan":loan, "form":form})
    
    def security_image(request): 
        security = Security.objects.get(id=request.session["current_securityID"])
        form = SecurityImageForm(request.POST, request.FILES or None, instance=security)
        if form.is_valid():
           form.save()
        return render(request, template_name="main/security_image.html", 
                    context={"loan":security, "form":form})

    def guarantor_image(request):
        guarantor= Guarantor.objects.get(id=request.session["current_guarantorID"])
        form = GuarantorImageForm(request.POST, request.FILES or None, instance=guarantor)
        if form.is_valid():
           form.save()
        return render(request, template_name="main/guarantor_image.html", 
                    context={"loan":guarantor, "form":form})
    

    
