from django import forms
from .models import Question, Answer


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
        question = Question(**self.cleaned_data)
        question.author = self._user
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question_id = forms.IntegerField(widget=forms.HiddenInput)
    question = forms.ModelChoiceField(queryset=Question.objects.all(),widget=forms.HiddenInput)
    #question = Question.objects.filter(id=question_id)
    def __init__(self, user=None, *args, **kwargs):
        self._user = user
        super(AnswerForm, self).__init__(*args, **kwargs)

    def save(self):
        answer = Answer(**self.cleaned_data)
        answer.author = self._user
        answer.save()
        return answer