from django import forms
from rango.models import Page, Category

class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Enter the category name")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	class Meta:
		# Tells which model to associate with and which fields to include
		model = Category
		fields = ('name',)

class PageForm(forms.ModelForm):
	title = forms.CharField(max_length=128, help_text="Enter the title of the page")
	url = forms.URLField(max_length=200, help_text="Enter the URL")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	# Overriding methods implemented as part of the
	# Django framework can provide you with an
	# elegant way to add that extra bit of functionality

	class Meta:
		model = Page
		exclude = ('category',)

	def clean(self):
		cleaned_data = self.cleaned_data
		url = cleaned_data.get('url')

    # If url is not empty and doesn't start with 'http://', prepend 'http://'.
		if url and not url.startswith('http://'):
			url = 'http://' + url
			cleaned_data['url'] = url

		return cleaned_data

