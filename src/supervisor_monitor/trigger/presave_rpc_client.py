from django.db.models.signals import pre_save
from django.dispatch import receiver
from ..models import Supervisor

from ..monitor import getIdentification


@receiver(pre_save, sender=Supervisor)
def rpc_identification_get(sender, instance, **kwargs):
    assert isinstance(instance, Supervisor)
    if not instance.identification:
        instance.identification = getIdentification(instance.url, instance.username, instance.password)
