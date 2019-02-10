# -*- coding: utf-8 -*-

from __future__ import unicode_literals



from django.shortcuts import render

from django.http import HttpResponse

from rango.models import Category

from rango.models import Page

from rango.forms import CategoryForm

from rango.forms import PageForm

from rango.forms import UserForm, UserProfileForm

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse 
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.

def index(request):

    category_list = Category.objects.order_by('-likes')[:5]

    most_viewed_pages=Page.objects.order_by("views")[:5]

    context_dict = {'categories': category_list,"views":most_viewed_pages}

    

    return render(request, 'rango/index.html', context_dict)

    #return HttpResponse("Rango says hey there partner!"+"<br/> <a href=/rango/about/>About'</a>")



def about(request):

    context_dict={"boldmessage": "Hello there!,Kenobi,dog"}

    return render(request,"rango/about.html", context=context_dict)

def show_category(request, category_name_slug):

    context_dict = {}

    try:



        category = Category.objects.get(slug=category_name_slug)

        

        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.

        context_dict['pages'] = pages

        # We also add the category object from

        # the database to the context dictionary.

        # We'll use this in the template to verify that the category exists.

        context_dict['category'] = category

    except Category.DoesNotExist:

    

        # the template will display the "no category" message for us.

        context_dict['category'] = None

        context_dict['pages'] = None

        # Go render the response and return it to the client.

    return render(request, 'rango/category.html', context_dict)


@login_required
def add_category(request):

    form = CategoryForm()

    if request.method=="POST":

        form = CategoryForm(request.POST)

        if form.is_valid():

            form.save(commit=True)

            return index(request)

        else:

            print(form.errors)

    return render(request, "rango/add_category.html",{"form": form})


@login_required
def add_page(request, category_name_slug):

    try:

        category = Category.objects.get(slug=category_name_slug)

    except Category.DoesNotExist:

        category = None



    form = PageForm()

    if request.method == 'POST':

        form = PageForm(request.POST)

        if form.is_valid():

            if category:

                page = form.save(commit=False)

                page.category = category

                page.views = 0

                page.save()

            return show_category(request, category_name_slug)

        else:

            print(form.errors)



    context_dict = {'form':form, 'category': category}



    return render(request, 'rango/add_page.html', context_dict)
	
	
def register(request):

    registered=False



    if request.method=="POST":

        user_form=UserForm(data=request.POST)

        profile_form=UserProfileForm(data=request.POST)



        if user_form.is_valid() and profile_form.is_valid():

            user=user_form.save()



            user.set_password(user.password)

            user.save()

            profile=profile_form.save(commit=False)

            profile.user=user



            if "picture" in request.FILES:

                profile.picture=request.FILES["picture"]

                profile.save()

                registered=True

            else:

                print(user_form.errors, profile_form.errors)



    else:

        user_form=UserForm()

        profile_form=UserProfileForm()

    return render(request, "rango/register.html", {"user_form":user_form,

                                                   "profile_form":profile_form,

                                                   "registered":registered})
												 
def user_login(request):



    if request.method=="POST":

        username=request.POST.get("username")

        password=request.POST.get("password")

        user = authenticate(username=username, password=password)





        if user:

            if user.is_active:

                login(request,user)

                return HttpResponseRedirect(reverse("index"))

            else:

                return HttpResponse("Your Rango account is disabled.")



        else:

            print("Invalid login details: {0}, {1}".format(username, password))

            return HttpResponse("Invalid login details supplied.")



    else:

        return render(request, 'rango/login.html', {})

@login_required

def restricted(request):

    return render(request, 'rango/restricted.html', {})
	
@login_required
def user_logout(request):
	# Since we know the user is logged in, we can now just log them out
	logout(request)
	# Take the user back to the homepage.
	
	return HttpResponseRedirect(reverse('index'))


