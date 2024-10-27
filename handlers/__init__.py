# handlers/__init__.py
from .menu import MenuHandler
from .order import OrderHandler
from .feedback import FeedbackHandler
from .calculate import CalculateHandler
from .download import DownloadHandler
from .main_info import MainInfoHandler
from .agreement import AgreementHandler
from .test import TestHandler  # Добавлено

__all__ = [
    'MenuHandler',
    'OrderHandler',
    'FeedbackHandler',
    'CalculateHandler',
    'DownloadHandler',
    'MainInfoHandler',
    'AgreementHandler',  # Добавлено
    'TestHandler',      # Добавлено
]
