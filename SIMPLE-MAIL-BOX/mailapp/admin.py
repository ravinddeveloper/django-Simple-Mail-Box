from django.contrib import admin
from .models import mail_data,user_verify
# Register your models here.
# admin.site.register(mail_data)




@admin.register(mail_data)
class mail_data_md(admin.ModelAdmin):
    list_display = ["user", "r_email","u_id"]

@admin.register(user_verify)
class user_verify(admin.ModelAdmin):
    list_display = ["user", "verify"]