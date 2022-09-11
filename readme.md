<h1>Overview</h1>
Django application to handle multiple courier providers

<h1>Requirments</h1>

- Python version 3.8.12

<h1>Setup</h1>

- ``pip install poetry`` 
- ``poetry install`` 
- Run command `python manage makemigrations`
- Run command `python manage migrate`


<h1>How to run</h1>

- Run command `python manage runserver`

  
<h1>Application APIs</h1>

- [GET] /v1/shipments/
    - return list of created shipments
- [POST]  /v1/shipments/
    - Create a shipment with specific defined provider
    
    
<h1>Framework usage</h1>

- To add new provider you have to create new Provider and client class using the abstract classes in ``providers_management/abstract.py``
- Add the new provider class to ```settings.COURIER_PROVIDERS```


