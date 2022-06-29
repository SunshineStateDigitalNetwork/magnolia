Command Line Interface
======================

Command-line interface when the module is called with ``python3 -m magnolia``.

Most actions can be explored with the ``--help`` flag.

The two main activities are:

* Harvest - :py:func:`magnolia.cli.harvest`
* Transform - :py:func:`magnolia.cli.transform`

Other command options relate to setting and querying the program environment and running the module self-test.

The path to the magnolia configuration files must either be defined with the ``MAGNOLIA_CONFIG`` environment variable or exist in one of two default locations:

* ``$HOME/.local/share/magnolia``
* the magnolia module directory

See :doc:`configuration` for more details.

.. toctree::
   :maxdepth: 1
   :caption: Explore the CLI

   cli_full
   cli_status
   cli_harvest
   cli_transform
   cli_functions
