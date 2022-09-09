"""
WSGI config for supercapacity project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import inspect
# ML registry
from ml.registry import MLRegistry
from ml.income_classifier.dummy_model import Dummy

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supercapacity.settings')

application = get_wsgi_application()

try:
    registry = MLRegistry()  # create ML registry
    # Random Forest classifier
    rf = Dummy()
    # add to ML registry
    registry.add_algorithm(endpoint_name="dummy_model",
                           algorithm_object=rf,
                           algorithm_name="dummy model",
                           algorithm_status="production",
                           algorithm_version="0.0.4",
                           owner="Dmitry Vedenichev",
                           algorithm_description="Dummy model for front test",
                           algorithm_code=inspect.getsource(Dummy))

except Exception as e:
    print("Exception while loading the algorithms to the registry,", str(e))
