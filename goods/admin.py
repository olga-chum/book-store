from django.contrib import admin

from goods.models import Categories, Products

# admin.site.register(Categories)
# admin.site.register(Products)

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name']

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'author_name', 'quantity', 'price', 'discount']
    list_editable = ['discount']
    search_fields = ['name', 'author_name']
    list_filter = ['quantity', 'price', 'category']
    fields = [('name', 'slug', 'author_name'),
                                              'description',
                                              'category',
                                              'image',
                                              ('price', 'discount'),
                                              'quantity', 
                                              'age', 
                                              'year_of_publish', 
                                              'publisher', 
                                              'cycle']