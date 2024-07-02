from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . global_views import *
from main.models import Client, StationStng, ClientTypeStng, Report, \
                        ReportTypeStng, ItemCategories, CashBook, VisitedLoans, Track_auto_item_adds
from datetime import datetime, timedelta


#setting vaules and objects
model=Client
client_typeID =0
stationID =0
global_variables = GlobalVariables()


class ClientView():
    #model 
    
    @login_required(login_url="/")
    def client_list(request):

        #ninitalizing station object
        station = None

        if not request.POST:
            try:
                if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                    client_set  = Client.objects.all().order_by("-id","-stationID")
                    station_name = "All Stations"
                else:
                    station = StationStng.objects.get(id=request.session["current_stationID"]) 
                    client_set  = Client.objects.filter(stationID=station).order_by("-id")
                    station_name = station.station_name
            except:
                pass


        if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
            
            if request.POST.get("station-id") and not request.POST.get("station-id")==0 and \
                                               not request.POST.get("station-id")=="0":

                    station = StationStng.objects.get(id=request.POST.get("station-id"))
                    station_name = station.station_name
                    client_set = Client.objects.filter(stationID = station,).order_by("-id", "stationID")
                    
            else:
               client_set= Client.objects.all().order_by("-id", "stationID")
        else:

            station = StationStng.objects.get(id=request.session["current_stationID"]) 
            client_set = Client.objects.filter(stationID = station,).order_by("-id")

        no_of_clients =0 
        total_debt=0
        for client in client_set:
            no_of_clients +=1
            total_debt +=client.current_total_balance


        return render(request, template_name="main/client_list.html",
                      context={"get_global_db_objects":global_variables.get_global_db_objects(request),
                               "client_set":client_set,
                               "station_name":station_name,
                               "total_debt":round(total_debt,1),
                               "no_of_clients":no_of_clients})




    #Choose user desired values
    #add client functions
    @login_required(login_url="/")    
    def add_client(request):
        
        if not request.method == "POST":
            return redirect("main:index")
        
        if request.POST.get("client-typeID"):
                client_typeIDx = request.POST.get("client-typeID")
                if not client_typeIDx == 0:
                    try:
                       client_typeIDy = ClientTypeStng.objects.get(id=client_typeIDx)
                    except:
                        client_typeIDy = ClientTypeStng.objects.get(id=request.session["default_client_typeID"])
                else:
                   client_typeIDy = ClientTypeStng.objects.get(id=request.session["default_client_typeID"])
        else:
            client_typeIDy = ClientTypeStng.objects.get(id=request.session["default_client_typeID"])

            #getting the station
        if request.POST.get("stationID"):
                stationIDx = request.POST.get("stationID")
                if not stationIDx == 0:
                   try:
                      stationIDy = StationStng.objects.get(id=stationIDx)
                   except:
                       stationIDy = StationStng.objects.get(id=request.session["current_stationID"])       
                else:
                   stationIDy = StationStng.objects.get(id=request.session["current_stationID"])
        else:
             stationIDy = StationStng.objects.get(id=request.session["current_stationID"])
        
        client_typeID = client_typeIDy
        stationID = stationIDy


        if request.method == "POST":
            #request.POST.get("actual-add") ensures that we do not add clients to the database
            #without user going to actual userform
            if request.POST.get("client-actual-add"):

                userID = request.user
                stationIDx= request.POST.get("stationID")
                stationID = StationStng.objects.get(id=stationIDx)
                client_typeIDx= request.POST.get("client-typeID")
                client_typeID = ClientTypeStng.objects.get(id=client_typeIDx)

                first_name = str(request.POST.get("first-name")).upper()
                surname = str(request.POST.get("surname")).upper()
                other_names = str(request.POST.get("other-names")).upper()
                national_identification_number = str(request.POST.get("national-identification-number"))
                gender = str(request.POST.get("gender")).upper()
                date_of_birth = request.POST.get("date-of-birth")
                physical_address = str(request.POST.get("physical-address").upper())
                contact_numbers = request.POST.get("contact-numbers")
                email_address  = request.POST.get("email-address")
                

      
                #Other important information
                district = str(request.POST.get("district")).upper()
                sub_county = str(request.POST.get("sub-county")).upper()
                lc1_village = str(request.POST.get("lc1-village")).upper()
                #Next of Kin info
                next_of_kin1 =str(request.POST.get("next-of-kin1")).upper()
                next_of_kin1_contacts =str(request.POST.get("next-of-kin1-contacts")).upper()
                next_of_kin1_address =str(request.POST.get("next-of-kin1-address")).upper() 
                next_of_kin2 =str(request.POST.get("next-of-kin2")).upper()
                next_of_kin2_contacts =str(request.POST.get("next-of-kin2-contacts")).upper()
                next_of_kin2_address =str(request.POST.get("next-of-kin2-address")).upper()
                #Banking and occuptaion
                occupation = str(request.POST.get("lc1-village")).upper()
                bank_name = str(request.POST.get("bank-name")).upper()
                accountNo = str(request.POST.get("accountNo")).upper()
                ATM_NO = str(request.POST.get("ATM-NO")).upper()
                ATM_PIN = request.POST.get("ATM-PIN")
                employer = str(request.POST.get("employer")).upper()
                employer_address = str(request.POST.get("employer-address")).upper()


                client = Client()
                client.client_typeID = client_typeID
                client.first_name = first_name
                client.surname = surname
                client.other_names = other_names
                client.national_identification_number = national_identification_number
                client.gender = gender
                client.date_of_birth = date_of_birth
                client.physical_address = physical_address
                client.contact_numbers = contact_numbers
                client.email_address = email_address

                
                client.district = district
                client.sub_county = sub_county
                client.lc1_village = lc1_village
                client.next_of_kin1 = next_of_kin1
                client.next_of_kin1_contacts = next_of_kin1_contacts
                client.next_of_kin1_address = next_of_kin1_address
                client.next_of_kin2 = next_of_kin2
                client.next_of_kin1_contacts = next_of_kin2_contacts
                client.next_of_kin2_address = next_of_kin2_address
                client.occupation = occupation
                client.bank_name = bank_name
                client.accountNo = accountNo
                client.ATM_NO = ATM_NO
                client.ATM_PIN = ATM_PIN
                client.employer = employer
                client.employer_address = employer_address
                client.userID = userID
                client.stationID = stationID

                client.save()
                    
                
                #set current client
                global_variables.set_client_typeID(request, int(str(client_typeID.id)))
                global_variables.set_current_client(request,client)
                global_variables.set_current_loan(request,None)
                #now redirec to edit page for more functionality

                return redirect("main:edit-client")

        return render(request, template_name="main/client_view_create_form.html", 
                      context={"stationID":stationID.id, "client_typeID":client_typeID.id})
    


    #Choose user desired values
    #add client functions
    @login_required(login_url="/")
    def edit_client(request):

        client = Client.objects.get(id=request.session["current_clientID"]) 
        client_typeID = client.client_typeID
        stationID = client.stationID
        
        if request.POST.get("actual-edit"):  
                userID = request.user          
                client_typeIDx = request.POST.get("client-typeID")
                stationIDx = request.POST.get("stationID")
                first_name = str(request.POST.get("first-name")).upper()
                surname = str(request.POST.get("surname")).upper()
                other_names = str(request.POST.get("other-names")).upper()
                national_identification_number = str(request.POST.get("national-identification-number")).upper()
                gender = str(request.POST.get("gender")).upper()

                try:
                   date_of_birth = request.POST.get("date-of-birth")
                except:
                    pass
                physical_address = str(request.POST.get("physical-address")).upper()
                contact_numbers = request.POST.get("contact-numbers").upper()
                email_address  = request.POST.get("email-address")
                
                national_id = request.FILES.get("national-id")
                client_img = request.FILES.get("client-img")
                #Other important information
                district = str(request.POST.get("district")).upper()
                sub_county = str(request.POST.get("sub-county")).upper()
                lc1_village = str(request.POST.get("lc1-village")).upper()
                #Next of Kin info
                next_of_kin1 =str(request.POST.get("next-of-kin1")).upper()
                next_of_kin1_contacts =str(request.POST.get("next-of-kin1-contacts")).upper()
                next_of_kin1_address =str(request.POST.get("next-of-kin1-address")).upper()
                next_of_kin2 =str(request.POST.get("next-of-kin2")).upper()
                next_of_kin2_contacts =str(request.POST.get("next-of-kin2-contacts")).upper()
                next_of_kin2_address =str(request.POST.get("next-of-kin2-address")).upper()
                #Banking and occuptaion
                occupation = str(request.POST.get("lc1-village")).upper()
                bank_name = str(request.POST.get("bank-name")).upper()
                accountNo = str(request.POST.get("accountNo")).upper()
                ATM_NO = str(request.POST.get("ATM-NO")).upper()
                ATM_PIN = request.POST.get("ATM-PIN").upper()
                employer = str(request.POST.get("employer")).upper()
                employer_address = str(request.POST.get("employer-address")).upper()
             

                if client_typeIDx is not None:
                   client_typeID = ClientTypeStng.objects.get(id=client_typeIDx)
                if stationIDx is not None:
                   stationID = StationStng.objects.get(id=stationIDx)

                client.stationID = stationID
                client.client_typeID = client_typeID
                client.first_name = first_name 
                client.surname = surname
                client.other_names = other_names
                client.national_identification_number = national_identification_number
                client.gender = gender
                try:
                   client.date_of_birth = date_of_birth
                except:
                    pass
                client.physical_address = physical_address
                client.contact_numbers = contact_numbers
                client.email_address = email_address

                #dealing with files
                if national_id is not None:
                    client.client_national_id = national_id
                if client_img is not None:
                   client.client_img= client_img

                client.district = district
                client.sub_county = sub_county
                client.lc1_village = lc1_village
                client.next_of_kin1 = next_of_kin1
                client.next_of_kin1_contacts = next_of_kin1_contacts
                client.next_of_kin1_address = next_of_kin1_address
                client.next_of_kin2 = next_of_kin2
                client.next_of_kin2_contacts = next_of_kin2_contacts
                client.next_of_kin2_address = next_of_kin2_address
                client.occupation = occupation
                client.bank_name = bank_name
                client.accountNo = accountNo
                client.ATM_NO = ATM_NO
                client.ATM_PIN = ATM_PIN
                client.employer = employer
                client.employer_address = employer_address
                client.userID = userID
                
                #saving the posted info
                client.save()

        def set_context_variables(client):
            """
            This is a function inside the edit_client() function
            It helps us to set the context for the edit client function, which contect
            we send to the edit_client html page
            """
            clientID = client.id
            stationID = client.stationID
            client_typeID=client.client_typeID
            first_name= client.first_name
            surname = client.surname
            other_names=client.other_names
            national_identification_number = client.national_identification_number
            gender = client.gender   
            if gender =="M": 
                gender_string ="Male"
            elif gender=="F":
                gender_string = "Female" 
            else:  
                gender_string = "NA"  

            #preparing date of birth     
            date_of_birthx =str(client.date_of_birth)
            date_of_birthy = date_of_birthx.split(" ")
            date_of_birth = date_of_birthy[0]

            physical_address=client.physical_address
            contact_numbers = client.contact_numbers
            email_address = client.email_address

            #dealing with files
            national_id=client.client_national_id
            client_img = client.client_img
            

            district = client.district
            sub_county = client.sub_county
            lc1_village = client.lc1_village
            next_of_kin1 = client.next_of_kin1
            next_of_kin1_contacts = client.next_of_kin1_contacts
            next_of_kin1_address = client.next_of_kin1_address
            next_of_kin2 = client.next_of_kin2
            next_of_kin2_contacts = client.next_of_kin2_contacts
            next_of_kin2_address = client.next_of_kin2_address
            occupation = client.occupation
            bank_name = client.bank_name
            accountNo = client.accountNo
            ATM_NO = client.ATM_NO
            ATM_PIN = client.ATM_PIN
            employer = client.employer
            employer_address = client.employer_address

            stationID_id= stationID.id
            stationID_name= stationID.station_name
            client_typeID_id = client_typeID.id
            client_typeID_name = client_typeID.client_type_name


            global_variables.set_current_client(request, client) 
            get_global_db_objects = global_variables.get_global_db_objects(request)
             
            context_obj={"stationID_id":stationID_id,"stationID_name":stationID_name, 
                        "client_typeID_id":client_typeID_id, "client_typeID_name":client_typeID_name,
                        "clientID":clientID,"stationID":stationID, "client_typeID":client_typeID,
                        "first_name": first_name, "surname":surname,"other_names":other_names,
                        "national_identification_number":national_identification_number,"national_id":national_id,
                        "gender":gender,"gender_string":gender_string, "date_of_birth":date_of_birth,"physical_address":physical_address, 
                        "contact_numbers":contact_numbers,"email_address":email_address,"client_img":client_img,
                        "district":district,"sub_county":sub_county,"lc1_village":lc1_village,
                        "next_of_kin1":next_of_kin1, "next_of_kin1_contacts":next_of_kin1_contacts,
                        "next_of_kin1_address":next_of_kin1_address, "next_of_kin2":next_of_kin2, 
                        "next_of_kin2_contacts":next_of_kin2_contacts, "next_of_kin2_address":next_of_kin2_address,
                        "occupation":occupation, "bank_name": bank_name,"accountNo":accountNo,
                        "ATM_NO":ATM_NO, "ATM_PIN" : ATM_PIN,"employer":employer, "employer_address":employer_address,
                        "get_global_db_objects": get_global_db_objects,                         
                        }
            return context_obj  

        return render(request, template_name="main/client_view_edit_form.html", 
                        context=set_context_variables(client))#context edns here
    



    @login_required(login_url="/")
    def search_for_a_client(request):

        client = None
        clients_byid = None
        clients_by_NIN = None
        clients_by_fullnames=None
        clients_by_fullnames= None
        clients_by_contacts=None
        station = StationStng.objects.get(id = request.session["current_stationID"])
        
        
        if request.POST.get("client-search"):
            
            #settin the search string
            search_query = request.POST.get("client-search")
            
            try:
                #using clientID
                if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                   clients_byid = Client.objects.filter(id=search_query) 
                else:
                   clients_byid = Client.objects.filter(id=search_query, stationID = station)                                
            except: 
                clients_byid = None

            try:
                #using client full_names
                if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                   clients_by_fullnames = Client.objects.filter(full_name__icontains=search_query)
                else:
                   clients_by_fullnames = Client.objects.filter(full_name__icontains=search_query, stationID = station)
            except: 
                clients_by_fullnames = None
            try:
                    #using contacts
                if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                   clients_by_contacts = Client.objects.filter(contact_numbers__icontains=search_query) 
                else:
                   clients_by_contacts = Client.objects.filter(contact_numbers__icontains=search_query,  stationID = station)  
            except:
                clients_by_contacts = None
            try:
                #using NIN
                if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                   clients_by_NIN = Client.objects.filter(national_identification_number=search_query) 
                else:
                   clients_by_NIN = Client.objects.filter(national_identification_number=search_query,  stationID = station) 
            except:
                clients_by_NIN = None

        return render(request, template_name="main/search_for_a_client.html",
                       context={"clients_byid":clients_byid, "clients_by_NIN":clients_by_NIN,
                       "clients_by_fullnames":clients_by_fullnames, "clients_by_contacts":clients_by_contacts})#context edns here
    
   

    
    @login_required(login_url="/")
    def set_search_for_a_client(request,id):
        """
        Function picks id from url, sets clientid,fullname and balance and then redirects back home
        """
        try:
          client = Client.objects.get(id=id)
          global_variables.set_current_client(request,client)
        except:
            pass
        
        try:
           if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                loan = Loan.objects.filter(clientID =client).order_by("-id")[0]
           else:
               station = StationStng.objects.get(id=request.session["current_stationID"])
               loan = Loan.objects.filter(clientID =client, stationID=station).order_by("-id")[0]


           #set current loan
           global_variables.set_current_loan(request, loan)
        except:
            #set current loan
            global_variables.set_current_loan(request, None)

       
        return redirect("main:index")




    @login_required(login_url="/")
    def set_prev_client(request):
        try: 
           station = StationStng.objects.get(id=request.session["current_stationID"])
           if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
              client = Client.objects.filter(id__lt=request.session["current_clientID"]).order_by("-id")[0] 
           else:
              client = Client.objects.filter(id__lt=request.session["current_clientID"], stationID=station).order_by("-id")[0] 
           global_variables.set_current_client(request, client)
        except:
            pass

        try:
           if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
               loan = Loan.objects.filter(clientID =client).order_by("-id")[0]
           else:
              loan = Loan.objects.filter(stationID=station, clientID =client).order_by("-id")[0]

           global_variables.set_current_loan(request, loan)
           
        except:
           global_variables.set_current_loan(request,None)

        return redirect("main:index")
    


    @login_required(login_url="/")
    def set_next_client(request):

        station = StationStng.objects.get(id=request.session["current_stationID"])
        try: 
           
           if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
              client = Client.objects.filter(id__gt=request.session["current_clientID"]).order_by("id")[0]
           else:
              client = Client.objects.filter(id__gt=request.session["current_clientID"],
                                          stationID=station).order_by("id")[0]
           global_variables.set_current_client(request, client)
        except:
            pass

        try:
           if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
               loan = Loan.objects.filter(clientID =client).order_by("-id")[0]
           else:
              loan = Loan.objects.filter(clientID =client, stationID = station).order_by("-id")[0]
           global_variables.set_current_loan(request, loan)
        except:
            global_variables.set_current_loan(request,None)

        return redirect("main:index")




    def edit_book(self, request):

        try: 
            user_station = request.session["current_stationID"]
            user_station = None
        except: 
            return redirect('main:index')
        
        if not (request.session["current_stationID"]):
            return redirect('main:index')

        if not (request.session["current_stationID"]):
            return redirect('main:index')
    
        client_id = int(request.POST.get("edit-client-rows"))

        client_book = Client.objects.get(id=client_id)

        if int(request.POST.get("no-of-rows")) == 0:
            try:
               track_book = Track_auto_item_adds.objects.get(clientID = client_book,
                                                            item_name="borrowers_book", closed = False)
               track_book.closed = True
               track_book.save()
            except:
                track_book = Track_auto_item_adds()
                track_book.clientID = client_book
                track_book.stationID = client_book.stationID
                track_book.closed = False
                track_book.item_name="borrowers_book"
                track_book.save()


        
        

            
        client_book.borrowers_book_record = int(request.session["records_in_borrowers_book"]) - int(request.POST.get("no-of-rows"))
        #client_book.borrowers_book_record = 10
        client_book.save()

        adjust_reason = Report()
               
        loan = Loan.objects.get(id= int(request.session["current_loanID"]))
        adjust_reason.loanID = loan
        adjust_reason.clientID = loan.clientID
        adjust_reason.stationID = loan.stationID
        adjust_reason.report_text = 'Remaining lines were: ' + str(request.POST.get("no-of-rows")) + \
                                    '\n | Reason :' + request.POST.get('adjust-reason')  
        #selecting report type
        report_type = ReportTypeStng.objects.get(report_name = 'record-book-adjustment')
        adjust_reason.report_typeID = report_type
        adjust_reason.userID = request.user
        #saving into report records
        adjust_reason.save()

        global_variables.set_current_client(request, client_book)
        return redirect("main:index")

    


    def book_adjustment_report(request):

        try: 
            user_station = request.session["current_stationID"]
            user_station = None
        except: 
            return redirect('main:index')
        
        station = StationStng.objects.get(id = int(request.session['current_stationID']))
        report_type = ReportTypeStng.objects.get(report_name = 'record-book-adjustment')
        book_list = None
     
        
        if request.POST.get('date1') and request.POST.get('date2'):
            date1  = request.POST.get("date1")
            date2_str = datetime.strptime(request.POST.get("date2"), '%Y-%m-%d')+ timedelta(days=1)
            date2_obj = str(date2_str).split("-")
            date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2] 
        else:
            #by default, todays data is immediately loaded
            today = datetime.today()
            year= today.year
            month = today.month
            day = today.day
            date1 = str(year)+"-"+str(month)+"-"+str(day)               
            date2_str = today + timedelta(days=1)
            date2_obj = str(date2_str).split("-")
            date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2]

        
        #we used the if statement to get date1 nd date2 appropriately so now all we do is 
        #select from the database
        if 1==1:
            try:
                if global_variables.user_rights(request.user, "allow_to_view_other_stations")=="Yes":
                    if request.POST.get("station-id") and not(request.POST.get("station-id")=='0') \
                                                      and not(request.POST.get("station-id")==0):

                        station = StationStng.objects.get(id= int(request.POST.get("station-id")))
                        report_list = Report.objects.filter(
                                                record_date__gte=date1, 
                                                record_date__lte=date2,
                                                report_typeID = report_type,
                                                stationID = station,
                                                )
                    else:
                        #by deafult a person with rights will view all records from their station
                        report_list = Report.objects.filter(
                                                record_date__gte=date1, 
                                                record_date__lte=date2,
                                                report_typeID = report_type,
                                                )
                else:
                   #by deafult a person will view only records from their station
                   report_list = Report.objects.filter(
                                                record_date__gte=date1,
                                                record_date__lte=date2,
                                                report_typeID = report_type,
                                                stationID = station,
                                                )
            except:
               pass




        return render(request, template_name="main/book_adjustment_report.html",
                       context={"report_list":report_list,"date1":date1, "date2":date2, 'station':station,
                        "get_global_db_objects":global_variables.get_global_db_objects(request),})#context edns here



    
    def set_client_all_time_balance(request):
        
        try:
            x = request.session["current_stationID"]
            x = None
        except:
            return redirect('main:index')

        if global_variables.user_rights(request.user, "allow_to_adjust_loan_balance")=="Yes":
            pass
        else:
            return redirect('main:index') 

        client = Client.objects.get(id= int(request.session["current_clientID"]))
        client.current_total_balance = request.POST.get("all-balance")
        request.session["current_client_balance"] = int(request.POST.get("all-balance"))
        client.save()

