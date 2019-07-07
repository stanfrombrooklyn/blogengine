from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from .models import *

class ObjectDetailMixin:
    #model = None
    #template = None

    def get(self, request, slug): #for GET HTTP method
        #post = Post.objects.get(slug__iexact=slug)

        # SELF object that mixin gets is the instance of a class where the mixin is used!
        # admin_object is needed for css to decide which buttons to show in admin panel
        # detail is needed for showing buttons only on particular posts, not lists of posts
        obj = get_object_or_404(self.model, slug__iexact=slug) #to get 404 page if post is not found
        return render(request,
                    self.template,
                    context={self.model.__name__.lower(): obj,
                            'admin_object': obj,
                            'detail': True
                            }
                    )

class ObjectCreateMixin:
    model_form = None # ????? these will never be used !!!
    template = None
    def get(self, request):
        form = self.model_form()
        return render(request, self.template, context={'form': form})

    def post(self, request):

        bound_form = self.model_form(request.POST)

        # call to is_valid() creates 'cleaned_data' field
        if bound_form.is_valid():
            new_obj = bound_form.save() #creates new Tag and saves it to db
            return redirect(new_obj) # go to new tag page

        # if input is invalid go back to input form with entered data
        return render(request, self.template, context={'form': bound_form})

class ObjectUpdateMixin:
    model = None
    model_form = None
    template = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(instance=obj)
        return render(request,
                    self.template,
                    context={'form': bound_form, self.model.__name__.lower(): obj}
                    )

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(request.POST, instance=obj) # get new edits from user

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)

        return render(request,
                    self.template,
                    context={'form': bound_form, self.model.__name__.lower(): obj}
                    )

class ObjectDeleteMixin:
    model = None
    template = None
    redirect_url = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse(self.redirect_url))
