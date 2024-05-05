
from glob import iglob, glob
from doit.tools import create_folder

ZIPARCH = 'arch.zip'
HTMLINDEX = "Documentation/_build/html/index.html"

def task_html():
    """Generate HTML docs."""
    return {
        'actions': ['sphinx-build -M html "Documentation" "_build"'],
        'file_dep': ["Documentation/index.rst", "Documentation/server_documentation.rst", "server/__init__.py"],
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
            'actions': ['pybabel extract -o MMUD.pot .'],
            'file_dep': [*iglob('*.py')],
            'targets': ['MMUD.pot'],
           }

def task_po():
    """Update translations."""
    return {
            'actions': ['pybabel update -D MMUD_Locale -d po -l ru_RU.UTF-8 -i MMUD.pot'],
            'file_dep': ['MMUD.pot'],
            'targets': ['po/ru_RU.UTF-8/LC_MESSAGES/MMUD_Locale.po'],
           }

def task_mo():
    """Compile translations."""
    return {
            'actions': [
                (create_folder, [f'po/ru_RU.UTF-8/LC_MESSAGES']),
                f'pybabel compile -D MMUD_Locale -l ru_RU.UTF-8 -i po/ru_RU.UTF-8/LC_MESSAGES/MMUD_Locale.po -d po'
                       ],
            'file_dep': ['po/ru_RU.UTF-8/LC_MESSAGES/MMUD_Locale.po'],
            'targets': ['po/ru_RU.UTF-8/LC_MESSAGES/MMUD_Locale.mo'],
           }

