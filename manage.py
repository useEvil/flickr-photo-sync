#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    app_path = os.path.dirname(os.path.realpath(__file__))
    module_path = os.path.dirname(os.path.join(app_path, 'flickrphotosync/'))
    if module_path not in sys.path:
        sys.path.append(module_path)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flickrphotosync.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
