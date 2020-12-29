"""ask URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
#from django.urls import path
from django.conf.urls import url
from qa import views

urlpatterns = [
   # url(r'^$',views.test, name='main'),
    url(r'^login/', views.test, name='login'),
    url(r'^signup/', views.test, name='signup'),
    url(r'^ask/', views.test, name='test'),
    url(r'^new/', views.test, name='test'),
    url(r'^question/(?P<slug>\w+)/$', views.question_details, name='question_details'),
    url(r'^$', views.page, name='questions_list'), # I thought ^page/(?P<slug>\w+)/$
    url(r'^popular/', views.popular_page, name='popular_questions_list'),
    url(r'^admin/', admin.site.urls),
]
