from django import forms
from .models import Question, Answer
from django.contrib.auth.models import User

class AskForm(forms.Form):
    title = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.Textarea)

    def __init__(self, user=None, *args, **kwargs):
        self._user = user
        super(AskForm, self).__init__(*args, **kwargs)

    def save(self):
        # was -- didn't work
        #self.cleaned_data['author'] = self._user
        #self.cleaned_data['title'] = self.title
        #self.cleaned_data['text'] = self.text
        #return Question.objects.create(**self.cleaned_data)
        #became (not my code)
        question = Question(**self.cleaned_data) #Question.objects.create() or #Question.objects.create_question()
        question.author = self._user
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question_id = forms.IntegerField(widget=forms.HiddenInput)
    question = forms.ModelChoiceField(queryset=Question.objects.all(),widget=forms.HiddenInput)
    #question = Question.objects.filter(id=question_id) problems with id...
    def __init__(self, user=None, *args, **kwargs):
        self._user = user
        super(AnswerForm, self).__init__(*args, **kwargs)

    def save(self):
        answer = Answer(**self.cleaned_data)
        answer.author = self._user
        answer.save()
        return answer

#Измените формы добавления вопроса (AskForm) и ответа (AnswerForm) так что бы они учитывали текущего пользователя
# и сохраняли его в поле author вопросов и ответов. Конструкторы форм должны получать стандартные
# для Django-форм аргументы, т.е. должна быть возможность создать объект формы как AskForm() или AnswerForm().

class RegistrationForm(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    def save(self):
        user = User.objects.create_user(username=self.username,
                                        first_name=self.first_name,
                                        last_name=self.last_name,
                                        password=self.password,
                                        email=self.email)
        return ...


class LoginForm(forms.Form):
    username = forms.CharField()
    #first_name = forms.CharField()
    #last_name = forms.CharField()
    #email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
