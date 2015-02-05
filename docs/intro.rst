============
Introduction
============

ScrewJack is a tiny command line tool for manipulating modules.

Basic Concepts
==============

Screwjack is a utility for helping module designers compose modules.
Modules are defined by a file named ``spec.json``. Here is the a example
of ``spec.json``: n

.. code:: javascript

      {
          "Name": "SVM",
          "Description": "A simple SVM",
          "Version": "0.1",
          "Cmd": "/usr/bin/python main.py",
          "Param": {
              "C": {
                  "Default": "",
                  "Type": "string"
              }
          },
          "Input": {
              "X": ["csv"],
              "Y": ["csv"]
          },
          "Output": {
              "MODEL": ["model.svm"]
          }
      }

In short, screwjack is a utility work around ``spec.json``. Typically,
there are 5 steps to write a module. The following tutorial will show
details steps.

#. Initialize a module
#. Add Inputs/Outputs/Params
#. Fill your code implementation
#. Test module

   #. Test in **local**
   #. Test in **docker**

#. Submit module

Installation
============

Screwjack will depends on `docker <http://www.docker.com/>`__, so you
should install docker first.

Install docker
--------------

A module developing environment need docker. Follow the link to install
docker for your linux distribution: http://docs.docker.io/installation/.

After that, don't forget add yourself into 'docker' group. For example,
in Ubuntu, you can do it like this:

.. code:: bash

      sudo usermod -aG docker your_linux_username

Install screwjack
-----------------

You can get screwjack directly from PyPI:

.. code:: bash

      pip install -U screwjack pyDataCanvas

Setup screwjack
---------------

Before you using screwjack, you should set your username. You can either
set environment variable:

.. code:: bash

       export DATACANVAS_USERNAME=your_username

Or, you can put your username into ``$HOME/.screwjack.cfg``:

::

      [user]
      username = your_username
      spec_server = playground.datacanvas.io:6006
      spec_auth = 3ce3e9fc12cf7260c433d2eec44c51ee


Or, you can use ``login`` subcommand to login into specific spec_server like following:

.. code:: bash

      screwjack --username=your_username --spec_server=playground.datacanvas.io:6006 login
