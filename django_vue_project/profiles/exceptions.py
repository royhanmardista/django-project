from __future__ import unicode_literals
from django.db import IntegrityError
from rest_framework.views import Response, exception_handler
from rest_framework import status


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first to get the standard error response.
    response = exception_handler(exc, context)
    print(response)
    return response
    # if there is an IntegrityError and the error response hasn't already been generated
    if isinstance(exc, IntegrityError) and not response:        
        data = response.data
        print(data.items(), 'sdfasdfasdf')
        response.data = {}
        errors = []
        for field, value in data.items():            
            errors.append("{} : {}".format(field, " ".join(value))) 
        response.data['errors'] = errors
        response.data['status'] = False 
        response.data['exception'] = str(exc)
 
    return response
