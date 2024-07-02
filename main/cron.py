from datetime import date, datetime, timedelta
from django .utils import timezone
from django_cron import CronJobBase,  Schedule
from main.models import Tbl_trigger_checker
import time

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 5
    RETRY_AFTER = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER)
    code = "main.my_cron_job"

    
    def do(self):

        trigger = None
        go_on = True
        try:
           trigger = Tbl_trigger_checker.objects.all().order_by("-id")[0]
           last_date = str(trigger.record_date).split(" ")
           if last_date[0] in str(datetime.datetime.now()):
               go_on = False
        except:
            go_on = True


        while go_on:
                
                track_trigger = Tbl_trigger_checker()
                track_trigger.triger_status =1
                track_trigger.save()
                go_on = False
  


            





    
    
   
