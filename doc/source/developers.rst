.. _developer:

Information for developers
==========================
If you would like to modify the LivingLabs API, first follow the API
installation tutorial.

Run end-to-end test
-------------------
After you made changes to the code, you can run an end-to-end test to check if
everything works properly. The test will setup a clean database, run the API
and test a site and participant. Afterwards everything is cleaned
up. To run the test, go to the root directory of the repository and issue:

.. sourcecode:: bash

    $ nosetests


Coding Style
------------
Core functionality should go in ll/core, the API (in ll/api) and Dashboard
(in ll/dashboard) the user this functionality.

Clients (in ll/client) are used for testing purposes and serve as baseline.

We (try to) stick to PEP8: https://www.python.org/dev/peps/pep-0008/ .


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
