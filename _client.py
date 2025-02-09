import socket
import sys
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# print(sys.argv)
portNumber = int(sys.argv[1])
message = str(sys.argv[2])

def send_message(portNumber, message):
    host = socket.gethostname()  # as both code is running on same pc
    port = portNumber  # socket server port number
    with socket.socket() as client_socket: # instantiate
        client_socket.connect((host, port))  # connect to the server
        client_socket.send(message.encode())  # send message

if __name__ == '__main__':
    logger.info("Sending message '{}' ...".format(message))
    send_message(portNumber, message)
    logger.info("Message sent")
