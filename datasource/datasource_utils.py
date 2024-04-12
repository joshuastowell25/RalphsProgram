from datasource.datasources.OfflineFlatFileDataSource import OfflineFlatFileDataSource

DATA_SOURCES = [OfflineFlatFileDataSource()] #TODO: add others later

def machineIsOnline():
    return False #TODO

def detectAvailableDataSources():
    return list(filter(lambda x: x.isAvailable(), DATA_SOURCES))

def getDataSource():
    data_source_list = detectAvailableDataSources()
    selection = input(f"What data source do you want to use? Options are: {list(map(lambda x: str(x), data_source_list))}\n")
    for source in DATA_SOURCES:
        if selection == source.dataSourceType:
            return source
    return None