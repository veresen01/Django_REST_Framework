from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=100)  # Имя пользователя
    last_name = models.CharField(max_length=100)   # Фамилия пользователя
    email = models.EmailField(unique=True)         # Уникальный email пользователя
    age = models.IntegerField()                    # Возраст
    job = models.CharField(max_length=100)         # Профессия

    def __str__(self):
        return f'{self.first_name} {self.last_name}'  # Строковое представление объекта
