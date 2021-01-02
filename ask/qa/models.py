#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class QuestionManager(models.Manager):
	def new(self):
		#return self.order_by('-added_at')
		return super(QuestionManager, self).get_queryset().order_by('-added_at') # not my
	def popular(self):
		return super(QuestionManager, self).get_queryset().order_by('-rating')  # not my


class Question(models.Model):
	title = models.CharField(max_length=255)
	text = models.TextField()
	added_at = models.DateTimeField(auto_now_add=True)
	rating =models.IntegerField(null=True, default=0)
	author = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
	#likes = models.ManyToManyField(User, related_name='likes_set') #!!!!!!!!!!!!!! use likes.set instead what does it mean?
	objects = QuestionManager() 

	def __unicode__(self):
		return self.text

	def get_url(self):
		return '/question/%d/' % self.id
	#????
	#def get_absolute_url(self):
#		return reverse('question_details', args=[self.slug,]) #было pk

class Answer(models.Model):
	text =  models.TextField()
	added_at = models.DateTimeField(auto_now_add=True)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


