from zipfile import ZipFile

def task_html():
    """Generate HTML docs."""
    return {
        'actions': ['sphinx-build -M html "Documentation" "_build"'],
        'file_dep': ["Documentation/index.rst", "Documentation/server_documentation.rst", "server/__init__.py"],
        'targets': ["Documentation/_build/html/index.html"]
    }

# def zipp(path, outfile):
#     with ZipFile(outfile, "w") as file:


def task_zip():
    """Create ZIP archive"""

def task_erase():
    """Erase all trash"""
    return {
        'actions': ['git clean -xdf']
    }
