# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_GET
from qa.models import Question
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
#	return HttpResponse("popular page:"+str(pagen)+"\r\n")

@require_GET
def main(request, *args, **kwargs):
	quests = Question.objects.new()
	limit = request.GET.get('limit',10)
	page = request.GET.get('page',1)
	paginator=Paginator(quests, limit)
	paginator.baseurl='/?page='
	contpage=paginator.page(page)
#	return HttpResponse('new page:'+str(page)+' limit:'+str(limit)+' paoginator:'+str(paginator.count))
	return render (request, 'index.html',{
		'quests': contpage.object_list,
		'paginator': paginator,
		'page':page,
		})

def question(request,QID):
	quest = get_object_or_404(Question,id=QID)
	answ=Answer.object.filter(question=QID).order_by('-id')
	context={
		'title':'Question page',
		'question':quest,
		'answ':answ,
	}
	return render(request,'question.html',context)
#	return HttpResponse('question ID:'+QID+'\r\n')

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
