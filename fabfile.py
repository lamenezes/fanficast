import binascii
import os

from fabric.api import env, lcd, local, prefix, run, settings
from fabric.contrib.project import rsync_project


# ssh connection settings
env.user = ''
env.hosts = [
    ''
]

# application conf
env.prj_name = ''
env.prj_path = '/home/%s/%s' % (env.user, env.prj_name)
env.local_path = os.path.dirname(os.path.abspath(__file__))
env.tmp_path = '%s/.tmp/%s' % (env.local_path, env.prj_name)
env.is_mezzanine = True

# passenger conf
# _remote_ python path
env.python_path = '/home/%s/opt/python2.7.11/bin/python' % env.user

# django utils
env.env_activate = '%s/env/bin/activate' % env.prj_path
env.django_path = '%s/prj' % env.prj_path
env.manage = 'python %s/manage.py' % env.django_path

# django conf
env.secret_key = ''
env.nevercache_key = ''
env.allowed_hosts = [
    ''
]

# db conf
env.db_name = env.prj_name
env.db_user = ''
env.db_pass = ''
env.db_host = ''

# template conf
TEMPLATES = {
    'passenger': {
        'template_path': 'deploy/passenger_wsgi.py.template',
        'output_path': '%s/passenger_wsgi.py' % env.local_path
    },
    'settings': {
        'template_path': 'deploy/local_settings.py.template',
        'output_path': '%s/%s/local_settings.py' % (env.local_path, env.prj_name)
    }
}


#########
# Utils #
#########


def clear_tmp():
    """ Remove the tmp file
    """
    local('rm -rf %s' % os.path.dirname(env.tmp_path))


def createsuperuser():
    """ Prompt the creations of a superuser remotely
    """
    with prefix('. %s' % env.env_activate):
        run('%s createsuperuser' % env.manage)


def create_virtualenv():
    """ Create the virtualenv remotely and install the requirements
    """
    run('virtualenv %s/env' % env.prj_path)
    with prefix('. %s/env/bin/activate' % env.prj_path):
        run('pip install -r %s/requirements.txt' % env.django_path)


def generate_secretkey():
    """ Generate a secretkey
    """
    return binascii.hexlify(os.urandom(64))


def migrate():
    """ Run django migrations remotely
    """
    run('test -e %s' % env.env_activate)
    with prefix('. %s' % env.env_activate):
        run('%s migrate' % env.manage)


def rsync_upload(remote_dir='', local_dir='', excludes=[]):
    """
    Upload the project using rsync. Exclude some files
    """
    if not remote_dir:
        remote_dir = env.prj_path
    if not local_dir:
        local_dir = env.tmp_path

    excludes += ["*.pyc", "*.pyo", "*.db", ".DS_Store", ".coverage",
                 "/static/media", "/.git", "/.hg", ".venv",
                 "*~", "*.sw[pmno]", "fabfile.py"]
    return rsync_project(remote_dir=remote_dir, local_dir=local_dir,
                         exclude=excludes)


#########################
# Install and configure #
#########################


def prepare():
    """ Create the folder structure locally to update the repo
    """
    local('mkdir -p %s' % env.tmp_path)
    with lcd(env.tmp_path):
        local('mkdir tmp public prj')
        local('touch tmp/restart.txt')

        local('cp -ax ../../* prj')
        local('mv prj/passenger_wsgi.py .')
        with settings(warn_only=True):
            local('mv prj/static public')


def create_files_from_templates():
    """ Create the parsed file from a given template path

    * template files must end with .template
    """
    for _, template_data in TEMPLATES.items():
        with open(template_data['template_path']) as template:
            text = template.read()
        text = text % env
        with open(template_data['output_path'], 'w') as f:
            f.write(text)


def append_local_settings():
    with open('%s/%s/settings.py' % (env.local_path, env.prj_name), 'a') as file:
        with open('deploy/include_settings.py') as include:
            file.write('\n' + include.read())


def install():
    """ First time installation (with superuser creation)
    """

    if not env.secret_key:
        env.secret_key = generate_secretkey()
    if not env.nevercache_key:
        env.nevercache_key = generate_secretkey()
    create_files_from_templates()
    prepare()

    if not env.is_mezzanine:
        append_local_settings()

    rsync_upload(os.path.dirname(env.prj_path), env.tmp_path)
    create_virtualenv()
    migrate()
    with prefix('. %s' % env.env_activate):
        run('%s collectstatic' % env.manage)
    createsuperuser()

    clear_tmp()


def update():
    """ Update the remote repo with the local files
    """
    prepare()
    excludes = ['settings.py', 'local_settings.py']
    rsync_upload(remote_dir=os.path.dirname(env.prj_path), excludes=excludes)
    clear_tmp()
