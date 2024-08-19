from django.contrib import admin

from .models import Balance

admin.site.register(Balance)
# class UserBalanceAdmin(admin.ModelAdmin):
#     list_display = ('user', 'balance')
#     search_fields = ('user__username', 'user__email')
#     readonly_fields = ('user',)
