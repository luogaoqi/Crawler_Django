'''
Created on 2012-6-7

@author: luogaoqi
'''
from django.contrib import admin
from Orbit.models import Hotel,User,Hotel_User

class Hotel_Admin(admin.ModelAdmin):  
    list_display = ['addr']   
    fields = ['addr'] 
    
class User_Admin(admin.ModelAdmin):  
    list_display = ['name']    
    fields = ['name'] 
    
class Hotel_User_Admin(admin.ModelAdmin):  
    list_display = ['hotel','user','rating','comments']  
    fields = ['hotel','user','rating','comments'] 
   
admin.site.register(Hotel, Hotel_Admin)
admin.site.register(User, User_Admin)
admin.site.register(Hotel_User, Hotel_User_Admin)