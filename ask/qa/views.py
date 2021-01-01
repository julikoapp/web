#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from qa.models import Question, Answer
from qa.forms import AskForm, AnswerForm, RegistrationForm, LoginForm
#import salt_and_hash
#import datetime
#import Session
#import generate_long_random_key
#import timedelta

# Create your views here.
def test(request, *args, **kwargs):
	return HttpResponse('OK')


def detail_page(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'GET':
        form = AnswerForm({'question_id': question.pk})
    elif request.method == 'POST':
        form = AnswerForm(request.POST)
        form._user = request.user
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
        form._user = request.user
        if form.is_valid():
            form.save()
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


#При GET запросе должна отображаться форма для ввода данных,
# при POST запросе создается новый пользователей,
# осуществляется вход (login) созданного пользователя на сайт,
# возвращается редирект на главную страницу.
def registration(request):
    if request.method == "GET":
        form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save() #-- actually better option, logic should not be in views
            # but we got error, soo
            # user = User.objects.create_user(
            #     username=form.cleaned_data['username'],
            #     password=form.cleadned_data['password1'], #or just password?
            #     email=form.cleadned_data['email']
            # )
            return HttpResponseRedirect('/')
    return render(request,"qa/registration.html",{
        "form" : form
    })


#def do_login(login, password):
#    try:
#        user = User.objects.get(username=login)
#    except User.DoesNotExist:
#        return None
#    hashed_pass = salt_and_hash(password)
#     if user.password != hashed_pass:
#         return None
#     session = Session()
#     session.key = generate_long_random_key()
#     session.user =user
#     session.expires = datetime.now() + timedelta(days=1)
#     session.save()
#     return session.key


#При GET запросе должна отображаться форма для ввода данных,
# при POST запросе происходит вход (login) на сайт, возвращается редирект на главную страницу.
# Пользователь должен получить авторизационную куку с именем sessionid.  ﻿
#Имена POST параметров и куки ﻿важны!
def login(request):
    error = ''
    if request.method == "GET":
        form = LoginForm()
    if request.method == "POST":
        form = LoginForm()
        username = request.POST.get('username')
        password = request.POST.get('password')
        url = request.POST.get('continue','/')

        user = authenticate(username=username, password=password)
        if user is not None:
            sessionid = login(request, user)

        #sessid = do_login(login, password)
            if sessionid:
                response = HttpResponseRedirect(url)
                response.set_cookie('sessionid', sessionid)
                return response
        else:
            error = 'Неверный логин\пароль'
    return render(request, 'qa/login.html', {
        'form': form,
        'error': error,
    })