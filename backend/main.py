from application import create_app 
from celery.schedules import crontab
from application.tasks import daily_remainders,monthly_remainders,revoke_overdues
from application.worker import celery_init_app
app=create_app()

celery_app=celery_init_app(app)
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Testing.
    #sender.add_periodic_task(10, daily_remainders.s(), name='daily remainder')
    #sender.add_periodic_task(60, monthly_remainders.s(), name='monthly report')
    sender.add_periodic_task(crontab(minute=0,hour=19), daily_remainders.s(), name='daily remainder') #7pm
    sender.add_periodic_task(crontab(0, 0, day_of_month='1'), monthly_remainders.s(), name='monthly report') #1stday
    sender.add_periodic_task(crontab(), revoke_overdues.s(), name='Revoke access') # every min
if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)