====
EXIT
====
A django based multiple choice game. Answer some question and have fun.

Game flow
---------
1. Enter name
2. Answer question


Setup
-----
Linux::

  python3 -m venv venv
  source venv/bin/activate

Windows::

  python -m venv venv
  venv\Scripts\activate

Install requirements::

  python -m pip install --upgrade pip
  python -m pip install -r requirements.txt

Setup Django::

  python exit\manage.py migrate
  python exit\manage.py createsuperuser

Import some game data::

  python .\exit\manage.py import .\data\ --delete

Run development server::

  python exit\manage.py runserver

Tools
-----
Check unused imported::

  python -m pip install flake8
  flake8 --select F401 exit
