import os


PLUGINS_DIR = 'plugins'
PLUGINS_PATH = os.path.join(os.path.dirname(__file__), PLUGINS_DIR)


def discover_dictionaries():
    for plugin_name in os.listdir(PLUGINS_PATH):
        plugin_path = os.path.join(PLUGINS_PATH, plugin_name, plugin_name + '.py')
        if os.path.isfile(plugin_path):
            try:
                name = '.'.join([PLUGINS_DIR, plugin_name, plugin_name])
                module = __import__(name, fromlist=['Dictionary'])
                yield plugin_name, getattr(module, 'Dictionary')()
            except ImportError:
                print('Error: could not import Dictionary from {0}'.format(plugin_path))
