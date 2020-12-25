from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator
from django.http import HttpResponse

# Create your views here.
def test(request, *args, **kwargs):
	return HttpResponse('OK')

@require_GET
def question_details(request,slug):
	question = get_object_or_404(Question, slug=slug)
	return render(request, 'TEMPLATE', { # template maybe 'qa/question_details.html'
		'title' : question.title #можно было бы шаблонизатором, указав спец.методы в модели(так даже лучше)
		'text': question.text,
	})

def page(request):
	questons = Question.objects.filter(date=fffff)# Необходимо использовать метод new менеджера QuestionManage
	limit = 10 #or request.GET.get('limit', 10)
	page = request.GET.get('page', 1)
	paginator = Paginator(questions, limit)
	paginator.baseurl = '/qa/all_questions/?page='
	page = paginator.page(page)
	return render(request, 'qa/question_by_date.html', {
		questions: page.object_list,
		paginator: paginator, 
		page: page,
	})
# На страницу выводится по 10 вопросов. В списке вопросов 
# должны выводится заголовки (title) вопросов и ссылки на страницы 
# отдельных вопросов
def popular_page(request):
	questions = Question.objects.filter(rating) #!!!!Необходимо использовать метод popular менеджера QuestionManager
	limit = 10 #or request.GET.get('limit', 10)
	page = request.GET.get('page', 1)
	paginator = Paginator(questions, limit)
	paginator.baseurl = '/qa/all_questions/popular/?page='
	page = paginator.page(page)
	return render(request, 'qa/question_by_date.html', {
		questions: page.object_list,
		paginator: paginator, 
		page: page,
	})

	
