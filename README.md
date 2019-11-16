# Project 3

Web Programming with Python and JavaScript

*REQUIRED*
"Reorder" package for Admin page
 $ pip3 install django-modeladmin-reorder

*DESCRIPTION*
In this project, I created an online shopping page for a pizza store. User can:
- View Menu: sectioned into Pizza, Subs, Salads,... with a Table of Contents on the side for easy browsing.
- Add item to cart: each type of item is displayed differently depending on the kind of selections and add-ons it allows. (E.g subs has sub-extra section, pizza with toppings has topping section,...)
- Manage cart: user can view details and remove items from cart. Cart will not have duplicates - adding the same item to cart will result in an increase in quantity of the existing cart item.
- Place order: there will be an confirmation modal before order submission.

My personal touch:
- Admin side: can view all in-progress orders, check details and change their status.
- User side: can view orders and check their status.