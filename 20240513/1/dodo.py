
from glob import glob
from doit.tools import create_folder

HTMLINDEX = "_build/html/index.html"

def task_html():
    """Generate HTML docs."""
    return {
        'actions': ['sphinx-build -M html "Documentation/docs" "_build"'],
        'file_dep': ["Documentation/docs/index.rst", "Documentation/docs/server_documentation.rst", "mood/server/__init__.py"],
        'task_dep': ['i18n'],
        'targets': [HTMLINDEX]
    }

def task_erase():
    """Erase all trash"""
    return {
        'actions': ['git clean -xdf']
    }


def task_pot():
    """Re-create .pot ."""
    return {
            'actions': ['pybabel extract --keywords=ngettext:2,3 --keywords=gettext:2 mood -o MMUD.pot'],
            'file_dep': glob('mood/server/*.py'),
            'targets': ['MMUD.pot'],
           }

def task_po():
    """Update translations."""
    return {
            'actions': ['pybabel update --ignore-pot-creation-date -D MMUD_Locale -d mood/po -l ru_RU.UTF-8 -i MMUD.pot'],
            'file_dep': ['MMUD.pot'],
            'targets': ['mood/po/ru_RU.UTF-8/LC_MESSAGES/MMUD_Locale.po'],
           }

def task_i18n():
    """Compile translations."""
    return {
            'actions': [
                (create_folder, [f'mood/po/ru_RU.UTF-8/LC_MESSAGES']),
                f'pybabel compile -D MMUD_Locale -l ru_RU.UTF-8 -i mood/po/ru_RU.UTF-8/LC_MESSAGES/MMUD_Locale.po -d mood/po'
                       ],
            'file_dep': ['mood/po/ru_RU.UTF-8/LC_MESSAGES/MMUD_Locale.po'],
            'targets': ['mood/po/ru_RU.UTF-8/LC_MESSAGES/MMUD_Locale.mo'],
           }

def task_test():
    """Update translations."""
    return {
            'actions': ['python3.10 -m unittest test_client_server.py'],
            'task_dep': ['i18n'],
           }

def task_sdist():
    """Build distributive."""
    return {
            'actions': ['python3.10 -m build -s -n'],
            'task_dep': ['erase'],
           }

def task_wheel():
    """Build binary wheel."""
    return {
            'actions': ['python3.10 -m build -w'],
            'task_dep': ['i18n'],
           }
