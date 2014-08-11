import os
from imp import find_module, load_module

BASE_DIR = os.path.dirname(__file__)
PLUGINS_PATH = os.path.join(BASE_DIR, 'plugins')


def discover_dictionaries():
    import plugins
    for plugin_name in os.listdir(PLUGINS_PATH):
        plugin_path = os.path.join(PLUGINS_PATH, plugin_name, plugin_name + '.py')
        if os.path.isfile(plugin_path):
            try:
                fp, pathname, description = find_module(plugin_name, plugins.__path__)
                m1 = load_module(plugin_name, fp, pathname, description)
                fp, pathname, description = find_module(plugin_name, m1.__path__)
                m2 = load_module(plugin_name, fp, pathname, description)
                class_ = getattr(m2, 'Dictionary')
                yield plugin_name, class_()
            except ImportError:
                print('Error: could not import Dictionary from {0}'.format(plugin_path))
