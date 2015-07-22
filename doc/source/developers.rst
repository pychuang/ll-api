.. _installation:

Information for developers
==========================
If you would like to modify the LivingLabs API, first follow the :ref:`tutorial to install the API<installation>`.

Run end-to-end test
-------------------
After you made changes to the code, you can run an end-to-end test to check if everything works properly.
The test will set=up a clean database, run the API and test a client and participant. Afterwards everything is cleaned
up. To run the test, go to the main directory of the repository(`ll-api/`) and issue:

.. sourcecode:: bash

    $ nosetests

Building Documentation
----------------------
.. note::  you probably don't have to build the documentation. A constantly
	updated version is available here: http://doc.living-labs.net/ .

Our documentation is created with Sphinx and comes largely directly from source
code. This makes it very easy to keep the documentation in sync with the code.

If you updated the documentation and want to test it, run these
commands in a shell from the root of the repository:

.. sourcecode:: bash
    
    $ cd doc
    $ make html
    $ open doc/build/html/index.html


If you receive the following error when building the documentation:

.. sourcecode:: bash

    ValueError: unknown locale: UTF-8
    make: *** [html] Error 1

Then, add these lines to your ~/.bash_profile:

.. sourcecode:: bash
    
    export LC_ALL=en_US.UTF-8
    export LANG=en_US.UTF-8
