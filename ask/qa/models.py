# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models.User import User

# Create your models here.
class QuestionManager(self):
	def new(self):
		return self.order_by('-added_at')
	def popular(self):
		return self.order_by('-rating')

class Question(models.Model):
	objects=QuestionManager()
	title=models.CharField(default="",max_length=255)
	text=models.TextField(default="")
	added_at=models.DataField(auto_now_add=true)
	rating=models.IntegerField(default=0)
	author=models.OneToOneField(User)
	like=models.OneToManyField(User)

	def __str__(self):
		return self.title

class Answer(models.Model):
	text=models.CharField(max_length=255)
	added_at=models.DataField()
	question=models.OneToOneField()
	author=models.OneToOneField()

	def __str__(self):
		return self.title
