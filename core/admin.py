from django.contrib import admin
from .models import Chart


class ChartAdmin(admin.ModelAdmin):
    class Meta:
        model = Chart

    fields = ['name', 'chart_type', 'end_point', 'number']
    list_display = ['name', 'slug', 'chart_type', 'end_point', 'number']


admin.site.register(Chart, ChartAdmin)
