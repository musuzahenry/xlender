from main.models import Loan,  Track_auto_item_adds, AutoItemAdds, StationStng

class ProcessingFee():

    def add_processing_fee(self, request):
                
        if not (request.session["current_stationID"]):
            return redirect('main:index')
            
        loan = Loan.objects.get(id = request.session["current_loanID"])
        principle = loan.principle
        station = StationStng.objects.get(id=request.session["current_stationID"])


        #getting processing fee that is between those limits set by the client   
        processing = AutoItemAdds.objects.get(item_name = "processing_fee",
                    lower_limit__lte=principle, loan_typeID= loan.loan_typeID,
                      upper_limit__gte=principle, stationID=station)
        
        
        tracking_number = processing.id
        processing_fee = processing.unit_price
        item_catID = processing.item_catID

        #checking whether processinf fee has already been added to tracking
        track_fee = None
        try:
            track_fee = Track_auto_item_adds.objects.get(loanID = loan, item_name="processing_fee")   
        except:
            track_fee  = None

        #we add processing fee only once
        #so we confirm whether it was added or not, if not, it is added
        #it also helps us to save it just once into the cashbook
        if track_fee is None:
            fee = Track_auto_item_adds()
            #updating tracking auto add items for later audit 
            #the book is saved into tracking items since it has to be tracked
            #we can follow from the cashbook since the cashbook is also saved into this record
            fee.loanID = loan
            fee.clientID = loan.clientID
            fee.item_name = "processing_fee"
            fee.stationID = loan.stationID
            fee.tracking_number = tracking_number #obtained from as Tracking_items_foreign key
            fee.userID = request.user
            fee.save()

  



        