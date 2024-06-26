import logging
import logging.config
import colorlog

# Define the logging configuration
logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'color': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            'log_colors': {
                'DEBUG': 'white',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'color',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'filename': 'app.log',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True
        },
        'my_module': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False
        },
        'aio_pika.robust_connection': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': False
        },
        'aiormq.connection': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': False
        },
        'aio_pika.exchange': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': False
        },
        'aio_pika.connection': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': False
        },
        'aio_pika.queue': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': False
        },
        'websockets.client': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': False
        },
        'websockets.server': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': False
        },
    }
}

# Configure logging
logging.config.dictConfig(logging_config)
