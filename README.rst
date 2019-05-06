============
simplechoice
============
I design a small multiple choice game. The django app simplechoice is the basic
core of this game. I write this package, because I like reusable apps. ;)

Take a look in the example folder and play with the project.


Development
-----------
Clone repo

.. code-block:: shell

  $ git clone https://github.com/axju/django-simplechoice.git

Create virtual environment for linux

.. code-block:: shell

  $ python3 -m venv venv
  $ source venv/bin/activate

or create virtual environment for windows

.. code-block:: shell

  $ python -m venv venv
  $ venv/Scripts/activate

update dev-tools

.. code-block:: shell

  $ python -m pip install --upgrade wheel pip setuptools twine tox flake8

Install local

.. code-block:: shell

  $ pip install -e .

Publish the packages

.. code-block:: shell

  $ python setup.py sdist bdist_wheel
  $ twine upload dist/*

Run some tests

.. code-block:: shell

  $ flake8 simplechoice
  $ python setup.py test
  $ python -m unittest discover -v
  $ tox

I do not know why, but tox will fail :(
