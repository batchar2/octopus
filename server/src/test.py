#!/usr/bin/env python3

import ctypes
import socket


from io import BytesIO

from nucleus.packets import chanell_level as ch
from nucleus.packets import default_options as op

class Client:

	_sock = None
	def __init__(self):
		self._sock = socket.socket()
		self._sock.connect(('localhost', 9988))
		
	def __call__(self):
		self.send_public_key()

	def send_public_key(self):
		# передача
		packet = ch.ChanelLevelPacket()
		packet.magic_number = op.MAGIC_NUMBER
		packet.type = op.CHANEL_PACKET_TYPE_PUBLIC_KEY_СLIENT_SERVER_EXCHANGE
		
		print("Data size={0}".format( ctypes.sizeof(packet)))
		self._sock.send(packet)

		# Ответ
		data = self._sock.recv(op.CHANEL_PACKET_BODY_SIZE)
		packet = ch.ChanelLevelPacketKeyAuth.from_buffer_copy(data)
		print("magic_number={0}".format(packet.magic_number))
		print("length={0}".format(packet.length))
		print("key={0}".format(packet.key))

		self._sock.close()

if __name__ == '__main__':
	client = Client()
	client()