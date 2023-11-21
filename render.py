#!/usr/bin/env python3

import os
import sys
from string import Template

# This is so that it doesn't collide with
# bash/shell variables since I'm not using
# Jinja for portability reasons
class CustomTemplate(Template):
    delimiter = '%'

print(CustomTemplate(sys.stdin.read()).substitute(os.environ))
