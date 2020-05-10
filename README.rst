.. image:: https://travis-ci.org/tanayseven/skim.svg?branch=master
    :target: https://travis-ci.org/tanayseven/skim
    :alt: Travis CI

.. image:: https://sonarcloud.io/api/project_badges/measure?project=tanayseven_skim&metric=alert_status
    :target: https://sonarcloud.io/dashboard?id=tanayseven_skim
    :alt: Quality Gate

.. image:: https://sonarcloud.io/api/project_badges/measure?project=tanayseven_skim&metric=bugs
    :target: https://sonarcloud.io/project/issues?id=tanayseven_skim&resolved=false&types=BUG
    :alt: Bugs

.. image:: https://sonarcloud.io/api/project_badges/measure?project=tanayseven_skim&metric=code_smells
    :target: https://sonarcloud.io/project/issues?id=tanayseven_skim&resolved=false&types=CODE_SMELL
    :alt: Code Smells

.. image:: https://sonarcloud.io/api/project_badges/measure?project=tanayseven_skim&metric=coverage
    :target: https://sonarcloud.io/code?id=tanayseven_skim
    :alt: Code Coverage

.. image:: https://sonarcloud.io/api/project_badges/measure?project=tanayseven_skim&metric=duplicated_lines_density
    :target: https://sonarcloud.io/component_measures?id=tanayseven_skim&metric=Duplications&view=list
    :alt: Duplicated Lines

.. image:: https://sonarcloud.io/api/project_badges/measure?project=tanayseven_skim&metric=ncloc
    :target: https://sonarcloud.io/code?id=tanayseven_skim
    :alt: Lines of Code

.. image:: https://sonarcloud.io/api/project_badges/measure?project=tanayseven_skim&metric=sqale_rating
    :target: https://sonarcloud.io/component_measures?id=tanayseven_skim&metric=Maintainability&view=list
    :alt: Maintainability Rating

.. image:: https://sonarcloud.io/api/project_badges/measure?project=tanayseven_skim&metric=reliability_rating
    :target: https://sonarcloud.io/component_measures?id=tanayseven_skim&metric=Reliability&view=list
    :alt: Reliability Rating

.. image:: https://sonarcloud.io/api/project_badges/measure?project=tanayseven_skim&metric=security_rating
    :target: https://sonarcloud.io/component_measures?id=tanayseven_skim&metric=Security&view=list
    :alt: Security Rating

.. image:: https://sonarcloud.io/api/project_badges/measure?project=tanayseven_skim&metric=sqale_index
    :target: https://sonarcloud.io/component_measures?id=tanayseven_skim&metric=sqale_index
    :alt: Technical Debt

.. image:: https://sonarcloud.io/api/project_badges/measure?project=tanayseven_skim&metric=vulnerabilities
    :target: https://sonarcloud.io/component_measures?id=tanayseven_skim&metric=vulnerabilities
    :alt: Vulnerabilities

.. image:: https://img.shields.io/github/license/tanayseven/skim
    :target: https://www.gnu.org/licenses/gpl-3.0.en.html
    :alt: License

====================================
Skim - Smarter Keyboard Input Method
====================================

Skim is a sentence prediction software that can predict the next word that you are
going to type. It is designed as a text-based input method library that can be
integrated with other software applications such as text editors. It uses an
N-Grams model which can be trained based on English (or any other language) text
given as input. It exposes a ZMQ interface which can be used by other programs
to talk to it to predict the next word in the sentence.


Features
========

- A lightweight application starts fast and runs really fast
- N-Grams model that can be trained locally
- ZeroMQ as a protocol for other applications to talk to Skim
- Works out of the box once you get it running as a background process
- Is designed for any application that needs sentence prediction


Examples
========

This can be used in the following types of programs:

- Web application backend/frontend
- The desktop text editing application
- Can be running in a mobile device and talk to the app


Documentation
=============

Nothing here


Languages this works with
=========================

- English


Setup/Running
=============

Setup the pre-commit hook
-------------------------

.. code-block:: shell

    poetry run pre-commit install


Installing all the dependencies
-------------------------------

.. code-block:: shell

    poetry run install


Start the program as a process
------------------------------

.. code-block:: shell

    poetry run python -m skim.cli --run-process


Train the model
---------------

.. code-block:: shell

    poetry run python -m skim.cli --train --language=en-gb --files=input/


Running tests
-------------

.. code-block:: shell

    poetry run pytest


License
=======

The project is licensed under the GPLv3
