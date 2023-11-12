from django.db import models
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.last_name} {self.first_name} - {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    subject = models.CharField(max_length=250, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Содержание')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class Mailing(models.Model):
    clients = models.ManyToManyField('Client', verbose_name='Клиенты рассылки')
    time_to_start = models.DateTimeField(verbose_name='Начало рассылки')
    time_to_finish = models.DateTimeField(verbose_name='Окончание рассылки')
    periodicity = models.CharField(choices=[('1', 'Раз в день'), ('2', 'Раз в неделю'), ('3', 'Раз в месяц')],
                                   default='1', verbose_name='Периодичность рассылки')
    status = models.PositiveSmallIntegerField(default=1, verbose_name='Статус рассылки')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, default=None, verbose_name='Сообщение')
    next_try = models.DateTimeField(verbose_name='Попытка следующей отправки', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Владелец', **NULLABLE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.clients} - {self.time_to_start} : {self.time_to_finish}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Logs(models.Model):
    time = models.DateTimeField(default=None, verbose_name='Дата и время последней попытки')
    mail = models.EmailField(max_length=100, verbose_name='Почта', **NULLABLE)
    response = models.BooleanField(default=False, verbose_name='Ответ почтового сервера', **NULLABLE)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Владелец', **NULLABLE)
