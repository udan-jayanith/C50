import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
import os
from datetime import datetime
import markdown2


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    encoded_content = content.encode('utf-8')
    if default_storage.exists(filename):
        with default_storage.open(filename, 'wb') as f:
            f.write(encoded_content)
    else:
        default_storage.save(filename, ContentFile(encoded_content))

def deleteEntry(title):
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)

def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def markdownToHTML(md):
    return markdown2.markdown(md)
    
def listContains(q):
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename) for filename in filenames if filename.endswith(".md") and q.lower() in filename.lower()))

def getEntryMetadata(title):
    filePath = os.path.join(settings.MEDIA_ROOT, 'entries', f"{title}.md")
    states = os.stat(filePath)
    return {
        "created": datetime.fromtimestamp(states.st_ctime),
        "modified": datetime.fromtimestamp(states.st_mtime)
    }