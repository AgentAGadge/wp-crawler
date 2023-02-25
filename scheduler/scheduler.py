"""
    Scheduler app (from apscheduler package)
"""

import sys

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from hyperlist import service as hyperlistService

APSC_JOB_CRAWL_ORIGINS = 'crawlOriginsJob'

def crawl_origins_job():
    """Job performing a crawl of all registered OriginURL in database
    Parameters 
    ---------- 

    Returns
    -------
    
    """
    hyperlistService.crawl_origins()


def start():
    """Start scheduler app method.
    Parameters 
    ---------- 

    Returns
    -------
    
    """
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    #List the jobs to be scheduled
    scheduler.add_job(crawl_origins_job, 'interval', hours=1, 
                      name=APSC_JOB_CRAWL_ORIGINS, jobstore='default', 
                      id = APSC_JOB_CRAWL_ORIGINS, replace_existing=True)

    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...", file=sys.stdout)
