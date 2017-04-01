import ctypes

from settings import SETTINGS

"""
Протокол коммуникации клиенских процессов и ядра
"""

class BaseNucleusPacket(ctypes.LittleEndianStructure):
    """ Базовый пакет, необходимый для идентификации типа пакета ядром сиситемы """
    _fields_ = [
        # Магическое число, отличающее пакет от прочего мусора
        ('magic_number', ctypes.c_ushort),
        ('version', ctypes.c_ubyte),
        ('type', ctypes.c_ubyte),
        # зарезервированное поле
        ('null', ctypes.c_uint32, 32),
    ]


class NucleusPacketRequestAuth(ctypes.LittleEndianStructure):
    """ Запрос авторизовать пользователя с таким идентификатором """
    _fields_ = [
        # Магическое число, отличающее пакет от прочего мусора
        ('magic_number', ctypes.c_ushort),
        ('version', ctypes.c_ubyte),
        ('type', ctypes.c_ubyte),
        # зарезервированное поле
        ('null', ctypes.c_uint32, 32),
        # размер данных
        ('length_username', ctypes.c_ushort),
        ('length_password', ctypes.c_ushort),
        # Тело сообщения (Логин и пароль в зашифрованом виде)
        ('username', ctypes.c_ubyte * SETTINGS['PROTOCOLS']['LOGIN_SIZE']),
        ('password', ctypes.c_ubyte * SETTINGS['PROTOCOLS']['PASSWORD_SIZE']),
    ]

class NucleusPacketResponseAuth(ctypes.LittleEndianStructure):
    """ Ответ ядра на попытку авторизовать пользователя """
    _fields_ = [
        # Магическое число, отличающее пакет от прочего мусора
        ('magic_number', ctypes.c_ushort),
        ('version', ctypes.c_ubyte),
        ('type', ctypes.c_ubyte),
        # зарезервированное поле
        ('null', ctypes.c_uint32, 32),
        # оnтвет сиситемы NUC_AUTH_SUCCESS или NUC_AUTH_FAILED
        ('response', ctypes.c_uint32, 32),
        # идентификатор сессии
        ('uuid', ctypes.c_ubyte *  SETTINGS['PROTOCOLS']['UUID_SIZE']),
    ]