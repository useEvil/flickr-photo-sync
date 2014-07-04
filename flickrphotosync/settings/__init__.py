import os
import sys

from settings import *

# load local settings file
try:
    from local import *
except Exception, e:
    # Ok... No local overrides
    pass
