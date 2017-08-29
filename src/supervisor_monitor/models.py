from django.db import models
from django.forms.widgets import PasswordInput
# Create your models here.
from .monitor import Monitor


class Supervisor(models.Model):
    url = models.URLField(help_text="supervisor web url")
    identification = models.CharField(max_length=254, help_text="supervisor server identification", unique=True)
    username = models.CharField(max_length=128, null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return "<Supervisor:{}>".format(self.identification)

    def getPid(self):
        with self.monitor() as sp:
            return sp.getPid()

    def monitor(self):
        monitor = Monitor(self.url, self.username, self.password)
        return monitor

    def reload(self):
        print("reload",self.monitor().reload())

    def restart(self):
        self.monitor().reboot()

    def status(self):
        return self.monitor().getStatus()

    def getServiceList(self):
        try:
            res = list(self.monitor().getServiceIter())
        except:
            res = list(self.services.all().values())
        return res


    def refresh_services(self):
        for service_info in self.monitor().getServiceIter():
            ss,_ = SupervisorService.objects.get_or_create(
                supervisor=self,
                name=service_info['name'],
                group=service_info['group']
            )


class SupervisorService(models.Model):
    supervisor = models.ForeignKey(
        Supervisor,
        on_delete=models.CASCADE,
        related_name='services'
    )
    name = models.CharField(max_length=254)
    group = models.CharField(max_length=254)

    pid = models.IntegerField()
    state = models.IntegerField()
    start_timestamp = models.PositiveIntegerField()
    stop_timestamp = models.PositiveIntegerField()
    now_timestamp = models.PositiveIntegerField()
    exit_status = models.IntegerField()
    modify_time = models.DateTimeField(auto_now=True, null=True)

    def status(self):
        status = self.supervisor.monitor().getProcessStatus(self.name)
        return status['state']

    def description(self):
        status = self.supervisor.monitor().getProcessStatus(self.name)
        return status['description']

    def stop(self):
        self.supervisor.monitor().stop(self.name)

    def start(self):
        self.supervisor.monitor().start(self.name)

    def restart(self):
        self.supervisor.monitor().restart(self.name)

    def __str__(self):
        return "<Service:{}({})>".format(self.name, self.group)

from . import trigger


