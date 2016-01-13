from django.apps import AppConfig
from django.db.models import signals
from django.apps import apps


class ModelJobAppConfig(AppConfig):
    name = 'modeljob'
    verbose_name = "Model Job"

    def ready(self):
        try:
            jobs = self.get_model("Job").objects.all()
            for job in jobs:
                self._bind_job(job)
        except Exception:
            import traceback
            traceback.print_exc()

    def _bind_job(self, job):
        app = apps.get_app_config(job.app_name)
        model_cls = self._get_app_model(app, job.model_name)
        signal = getattr(signals, job.signal_type)
        signal.connect(job.trigger, sender=model_cls, weak=False)

    @staticmethod
    def _get_app_model(app, model_name):
        return app.models[model_name.lower()]
