from django.contrib import admin
from .models import Action


@admin.register(Action)
class ActionADmin(admin.ModelAdmin):
    list_display = ('user', 'verb', 'target', 'created')
    list_filter = ('created',)
    search_fields = ('verb',)
