from django.contrib.sites.models import Site
from django.db import models
from ittybitty.utils import gen_shortcut

SITE = Site.objects.get_current()

class IttyBittyURL(models.Model):
    """
    The Itty Bitty URL model that is responsible for matching shortcuts up with
    a real URL.
    """
    shortcut = models.CharField(max_length=10, blank=True, unique=True)
    url = models.URLField(unique=True)
    hits = models.PositiveIntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.url

    def get_shortcut(self):
        return 'http://%s/%s' % (SITE.domain, self.shortcut)

    class Meta:
        ordering = ('-date_created', 'shortcut')
        verbose_name = 'Itty Bitty URL'
        verbose_name_plural = 'Itty Bitty URLs'

def set_shortcut(sender, instance, created, *args, **kwargs):
    """
    Generates the shortcut for an Itty Bitty URL object if it hasn't already
    been generated.
    """
    if not instance.shortcut:
        instance.shortcut = gen_shortcut(instance.id)
        instance.save()
    return instance
models.signals.post_save.connect(set_shortcut, sender=IttyBittyURL)
