package netpackets

import (
    "mview/conf"
)

type NetworkPacketHeader struct {
    Header PacketHeader
    // Тело сообщения (может быть зашифровано)
    body [conf.NETWORK_BODY_SZIE]byte
}


func (header *NetworkPacketHeader) SetBody(body [conf.NETWORK_BODY_SZIE] byte) {
    header.body = body
}

func (header *NetworkPacketHeader) GetBody() [conf.NETWORK_BODY_SZIE] byte {
    return header.body
}