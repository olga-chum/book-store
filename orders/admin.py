from django.contrib import admin

from orders.models import Order, OrderItem

class OrderItemTabulareAdmin(admin.TabularInline):
    model = OrderItem
    fields = "product", "name", "author_name", "price", "quantity"
    search_fields = (
        "product",
        "name",
        "author_name"
    )
    extra = 0


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = "order", "product", "name", 'author_name', "price", "quantity"
    search_fields = (
        "order",
        "product",
        "name",
        'author_name'
    )


class OrderTabulareAdmin(admin.TabularInline):
    model = Order
    fields = (
        "status",
        "is_paid",
        "created_timestamp",
    )

    search_fields = (
        "is_paid",
        "created_timestamp",
    )
    readonly_fields = ("created_timestamp",)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "status",
        "is_paid",
        "created_timestamp",
    )

    search_fields = (
        "id",
    )
    readonly_fields = ("created_timestamp",)
    list_filter = (
        "status",
        "is_paid",
    )
    inlines = (OrderItemTabulareAdmin,)