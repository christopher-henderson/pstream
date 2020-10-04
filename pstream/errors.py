class InfiniteCollectionError(Exception):

    def __init__(self, method):
        super(InfiniteCollectionError, self).__init__('Stream.{} was called on an infinitely repeating iterator. '
                                                      'If you uses Stream.repeat, then you MUST include either a '
                                                      'Stream.take or a Stream.take_while if you wish to '
                                                      'call Stream.{}'.format(method, method))
