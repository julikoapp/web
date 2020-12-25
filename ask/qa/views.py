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
	return render(request, 'qa/question_details.html', { # template maybe 'qa/question_details.html'
		'title' : question.title, #можно было бы шаблонизатором, указав спец.методы в модели(так даже лучше)
		'text': question.text,
	})

def page(request):
	questions = Question.objects.all() # or .filter(published=True)
	questions = questions.order_by('-new')
	limit = 10 #or request.GET.get('limit', 10)
	page = request.GET.get('page', 1)
	paginator = Paginator(questions, limit)
	paginator.baseurl = '/?page=' # like in urls.py -- need update obv
	# perfect baseurl - '/qa/all_questions/?page=' but you need to get url in app отдельно
	page = paginator.page(page)
	return render(request, 'qa/question_by_date.html', {
		'questions': page.object_list,
		'paginator': paginator, 
		'page': page,
	})
# На страницу выводится по 10 вопросов. В списке вопросов 
# должны выводится заголовки (title) вопросов и ссылки на страницы 
# отдельных вопросов
def popular_page(request):
	questions = Question.objects.all() # or .filter(published=True)
	questions = questions.order_by('-popular')
	limit = 10 #or request.GET.get('limit', 10)
	page = request.GET.get('page', 1)
	paginator = Paginator(questions, limit)
	paginator.baseurl = '/popular/?page=' # like in urls.py -- need update obv
	# perfect baseurl - '/qa/all_questions/popular/?page=' but you need to get url in app отдельно
	page = paginator.page(page)
	return render(request, 'qa/question_by_date.html', {
		questions: page.object_list,
		paginator: paginator, 
		page: page,
	})

	
