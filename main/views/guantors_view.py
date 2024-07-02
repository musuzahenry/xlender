from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from main . models import Guarantor, Loan
from main . views import GlobalVariables


global_variable = GlobalVariables()

class GuarantorView:


    @login_required(login_url="/")
    def guarantor_list(request):
        
        loan = Loan.objects.get(id=request.session["current_loanID"])
        guarantors_list  = Guarantor.objects.filter(loanID = loan)

        return render(request, template_name="main/guarantor_view_list.html", 
                      context={"guarantors_list":guarantors_list})
    



    @login_required(login_url="/")
    def set_edit_from_list_guarantor(request, id):
        global_variable.set_current_guarantor(request, id)
        return redirect ("main:edit-guarantor")
    



    @login_required(login_url="/")
    def add_guarantor(request):
        if request.POST.get("add-guarantor"):
            surnane =request.POST.get("surnane")
            first_name =request.POST.get("first-name")
            other_names =request.POST.get("other-names")
            national_identification_number =request.POST.get("national-identification-number")
            gender =request.POST.get("gender")
            date_of_birth =request.POST.get("date-of-birth")
            physical_address = request.POST.get("physical-address")
            contact_numbers =request.POST.get("contact-numbers")
            email_address =request.POST.get("email-address")
            occupation =request.POST.get("occupation")
            


            loan = Loan.objects.get(id=request.session["current_loanID"])
            guarantor = Guarantor()

            guarantor.loanID = loan
            guarantor.userID = request.user
            guarantor.surnane = surnane
            guarantor.first_name = first_name
            guarantor.other_names = other_names
            guarantor.national_identification_number = national_identification_number
            guarantor.gender = gender
            guarantor.date_of_birth = date_of_birth
            guarantor.contact_numbers= contact_numbers
            guarantor.physical_address = physical_address
            guarantor.email_address = email_address
            guarantor.occupation = occupation

            guarantor.save()
            guarantorID = guarantor.id
            global_variable.set_current_guarantor(request, guarantorID)
            return redirect("main:edit-guarantor")


        return render(request, template_name="main/guarantor_view_add.html")
    




    @login_required(login_url="/")
    def edit_guarantor(request):

        guarantor = Guarantor.objects.get(id = request.session["current_guarantorID"])

        if request.POST.get("edit-guarantor"):
            surnane =request.POST.get("surnane")
            first_name =request.POST.get("first-name")
            other_names =request.POST.get("other-names")
            national_identification_number =request.POST.get("national-identification-number")
            gender =request.POST.get("gender")
            date_of_birth =request.POST.get("date-of-birth")
            physical_address = request.POST.get("physical-address")
            contact_numbers =request.POST.get("contact-numbers")
            email_address =request.POST.get("email-address")
            occupation =request.POST.get("occupation")
   
            guarantor.surnane = surnane
            guarantor.first_name = first_name
            guarantor.other_names = other_names
            guarantor.national_identification_number = national_identification_number
            guarantor.gender = gender
            guarantor.date_of_birth = date_of_birth
            guarantor.contact_numbers= contact_numbers
            guarantor.physical_address = physical_address
            guarantor.email_address = email_address
            guarantor.occupation = occupation

            guarantor.save()
            return redirect("main:edit-guarantor")
        
        guarantorID = guarantor.id
        surnane = guarantor.surnane
        first_name = guarantor.first_name
        other_names = guarantor.other_names
        national_identification_number = guarantor.national_identification_number
        gender = guarantor.gender
        date_of_birthx = guarantor.date_of_birth
        contact_numbers = guarantor.contact_numbers
        email_address = guarantor.email_address
        occupation = guarantor.occupation
        guarantor_img = guarantor.guarantor_img


        #working on date of birth
        date_of_birth = str(date_of_birthx).split(" ")


        return render(request, template_name="main/guarantor_view_edit.html",
                      context ={"guarantorID":guarantorID,
        "surnane":surnane, "first_name":first_name, "other_names":other_names,
        "national_identification_number":national_identification_number, 
        "gender":gender, "date_of_birth":date_of_birth[0], "contact_numbers":contact_numbers,
        "email_address":email_address, "occupation":occupation, "guarantor_img":str(guarantor_img)
         })





    
    


    

