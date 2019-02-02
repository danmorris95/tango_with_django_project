# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page

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
