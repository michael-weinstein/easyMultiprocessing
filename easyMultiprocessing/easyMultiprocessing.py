def calculateAvailableCores():
    import multiprocessing
    return max([multiprocessing.cpu_count() - 1, 1])


def calculateChunkSize(length, workers:int):
    return -1 * ((-1*length) // workers)


def parallelProcessRunner(processor, itemsToProcess, coreLimit:int = 0, filterFunction = False, totalSizeEstimate = None):
    import multiprocessing
    import inspect
    import collections
    assert callable(processor), "Processor must be a callable function/method"
    assert len(inspect.signature(processor).parameters) == 1, "Processor function must take one argument"
    assert isinstance(itemsToProcess, collections.Iterable), "Items to process must be an iterable of some kind"
    coreLimit = max([0, coreLimit])
    if not coreLimit:
        coreLimit = calculateAvailableCores()
    workers = multiprocessing.Pool(coreLimit)
    try:
        length = len(itemsToProcess)
        chunkSize = calculateChunkSize(length, coreLimit)
        mapper = workers.map
    except TypeError:
        if not totalSizeEstimate:
            totalSizeEstimate = 50000
            print("Using default total size estimate of 50,000 because none was given.")
        chunkSize = calculateChunkSize(totalSizeEstimate, coreLimit)
        mapper = workers.imap
    if not filterFunction:
        return mapper(processor, itemsToProcess, chunkSize)
    else:
        results = mapper(processor, itemsToProcess, chunkSize)
        return [result for result in results if result]