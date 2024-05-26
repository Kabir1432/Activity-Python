import os
from django.conf import settings
from celery import Celery

if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

app = Celery('activityngo')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.set_default()
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    # 'Process Electricity Consumption every 1 hour': {
    #         'task': 'smartgen.energy_statistics.tasks.process_electricity_consumption',
    #         'schedule': timedelta(hours=1),
    #         'args': (),
    #     },
}

app.conf.timezone = 'UTC'
