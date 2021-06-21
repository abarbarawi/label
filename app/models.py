import uuid
from django.db import models
from django.contrib import auth
from django.contrib.auth.models import User
from django.forms import forms



class reters(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True)
    name=models.CharField(max_length=500)
    created=models.DateField(auto_now=True)
    modified=models.DateField(auto_now=True)

    def __str__(self):
        return str(self.id)


class data_sets(models.Model):
     id=models.AutoField(primary_key=True)
     name=models.CharField(max_length=200)
     path=models.CharField(max_length=500)
     created = models.DateField(auto_now=True)
     modified = models.DateField(auto_now=True)

     def __str__(self):
         return str(self.name)
class transcription(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=500)
    path=models.CharField(max_length=500)
    created = models.DateField(auto_now=True)
    modified = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.id)


class clips(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=500)
    path=models.CharField(max_length=500)
    data_set = models.ForeignKey(data_sets, on_delete=models.PROTECT,null=True, blank=True)
    text = models.ForeignKey(transcription, on_delete=models.PROTECT, null=True, blank=True)
    created = models.DateField(auto_now=True)
    modified = models.DateField(auto_now=True)


    def __str__(self):
        return (str(self.id))

class evaluations(models.Model):
    id = models.AutoField(primary_key=True)
    clip=models.ForeignKey(clips,on_delete=models.PROTECT)
    label_choices = (
        (0, 'clearvoice'), (1, 'sound_repetition'), (2, 'word_repetition'), (3, 'phrase_repetition'),
        (4, 'interjection'),
        (5, 'prolongation'), (6, 'block'), (7, 'part_word_repetition'))
    label = models.IntegerField(choices=label_choices, default=0)
    text = models.ForeignKey(transcription, on_delete=models.PROTECT, null=True, blank=True)
    rater = models.ForeignKey(reters, on_delete=models.PROTECT, null=True, blank=True)
    created = models.DateField(auto_now=True)
    modified = models.DateField(auto_now=True)


    def __str__(self):
        return (str(self.id))