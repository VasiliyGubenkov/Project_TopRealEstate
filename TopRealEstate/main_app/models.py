from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


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
    price = models.DecimalField(max_digits=20,
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
    types = [('Flat', 'Flat'), ('House', 'House')]
    type = models.CharField(max_length=100,
                            choices=types,
                            verbose_name='Квартира или частный дом',
                            help_text='Укажите тип жилья, квартира или частный дом',
                            blank=False,
                            null=True,
                            default='Flat',)
    created_or_updated_date = models.DateTimeField(auto_now=True,)
    owner = models.ForeignKey(User,
                              verbose_name='Пользователь',
                              help_text='Выберите пользователя, создающего объявление',
                              on_delete=models.CASCADE,
                              related_name='adverts',
                              null=True,
                              blank=False,
                              default=1,
                              )
    is_active = models.BooleanField(default=True,
                                    verbose_name='Активность обьявления',
                                    help_text='Выберите, активно объявление или нет',
                                    )
    image = models.ImageField(upload_to="foto/%Y/%m/%d/",
                              verbose_name="Фото недвижимости",
                              help_text="Загрузите сюда ссылку на изображение с недвижимостью",
                              blank=True,
                              null=True,
                              )
    average_rating = models.FloatField(default=0.0,
                                       verbose_name="Средний рейтинг",
                                       help_text="Здесь будет автоматически посчитан средний рейтинг, на основании отзывов пользователей",
                                       blank=True)

    def update_average_rating(self):
        avg_rating = self.ratings.aggregate(Avg('rating'))['rating__avg']
        self.average_rating = avg_rating if avg_rating else 0.0
        self.save()

    class Meta():
        ordering = ['title']
        verbose_name = 'Advert'
        verbose_name_plural = 'Adverts'
    def __str__(self):
        return f"{self.title}"
#alex = User.objects.create_user(username='alex', password='87654321', email='v.gubenkov@gmail.com')


class Rating(models.Model):
    advert = models.ForeignKey(Advert,
                               verbose_name="Объявление",
                               help_text="Выберите обьявление, к которому хотите оставить отзыв",
                               on_delete=models.CASCADE,
                               related_name='ratings',
                               null=False,
                               blank=True,
                               )
    owner = models.ForeignKey(User,
                              verbose_name='Пользователь',
                              help_text='Выберите пользователя, создающего отзыв',
                              on_delete=models.SET_NULL,
                              related_name='ratings',
                              null=True,
                              blank=False,
                              default=1,
                              )
    numbers = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)]
    rating = models.PositiveIntegerField(choices=numbers,
                                         verbose_name="Рейтинг",
                                         help_text="Поставьте рейтинг по шкале от 1 до 10, где 10 максимальная оценка",
                                         null=True,
                                         default=10,
                                         blank=False,
                                         )