# forecast/tasks.py
from celery import shared_task
from .management.commands.train_forecast import Command as TrainForecastCommand

@shared_task
def retrain_forecast():
    cmd = TrainForecastCommand()
    cmd.handle()
