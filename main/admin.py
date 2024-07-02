from django.contrib import admin
from . models import *

# Register your models here.


admin.site.register(BusinessStng)

admin.site.register(StationStng)
admin.site.register(SystemCustomSettings)
admin.site.register(ReportTypeStng)
admin.site.register(LoanTypeStng)
admin.site.register(ItemType)
admin.site.register(ItemCategories)
admin.site.register(Paymethod)
admin.site.register(ReportTemplate)
admin.site.register(Report)
admin.site.register(UserStationDetailsVew)
admin.site.register(Track_auto_item_adds)
admin.site.register(DailyPayBacksInterest)
admin.site.register(InterestBook)
admin.site.register(cashBookMain)
admin.site.register(DeletedItems)
admin.site.register(WeeklyBook)
admin.site.register(VisitedLoans)
admin.site.register(AgreementFile)
admin.site.register(DisbursementFile)

#admin.site.register(Client)
#admin.site.register(Loan)
#admin.site.register(Custom_user_rights)
class ClientTypeStngAdmin(admin.ModelAdmin):
    
    exclude =["interest_rate",]

admin.site.register(ClientTypeStng, ClientTypeStngAdmin)

class Custom_user_rightsAdmin(admin.ModelAdmin):
    exclude =["user_rightID",]
admin.site.register(Custom_user_rights, Custom_user_rightsAdmin)

class ClientAdmin(admin.ModelAdmin):
    model=Client
    search_fields=['full_name', 'contact_numbers']   
 
        
admin.site.register(Client, ClientAdmin)



admin.site.register(OtherPayments)

class LoanAdmin(admin.ModelAdmin):
    search_fields = ['id',]
admin.site.register(Loan, LoanAdmin)


admin.site.register(Guarantor)
admin.site.register(Security)
admin.site.register(DailyPayBack)
admin.site.register(Interest)
admin.site.register(CashBook)
admin.site.register(Windows)
admin.site.register(AutoItemAdds)
admin.site.register(CourtQueue)
admin.site.register(Employee)

admin.site.register(Daily_item_catID_totals)
admin.site.register(Monthly_ite_totals)
admin.site.register(Yearly_ite_totals)

