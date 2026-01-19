from django.contrib import admin
from .models import LostItem

@admin.register(LostItem)
class LostItemAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'location',
        'lost_date',
        'found',
        'owner'
    )

    list_filter = ('found', 'lost_date', 'location')
    search_fields = ('title', 'description', 'location')
    list_editable = ('found',)
    ordering = ('-lost_date',)

    readonly_fields = ('lost_date',)

    fieldsets = (
        ('Item Info', {
            'fields': ('title', 'description', 'image')
        }),
        ('Status', {
            'fields': ('found',)
        }),
        ('Owner Info', {
            'fields': ('owner',)
        }),
        ('Location & Date', {
            'fields': ('location', 'lost_date')
        }),
    )
