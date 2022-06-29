Transformation maps
===================

Maps define how data exposed through :doc:`api_scenarios` are manipulated to build :doc:`source_resource` objects.

``magnolia.cli.transform`` reads the configuration file ``magnolia_scenarios.cfg`` to determine which map to apply for which source. Configuration options are covered in :ref:`Configuring magnolia <anchor02>`.

.. note:: You'll probably want to write custom maps as detailed in :ref:`Writing custom maps <anchor01>`

Standard maps
-------------

Default maps bundled in magnolia.

.. autofunction:: magnolia.maps.dc_standard_map
.. code-include :: :func:`magnolia.maps.dc_standard_map`

.. autofunction:: magnolia.maps.qdc_standard_map
.. code-include :: :func:`magnolia.maps.qdc_standard_map`

.. autofunction:: magnolia.maps.mods_standard_map
.. code-include :: :func:`magnolia.maps.mods_standard_map`
