

def set_options(obj, options, keys=[]):
    for key in keys:
        value = None
        try:
            value = getattr(obj, key)
        except:
            setattr(obj, key, value)

        option = options.get(key, value)
        if option:
            setattr(obj, key, option)

def skip_files_and_directories(dirnames, filenames):
    for filename in filenames:
        for name in ['.DS_Store', '.localized', 'iPhoto Library', 'Aperture Library', '.cr2']:
            if name in filename:
                filenames.remove(filename)
    for dirname in dirnames:
        for name in ['iChat Icons', 'iPhoto Library', 'Aperture Library']:
            if name in dirname:
                dirnames.remove(dirname)
