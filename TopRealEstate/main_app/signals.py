from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Rating, Advert

@receiver(post_save, sender=Rating)
@receiver(post_delete, sender=Rating)
def update_advert_rating(sender, instance, **kwargs):
    instance.advert.update_average_rating()
