from django.db import models

# Create your models here.
class User(models.Model):  
    user_ID = models.AutoField('user_ID', primary_key = True)
    name = models.CharField('name',max_length = 100)
    def __unicode__(self):  
        return self.name  
    
class Hotel(models.Model):  
    hotel_ID = models.AutoField('hotel_ID', primary_key = True)
    addr = models.CharField('addr',max_length = 100)
    user = models.ManyToManyField(User, through='Hotel_User')
    def __unicode__(self):  
        return self.addr

class Hotel_User(models.Model):  
    hotel = models.ForeignKey(Hotel)
    user = models.ForeignKey(User)
    rating = models.CharField('rating',max_length = 100)
    comments = models.TextField('comment')