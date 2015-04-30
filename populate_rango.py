import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

import django
django.setup()

from rango.models import Category, Page

def populate():
	character_cat = add_cat('Characters')

	add_page(cat=character_cat, 
		title="Vince Noir", 
		url="http://mightyboosh.wikia.com/wiki/Vince_Noir")

	for c in Category.objects.all():
		for p in Page.objects.filter(category=c):
			print "- {0} - {1}".format(str(c), str(p))

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    return c

# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    populate()