===================
Transformation maps
===================

Default maps bundled into magnolia.

Maps define how data exposed through ``magnolia.Scenarios`` are manipulated to build ``magnolia.SourceResource`` objects

``magnolia.cli.transform`` read the configuration file ``magnolia_scenarios.cfg``.to determine which map to apply for which source. Configuration options are covered in :ref:`Configuring magnolia <anchor02>`

.. note:: You'll probably want to write custom maps as detailed in :ref:`Writing custom maps <anchor01>`

.. autofunction:: magnolia.maps.dc_standard_map

.. autofunction:: magnolia.maps.qdc_standard_map

.. autofunction:: magnolia.maps.mods_standard_map
