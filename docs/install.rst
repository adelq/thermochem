Installing thermochem
=====================

The first step to use the thermochem library in Python is to install it onto
your computer properly.

Pip
---

Installing the latest stable version (or a specific version) of thermochem is
easiest using the ``pip`` tool. Simply run this command in your terminal::

    $ pip install thermochem

If you do not have pip installed, head over to the `Python installation guide
<http://docs.python-guide.org/en/latest/starting/installation/>`_, which
contains instructions on installing pip.

Source
------

Thermochem is developed on `GitHub <https://github.com/adelq/thermochem>`_. To
get the source code, you should `install git
<https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`_ if you haven't
already, then run the following command in your terminal::

    $ git clone https://github.com/adelq/thermochem.git

If you are not interested in developing and installing git is difficult, you can
download the tarball::

    $ curl -OL https://github.com/adelq/thermochem/tarball/master

Once you have a copy of the source, you can install it simply using the included
``setup.py``::

    $ cd thermochem
    $ python setup.py install
