from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (Choice, Question, Category, PersonalCare,
QuizModal, Customer, Hydration, Concerns, Products, Skin_profile, SkinTest)

"""
@admin.register(Choice)
class ChoiceAdmin(ImportExportModelAdmin):
    list_display = ('id', 'choice_text', 'marks')
    list_filter = ['choice_text']
    search_fields = ['choice_text']
"""


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4
    # fk_name = "question"
    # fieldsets = [
    #    (None, {'fields': ['choice_text', 'marks']}),
    # ]
    exclude = ('votes',)
    can_delete = True


@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    list_display = ('code', 'name', 'category', 'pc_name')
    list_filter = ['pub_date', 'category']
    search_fields = ['name', 'category__name', 'category__personalcare__name']
    list_display_links = ['name']
    ordering = ('code',)
    # list_editable = ['code', ]
    # prepopulated_fields = {"name": ("name",)}

    fieldsets = [
        ('Question Information', {'fields': [('code', 'name', 'category')]}),
        # ('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

    def pc_name(self, obj):
        """return choice question"""
        return obj.category.personalcare.name


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('id', 'code', 'name', 'personalcare')
    list_filter = ['name']
    search_fields = ['personalcare']
    list_display_links = ['code', 'name']
    ordering = ('code',)


@admin.register(QuizModal)
class QuizModalAdmin(ImportExportModelAdmin):
    list_display = ('test_code', 'pc_name', 'question_code', 'question', 'choice', 'marks', 'customer')
    list_filter = ['customer']
    search_fields = ['choice', 'customer__name']

    def question(self, obj):
        """return choice question"""
        return obj.choice.question
    
    def question_code(self, obj):
        """return choice question"""
        return obj.choice.question.code

    def marks(self, obj):
        """return user email"""
        return obj.choice.marks
    
    def test_code(self, obj):
        return obj.skin_test.code
    
    def pc_name(self, obj):
        return obj.choice.question.category.personalcare.name


@admin.register(PersonalCare)
class PersonalCareAdmin(ImportExportModelAdmin):
    list_display = ('id', 'code', 'name')
    list_filter = ['name']
    list_display_links = ['code', 'name']
    search_fields = ['name']
    ordering = ('code',)


@admin.register(Customer)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('employee_id', 'name', 'gender', 'age', 'location')
    list_filter = ['name']
    search_fields = ['employee_id', 'name']


@admin.register(Hydration)
class HydrationAdmin(ImportExportModelAdmin):
    list_display = ('id', 'test_code', 'customer', 'weight','physical_activity', 'water_intake', 'status')
    list_filter = ['customer', 'status']
    list_display_links = ['customer', 'status']
    search_fields =  ['customer', 'status']

    def test_code(self, obj):
        return obj.skin_test.code


@admin.register(Concerns)
class ConcernsAdmin(ImportExportModelAdmin):
    list_display = ('id', 'test_code', 'customer', 'is_primary')
    list_filter = ['customer']
    list_display_links = ['customer']
    search_fields =  ['customer']

    def test_code(self, obj):
        return obj.skin_test.code


@admin.register(Products)
class ProductsAdmin(ImportExportModelAdmin):
    list_display = ('code', 'title', 'cleanser', 'moisturizer', 'serum')
    list_filter = ['title']
    list_display_links = ['code', 'title']
    search_fields = ['code', 'title', 'cleanser', 'moisturizer', 'serum']

@admin.register(Skin_profile)
class SkinProfileAdmin(ImportExportModelAdmin):
    list_display = ('id', 'category_code', 'category', 'from_score', 'to_score', 'skin_status')
    list_filter = ['category', 'skin_status']
    list_display_links = ['category', 'skin_status']
    search_fields =['category', 'skin_status']

    def category_code(self, obj):
        """return category code"""
        return obj.category.code

@admin.register(SkinTest)
class SkinTestAdmin(ImportExportModelAdmin):
    list_display = ('code', 'customer')
    list_filter = ['code', 'customer']
    list_display_links = ['code', 'customer']
    search_fields = ['code', 'customer']