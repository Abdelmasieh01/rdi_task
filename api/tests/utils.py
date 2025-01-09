import os
from django.core.files.base import ContentFile

def get_test_file_path(filename):
    """Get the absolute path of the test file."""
    return os.path.join(os.path.dirname(__file__), 'test_files', filename)

def get_file(filename):
    file_path = get_test_file_path(filename)
    with open(file_path) as f:
        file = ContentFile(f.read(), name=filename)
    return file