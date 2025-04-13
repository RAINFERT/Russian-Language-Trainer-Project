"""
URL configuration for trainer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.urls import path
from . import views, views2

urlpatterns = [
    path('', views.index, name='index'),
    path('words-list', views.words_list),
    path('add-word', views.add_word),
    path('send-word', views.send_word),
    path('stats', views.show_stats),
    path('test-words/', views.test_words, name='test_words'),
    path("reset-test/", views.reset_test, name="reset_test"),
    path('', views2.index, name='index'),
    path('add-example/', views2.add_example, name='add_example'),
    path('send-example/', views2.send_example, name='send_example'),
    path('examples-list/', views2.examples_list, name='example_list'),
]
