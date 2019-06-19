import os
import sys
from django.core.wsgi import get_wsgi_application

INTERP = "~/opt/python2.7.11/bin/python"
# INTERP is present twice so that the new python interpreter knows the actual executable path
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

cwd = os.getcwd()
sys.path.append(cwd)
sys.path.append(cwd + '/prj')

sys.path.insert(0, cwd + '/env/bin')
sys.path.insert(0, cwd + '/env/lib/python2.7/site-packages/django')
sys.path.insert(0, cwd + '/env/lib/python2.7/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = "prj.fanficast.settings"
application = get_wsgi_application()
