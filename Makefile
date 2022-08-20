run-product-service:
	python product_service/manage.py runserver 0.0.0.0:8000 >> /dev/null 

run-checkout-service:
	python checkout_service/manage.py runserver 0.0.0.0:8001 >> /dev/null

run-backend:
	make run-product-service & make run-checkout-service


install:
	pip install -r requirements.txt