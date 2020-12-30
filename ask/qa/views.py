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


def detail_page(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'GET':
        form = AnswerForm({'question_id': question.pk})
    elif request.method == 'POST':
        form = AnswerForm(request.POST)
        #form._user = request.user
        if form.is_valid():
            form.save()
            return redirect('detail', pk=question.pk)
    return render(request, 'qa/detail.html', {
        'question': question,
        'answers': question.answer_set.all(),
        'form': form
    })


def ask_page(request):
    if request.method == 'GET':
        form = AskForm()
    elif request.method == 'POST':
        form = AskForm(request.POST)
       # form._user = request.user
        if form.is_valid():
            question = form.save().id
            return redirect('/question/'+str(question)+'/')
    return render(request, 'qa/ask.html', {
        'form': form
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

	
