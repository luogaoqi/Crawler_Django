from django.db import models

# Create your models here.
class Trip_URL(models.Model):  
    url = models.URLField('addr',max_length = 100, unique = True,primary_key=True)
    city = models.CharField('city',max_length = 100)
    is_save = models.BooleanField('save_flag',default= False)
    date = models.DateTimeField('saving time')  
    def __unicode__(self):  
        return self.url  

class Orbit_URL(models.Model):  
    url = models.URLField('addr',max_length = 100, unique = True,primary_key=True)
    city = models.CharField('city',max_length = 100)
    is_save = models.BooleanField('save_flag',default= False)
    date = models.DateTimeField('saving time')  
    def __unicode__(self):  
        return self.url 
    
class Priceline_URL(models.Model):  
    url = models.URLField('addr',max_length = 100, unique = True,primary_key=True)
    city = models.CharField('city',max_length = 100)
    is_save = models.BooleanField('save_flag',default= False)
    date = models.DateTimeField('saving time')  
    def __unicode__(self):  
        return self.url 
    
