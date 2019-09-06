from __future__ import unicode_literals
from django import forms
from qa.models import Question, Answer
#from django.contrib.auth.models import User
#from django.contrib.auth import authenticate,login
#from django.contrib.auth.hashes import make_password
#ask form
class AskForm(forms.Form):
	title = forms.CharField(max_length=100)
	text = forms.CharField(widget=forms.Textarea)
	def clean_title(self):
		title = self.cleaned_data['title']
		if title.strip() == '':
			raise forms.ValidationError('Incorrest title!', code='validation_eror')
		return title

	def clean_text(self):
		text=self.cleaned_data['text']
		if text.strip == '':
			raise forms.ValidationError('Incorrect text!', code='validation_error')
		return text

	def save(self):
		question=Question(**self.cleaned_data)
#		question.author_id =  self._user.id
		question.save()
		return question
#answer form
class AnswerForm(forms.Form):
	text = forms.CharField(widget=forms.Textarea)
	question = forms.IntegerField(widget=forms.HiddenInput)

	def clean_text(self):
		text = self.cleaned_data['text']
		if text.strip() == '':
			raise forms.ValidationError('Incorrect text!', code='validation_error')
		return text

	def clean_question(self):
		question_id = self.cleaned_data['question']
		try:
			question= Question.objects.get(id=question_id)
		except Question.DoesNotExist:
			raise forms.ValidationError('No such question!',code='validation_error')
		return question

	def save(self):
		answer=Answer(**self.cleaned_data)
#		answer.author_id = self._user.id
		answer.save()
		return answer
