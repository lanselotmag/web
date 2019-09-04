# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
#class Choise(models.Model):
#	choice_text=models.CharField(max_length=200)
#	votes=models.IntegerField(default=0)

# Create your models here.
class QuestionManager(models.Manager):
	def new(self):
		return self.order_by('-added_at')

	def popular(self):
		return self.order_by('-rating')

class Question(models.Model):
	objects=QuestionManager()
	title=models.CharField(default="",max_length=255)
	text=models.TextField(default="")
	added_at=models.DateField(auto_now_add=True,null=True)
	rating=models.IntegerField(default=0)
	author=models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
	likes=models.ManyToManyField(User, related_name='question_like_user')
#	def __str__(self):
#		return self.title
#	def get_url(self):
#		return "/question/{}/".format(self.id)
#	class Meta:
#		app_label='qaQuestion'
#		db_table= 'Questions'
#		managed=True
#
class Answer(models.Model):
	text=models.TextField(default='')
	added_at=models.DateField(auto_now_add=True,null=True)
	question=models.ForeignKey(Question,null=True,on_delete=models.SET_NULL)
	author=models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
#
#	def __str__(self):
#		return self.text
#	class Meta:
#		app_label='qaAnswer'
#		db_table='Answer'
#		managed=True
