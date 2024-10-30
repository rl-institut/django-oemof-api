
.. figure:: https://user-images.githubusercontent.com/14353512/185425447-85dbcde9-f3a2-4f06-a2db-0dee43af2f5f.png
    :align: left
    :target: https://github.com/rl-institut/django-oemof-api/
    :alt: Repo logo

================
django-oemof-api
================

**A to test [django-oemof](https://github.com/rl-institut/django-oemof).**

.. list-table::
   :widths: auto

   * - License
     - |badge_license|
   * - Documentation
     - |badge_documentation|
   * - Publication
     - 
   * - Development
     - |badge_issue_open| |badge_issue_closes| |badge_pr_open| |badge_pr_closes|
   * - Community
     - |badge_contributing| |badge_contributors| |badge_repo_counts|

.. contents::
    :depth: 2
    :local:
    :backlinks: top

Requirements
============
python 3.10
postgresql 14 or higher

Introduction
============
0. create a virtual environment with python 3.10

1. install requirements in the virtual environment with

```
    pip install -r requirements
```

2. setup a postgresql database and provide the following environment variables

```
SQL_ENGINE="django.db.backends.postgresql"
SQL_DATABASE="name_of_your_database"
SQL_USER="name_of_your_user"
SQL_PASSWORD="pw_of_your_user"
SQL_HOST="localhost"
SQL_PORT="postgresql port, usually 5434"

# replace 'localhost' by the name of the container if using docker
CELERY_BROKER_URL="redis://localhost:6379/0"
CELERY_RESULT_BACKEND="redis://localhost:6379/0"

```

3. run migrations

```
    python manage.py migrate
```

4. run the server

```
    python manage.py runserver
```

4. visit the webapp at 127.0.0.1:8000/oemof

In order to simulate a scenario from a datapackage you should place datapackages in the django_oemof_api/data/oemof folder.

One this is done, open a new terminal with the same virtual environment and make sure you provide those two environment variables as well

```
CELERY_BROKER_URL="redis://localhost:6379/0"
CELERY_RESULT_BACKEND="redis://localhost:6379/0"

```
Then start the celery worker with

```
celery -A django_oemof_api.celery worker --loglevel=info -E
```


Finally, you can send a post request from a third terminal

```
import requests
import json

HOST = "http://127.0.0.1:8000"
SIMULATE_URL = f"{HOST}/oemof/simulate"

payload = {
    "scenario": "<name of a scenario datapackage within data/oemof folder>",
    "parameters": json.dumps({"some": "paremeters"}),
}

with requests.session() as client:
    req = client.post(
        SIMULATE_URL,
        data=payload,
    )
    answer = json.loads(req.text)
    print(f"{SIMULATE_URL}}?task_id={answer['task_id']}")
```


Documentation
=============
| The documentation is created with Markdown using `MkDocs <https://www.mkdocs.org/>`_.
| All files are stored in the ``docs`` folder of the repository.
| A **GitHub Actions** deploys the ``production`` branch on a **GitHub Page**.
| The documentation page is `rl-institut.github.io/django-oemof-api/ <https://rl-institut.github.io/django-oemof-api/>`_

Collaboration
=============
| Everyone is invited to develop this repository with good intentions.
| Please follow the workflow described in the `CONTRIBUTING.md <CONTRIBUTING.md>`_.

License and Citation
====================
| The code of this repository is licensed under the **MIT License** (MIT).
| See `LICENSE.txt <LICENSE.txt>`_ for rights and obligations.
| See the *Cite this repository* function or `CITATION.cff <CITATION.cff>`_ for citation of this repository.
| Copyright: `django-oemof-api <https://github.com/rl-institut/django-oemof-api/>`_ © `Reiner Lemoine Institut <https://reiner-lemoine-institut.de/>`_ | `MIT <LICENSE.txt>`_


.. |badge_license| image:: https://img.shields.io/github/license/rl-institut/django-oemof-api
    :target: LICENSE.txt
    :alt: License

.. |badge_documentation| image:: https://img.shields.io/github/actions/workflow/status/rl-institut/django-oemof-api/gh-pages.yml?branch=production
    :target: https://rl-institut.github.io/django-oemof-api/
    :alt: Documentation

.. |badge_contributing| image:: https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat
    :alt: contributions

.. |badge_repo_counts| image:: http://hits.dwyl.com/rl-institut/django-oemof-api.svg
    :alt: counter

.. |badge_contributors| image:: https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square
    :alt: contributors

.. |badge_issue_open| image:: https://img.shields.io/github/issues-raw/rl-institut/django-oemof-api
    :alt: open issues

.. |badge_issue_closes| image:: https://img.shields.io/github/issues-closed-raw/rl-institut/django-oemof-api
    :alt: closes issues

.. |badge_pr_open| image:: https://img.shields.io/github/issues-pr-raw/rl-institut/django-oemof-api
    :alt: closes issues

.. |badge_pr_closes| image:: https://img.shields.io/github/issues-pr-closed-raw/rl-institut/django-oemof-api
    :alt: closes issues
