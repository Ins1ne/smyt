Simple test web application
===========================

Create dynamic models in memory from yaml file. This models can be edited from
django admin and support migrations. Also uses [
angular.js](https://angularjs.org) for frontend and contenteditable attribute
in table rows for inline edit.

Application uses sqlite3 as database, so it can work little slow ^_^


Install
-------

Create virtualenv, install requirements and run syncdb with migrations

    make

Local run
---------

Start development server on [http://127.0.0.1:8000](http://127.0.0.1:8000)

    make run

Run tests
---------

    make test


System requirements
-------------------

* Python 2.7 or Python 3.4
