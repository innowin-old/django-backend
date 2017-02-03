import os
import yaml


def get_config(BASE_DIR):
    default_config_path = os.path.join(BASE_DIR, 'default-config.yml')
    with open(default_config_path, 'r') as stream:
        default_config = yaml.load(stream)
    config_path = os.path.join(BASE_DIR, 'config.yml')
    if os.path.exists(config_path):
        with open(config_path, 'r') as stream:
            config = yaml.load(stream)
            default_config.update(config)
    default_config['BASE_DIR'] = BASE_DIR
    return default_config


def get_db_settings(config):
    BASE_DIR = config.get('BASE_DIR')
    db_config = config.get('DATABASE')
    if db_config is None:
        return None
    db_config = dict(db_config)  # copy
    if db_config['ENGINE'] == 'django.db.backends.sqlite3':
        db_config['NAME'] = os.path.join(BASE_DIR, db_config['NAME'])
    return db_config
