from django.db import models

import django_rq


PRE_SAVE_SIGNAL = "pre_save"
POST_SAVE_SIGNAL = "post_save"
SIGNAL_TYPES = (
    (PRE_SAVE_SIGNAL, "Pre-Save"),
    (POST_SAVE_SIGNAL, "Post-Save"),
)


class Job(models.Model):
    name = models.CharField(max_length=100)
    signal_type = models.CharField(max_length=35, choices=SIGNAL_TYPES)
    app_name = models.CharField(max_length=35)
    model_name = models.CharField(max_length=35)

    def __unicode__(self):
        return self.name

    def should_execute(self, sender, instance):
        rules = self.rules.filter(parent=None)
        for rule in rules:
            success = rule.evaluate(sender, instance)
            if not success:
                return False
        return True

    def trigger(self, sender, instance, **kwargs):
        if self.should_execute(sender, instance):
            self._add_to_queue(sender, instance)

    def _add_to_queue(self, sender, instance):
        tasks = self.tasks.all()
        prev_job = None
        for task in tasks:
            func = task.func
            args = eval(task.args)
            kwargs = eval(task.kwargs)
            job = django_rq.enqueue(
                func=func, args=args, kwargs=kwargs,
                depends_on=getattr(prev_job, "id", None),
            )
            prev_job = job


class Task(models.Model):
    job = models.ForeignKey(Job, related_name="tasks")
    func = models.CharField(max_length=100)
    args = models.CharField(max_length=200, default="[]")
    kwargs = models.CharField(max_length=200, default="{}")
    timeout = models.PositiveSmallIntegerField(default=180)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]


class JobRule(models.Model):
    model_job = models.ForeignKey(Job, related_name="rules")
    name = models.CharField(max_length=35)
    condition = models.CharField(max_length=210)
    priority = models.SmallIntegerField()
    parent = models.ForeignKey(
        "self", blank=True, null=True, related_name="children"
    )

    def __unicode__(self):
        return self.name

    def evaluate(self, sender, instance):
        old = None
        new = instance
        try:
            old = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            pass

        try:
            success = eval(self.condition)
        except AttributeError:
            return False
        if not success:
            return False
        children = self.children.all()
        for child_rule in children:
            if not child_rule.evaluate(sender, instance):
                return False
        return True

    class Meta:
        ordering = ["priority"]
