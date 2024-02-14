from django.contrib import admin
from .models import CustomUser, Fanlar, Teachers, Shartnoma, Contact

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_filter = ['date_joined', 'tavallud_sanasi']
    search_fields = ["first_name", "last_name"]
@admin.register(Fanlar)
class CustomFanlarAdmin(admin.ModelAdmin):
    list_filter = ['created_at']
    search_fields = ["fan_nomi"]
@admin.register(Teachers)
class CustomTeachersAdmin(admin.ModelAdmin):
    list_filter = ['date_joined']
    search_fields = ["ismi", "familiyasi"]
@admin.register(Shartnoma)
class CustomShartnomaAdmin(admin.ModelAdmin):
    list_filter = ['boshlanish_sanasi', 'tugash_sanasi' , 'baho']
    # list_display = ['shartnoma_id']
@admin.register(Contact)
class CustomContactAdmin(admin.ModelAdmin):
    list_filter = ['created_at']
    search_fields = ["ism", "xabar"]