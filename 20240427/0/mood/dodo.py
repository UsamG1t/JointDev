def task_html():
    """Generate HTML docs."""
    return {
        'actions': ['sphinx-build -M html "Documentation" "_build"'],
        'file_dep': ["Documentation/index.rst", "Documentation/server_documentation.rst", "server/__init__.py"]
    }

def task_erase():
    """Erase all trash"""
    return {
        'actions': ['git clean -xdf']
    }
