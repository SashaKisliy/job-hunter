import os

from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
application = get_wsgi_application()

with open('dump_json/data.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', 'job_hunter', indent=4, stdout=f)
