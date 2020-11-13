from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Ticket, Event, Tag, Comment


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    list_display_links = ('title', 'slug',)
    prepopulated_fields = {'slug': ('title',)}


class EventFormAdmin(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Event
        fields = '__all__'


class EventAdmin(admin.ModelAdmin):
    form = EventFormAdmin
    list_display = (
        'author', 'title', 'number_tickets', 'tickets_left', 'location', 'category', 'created_date', 'published_date',
        'edit_date', 'published', 'views', 'get_photo')
    list_display_links = (
        'author', 'title', 'number_tickets', 'location', 'category', 'created_date', 'published_date', 'edit_date',
        'views', 'get_photo')
    list_filter = ('category', 'author')
    list_editable = ('published',)
    search_fields = ('title', 'content')
    readonly_fields = ('get_photo', 'views', 'author', 'tickets_left')
    prepopulated_fields = {'slug': ('title',)}
    save_as = True
    save_on_top = True

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')

    get_photo.short_description = 'Фото'

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.tickets_left = obj.number_tickets
        super().save_model(request, obj, form, change)


class TicketAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'event', 'email', 'published_date')
    list_display_links = ('name', 'surname', 'event')
    list_filter = ('event', 'email')
    search_fields = ('name', 'surname', 'event', 'email')
    save_as = True
    save_on_top = True


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'event', 'content', 'email', 'published_date')
    list_display_links = ('name', 'surname', 'event')
    list_filter = ('event',)
    search_fields = ('name', 'surname', 'event', 'content', 'email')
    save_as = True
    save_on_top = True


admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Comment, CommentAdmin)
