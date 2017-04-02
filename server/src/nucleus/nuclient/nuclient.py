import os
import sys
import uuid
import select
import socket
import logging

import netpackets

from settings import SETTINGS

from factory.method import FactoryMethod

from .factory_chanel import actions as actions_chanel
from .factory_chanel import creators as creators_chanel

from .factory_network import actions as actions_network
from .factory_network import creators as creators_network 


class NuClient:
    """
    Реализует в отдельном процессе взаимодействие с клиентом
    """

    # сокет для связи с пользователем
    _tcp_user_socket = None

    # сокет для связи с ядром системы
    _nucleus_file_socket = None

    # Фабричный метод идентификации и обработки пакетов канального уровня
    _chanel_factory_actions = None
    # Фабричный метод идентификации и обработки пакетов сетевого уровня
    _network_factory_actions = None

    def __init__(self, *, tcp_socket, file_socket_name):
        """ Конструктор класса
        :param tcp_socket: tcp-сокет, созданный при установлении связи с клиентом. 
                        Нужен для авторизации и обменом текстовых сообщений
        :param file_socket_name: имя файла-сокета, для связи с ядром
        """

        self._tcp_socket = tcp_socket
        # создаем канал связи с ядром системы
        self._nucleus_file_socket = self._create_nucleus_socket(file_socket_name)

        # инициализируем обработчики пакетов канального уровня
        self._init_chanel_actions()
        # инициализирую обработчики пакетов сетевого уровня
        self._init_network_actions()


    def _create_nucleus_socket(self, file_socket_name):
        """ Создает сокет для связи с ядром системы """
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(file_socket_name)
        return sock


    def _init_chanel_actions(self):
        """ Инициализирует обработчики сообщения канального уровня через фабричный метод """
        self._chanel_factory_actions = FactoryMethod(base_class=netpackets.chanel.ChanelPacket)        
        packet_type = SETTINGS['PROTOCOLS']['CHANEL']['PROTOCOL']

        # обработчик пакета зашифрованого открытым ключем
        self._chanel_factory_actions.addAction(packet_type=packet_type['TYPE_SECURE_PUBLIC_KEY'], 
                concrete_factory=creators_chanel.ChanelPacketCreator(), 
                cmd=actions_chanel.ActionSecurePublicKey(related_object=self))
        # обработчик пакета зашифрованого симметричным ключем
        self._chanel_factory_actions.addAction(packet_type=packet_type['TYPE_SECURE_SIMMETRIC_KEY'], 
                concrete_factory=creators_chanel.ChanelPacketCreator(), 
                cmd=actions_chanel.ActionSecureSimmetricKey(related_object=self))
        # обработчик не зашифрованого пакета
        self._chanel_factory_actions.addAction(packet_type=packet_type['TYPE_NOT_SECURE'], 
                concrete_factory=creators_chanel.ChanelPacketCreator(), 
                cmd=actions_chanel.ActionNotSecure(related_object=self))


    def _init_network_actions(self):
        """ Инициализация обработчиков пакетов сетевого уровня через фабричный метод """
        self._network_factory_actions = FactoryMethod(base_class=netpackets.network.NetworkMessage)
        packet_type = SETTINGS['PROTOCOLS']['NETWORK']['PROTOCOL']

        # пакет с пользовательской информацией (текст, картинка, документ и прочее)
        self._network_factory_actions.addAction(packet_type=packet_type['TYPE_PACKET_ROUTE'], 
                concrete_factory=creators_network.NetworkPacketCreator(), 
                cmd=actions_network.ActionPacketRoute(related_object=self))
        # пакет авторизации
        self._network_factory_actions.addAction(packet_type=packet_type['TYPE_AUTHORIZATION'], 
                concrete_factory=creators_network.NetworkPacketCreator(), 
                cmd=actions_network.ActionPacketAuth(related_object=self))
        # пакет проверки качества соединения
        self._network_factory_actions.addAction(packet_type=packet_type['TYPE_QOS'], 
                concrete_factory=creators_network.NetworkPacketCreator(), 
                cmd=actions_network.ActionPacketQOS(related_object=self))


    def chanel_identity(self, *, data):
        """ Запускает фабрику идентификации канального пакета 
        :param data: данные принятые по сети
        """
        self._chanel_factory_actions.response(data)


    def network_identity(self, *, data):
        """ Запускает фабрику идентификации сетевого пакета
        :param data: данные для построения пакета сетевого уровня
        """
        self._network_factory_actions.response(data)


    def run(self):
        """ Запуск цикла обработки сообщений """
        packet_size = SETTINGS['PROTOCOLS']['PACKET_SIZE']

        while True:
            # Формирую список дескрипторов, для опроса данных с них
            rfds = [self._tcp_socket, self._nucleus_file_socket]
            

            # Жду прихода данных на один из дескипторов
            fd_reads, _, e = select.select(rfds, [], [])
            for fd in fd_reads:
                # данные от пользователя по tcp-сокету
                data = fd.recv(packet_size)
                
                if data:
                    if fd == self._tcp_socket:
                        self.chanel_identity(data=data)
                    elif fd == self._nucleus_file_socket:
                        pass
                else:
                    self._tcp_socket.close()
                    self._nucleus_file_socket.close()
                    sys.exit(0)
        
        sys.exit(0)