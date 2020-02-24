# Pinocchio Pizza & Subs

## Table of contents
* [Description](#description)
* [Installation](#installation)
* [Technologies](#technologies)

## Description

This project is a web application for handling a pizza restaurant’s online orders, with features available for both users and restaurant owners. The menu was built with relational database design, allowing restaurant owner to update their menu items with ease on Django Admin site.

Made for project 3 of CS50W.

### Features
User can:
- Browse restaurant's menu, select toppings/extras (if any) and add items to cart
- Manage cart with an option to remove selected items
- Submit order, view order details and check order's status

Restaurant owner can: 
- Add and update menu items
- View submitted and in-progress orders
- Change an order's status

## Installation

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

```
pip3 install django
pip3 install django-modeladmin-reorder
```

### Installing
1. Clone the repo
```
git clone https://github.com/meemeee/pizza.git
```

2. Run on local server
```
python3 manage.py runserver
```

## Technologies

* [Django](https://docs.djangoproject.com/en/3.0/) - Python Web framework
* [Bootstrap](https://getbootstrap.com/docs/4.0/) - CSS framework
* [AOS](https://michalsnik.github.io/aos/) - Animate on scroll library