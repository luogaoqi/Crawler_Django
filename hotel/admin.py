'''
Created on 2012-6-4

@author: luogaoqi
'''

from django.contrib import admin
from hotel.models import Trip_URL,Orbit_URL,Priceline_URL

class Trip_URL_Admin(admin.ModelAdmin):  
    list_display = ('url','city','is_save','date')  
    #ordering = ('-id',)  
    list_filter = ['is_save','date','city']  
    fields = ['url','is_save'] 

class Orbit_URL_Admin(admin.ModelAdmin):  
    list_display = ('url','city','is_save','date')  
    #ordering = ('-id',)
    list_filter = ['is_save','date','city']  
    fields = ['url','is_save'] 

class Piceline_URL_Admin(admin.ModelAdmin):  
    list_display = ('url','city','is_save','date')  
    #ordering = ('-id',)  
    list_filter = ['is_save','date','city'] 
    fields = ['url','is_save'] 
   
admin.site.register(Trip_URL, Trip_URL_Admin)
admin.site.register(Orbit_URL, Orbit_URL_Admin)
admin.site.register(Priceline_URL, Piceline_URL_Admin)




