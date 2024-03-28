from django.contrib import admin
from .models import Orders, Items, RequestRows, CustomUser
# Register your models here.


class CustomUserAdmin(admin.ModelAdmin):

    list_display = ('first_name', 'last_name', 'email', 'role',)
    search_fields = ('first_name', 'last_name', 'email', 'role',)
    list_filter = ('role', 'first_name', 'last_name',)
    fields = ['first_name', 'last_name', 'email', 'role']


class ItemsAdmin(admin.ModelAdmin):

    list_display = ('item_id', 'item_group', 'unit_measurement', 'quantity', 'price',
                    'status', 'storage_location', 'contact_person')
    search_fields = ('item_group', 'unit_measurement', 'quantity', 'price',
                     'status', 'storage_location', 'contact_person')
    list_filter = ('item_group', 'unit_measurement', 'quantity', 'price',
                   'status', 'storage_location', 'contact_person')


class OrdersAdmin(admin.ModelAdmin):

    list_display = ('request_id', 'employee_name', 'item_id', 'unit_measurement', 'quantity', 'price',
                    'comment', 'status')

    search_fields = ('request_id', 'employee_name', 'item_id', 'unit_measurement', 'quantity', 'price',
                     'comment', 'status')
    list_filter = ('request_id', 'employee_name', 'item_id', 'unit_measurement', 'quantity', 'price',
                   'comment', 'status')


class RequestRowsAdmin(admin.ModelAdmin):

    list_display = ('request_row_id', 'request_id', 'item_id', 'unit_measurement', 'quantity', 'price', 'comment')
    search_fields = ('request_row_id', 'request_id', 'item_id', 'unit_measurement', 'quantity', 'price')
    list_filter = ('request_row_id', 'request_id', 'item_id', 'unit_measurement', 'quantity', 'price')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Items, ItemsAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(RequestRows, RequestRowsAdmin)
