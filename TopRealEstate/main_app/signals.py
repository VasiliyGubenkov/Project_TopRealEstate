from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Rating, Advert, AdvertDates
from django.db.models.signals import post_save


@receiver(post_save, sender=Rating)
@receiver(post_delete, sender=Rating)
def update_advert_rating(sender, instance, **kwargs):
    instance.advert.update_average_rating()



@receiver(post_save, sender=Advert)
def create_advert_dates(sender, instance, created, **kwargs):
    if created:
        AdvertDates.objects.create(advert=instance)
    else:
        # Обновляем даты, если Advert уже существует
        advert_dates, created = AdvertDates.objects.get_or_create(advert=instance)
        advert_dates.update_dates()
        advert_dates.save()

