
import time
from  pivot_tabling import PivotTabling


run_pivots = PivotTabling()


#this is the main function that updates interest and totals



while True:
   #Other variables
   #Instance is created
   time.sleep(2)
   run_pivots.update_interest_and_totals()
