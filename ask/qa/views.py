#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404,redirect
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from qa.models import Question, Answer
from qa.forms import AskForm, AnswerForm

# Create your views here.
def test(request, *args, **kwargs):
	return HttpResponse('OK')


def question_details(request,slug):
	question = get_object_or_404(Question, id=slug)
	if request.method == 'POST':
		form = AnswerForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("question_details", slug=question.id)
	else:
		form = AnswerForm({'question_id':question.id})
	#answer = get_object_or_404(Answer, question=question)
	return render(request, 'qa/question_details.html', { # template maybe 'qa/question_details.html'
		'title' : question.title, #можно было бы шаблонизатором, указав спец.методы в модели(так даже лучше)
		'text': question.text,
		'answers': question.answer_set.all(), #!!!!! didn't know!!!
		'answer_form':form,
	})

def add_question(request):
	if request.method == 'POST':
		form = AskForm(request.POST)
		if form.is_valid():
			asked = form.save()
			url = asked.get_url()
			return HttpResponseRedirect(url)
	else:
		form = AskForm()
	return render(request, 'qa/ask_form.html',{
		'ask_form':form
	})


def page(request):
	questions = Question.objects.new() # or .filter(published=True)
	#questions = questions.order_by('-new')
	paginator = Paginator(questions, 10)
	page = request.GET.get('page', 1)#1
	paginator.baseurl = '/?page=' # like in urls.py -- need update obv
	# perfect baseurl - '/qa/all_questions/?page=' # but you need to get url in app отдельно
	page = paginator.page(page)
	#page_obj = paginator.get_page(page_number)
	return render(request, 'qa/question_by_date.html', {
		'questions': page.object_list,
		'paginator': paginator,
		'page': page,
	})
# На страницу выводится по 10 вопросов. В списке вопросов 
# должны выводится заголовки (title) вопросов и ссылки на страницы 
# отдельных вопросов
def popular_page(request):
	questions = Question.objects.popular() # or .filter(published=True)
	paginator = Paginator(questions, 10)
	page = request.GET.get('page', 1)  # 1
	paginator.baseurl = '/?page='  # like in urls.py -- need update obv
	# perfect baseurl - '/qa/all_questions/?page=' # but you need to get url in app отдельно
	page = paginator.page(page)
	# page_obj = paginator.get_page(page_number)
	return render(request, 'qa/question_by_date.html', {
		'questions': page.object_list,
		'paginator': paginator,
		'page': page,
	})

	
