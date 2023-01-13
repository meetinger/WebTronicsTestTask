# Logger Configuration
LOGGER_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            'access': {
                '()': 'uvicorn.logging.AccessFormatter',
                'fmt': '%(levelprefix)s [%(asctime)s] - %(client_addr)s - "%(request_line)s" %(status_code)s',
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "use_colors": True
            },
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s [%(asctime)s] - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "use_colors": True
            },
            'default_with_name': {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s [%(asctime)s] %(name)s: - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "use_colors": True
            },
            "default_without_color": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s [%(asctime)s] - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "use_colors": False
            },
            'default_with_name_without_color': {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s [%(asctime)s] %(name)s: - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "use_colors": False
            }

        },
        "handlers": {
            'access': {
                'class': 'logging.StreamHandler',
                'formatter': 'access',
                'stream': 'ext://sys.stdout'
            },
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            "default_with_name": {
                "formatter": "default_with_name",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            "file": {
                'class': 'logging.FileHandler',
                'formatter': 'default_without_color',
                'filename': 'logs.log'
            },
            "file_with_name": {
                'class': 'logging.FileHandler',
                'formatter': 'default_with_name_without_color',
                'filename': 'logs.log'
            }
        },
        "loggers": {
            '': {
                "handlers": ["default_with_name", 'file_with_name'],
                "level": "INFO",
                "propagate": False
            },
            "uvicorn": {
                "handlers": ["default", 'file'],
                "level": "INFO",
                "propagate": True
            },
            'uvicorn.access': {
                'handlers': ['access', 'file'],
                'level': 'INFO',
                'propagate': False
            },
            'uvicorn.error': {
                "handlers": ["default", 'file'],
                'level': 'INFO',
                'propagate': False
            }
        },
    }