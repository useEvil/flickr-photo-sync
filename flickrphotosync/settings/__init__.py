import os
import sys

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from settings import *

# load local settings file
try:
    from local import *
except Exception, e:
    # Ok... No local overrides
    pass
