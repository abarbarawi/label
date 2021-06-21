from django.contrib import admin
from .models import clips,reters,evaluations,transcription,data_sets

class clips_admin(admin.ModelAdmin):
    list_display = ['id','name', 'path','data_set','text','created','modified']
    search_fields = ['id']
    ordering = ('id',)

admin.site.register(clips, clips_admin)

class reters_admin(admin.ModelAdmin):
    list_display = ['id','name', 'user','created','modified']
    search_fields = ['id']
    ordering = ('id',)

admin.site.register(reters, reters_admin)


class evaluations_admin(admin.ModelAdmin):
    list_display = ['id','clip', 'label','text','rater','created','modified']
    search_fields = ['id']
    ordering = ('id',)

admin.site.register(evaluations, evaluations_admin)

class transcription_admin(admin.ModelAdmin):
    list_display = ['id','name', 'path','created','modified']
    search_fields = ['id']
    ordering = ('id',)

admin.site.register(transcription, transcription_admin)

class data_sets_admin(admin.ModelAdmin):
    list_display = ['id','name', 'path','created','modified']
    search_fields = ['id']
    ordering = ('id',)

admin.site.register(data_sets, data_sets_admin)


