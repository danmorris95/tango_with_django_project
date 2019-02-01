from django.contrib import admin
from rango.models import Category, Page #imported for chapter 5 (database) work

#admin.site.register(Category)
##

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class PageAdmin (admin.ModelAdmin):
    #fields = ['category', 'url']
    list_display = ('title', 'category', 'url')

    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)


#class QuestionAdmin(admin.ModelAdmin):
#    fieldsets = [
#        (None,               {'fields': ['question_text']}),
#        ('Date information', {'fields': ['pub_date']}),
#    ]
