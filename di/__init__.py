from dishka import make_container

from .providers.app import AppProvider

container = make_container(AppProvider())