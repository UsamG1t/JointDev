def task_html():
    """Generate HTML docs."""
    return {
        'actions': ['sphinx-build -M html "." "_build"']
    }

def task_erase()"
    """Erase all trash"""
    return {
        'actions': ['git clean -xdf']
    }
