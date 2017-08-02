from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def index(request):
	'''The Homepage for Learning Log'''
	return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
	'''Displays all topics'''
	topics = Topic.objects.filter(owner=request.user).order_by('date_added')
	context ={'topics':topics}

	return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
	'''Displays a Specific Topic Page with all entries'''
	topic = get_object_or_404(Topic, id=topic_id)
	#make sure topic belongs to user
	check_topic_owner(request, topic.owner, topic.public)

	entries = topic.entry_set.order_by('-date_added')

	context = {'topic':topic, 'entries':entries}
	return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
	'''Add a new topic'''
	if request.method != 'POST':
		#no data submitted; create a blank form
		form = TopicForm()
	else:
		#POST data submitted; process data
		form = TopicForm(request.POST)
		if form.is_valid():
			new_topic = form.save(commit = False)
			new_topic.owner = request.user
			new_topic.save()
			return HttpResponseRedirect(reverse('learning_logs:topics'))

	context = {'form':form}
	return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
	"""Add a new Entry for a particular topic"""
	topic = get_object_or_404(Topic, id = topic_id)
	check_topic_owner(request, topic.owner, topic.public)

	if request.method != 'POST':
		#No Data Submitted; create a blank form
		form = EntryForm()
	else:
		#POST data submitted; process data.
		form = EntryForm(data = request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.owner = request.user
			new_entry.save()
			return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
	
	context = {'topic': topic, 'form': form}
	return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
	'''Edit an Existing Entry'''
	entry = get_object_or_404(Entry, id = entry_id)
	topic = entry.topic
	#Makes sure only the Owner can access
	check_topic_owner(request, topic.owner, topic.public)

	if request.method != 'POST':
		#Initial Request; Pre fill form with current Entry
		form = EntryForm(instance=entry)
	else:
		#POST data submitted; process data
		form = EntryForm(instance=entry, data = request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('learning_logs:topic', args = [topic.id]))
	
	context = {'entry':entry, 'topic':topic, 'form': form}
	return render(request, 'learning_logs/edit_entry.html', context)

def check_topic_owner(request, owner, public):
	#Make Sure the User as Access
	if owner != request.user and public == False:
		raise Http404

def public(request):
	'''Displays all Public Topics'''
	topics = Topic.objects.filter(public=True).order_by("date_added")

	context = {'topics':topics}

	return render(request, 'learning_logs/public.html', context)

@login_required
def switch(request, topic_id):
	'''Switches Public Boolean on a specific topic'''
	topic = get_object_or_404(Topic, id=topic_id)
	if topic.owner != request.user:
		raise Http404

	if topic.public == True:
		#Switch Public to False
		topic.public =False
	else:
		topic.public = True

	topic.save()
	return HttpResponseRedirect(reverse('learning_logs:topics'))

	







