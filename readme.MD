## REST API for managing products and checkout Django REST Framework

### Getting Started

First clone the repository from Github and switch to the project directory:

    $ git clone https://github.com/mhope-2/mfsassignment
    $ cd mfsassignment
    
Create a Vitual Environment (Linux, Mac)

    $ python3 -m venv env

Activate the virtualenv for your project

    $ source env/bin/activate
    
Install project requirements:

    $ make install
    
    
Then simply apply the migrations:

    $ cd product_service
    $ python manage.py makemigrations
    $ python manage.py migrate

    $ cd checkout_service
    $ python manage.py makemigrations
    $ python manage.py migrate

    

You can now run the development server:

    $ make run-backend

Run Tests:

    $ cd product_service
    $ python manage.py test

    $ cd checkout_service
    $ python manage.py test 


Swagger API doc:

    $ http://localhost:8000/swagger-ui/
    $ http://localhost:8000/swagger-ui/