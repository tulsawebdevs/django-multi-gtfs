How To Contribute
=================
We'd love your help in building ``multigtfs``.  Here's some tips:

* Fork the project on GitHub_, clone it locally, and create a
  feature branch for your work.
* When working with your Django project, use
  ``pip install -e /path/to/multigtfs`` to use your modified version.
* Use a seperate virtualenv_ for development (virtualenvwrapper_ is helpful
  as well).  Install the recommended requirements
  (``pip install -r requirements.txt; pip install -r requirements.dev.txt``).
* Test changes with ``./run_tests.py``
* Test `PEP 8`_ and code coverage with ``./qa_check.sh``
* Add yourself to ``AUTHORS.rst``
* When you are happy with the change, publish your branch on GitHub and
  request a merge to the master branch.

.. _virtualenv: http://www.virtualenv.org/en/latest/
.. _`PEP 8`: http://www.python.org/dev/peps/pep-0008/
.. _GitHub: https://github.com/tulsawebdevs/django-multi-gtfs
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/
