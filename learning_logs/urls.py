'''Defines URL patterns for learning_logs.'''

from django.conf.urls import url

from . import views

urlpatterns = [
	#Home Page
	url(r'^$', views.index, name = 'index'),
	#Show all Topics
	url(r'^topics/$', views.topics, name = 'topics'),
	#SHow an Individual Topic
	url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name = 'topic'),
	#Page for Adding a new Topic
	url(r'^new_topic/$', views.new_topic, name = 'new_topic'),
	#Page for Adding a New Entry
	url(r'^new_entry/(?P<topic_id>\d+)$', views.new_entry, name = 'new_entry'),
	#Page to Edit Entry
	url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name = 'edit_entry'),
]
