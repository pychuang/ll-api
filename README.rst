Tutorial
========


This tutorial describes how to install, run and develop with the Living Labs
Challenge software. 

If all you want is to compete in the challenge, you do not necessarily need any
of the following. Instead you could just go ahead and implement your client
that talks to our API at http://living-labs.net:5000/api/.
However, the code we provide does include a simple baseline implementation 
that talks to our API and that you may find useful.
Furthermore, if you do install the API/dashboard/.. on your own machine,
debugging your code will become much easier.

In case you have any comments or questions, please do not
hesitate to file an issue here: http://git.living-labs.net/ll-challenge/issues.
Or, you can contact the main developer directly at anne.schuth@uva.nl.

For more information on the challenge, see http://living-labs.net/challenge.
Documentation (including this tutorial) can be found here:
http://doc.living-labs.net/en/latest/


Obtain source code
------------------

You can clone the repository that contains all the Living Labs Challenge's code
as follows:

.. sourcecode:: bash

    $ git clone https://bitbucket.org/living-labs/ll-challenge.git

In case you plan on making changes, please first make a fork through the
bitbucket interface and then clone your own fork. That way, you will be able to
push your changes and to ask for a pull request so that your changes can be
merged back.

Install prerequisites
---------------------

Our code is Python 2.6/2.7 code. It definitely won't run on Python 3.x, and most 
likely not on earlier versions of Python.
If you want to run the API yourself or if you want to run pre-packed clients 
that communicate with an API, then a couple of prerequisites are needed.
However, installing them is easy (if you have pip installed):

.. sourcecode:: bash

    $ sudo pip install -r requirements.txt

If you don't have pip yet, install it using :code:`easy_install pip`. Windows
users may want to read here:
http://stackoverflow.com/questions/4750806/how-to-install-pip-on-windows

You may need to install the python-dev package. And it sometimes happens 
(for instance on Windows), that you need to install Numpy/Scipy manually first.

Done?
-----

If you only want to run a client, you have all you need. Clients are pieces of
code that talk to the Living Labs API. We recognize two types of clients:
participants and sites. Example clients are in the repository in the
:code:`ll/clients` directory. See `Running Clients`_.

In case you want to run your own version of the API (for testing purposes),
you'll have to continue.

You don't necessarily have to do that, our challenge API is running here:
http://living-labs.net:5000/api/


Setup MongoDB
-------------

If you don't already have MongoDB, you may follow a guide for your operating
system at this page: http://docs.mongodb.org/manual/installation/.
You'll need MongoDB version >=2.6.

Then you can choose to run with or without authentication (without is easier,
but unsecure).

Authenticated
^^^^^^^^^^^^^

To run MongoDB with authentication enabled you can run it with the provided
configuration file config/mongodb.conf (you may have to edit the data path).

First start a MongoDB daemon as follows:

.. sourcecode:: bash

    $ mongod --config ll-challenge/config/mongodb.conf

Then, create two users (replace ADMINSECRET and USERSECRET with actual password
and remember those):

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

Create a local copy of the config/livinglabs.ini file and edit it to add the
USERSECRET password to the mongodb section. Put this password in quotes. 
Also edit the database name if you wish.

.. sourcecode:: bash

    $ cp config/livinglabs.ini config/livinglabs.local.ini
    $ vim config/livinglabs.local.ini
    
Remember to never add the file containing your password to a code repository,
that would be a severe security threat.

Non-Authenticated
^^^^^^^^^^^^^^^^^

For developing purposes, this is fine. Otherwise, make sure to use
authentication. Start a MongoDB deamon as follows:

.. sourcecode:: bash

    $ mongod

Create a local copy of the config/db.ini file. Edit the database name if you
wish.

.. sourcecode:: bash

    $ cp config/livinglabs.ini config/livinglabs.local.ini



Run the API
-----------

If you didn't do so yet, make a copy of the configuration and at least fill out
the mongodb section:

.. sourcecode:: bash

    $ cp config/livinglabs.ini config/livinglabs.local.ini


To start the API, run the following command: 

.. sourcecode:: bash
    
    $ ./bin/api -c config/livinglabs.local.ini

If you want to automatically have the API reload when you change the code (which
is incredibly handy when developing) then run this with :code:`--debug` the
debug flag: 

.. sourcecode:: bash

    $ ./bin/api -c config/livinglabs.local.ini --debug

In general, use :code:`--help` or :code:`-h` for more information.


Fill the Database
-----------------

If there is a `Dashboard`_ running, probably you should just create some users
through the `Dashboard`_. Otherwise, continue here.

To create site or admin users, you will still need the bin/admin tool.

To create an example participant and a site (for development/testing purposes),
you can run the following script: 

.. sourcecode:: bash 

    $ ./bin/admin user -c config/livinglabs.local.ini config/example-data/site.ini --password CHOOSEAPASSWORD
    $ ./bin/admin user -c config/livinglabs.local.ini config/example-data/user.1.ini --password CHOOSEAPASSWORD

The passwords are used for the `Dasboard`.

In return, you will see two API keys, one for a site and one for a participant.
Record the keys as SITEKEY and PARTICIPANTKEY, you'll need them for the clients.

Instead, you can also provide your own details, see the help on how to do that:

.. sourcecode:: bash 

   $ ./bin/admin user -h


Reset the Database
------------------

In case you need a reset, you can simply run this. But, BE CAREFUL, it can not
be undone (or, probably it can, the MongoDB is journalled, but it will not be
trivial).

.. sourcecode:: bash 

   $ ./bin/admin db --clear

Don't forget to recreate users (see above).


Running Clients
---------------

Clients are pieces of code that talk to the Living Labs API. We recognize two
types of clients: participants and sites. Sites are search engines that share
queries, documents and clicks. Participants rank documents for queries using
clicks. Clients need API keys. The easiest way of obtaining a key is through
the `Dashboard`_.


Run a Site
^^^^^^^^^^

To run a site client and upload queries and documents, you can do the following:

.. sourcecode:: bash 

   $ ./bin/client-site --key SITEKEY -q -d

This will take TREC queries/runs/document (see :code:`-h` for file locations and
how to change them) as a basis.

Then, to simulate interactions, run the following:

.. sourcecode:: bash 

   $ ./bin/client-site --key SITEKEY -s
   
Again, this will take TREC data (qrels) to simulate clicks using a simple
cascade click model.

Note that you may need to specify the host/port where the API is running (see
:code:`-h` for details on how to do that).

The simple simulator will print the NDCG value of all the rankings it receives
from the API. 

Note that the site client is not at all aware of the participants, the site
client simply talks to the API. So if there are multiple participant clients
present, the API does not know about this and the NDCG will thus reflect the
average performance of all participants. This is by design. For per-participant
statistics, one should use the `Dashboard`_.

If you want to run multiple sites, you should create multiple keys and start
multiple instances that talk to the same API.


Run a Participant
^^^^^^^^^^^^^^^^^

To run a simple participant implementation, you can do this:

.. sourcecode:: bash 

   $ ./bin/client-participant -k PARTICIPANTKEY -s
   
The API key can be obtained through a procedure explained in `Fill the Database`
or through the `Dashboard`_.

This will run a baseline system that simply greedily reranks by the number of
clicks. Note that you may need to specify the host/port where the API is
running (see :code:`-h` for details on how to do that).

If you want to run multiple participants, you should create multiple keys and
start multiple instances that talk to the same API.

Dashboard
=========

A dashboard is already running here: http://living-labs.net:5001/.


Users with admin privileges, have a few more options in the dashboard. Use the
bin/admin tool to create a user with those privileges.

However, if you are running a local version of the API for development, it is a
good idea to also run a dashboard with it.
 
To start the dashboard, fill out the dashboard fields in your local copy of the
config (config/livinglabs.local.ini). In particular, you will need a recaptcha
key (see http://www.google.com/recaptcha), a csrfsecrettoken, and a secretkey
(both are just random strings you should generate).

Then run the following command:

.. sourcecode:: bash

    $ ./bin/dashboard -c config/livinglabs.local.ini

In general, use :code:`--help` or :code:`-h` for more information. By default
the dashboard will run on port 5001.


Building Documentation
======================

Note that you probably don't have to build the documentation. A constantly
updated version is available here: http://doc.living-labs.net/

To build this documentation, run these commands in a shell:

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

Then, add these lines to your ~/.bash_profile:

.. sourcecode:: bash
    
    export LC_ALL=en_US.UTF-8
    export LANG=en_US.UTF-8