Xlender
=======================
Xlender is a money lender system created in Django, Python, MySQL, CSS and HTML
It demonstrates MySQL optimization through denormalization and indexing when ever necessary. 
Denormalization save us from slow complex join quieries.
The system also demonstrates custom rights management per user in the frontend.
Finally a busniess owner can own a multi station business

Installation Part 1
=======================================================================
1. Use command prompt to navigate into the easylender folder
2. Intall requiremnts.txt
3. Create django super user
4. Run django server and go to the admin:
5. Add A business name and a station name
6. Add users and eployees
7. Navigate to Custom user rights and give your self rights, but dont add the same right twice
8. Navigate to Loan Types and enter loan types namely: i. Daily loans, ii. Monthly loans
9. Navigate to System Custom Settings and add the following
	1. Settings Name =defaulter_grace_period, User Friendly Name= Defaulter Grace Period, Value =3, Allow = True
	2. Settings Name =defaulter_interest, User Friendly Name= Defaulter's Interest(%100), Value =30, Allow = True
	3. Settings Name =records_in_borrowers_book, User Friendly Name= How many records can the borrowers book take?, Value =61, Allow = True
	4. Settings Name =daily_principle_pay_percent, User Friendly Name= Daily principle Payment(100%), Value =83.5, Allow = True
	5. Settings Name =loan_duration, User Friendly Name= Loan Duration, Value =30, Allow = True
	6. Settings Name =default_client_typeID, User Friendly Name= Default Client TypeID, Value =1, Allow = True
	7. Settings Name =daily_interest_increment, User Friendly Name= Daily Interest(%100), Value =20, Allow = True
	8. Settings Name =allow_daily_partial_payments, User Friendly Name= Allow Daily Partial Payments, Value =None, Allow = True
	9. Settings Name =loan_interest_percent, User Friendly Name= Loan Interest (%100), Value =20, Allow = True
	10. Settings Name =max_court_days, User Friendly Name= How many days to add court Queue, Value =90, Allow = True

Installation Part 2
=======================================================================
This includes intallation of custom scripts 
They run in the background and add fines to loan defaulters
1. Use command prompt to navigate into the custom_scripts folder
2. Create for it a separate directory, create a virutal environment and install requirements.tx
3. Run main.py

   Lastly
   ========================================================================
    Now you can add clients, give out loans, pay loans and view reports
   

 
