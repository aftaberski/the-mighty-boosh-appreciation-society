from django.shortcuts import render
from django.http import HttpResponse

from rango.models import Category, Page
from rango.forms import CategoryForm


def index(request):
	category_list = Category.objects.order_by('-likes')[:5]
	context_dict = {'categories' : category_list}
	return render(request, 'rango/index.html', context_dict)

def about(request):
	return render(request, 'rango/about.html')

def category(request, category_name_slug):
	context_dict = {}

	try:
		category = Category.objects.get(slug=category_name_slug)
		context_dict['category_name'] = category.name

		# Retrieve all of the associated pages
		pages = Page.objects.filter(category=category)

		context_dict['pages'] = pages

		# Also add category object to the context dictionary
		# We can use this in the template to verify that the
		# category exists
		context_dict['category'] = category
	except Category.DoesNotExist:
		# Template automatically displays "no category message for us"
		pass

	# Render response and return it to the client
	return render(request, 'rango/category.html', context_dict)


def add_category(request):
	# Is it a POST?
	if request.method == 'POST':
		form = CategoryForm(request.POST)

		# Is it valid?
		if form.is_valid():
			form.save(commit=True)

			# Return the user to the index pages
			return index(request)
		else:
			# What are the errors?
			print form.errors
	else:
		form = CategoryForm()

	# Bad form (or form details)...
	# Render the form with error messages (if any)
	return render(request, 'rango/add_category.html', {'form': form})
