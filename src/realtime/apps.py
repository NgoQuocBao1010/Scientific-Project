from django.apps import AppConfig


class RealtimeConfig(AppConfig):
    name = "realtime"

    def ready(self):
        import realtime.signals
