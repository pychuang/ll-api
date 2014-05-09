Tutorial
========

Obtain source code
------------------

You can clone the repo with all Living Labs Challenge's code as follows:

.. sourcecode:: bash

    $ git clone git@bitbucket.org:living-labs/ll-challenge.git


Install prerequisites
---------------------

Then, installing the python prerequisites is easy:

.. sourcecode:: bash

    $ pip install -r requirements.txt

.. note: If you don't have pip yet, install it using "easy_install pip".

Done?
-----

If you only want to run a client, you have all you need. Expample clients are in ll/clients

In case you want to run your own version of the API (for testing purposes), you'll have to continue.

Setup MongoDB
-------------

If you don't already have MongoDB, follow this guide: http://docs.mongodb.org/manual/installation/.

Then you can choose to run with or without authentication (without is easier).

Authenticated
^^^^^^^^^^^^^

To run MongoDB with authorization enabled you can run with the provided configuration file config/mongodb.conf (you may have to edit the data path).

First start a deamon as follows:

.. sourcecode:: bash

    $ mongod --config ll-challenge/config/mongodb.con

Then, create users (replace ADMINSECRET and USERSECRET with actual password and remember those):

.. sourcecode:: bash

    # CREATE ADMIN
    $ mongo
    > use admin
    > db.createUser(
      {
        user: "admin",
        pwd: "ADMINSECRET",
        roles:
        [
          {
            role: "userAdminAnyDatabase",
            db: "admin"
          }
        ]
      }
    )
    
    # CREATE USER
    $ mongo -u admin -p --authenticationDatabase admin
    > use ll
    > db.createUser(
        {
          user: "ll",
          pwd: "USERSECRET",
          roles: ["readWrite"],
        }
    )

Create a local copy of the config/db.ini file and edit it to add the USERSECRET password. Also edit the database name if you wish.

.. sourcecode:: bash

    $ cp config/db.ini config/db.local.ini

Non-Authenticated
^^^^^^^^^^^^^^^^^

For developping purposes, this is fine. Otherwise, make sure to use authentication.
Start a MongoDB deamon as follows:

.. sourcecode:: bash

    $ mongod

Create a local copy of the config/db.ini file. Edit the database name if you wish.

.. sourcecode:: bash

    $ cp config/db.ini config/db.local.ini

Fill the database
-----------------

To create a example user and a site (for development/testing purposes):

.. sourcecode:: bash
    
    $ ./bin/admin user -c config/db.local.ini config/example-data/site.ini
    $ ./bin/admin user -c config/db.local.ini config/example-data/user.1.ini

Record both keys, you'll need them for the clients.

Run the API
-----------

To start the API, run the following command: 

.. sourcecode:: bash
    
    $ ./bin/api -c config/db.local.ini config/api.ini

If you did nit start MongoDB with authentication, or if you want automated code reloaded, then run this with --debug: 

.. sourcecode:: bash

    $ ./bin/api -c config/db.local.ini config/api.ini --debug


Run a Site
----------


Run a Participant
-----------------


Building Documentation
======================

To build the docs, run these commands in a shell:

.. sourcecode:: bash
    
    $ cd doc
    $ make html
    $ open doc/build/html/index.html

Troubleshooting
---------------


If you receive the following error when building the documentation:

.. sourcecode:: bash

    ValueError: unknown locale: UTF-8
    make: *** [html] Error 1

The, add these lines to your ~/.bash_profile:

.. sourcecode:: bash
    
    export LC_ALL=en_US.UTF-8
    export LANG=en_US.UTF-8
