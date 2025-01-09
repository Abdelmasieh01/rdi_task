import os
from django.core.files.base import ContentFile
from django.conf import settings


def get_test_file_path(filename):
    """Get the absolute path of the test file."""
    return os.path.join(os.path.dirname(__file__), 'test_files', filename)

def get_file(filename):
    file_path = get_test_file_path(filename)
    with open(file_path) as f:
        file = ContentFile(f.read(), name=filename)
    return file

def delete_file(file_path):
    """Delete a single file by its path."""
    if not file_path.startswith(str(settings.BASE_DIR)):
        file_path = os.path.join(settings.BASE_DIR, file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted file: {file_path}")
    else:
        print(f"File not found: {file_path}")