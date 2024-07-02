import mysql.connector
from mysql.connector import Error
from datetime import timezone, timedelta, date
import datetime

#my constatnts
HOST = '127.0.0.1'
DATABASE = 'lenderdb'
USERNAME = 'root'
PASSWORD = ''

#Connection is to mysql server version 5.7.31
try:
    connection =mysql.connector.connect(host=HOST, database=DATABASE, user=USERNAME, password=PASSWORD, auth_plugin='mysql_native_password')
    if connection.is_connected():
        #db_info = connection.get_server_info()
        #print("connected to mysql server version", db_info)
        pass
except Error as e:
    err_message = f"Error connecting to server {e}"



#creating a database instance cursor
db_cursor = connection.cursor(dictionary=True, buffered=True)



#picking loan general interest percentage for use on monthly and other loans calculation updates
qry_select_loan_general_interest = "SELECT * FROM main_systemcustomsettings WHERE " \
"settings_name ='defaulter_interest'"
db_cursor.execute(qry_select_loan_general_interest)
loan_interest_set = db_cursor.fetchone()
DETAULTER_LOAN_INTEREST = loan_interest_set["settings_value"]


#picking number of days a client with balance >0 takes to get into defaulters list
qry_loan_duration_days = "SELECT * FROM main_systemcustomsettings WHERE " \
"settings_name ='loan_duration'"
db_cursor.execute(qry_loan_duration_days)
loan_duration_days_set = db_cursor.fetchone()
LOAN_DURATION_DAYS= loan_duration_days_set["settings_value"]



qry_defaulter_grace_period = "SELECT * FROM main_systemcustomsettings WHERE " \
"settings_name ='defaulter_grace_period'"
db_cursor.execute(qry_defaulter_grace_period)
defaulter_grace_period_set = db_cursor.fetchone()
FINES_GRACE_PERIOD = defaulter_grace_period_set["settings_value"]



qry_max_court_days = "SELECT * FROM main_systemcustomsettings WHERE " \
"settings_name ='max_court_days'"
db_cursor.execute(qry_max_court_days)
max_court_days_set = db_cursor.fetchone()
MAX_COURT_DAYS_COUNT = max_court_days_set["settings_value"]



#getting a set of all stations that we have
qry_stations = "SELECT * FROM main_stationstng"
db_cursor.execute(qry_stations)
STATIONS_SET = db_cursor.fetchall()




class PivotTabling():
    def update_fines(self):  

        #checking whether execution occured today
        #if some days where skipped, that will automatically coverup
        #check whether execution has been done today
        qry_select_trigger_checker = "SELECT DATEDIFF(UTC_TIMESTAMP, record_date) AS date_diff " \
        " , record_date, id FROM main_tbl_trigger_checker " \
        " WHERE DATEDIFF(UTC_TIMESTAMP, record_date) = 0 ORDER BY id DESC LIMIT 1"
        
        #check last date entry was made
        qry_select_max_trigger_checker_max = "SELECT DATEDIFF(UTC_TIMESTAMP, record_date) AS date_diff " \
        " , record_date, id FROM main_tbl_trigger_checker  ORDER BY id DESC LIMIT 1"

        
        db_cursor.execute(qry_select_trigger_checker)
        res_select_trigger_checker = db_cursor.fetchone()
        
        db_cursor.execute(qry_select_max_trigger_checker_max)
        res_select_trigger_checker_max = db_cursor.fetchone()
        date_diff = 0
        if res_select_trigger_checker_max:
           date_diff = res_select_trigger_checker_max["date_diff"]

       

        if res_select_trigger_checker is None: #means execution hasnt been done yet today
            
            if res_select_trigger_checker_max is None:   
                date_diff=1
            #Then execute for today
            #running the updates
            #Execute missing updates for date_diff days
            #if the server was off for more than date_diff days, then the programmer has to deal with it from here
            for day_counter in range(date_diff): #we want to run date_diff days
                counter_executer = day_counter + 1#because we enter defaulters from yesterday
                if not(counter_executer > date_diff):
                    print("Eexcuter:  "+str(counter_executer))
                    print("======================================================")
                    if int(date_diff) < 60:
                       self.update_monthly_pay_back_first_time(counter_executer)#for special care of grace period
                    self.update_monthly_pay_back(counter_executer)#for the case of other monthly pay backs
                    self.append_to_court_queue(counter_executer)

            #finally marking off today as finished execution
            qry_insert_trigger_checker = "INSERT INTO main_tbl_trigger_checker " \
                "(triger_status, record_date)  VALUES (1, UTC_TIMESTAMP) "
            db_cursor.execute(qry_insert_trigger_checker)    
        else:
            #do nothing since execution has already been done
            print("Updates already done")
        
        #commit the transactions
        #this line is always execued last
        connection.commit()
        print("Success, execution finished ====")




    def update_monthly_pay_back_first_time(self, date_diff):
        print(int(LOAN_DURATION_DAYS)+int(FINES_GRACE_PERIOD)+date_diff)
        print("=============================================")
        print(int(FINES_GRACE_PERIOD)+int(date_diff))
        print("++++++++++++++===========================")

        if int(FINES_GRACE_PERIOD) >0:

           

            #select all the monthly loans with this specific date diff and balance>0

            #we select where loan_typeID not 1, since 1 is daily. So we cater for all others from here
            qry_select_loans_with_balance = "SELECT * FROM main_loan " \
                    " WHERE stop_loan_counting=0 AND current_balance >0 AND  " \
                    " DATEDIFF(UTC_TIMESTAMP, record_date) = %s"

            day_of_month_diff_set =((int(LOAN_DURATION_DAYS)+int(FINES_GRACE_PERIOD)+int(date_diff)),)
            db_cursor.execute(qry_select_loans_with_balance, day_of_month_diff_set)
            monthly_loans = db_cursor.fetchall()
        else:
            qry_select_loans_with_balance = "SELECT * FROM main_loan " \
                    " WHERE stop_loan_counting=0 AND current_balance >0 AND  " \
                    " DATEDIFF(UTC_TIMESTAMP, record_date) = %s"

            day_of_month_diff_set =((int(LOAN_DURATION_DAYS)+int(date_diff)),)
            db_cursor.execute(qry_select_loans_with_balance, day_of_month_diff_set)
            monthly_loans = db_cursor.fetchall()

        if True:
            #print(monthly_loans)

            for loan in monthly_loans:
                    loanID = loan["id"]
                    clientID =loan["clientID_id"]
                    stationID = loan["stationID_id"]
                    principle = loan["principle"]
                    current_principle = loan["current_principle"]
                    full_name = loan["full_name"]
                    original_interest = loan["original_interest"]
                    current_interest = loan["current_interest"]
                    total_loan_interest = loan["total_loan_interest"]
                    current_balance = loan["current_balance"]
                    fines = loan["total_fines"]


                    #selecting the station for its percentage                   
                    qry_get_defaulter_percent = "SELECT * FROM main_stationstng " \
                        " WHERE id = %s"
                    station_id_set = (loan["stationID_id"],)
                    db_cursor.execute(qry_get_defaulter_percent, station_id_set)
                    this_station = db_cursor.fetchone()
                    
                    if loan["loan_typeID_id"] == 1:
                       defualter_percent = int(this_station["defaulters_percent"]) or 0
                    elif loan["loan_typeID_id"] == 2:
                       defualter_percent = int(this_station["monthly_defaulters_percent"]) or 0
                    else:
                        defualter_percent = int(DETAULTER_LOAN_INTEREST)


                    #getting current principle and current interest 
                    if  defualter_percent > 0:
                        new_current_interest =  current_balance *(float(defualter_percent)/100)
                    else:
                       new_current_interest =  current_balance *(float(DETAULTER_LOAN_INTEREST)/100)

                    new_current_balance =current_balance + new_current_interest
                    record_date = datetime.datetime.now(timezone.utc) - timedelta(days = (int(date_diff)-1))

                    #First insert into the interest Table
                    qry_interest_insert_today = "INSERT INTO main_interest " \
                            "(clientID_id, stationID_id, loanID_id, full_name, original_principle, " \
                            "current_principle, original_interest, amount,  record_date) " \
                            "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    val_tupple =(clientID, stationID, loanID, full_name, principle,
                                    current_principle, original_interest, new_current_interest, record_date)
                    db_cursor.execute(qry_interest_insert_today, val_tupple)


                    #then we have to update the loan as per this daily pay interest increment
                    qry_loan_update = "UPDATE main_loan SET " \
                                        "current_principle = %s, " \
                                        "current_balance = current_balance + %s, " \
                                        "current_interest = %s, " \
                                        "total_fines = total_fines + %s, " \
                                        "total_loan_interest =total_loan_interest + %s " \
                                        "WHERE id = %s"
                    val_loan_uppdate_set=(current_principle, new_current_interest, new_current_interest,
                                        new_current_interest, new_current_interest, loanID)
                    db_cursor.execute(qry_loan_update, val_loan_uppdate_set)

                    #Finally update the client balance
                    qry_update_client_balance  = "UPDATE main_client SET " \
                                                "current_total_balance =current_total_balance + %s  " \
                                                "WHERE id = %s"
                    val_update_client_balance_set =(new_current_interest, clientID)
                    db_cursor.execute(qry_update_client_balance, val_update_client_balance_set)






    def update_monthly_pay_back(self, date_diff):

        #select all the monthly loans with this specific date diff and balance>0

        #we select where loan_typeID not 1, since 1 is daily. So we cater for all others from here
        qry_select_loans_with_balance = "SELECT * FROM main_loan " \
                "WHERE stop_loan_counting=0 AND current_balance > 0 AND  " \
                " MOD(DATEDIFF(UTC_TIMESTAMP, record_date), 30)= %s AND " \
                " DATEDIFF(UTC_TIMESTAMP, record_date) > 60"
        day_of_month_diff_set =(int(date_diff),)
        db_cursor.execute(qry_select_loans_with_balance, day_of_month_diff_set)

        monthly_loans = db_cursor.fetchall()

        for loan in monthly_loans:
                loanID = loan["id"]
                clientID =loan["clientID_id"]
                stationID = loan["stationID_id"]
                principle = loan["principle"]
                current_principle = loan["current_principle"]
                full_name = loan["full_name"]
                original_interest = loan["original_interest"]
                current_interest = loan["current_interest"]
                total_loan_interest = loan["total_loan_interest"]
                current_balance = loan["current_balance"]
                fines = loan["total_fines"]
                #getting current principle and current interest  


                #selecting the station for its percentage                   
                qry_get_defaulter_percent = "SELECT * FROM main_stationstng " \
                    " WHERE id = %s"
                station_id_set = (loan["stationID_id"],)
                db_cursor.execute(qry_get_defaulter_percent, station_id_set)
                this_station = db_cursor.fetchone()
                defualter_percent = int(this_station["defaulters_percent"]) or 0

                #getting current principle and current interest 
                if  defualter_percent > 0:
                    new_current_interest =  current_balance *(float(defualter_percent)/100)
                else:
                    new_current_interest =  current_balance *(float(DETAULTER_LOAN_INTEREST)/100)

                #new_current_interest =  current_balance *(float(DETAULTER_LOAN_INTEREST)/100)
                new_current_balance =current_balance + new_current_interest
                record_date = datetime.datetime.now(timezone.utc) - timedelta(days = (int(date_diff)-1))

                #First insert into the interest Table
                qry_interest_insert_today = "INSERT INTO main_interest " \
                        "(clientID_id, stationID_id, loanID_id, full_name, original_principle, " \
                        "current_principle, original_interest, amount,  record_date) " \
                        "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val_tupple =(clientID, stationID, loanID, full_name, principle,
                                current_principle, original_interest, new_current_interest, record_date)
                db_cursor.execute(qry_interest_insert_today, val_tupple)


                #then we have to update the loan as per this daily pay interest increment
                qry_loan_update = "UPDATE main_loan SET " \
                                    "current_principle = %s, " \
                                    "current_balance =  %s, " \
                                    "current_interest = %s, " \
                                    "total_fines =  total_fines + %s, " \
                                    "total_loan_interest =total_loan_interest + %s " \
                                    "WHERE id = %s"
                val_loan_uppdate_set=(current_principle, new_current_balance, new_current_interest,
                                    new_current_interest, new_current_interest, loanID)
                db_cursor.execute(qry_loan_update, val_loan_uppdate_set)

                #Finally update the client balance
                qry_update_client_balance  = "UPDATE main_client SET " \
                                            "current_total_balance =current_total_balance + %s  " \
                                            "WHERE id = %s"
                val_update_client_balance_set =(new_current_interest, clientID)
                db_cursor.execute(qry_update_client_balance, val_update_client_balance_set)



                #Update CourtQueue
                qry_courtqueue_update = "UPDATE main_courtqueue SET " \
                                    " loan_debt = loan_debt + %s " \
                                    " WHERE loanID_id = %s"
                val_courtqueue_update_set=(new_current_interest, loanID)
                db_cursor.execute(qry_courtqueue_update, val_courtqueue_update_set)




    def append_to_court_queue(self, date_diff):

        qry_select_loans_for_court_queue = "SELECT * FROM main_loan " \
                    " WHERE sent_to_court=0 AND current_balance > 0 AND  " \
                    " DATEDIFF(UTC_TIMESTAMP, record_date) = %s "
        loans_set =(int(MAX_COURT_DAYS_COUNT)+int(date_diff),)

        db_cursor.execute(qry_select_loans_for_court_queue, loans_set)
        

        loans_for_court = db_cursor.fetchall()

        print("*********************** " + str(int(MAX_COURT_DAYS_COUNT)+int(date_diff)) +" *****************************")
        print("****************************************************")
        print(loans_for_court)
        print("****************************************************")

        for loan in  loans_for_court:
            loanID = loan["id"]
            clientID =loan["clientID_id"]
            stationID = loan["stationID_id"]
            principle = loan["principle"]
            loan_record_date = loan["record_date"]
            full_name = loan["full_name"]
            loan_expected_pay_date = loan["expected_clearance_date"]
            loan_debt= loan["current_balance"]

            record_date = datetime.datetime.now(timezone.utc) - timedelta(days = (int(date_diff)-1))

            qry_insert_court_queue_today = "INSERT INTO main_courtqueue " \
                        "(clientID_id, loanID_id, stationID_id, full_name, loan_principle, " \
                        "loan_expected_pay_date, loan_record_date, loan_debt,remove_from_court_queue, record_date) " \
                        " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val_tupple =(clientID, loanID, stationID,  full_name, principle,
                         loan_expected_pay_date,loan_record_date, loan_debt, 0, record_date,)
            db_cursor.execute(qry_insert_court_queue_today, val_tupple)


            #then we have to update the loan as per this daily pay interest increment
            qry_loan_sent_to_court_update = "UPDATE main_loan SET " \
                                    "sent_to_court = %s " \
                                    "WHERE id = %s"
            val_loan_court_sent_update_set=(1, loanID,)
            db_cursor.execute(qry_loan_sent_to_court_update, val_loan_court_sent_update_set)
        