class InfiniteCollectionError(Exception):

    def __init__(self):
        super(InfiniteCollectionError, self).__init__('Stream.collect was called on an infinitely repeating iterator. '
                                                      'If you uses Stream.repeat, then you MUST include either a '
                                                      'Stream.take or a Stream.take_while if you wish to '
                                                      'call Stream.collect')
