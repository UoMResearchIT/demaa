#!/usr/bin/env python

import json
import os.path, pkgutil
import modules

pkgpath = os.path.dirname(modules.__file__)

print(json.dumps([name for _, name, _ in pkgutil.iter_modules([pkgpath])]))
