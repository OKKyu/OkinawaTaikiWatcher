from django.db import models

# Create your models here.


class Criterias(models.Model):
    '''
      Criterias each of substitutions.
    '''
    substitute = models.CharField(max_length=10)
    start_timestamp = models.DateTimeField(auto_now_add=True)
    end_timestamp = models.DateTimeField(auto_now_add=True)
    criteria = models.FloatField(default=0.0, null=False)
    registed_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.substitute + ":" + str(self.criteria)


class Kyokus(models.Model):
    '''
      Kyoku.
    '''
    name = models.TextField(max_length=20, default="", null=False)
    alert_flg = models.BooleanField(default=True, null=False)
    registed_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + ":" + self.name


class Settings(models.Model):
    '''
      Basical Settings.
    '''
    # Toggle running scraping.
    name = models.CharField(max_length=10, default='settings', null=False)
    boot_switch = models.BooleanField(default=True, null=False)
    boot_exclude_holiday = models.BooleanField(default=False, null=False)
    boot_exclude_public_holiday = models.BooleanField(default=False, null=False)

    # Register Access Token for LINE-Notify.
    register_line_notify_access_token = models.TextField(default='', null=False)

    def __str__(self):
        return self.name + " boot:" + str(self.boot_switch)
