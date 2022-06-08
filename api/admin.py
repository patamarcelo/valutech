from django.contrib import admin
from .models import ValuRisk

# admin.site.register(ValuRisk)


@admin.register(ValuRisk)
class ValuriskAdmin(admin.ModelAdmin):
    list_display = ('data', 'fechamento')
    ordering = ('-data',)



