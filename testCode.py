class RandomDNASequenceMaker(object):

    def __init__(self, length):
        self.length = length
        self.bases = list("ATGC")

    def makeSequence(self, throwAway = 0):
        import random
        sequence = []
        for i in range(self.length):
            sequence.append(random.choice(self.bases))
        return "".join(sequence)

if __name__ == "__main__":
    import datetime
    from easyMultiprocessing import easyMultiprocessing
    seqGen = RandomDNASequenceMaker(100)
    numberOfSequences = list(range(1000000))
    start = datetime.datetime.now()
    sequenceCollector = []
    for i in numberOfSequences:
        sequenceCollector.append(seqGen.makeSequence(i))
    end = datetime.datetime.now()
    print("Serial process completed in %s" %(end - start))
    start = datetime.datetime.now()
    multiResult = easyMultiprocessing.parallelProcessRunner(seqGen.makeSequence, numberOfSequences)
    end = datetime.datetime.now()
    print("Parallel process completed in %s" %(end - start))
