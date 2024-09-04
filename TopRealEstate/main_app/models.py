from django.db import models
from django.contrib.auth.models import User


class CategoryOfRealEstate(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name='Категория жилья',
                            help_text='Создайте категорию жилья, т.е. квартира или частный дом',
                            unique=True,
                            blank=False,
                            null=False,
                            )
    slug = models.SlugField(max_length=100,
                            verbose_name="URL",
                            help_text="Укажите URL-слаг",
                            unique=True,
                            blank=False,
                            null=False,)
    class Meta():
        db_table = 'Категория жилья'
        verbose_name='Категорию жилья'
        verbose_name_plural='Категории жилья'
    def __str__(self):
        return f"{self.name}"


class Advert(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Заголовок обьявления',
                             help_text='Напишите заголовок вашего обьявления',
                             unique=False,
                             blank=False,
                             null=True,
                             default='The owner did not specify a title.',
                             )
    description = models.TextField(verbose_name='Описание',
                                   help_text='Опишите ваш объект недвижимости',
                                   null=True,
                                   blank=False,
                                   default='The owner did not provide a description',
                                   )
    address_city_name = models.CharField(max_length=200,
                                         verbose_name='Город',
                                         help_text='Напишите название населённого пункта',
                                         unique=False,
                                         blank=False,
                                         null=True,
                                         default='The owner did not indicate the name of the city',
                                         )
    address_street_name = models.CharField(max_length=200,
                                           verbose_name='Улица',
                                           help_text='Напишите название улицы',
                                           unique=False,
                                           blank=False,
                                           null=True,
                                           default='The owner did not indicate the street name.',
                                           )
    address_house_number = models.CharField(max_length=100,
                                            verbose_name='Номер дома',
                                            help_text='Напишите номер дома',
                                            unique=False,
                                            blank=False,
                                            null=True,
                                            default='The owner did not indicate the house number',
                                            )
    price = models.DecimalField(max_digits=5,
                                decimal_places=2,
                                verbose_name='Цена',
                                help_text='Напишите цену, за месяц аренды',
                                null=True,
                                blank=False,
                                default=1.00,
                                )
    number_of_rooms = models.PositiveIntegerField(verbose_name='Количечство комнат',
                                                  help_text='Укажите количество комнат',
                                                  null=True,
                                                  blank=False,
                                                  default=1,
                                                  )
    type = models.ForeignKey(CategoryOfRealEstate,
                                            verbose_name='',
                                            help_text='',
                                            on_delete=models.SET_NULL,
                                            related_name='type',
                                            null=True,
                                            blank=False,
                                            default='Flat',
                             )
    created_or_updated_date = models.DateTimeField(auto_now=True,)
    owner = models.ForeignKey(User,
                              verbose_name='Пользователь',
                              help_text='Выберите пользователя, создающего объявление',
                              on_delete=models.CASCADE,
                              related_name='owner',
                              null=True,
                              blank=False,
                              )
    is_active = models.BooleanField(default=True,
                                    verbose_name='Активность обьявления',
                                    help_text='Выберите, активно объявление или нет',
                                    )
    class Meta():
        db_table = 'Объявления'
        ordering = ['title']
        verbose_name='Объявление'
        verbose_name_plural = 'Объявления'
    def __str__(self):
        return f"{self.title}"