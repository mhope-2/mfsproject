### Product and Checkout Management Service

### Brief Overview
This project contains two django backend services (product service and checkout service) and a frontend written in Vue. The backend services are two separate django projects that interact via API calls. The product service consists of a user app, a customer app and a product app while the checkou service contains a quotation app and an invoice app; they all have CRUDL operations.

The frontend app makes requests to both services based on the flow from products to checkout.


### Getting Started

First clone the repository from Github and switch to the project directory:

    $ git clone https://github.com/mhope-2/mfsproject.git
    $ cd mfsproject
    
Create a Vitual Environment (Linux, Mac)

    $ python3 -m venv env

Activate the virtualenv for your project

    $ source env/bin/activate
    
Install project requirements using make:

    $ make install
    
    
Then simply apply the migrations:

    $ cd product_service
    $ python manage.py makemigrations
    $ python manage.py migrate

    $ cd checkout_service
    $ python manage.py makemigrations
    $ python manage.py migrate

    

You can now run the development server using make:

    $ make run-backend

Run Tests:

    $ cd product_service
    $ python manage.py test

    $ cd checkout_service
    $ python manage.py test (depends on product service)


Swagger API doc:

    $ http://localhost:8000/swagger-ui/
    $ http://localhost:8001/swagger-ui/