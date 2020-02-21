.. image:: https://travis-ci.org/tanayseven/skim.svg?branch=master
    :target: https://travis-ci.org/tanayseven/skim
    :alt: Travis CI

.. image:: https://coveralls.io/repos/github/tanayseven/skim/badge.svg?branch=master
    :target: https://coveralls.io/github/tanayseven/skim?branch=master
    :alt: Coveralls

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

Installing all the dependencies
-------------------------------

.. code-block:: shell

    poetry run install


Start the program as a process
------------------------------

.. code-block:: shell

    poetry run python -m skim.cli --run-process


Train the model
------------------------------

.. code-block:: shell

    poetry run python -m skim.cli --train --language=en-gb --files=input/


Running tests
-------------

.. code-block:: shell

    poetry run pytest


License
=======

The project is licensed under the GPLv3
