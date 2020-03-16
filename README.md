# Pinocchio Pizza & Subs

## Table of contents
* [Description](#description)
* [Installation](#installation)
* [Technologies](#technologies)

## Description

This project is a web application for handling a pizza restaurant’s online orders, with features available for both users and restaurant owners. The menu was built with Django framework and relational database design, allowing restaurant owner to update their menu items with ease on Django Admin site.

Made for project 3 of [CS50Web](https://cs50.harvard.edu/web/).

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

1. Clone the repo
```
git clone https://github.com/meemeee/pizza.git
```

2. Install requirements
```
pip3 install -r requirements.txt
```

3. Run on local server
```
python3 manage.py runserver
```

## Technologies

* [Django](https://docs.djangoproject.com/en/3.0/) - Python Web framework
* [Bootstrap](https://getbootstrap.com/docs/4.0/) - CSS framework
* [AOS](https://michalsnik.github.io/aos/) - Animate on scroll library