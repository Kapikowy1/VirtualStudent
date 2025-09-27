import os, sys
import django
from django.core.management import call_command


sys.path.append('/home/username/DjangoDocoApp/DocumentAi') # TODO: insert your username there

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DocumentAi.settings')


def run_qcluster():
    try:
        activate_this = '/home/username/.virtualenvs/venv/bin/activate_this.py' # TODO: insert your username there
        exec(open(activate_this).read(), {'__file__': activate_this})
        django.setup()
        call_command('qcluster')
        print("succes qcluster runs")
    except Exception as e:
        print(f"An error occurred while running qcluster: {e}")

if __name__ == "__main__":
    run_qcluster()
