import re

def processLink(app, docname, source):
    original = source[0]
    subbed = re.sub(r"\.md", r"\.html", original)
    source[0] = subbed

def setup(app):
    app.connect('source-read', processLink)
