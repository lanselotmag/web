# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_GET
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from qa.models import Question,Answer
from qa.forms import AskForm, AnswerForm, LoginForm, SignupForm
#test view
def test(request,*args,**kwargs):
	return HttpResponse('OK')
# Create your views here.
@require_GET
def popular(request, *args, **kwargs):
	quests=Question.objects.popular()
	paginator, page, limit = paginate(request, quests)
	context = {
		'title':'Popular questions',
		'quests':page,
		'paginator':paginator,
		'limit':limit,
	}
	return render(request, 'popular.html',context)

@require_GET
def main(request, *args, **kwargs):
	quests = Question.objects.new()
	limit = request.GET.get('limit',10)
	page = request.GET.get('page',1)
	paginator=Paginator(quests, limit)
	paginator.baseurl='/?page='
	contpage=paginator.page(page)
	return render (request, 'index.html',{
		'quests': contpage.object_list,
		'paginator': paginator,
		'page':page,
		})
def ask(request):
	if request.method == 'POST':
		form = AskForm(request.POST)
		if form.is_valid():
			form._user = request.user
			question = form.save()
			url = question.get_url()
			return HttpResponseRedirect(url)
	else:
		form = AskForm()
	return render (request, 'ask.html', {
		'form':form
	})

def question(request,QID):
	quest = get_object_or_404(Question,id=QID)
	answ=Answer.objects.filter(question=QID).order_by('-id')
	if request.method == 'POST':
		form = AnswerForm(request.POST)
		if form.is_valid():
			form._user = request.user
			answer=form.save()
			url = quest.get_url()
			return HttpResponseRedirect(url)
	else:
		form=AnswerForm()
	context={
			'title':'Question page',
			'question':quest,
			'answ':answ,
			'form':form,
	}
	return render(request,'question.html',context)

def paginate(request, lst):
	try:
		limit = int(request.GET.get('limit',10))
	except ValueError:
		limit = 10
	if limit > 100:
		limit = 10
	paginator = Paginator(lst, limit)
	try:
		page = int(request.GET.get('page',1))
	except ValueError:
		raise http404
	try:
		page = paginator.page(page)
	except EmptyPage:
		page =  paginator.page(paginator.num_pages)
	return paginator, page, limit

def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data['username']
			password = form.raw_password
			user = authenticate(username=username,password=password)
			if user is not None:
				login(request,user)
			return HttpResponseRedirect(reverse('index'))
	else:
		form = SignupForm()
	return render(request, 'signup.html',{'form':form})

def login(request):
	error=''
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request,user)
			return HttpResponseRedirect(reverse('index'))
	return render(request, 'login.html', {'form' : form})
