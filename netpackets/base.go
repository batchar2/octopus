package netpackets

import (
	"bytes"
	"encoding/binary"
)

type PacketHeader struct {
	// Магическое число, отличающее пакет от прочего мусора
	magicNumber uint16
	// Весрия протокола
	version uint8
	// Тип принимаемого пакета
	packetType uint8
}

func (header *PacketHeader) SetMagicNumber(magicNumber uint16) {
	header.magicNumber = magicNumber
}

func (header *PacketHeader) GetMagicNumber() uint16 {
	return header.magicNumber
}

func (header *PacketHeader) SetProtocolVersion(version uint8) {
	header.version = version
}

func (header *PacketHeader) GetProtocolVersion() uint8 {
	return header.version
}

func (header *PacketHeader) SetPacketType(packetType uint8) {
	header.packetType = packetType
}

func (header *PacketHeader) GetPacketType() uint8 {
	return header.packetType
}

// преобразует массив данных в представление пакета
func (header *PacketHeader) DataCopyPacket(data *bytes.Buffer) {

	buf := data.Bytes()

	slMagicNumber := []byte{buf[0], buf[1]}
	//slVersion := []byte{buf[2]}
	//slPackeType := []byte{buf[3]}

	header.magicNumber = binary.BigEndian.Uint16(slMagicNumber)
	//header.version = binary.BigEndian.Int8(slVersion)
	//header.packetType = binary.BigEndian.Uint8(slPackeType)
}
