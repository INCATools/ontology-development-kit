#!/usr/bin/env python3

import json
import sys

try:
    context = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit("Cannot read context file")

if not '@context' in context:
    sys.exit("No @context in supposed context file")

print("prefix,base")
for prefix_name, url_prefix in context['@context'].items():
    print(f"{prefix_name},{url_prefix}")
