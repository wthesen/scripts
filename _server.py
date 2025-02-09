import socket
import logging

logger = logging.getLogger(__name__)

def start_server(handlePortFunc, handleMessageFunc):
    with socket.socket() as server_socket:

        # bind host address and port together, 0 to find a available port to use
        server_socket.bind((socket.gethostname(), 0))

        port = server_socket.getsockname()[1]
        logger.info("Listening at port: {} ...".format(port))
        handlePortFunc(port)

        logger.info('Python script connected')
        logger.info('Ready to receive command')
        server_socket.listen(2)
        while True:
            conn, _ = server_socket.accept()  # accept new connection
            with conn:
                data = conn.recv(1024).decode()
                if not data:
                    logger.info("No data received")
                    continue

                if handleMessageFunc(data):
                    continue

                elif data == "shutdown":
                    logger.info("Shutting down ...")
                    break

                else:
                    logger.info("Message '{}' can't be handled".format(data))