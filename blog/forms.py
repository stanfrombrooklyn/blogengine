from django import forms
from .models import Tag, Post
from django.core.exceptions import ValidationError

# to be DRY change Form to ModelForm!

class TagForm(forms.ModelForm):
#class TagForm(forms.Form):
#    title = forms.CharField(max_length=50)
#    slug = forms.CharField(max_length=50)

    # attr is dictionary. we update it with class 'form-control' for input
    # which we take from bootstrap website -> components -> forms -> input
#    title.widget.attrs.update({'class': 'form-control'})
#    slug.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Tag
        fields = ['title', 'slug']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_slug(self): # validate slug input, so that it's not 'create' and lowercase
        # can use dict and not get method, because at this point slug is certain to exist
        # self.cleaned_data.get('slug')
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')

        # check if slug already exists
        # method count() is True if filter has any values
        if Tag.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError(f'Slug "{new_slug}" already exists. It must be unique')
        return new_slug

    # ModelForm has it's own save()
    # Method below creates new Tag every time even if we only need to change it
#    def save(self):
#        new_tag = Tag.objects.create(
#            title=self.cleaned_data['title'],
#            slug=self.cleaned_data['slug']
#        )
#        return new_tag

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'tags']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'})
        }
    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')

        return new_slug
