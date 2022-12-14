import socket

import numpy as np

from .commn_server import CommnServer
from .commn_client import CommnClient
import cv2


class Communicator:
    def __init__(self, host=socket.gethostname(), py_port=10101, unity_port=20202, env='unity'):
        if env == 'unity':
            self.host = host
            self.py_port = py_port
            self.unity_port = unity_port
            self.server = CommnServer(self.host, self.py_port)

    def close_msg(self):
        client = CommnClient(self.host, self.unity_port)
        client.close_msg()

    def send_msg(self, msg_str):
        client = CommnClient(self.host, self.unity_port)
        client.send_msg(msg_str)

    def send_image(self, img_bytes):
        client = CommnClient(self.host, self.unity_port)
        bytes_array = bytes(cv2.imencode('.jpg', img_bytes)[1].tobytes())
        client.send_image(bytes_array)

    def imread_screen(self):
        client = CommnClient(self.host, self.unity_port)
        img = client.imread_screen()
        img_np = cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_COLOR)
        return img_np

    def imread_file(self, file_path):
        client = CommnClient(self.host, self.unity_port)
        img = client.imread_file(file_path)
        img_np = cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_COLOR)
        return img_np

    def start_server(self):
        self.server.server_closed = False
        self.server.start_server()

    def close_server(self):
        self.server.close()

    def get_server_pipeline(self):
        if not self.server.server_closed:
            return self.server.get_data_pipeline()

    def get_server_data(self):
        if not self.server.server_closed:
            return self.server.get_last_req()
