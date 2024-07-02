
from django_cron import CronJobBase,  Schedule
from main.models import Track_auto_item_adds


track_trigger = Track_autoitem_adds()
track_trigger.triger_status =1
track_trigger.save()