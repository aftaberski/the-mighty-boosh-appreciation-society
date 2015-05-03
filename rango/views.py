from django.shortcuts import render
from django.http import HttpResponse

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm


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

		# Added in order to add page to category
		context_dict['category_name_slug'] = category_name_slug
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

def add_page(request, category_name_slug):

	try:
		cat = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		cat = None

	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if cat:
				page = form.save(commit=False)
				page.category = cat
				page.views = 0
				page.save()

				# potentially better to use a redirect here
				return category(request, category_name_slug)
		else:
			print form.errors
	else:
		form = PageForm()

	context_dict = {'form': form, 'category': cat, 'category_name_slug': category_name_slug}

	return render(request, 'rango/add_page.html', context_dict)

def register(request):

	# Was the registration successful?
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		# If both forms are valid...
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()

			# Hash PW with set_password method
			# Then update user object
			user.set_password(user.password)
			user.save()

			# Now for the UserProfile instance
			# Since we want to user attribute ourselves, we commit= False
			# Adds User model to profile
			profile = profile_form.save(commit=False)
			profile.user = user

			# If users provides a profile picture:
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			# Now save the UserProfile instance
			profile.save()

			# Update to say registration was successful
			registered = True

		# If invalid form/forms:
		else:
			print user_form.errors, profile_form.errors

	# Not a POST? Render form using two ModelForm instances
	# Forms will be blank and ready for user input
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
	return render(request, 'rango/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				# Log user in, and send to homepage
				login(request, user)
				return HttpResponseRedirect('/rango/')
			else:
				return HttpResponse("Your account is disabled")
		else:
			# Bad login details were provided
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")
	else:
		# request is not a POST
		# Include blank dictionary object b/c no context variables
		return render(request, 'rango/login.html', {})


