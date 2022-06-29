magnolia.maps
=============

Maps define how data exposed through ``magnolia.Scenarios`` are manipulated to build ``magnolia.SourceResource`` objects

``magnolia.cli.transform`` reads the configuration file ``magnolia_scenarios.cfg``.to determine which map to apply for which source. Configuration options are covered in :ref:`Configuring magnolia <anchor02>`

.. note:: You'll probably want to write custom maps as detailed in :ref:`Writing custom maps <anchor01>`

.. automodule:: magnolia.maps

   .. rubric:: Functions

   .. autosummary::
   
      dc_standard_map
      qdc_standard_map
      mods_standard_map

