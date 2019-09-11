from __future__ import unicode_literals
from django import forms
from qa.models import Question, Answer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm
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
#login form
class LoginForm(forms.Form):
	username = forms.CharField(max_length = 100)
	password = forms.CharField(widget=forms.PasswordInput)

	def clean_username(self):
		username = self.cleaned_data['username']
		if username.strip == '':
			raise forms.ValidationError('Fill username filed',code='validation_error')
		return username

	def clean_password(self):
		password = self.cleaned_data['password']
		if password.strip() == '':
			raise forms.ValidationError('Fill password field',code='validation_error')
		return password

	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			raise froms.ValidationError('Incorrect username or password!')
		if not user.check_password(password):
			raise forms.ValidationError('Incorrect username or password!')
#Signup form
#class SignupForm(forms.Form):
class SignupForm(UserCreationForm):
#	username = forms.CharField(max_length=100,required=True)
	email = forms.EmailField(max_length=100,required=False)
#	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ('username','email','password')

	def clean_username(self):
		username = self.cleaned_data['username']
		if username.strip == '':
			raise forms.ValidationError('Fill username filed',code='validation_error')
		try:
			User.objects.get(username=username)
			raise forms.ValidationError('Already exists!',code='validation_error')
		except User.DoesNotExist:
			pass
		return username

	def clean_email(self):
		email = self.cleaned_data['email']
		if email.strip() == '':
			raise forms.ValidationError('Fill email field',code='validation_error')
		return email

	def clean_password(self):
		password = self.cleaned_data['password']
		if password.strip() == '':
			raise forms.ValidationError('Fill password field',code='validation_error')
#		self.raw_passwrd = password
		return make_password(password)

	def save(self):
		user = User(**self.cleaned_data)
		user.save()
		return user
