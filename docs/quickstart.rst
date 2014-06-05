===========
Quick Start
===========

You can get screwjack directly from PyPI:

.. code:: bash

    pip install screwjack

Basic Concepts
==============

Screwjack is a utility for helping module designers compose modules.
Modules are defined by a file named ``spec.json``. Here is the a example
of ``spec.json``:

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

Step 0: Install docker and screwjack
====================================

Install docker
--------------

A module developing environment need docker. Follow the link to install
docker for your linux distribution :
http://docs.docker.io/installation/.

After that, don't forget add yourself into 'docker' group. For example,
in Ubuntu, you can do it like this:

.. code:: bash

      sudo usermod -aG docker your_linux_username

Install screwjack
-----------------

.. code:: bash

      pip install -U screwjack

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

Or, you can add ``--username`` option for screwjack like following:

.. code:: bash

      screwjack --username=your_username init
      screwjack --username=your_username param_add
      screwjack --username=your_username input_add
      screwjack --username=your_username output_add

Step 1: Initialize a module
===========================

::

      screwjack init --name="SVM" --description="A simple SVM"

Then, it will prompt to setup other options, like the following. In this
case, we want use scikit-learn, which are packed in base image
``zetdata/sci-python:2.7``.

::

      Module Version [0.1]: 
      Module Entry Command [/usr/bin/python main.py]: 
      Base Image [zetdata/ubuntu:trusty]: zetdata/sci-python:2.7
      Sucessfully created 'svm'

Or, you can use single command to do this:

.. code:: bash

      screwjack init --name=SVM --description="A simple SVM" --version="0.1" --cmd="/usr/bin/python main.py" --base-image="zetdata/sci-python:2.7"

Now, we can get a directory with initial verison of basic module:

::

      svm
      |-- Dockerfile
      |-- main.py
      |-- spec.json
      `-- specparser.py

      0 directories, 4 files

We should change to the directory of the new module, the following steps
will assume we are working at that directory.

.. code:: bash

      cd svm

Step 2: Add Input/Output/Param
==============================

Image we want create a module with two \*Input\*s, one **Output**, and
one parameter. Just like the following diagram shows:

.. code:: ditaa

              /-----------------\
              | SVM             |
      X(csv)  +-----------------+
    --------->|                 |  MODEL(model.svm)
              | Params:         |------------------->
              +=================|
      Y(csv)  | o C(float)      |
    --------->|                 |
              \-----------------/

|image0|

Now we can add a parameter using the following command:

.. code:: bash

      screwjack param_add C

And, we add two Inputs:

.. code:: bash

      screwjack input_add X csv
      screwjack input_add Y csv

Finally, a Output:

.. code:: bash

      screwjack output_add model model.svm

Step 3: Fill your code implementation
=====================================

Now, you can write your awesome implementation now:

.. code:: bash

      vim main.py

If you want add additional files for this module, don't forget add files
in ``Dockerfile``.

.. code:: bash

      vim Dockerfile

For example, if you have additional file, you should append the
following line into ``Dockerfile``:

::

      ADD your_additional_file /home/run/

In the case if you want add additional folder, you should append a line
like this:

::

      ADD your_additional_folder /home/run/your_additional_folder

For more information about ``Dockerfile``, please reference
`Dockerfile <http://docs.docker.io/reference/builder/>`__.

Step 4.1: Test in **local**
===========================

After write fill code into this module, we might want test it. The
``screwjack run`` subcommands are design for this.

.. code:: bash

      screwjack run local --help

.. code:: bash

      Usage: screwjack run local [OPTIONS]
      Options:
        --param-C TEXT  Param(string)
        --X TEXT        Input
        --Y TEXT        Input
        --MODEL TEXT    Output
        --help          Show this message and exit.

Now, we can test our module in local environment, which is very close to
your developing environment.

.. code:: bash

      screwjack run local --param-C=0.1 --X=a.csv --Y=b.csv --MODEL=tmp.model

Step 4.2: Test in **docker**
============================

Then, we can try to execute module by docker:

.. code:: bash

      screwjack run docker --param-C=0.1 --X=a.csv --Y=b.csv --MODEL=tmp.model

Step 5: Submit module
=====================

You should provide the URL of ``spec_server`` to submit:

.. code:: bash

      screwjack submit

.. |image0| image:: ./module.png
