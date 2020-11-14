import os


def load_config(mode=os.environ.get('FLASK_ENV')):
    """Load config."""
    try:
        if mode == 'production':
            from .production import ProductionConfig
            return ProductionConfig
        elif mode == 'testing':
            from .testing import TestingConfig
            return TestingConfig
        else:
            from .development import DevelopmentConfig
            return DevelopmentConfig
    except ImportError:
        from .config import Config
        return Config
