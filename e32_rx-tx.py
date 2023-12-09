### Huge thanks to the guys from this thread
### https://github.com/sandeepmistry/arduino-LoRa/issues/203
### For actually reversing the procotol of Ebyte E32

import radio
import time

modem = radio.get_modem()


def getKey(channelNo):
    lsbTable = [0x0A, 0x09, 0x08, 0x0F, 0x0E, 0x0D, 0x0C,
                0x03, 0x02, 0x01, 0x00, 0x07, 0x06, 0x05, 0x04, 0x0B]
    return ((channelNo + 0x99) & 0xF0) | lsbTable[channelNo & 0x0F]


def decode_msg(data):
    
    decoded = ""
    eKey = getKey(data[1]) 
    
    print(f"Calculated key: {eKey}")
    
    hex_data = [hex(b) for b in data]
    print(f"Received data: {hex_data}")
    
    for b in range(4, len(data)-1):
        decoded += chr(data[b] ^ eKey)
    
    return decoded


def calcCheckSum(buf):
    sum_val = 0
    for i in range(len(buf)):
        sum_val += buf[i]
    sum_val = 0x100 - (sum_val & 0xFF)
    return sum_val & 0xFF


def prepare_packet(msg):
    
    enc_msg = bytearray(msg.encode('utf-8'))
    packet_buf = bytearray()

    packet_buf.append(len(enc_msg))   # append data size
    
    # Index of the encryption key. Drove me crazy until I figured this out.
    # Starts from D0 and is incremented by 0x08
    # for every new added byte in the data
    packet_buf.append(0xD0 + 0x08 * (len(msg)-1) )
    
    packet_buf.append(0x00)   # dev address high bit
    packet_buf.append(0x00)   # dev address low bit

    # Encode data with the key
    for ch in enc_msg:
        packet_buf.append(ch ^ getKey(packet_buf[1])) # encrypt each char with channel No

    packet_buf.append(calcCheckSum(packet_buf))
    
    print(f"Raw packet: {packet_buf}")
    
    return packet_buf


def receive():
    while True:
        rx = modem.recv()
        if rx:
            print(rx)
            print(decode_msg(rx))

def send(msg):
    a = prepare_packet(msg)
    print(f"Data sent : {decode_msg(a)}")
    modem.send(a)


send("Hey, it works!")
#receive()


        
            