# Django-Model-Job
Django application for enqueuing RQ (Redis Queue) jobs based on model changes.

## Definitions
Definition    | Meaning
------------- | -------------
Job           | A set of tasks, forming together a job, which might trigger
Task          | Call to a function, that might be enqueued

## How it works?
From the Django administrative panel you are able to define `Jobs`. Every `Job` is waiting for particular Django [model signal](https://docs.djangoproject.com/en/1.9/topics/signals/) to trigger (e.g. `pre_save` or `post_save`). Signal binding is defined via the administrative panel as well.

Whenever the signal is received, jobs rules are evaluated, and return a boolean value. In case of positive evaluation, the job triggers and tasks defined for the job are enqueued, while every task depends on the successful execution of the previous.

## Requirements
* [Django-RQ](https://github.com/ui/django-rq) (used for queuing jobs)
