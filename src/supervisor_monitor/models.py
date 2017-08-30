from django.db import models
from django.forms.widgets import PasswordInput
# Create your models here.
from .monitor import Monitor


class Supervisor(models.Model):
    OFFLINE = -100

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
        try:
            return self.monitor().getStatus()
        except:
            return ""

    def getServiceList(self):
        try:
            res = list(self.monitor().getServiceIter())
        except:
            res = list(self.services.all().values())
        return res


    def refresh_services(self):
        old_names = set(SupervisorService.objects.filter(supervisor=self).values_list("name", flat=True))
        for service_info in self.monitor().getServiceIter():
            if service_info["name"] in old_names:
                old_names.remove(service_info["name"])
            ss, _ = SupervisorService.objects.update_or_create(
                {
                    "group": service_info['group'],
                    "pid": service_info['pid'],
                    "state": service_info['state'],
                    "start_timestamp": service_info["start"],
                    "stop_timestamp": service_info['stop'],
                    "now_timestamp": service_info["now"],
                    "exit_status": service_info["exit_status"]
                },
                supervisor=self,
                name=service_info['name'],
            )
        SupervisorService.objects.filter(supervisor=self, name__in=list(old_names)).delete()

class SupervisorService(models.Model):
    OFFLINE = -100
    STOPPED = 0
    STARTING = 10
    RUNNING = 20
    BACKOFF = 30
    STOPPING = 40
    EXITED = 100
    FATAL = 200
    UNKNOWN = 1000

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
        try:
            status = self.supervisor.monitor().getProcessStatus(self.name)
            return status['state']
        except:
            return -100

    def description(self):
        try:
            status = self.supervisor.monitor().getProcessStatus(self.name)
            return status['description']
        except:
            return ""

    def stop(self):
        self.supervisor.monitor().stop(self.name)

    def start(self):
        self.supervisor.monitor().start(self.name)

    def restart(self):
        self.supervisor.monitor().restart(self.name)

    def __str__(self):
        return "<Service:{}({})>".format(self.name, self.group)

from . import trigger


