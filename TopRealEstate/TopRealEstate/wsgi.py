import os
import sys

sys.path.append('/root/TopRealEstate')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TopRealEstate.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
