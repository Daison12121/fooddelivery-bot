from sqladmin import ModelView
from app.models import User, Restaurant, MenuItem, Order

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email]
    name = "User"
    name_plural = "Users"
    icon = "fa fa-user"

class RestaurantAdmin(ModelView, model=Restaurant):
    column_list = [Restaurant.id, Restaurant.name]
    name = "Restaurant"
    name_plural = "Restaurants"
    icon = "fa fa-cutlery"

class MenuItemAdmin(ModelView, model=MenuItem):
    column_list = [MenuItem.id, MenuItem.name, MenuItem.price]
    name = "Menu Item"
    name_plural = "Menu Items"
    icon = "fa fa-list"

class OrderAdmin(ModelView, model=Order):
    column_list = [Order.id, Order.user_id, Order.status]
    name = "Order"
    name_plural = "Orders"
    icon = "fa fa-shopping-cart"
