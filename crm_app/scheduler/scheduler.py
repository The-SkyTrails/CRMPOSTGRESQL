from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from django.core.management import call_command
def backup_every_one_hour():
    
    call_command('dbbackup', clean=True)


@util.close_old_connections
def delete_old_job_executions(max_age=2):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
    

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(),"default")
    scheduler.add_job(backup_every_one_hour,'interval',hours=1,jobstore='default',id="backup_every_one_hour",replace_existing=True)
    
    scheduler.add_job(delete_old_job_executions,'interval',seconds=10,jobstore='default',id="delete_old_job_executions",replace_existing=True)

    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()