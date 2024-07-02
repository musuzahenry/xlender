from django import forms
from main.models import Client, Loan, Guarantor, Security




class ClientImageForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['client_img']




class NationalIDImageForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["client_national_id"]




class AgreementImageForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ["loan_agreement_file"]




class DisburseImageForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ["loan_disbursement_file"]




class GuarantorImageForm(forms.ModelForm):
    class Meta:
        model = Guarantor
        fields = ["guarantor_img"]




class SecurityImageForm(forms.ModelForm):
    class Meta:
        model = Security
        fields = ["image"]