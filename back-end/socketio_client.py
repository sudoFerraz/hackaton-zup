from socketIO_client import SocketIO, LoggingNamespace
import logging
logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
logging.basicConfig()

with SocketIO('localhost', 5000, LoggingNamespace) as socketIO:
    socketIO.emit('aaa')
    socketIO.wait(seconds=1)
