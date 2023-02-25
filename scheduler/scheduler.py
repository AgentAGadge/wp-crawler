from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
import sys
from hyperlist import service as hyperlistService

APSC_JOB_CRAWL_ORIGINS = 'crawlOriginsJob'

# This is the function you want to schedule - add as many as you want and then register them in the start() function below
def crawl_origins_job():
    """Job performing a crawl of all registered OriginURL in database
    Parameters 
    ---------- 

    Returns
    -------
    
    """
    hyperlistService.crawl_origins()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    #List the jobs to be scheduled
    scheduler.add_job(crawl_origins_job, 'interval', hours=1, 
                      name=APSC_JOB_CRAWL_ORIGINS, jobstore='default', 
                      id = APSC_JOB_CRAWL_ORIGINS, replace_existing=True)

    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...", file=sys.stdout)
