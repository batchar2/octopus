// Построитель пакета для авторизации
package auth

import (
	"octopus/conf"
	"octopus/netpackets"
	"octopus/response/pipeline"
)

type NetworkAuthPacketMaker struct {
	pipeline.ResponseInterface

	packet netpackets.NetworkPacketHeader
}

// собрать пакет из данных
func (self *NetworkAuthPacketMaker) MakePacket(data []byte) bool {
	self.packet = netpackets.NetworkPacketHeader{}

	self.packet.SetBody(data)
	self.packet.SetMagicNumber(conf.MAGIC_NUMBER)
	self.packet.SetPacketType(conf.NETWORK_PACKET_TYPE_AUTH)

	return false
}

// Получить бинарное представление пакета
func (self *NetworkAuthPacketMaker) GetBinaryPacketData() []byte {
	return self.packet.Binary()
}