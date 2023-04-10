from django.contrib import admin

# Register your models here.
from .models import Raffle, Prize, Ticket


class RaffleAdmin(admin.ModelAdmin):
    list_display = (['name'])


class PrizeAdmin(admin.ModelAdmin):
    list_display = (['name'])


class TicketAdmin(admin.ModelAdmin):
    list_display = (['raffle', 'verification_code'])


admin.site.register(Raffle, RaffleAdmin)
admin.site.register(Prize, PrizeAdmin)
admin.site.register(Ticket, TicketAdmin)
