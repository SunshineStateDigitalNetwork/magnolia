class DataProvider(object):
    __slots__ = ('__dict__', 'key', 'scenario', 'map', 'data_provider', 'intermediate_provider')

    def __init__(self):
        """
        DataProvider object model.
        __slots__:
            * key: Unique string identifying organization providing the data
            * scenario: magnolia.scenario magnolia used to encapsulate records
            * map: Name of function used to map records from OAI-PMH into MAPv4. Can come from magnolia.maps or be defined elsewhere such as a custom map from the Custom Map Directory defined in magnolia.cfg
            * data_provider: Name of organization providing the data (dpla.dataProvider)
            * intermediate_provider: Name of organization serving as an intermediary data provider (dpla.intermediateProvider) -- optional
        """
        object.__init__(self)
