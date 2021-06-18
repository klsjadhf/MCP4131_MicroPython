# MicroPython library for MCP4131 digital potentiometer from Microchip（7 bit SPI)

import time
from micropython import const
from machine import Pin, SPI

MODE_00 = const(0)
MODE_11 = const(1)

ADDR_WPR_0 =  const(0x00)
# ADDR_WPR_1 =  const(0x01)
ADDR_TCON =   const(0x04)
ADDR_STATUS = const(0x05)

CMD_WRITE = const(0b00)
CMD_INCR =  const(0b01)
CMD_DECR =  const(0b10)
CMD_READ =  const(0b11)

RES_5K =   const(5000)
RES_10K =  const(10000)
RES_50K =  const(50000)
RES_100K = const(100000)

TERM_WPR = const(1)
TERM_A =   const(2)
TERM_B =   const(0)
TERM_SHUTDOWN =  const(3)

CONNECT =    const(1)
DISCONNECT = const(0)


def limit(num, min, max):
    if num < min:
        return min
    elif num > max:
        return max
    else:
        return num


def extract_bit(num, bit):
    return (num >> bit) & 1


class MCP4131:
    used_cs_pins = []

    def __init__(self, cs, bus=1, res=RES_10K, mode=MODE_11, baud=250000):
        self.spi_bus = bus
        self.baud = baud  # @250kHz actual baudrate=328125
        self.set_mode(mode)

        self.max_resistance = res 
        self.cmderr = 1  # 0 is error

        self.cs_pin = Pin(cs)
        if self.cs_pin.name() not in self.used_cs_pins:
            self.cs_pin.init(mode=Pin.OUT, value=1)
            self.used_cs_pins.append(self.cs_pin.name())
        else:
            raise Exception("Pin {} is already in use!".format(cs))

        self.spi = SPI(self.spi_bus, baudrate=self.baud, polarity=self.pol, phase=self.phase, firstbit=SPI.MSB)
        # print(self.spi)  # show real baud rate


    def deinit(self):
        self.spi.deinit()
        self.cs_pin.init(mode=Pin.IN)
        self.used_cs_pins.remove(self.cs_pin.name())


    def set_mode(self, mode):
        self.mode = mode

        if self.mode == MODE_00:
            self.pol = 0
            self.phase = 0
        elif self.mode == MODE_11:
            self.pol = 1
            self.phase = 1


    # resistance between wiper and b
    def res(self, resistance=-1):
        if resistance != -1:
            self.pos( resistance/self.max_resistance )
        return (self.pos() * self.max_resistance)

    # set wiper position away from terminal B (0 at B, 1 at A)
    def pos(self, pos=-1):
        if pos != -1:
            data = limit(int(127 * pos), 0, 127)
            self.write(ADDR_WPR_0, data)
        return self.read(ADDR_WPR_0) / 127


    def write(self, reg, data):
        self.cs_pin(0)
        time.sleep_us(60)

        cmd = (reg<<4) | (CMD_WRITE<<2) 
        self.send(cmd, data)

        self.cs_pin(1)


    # returns true for vaild cmd, false for error
    def send(self, cmd, data=None):
        # cmd =  cmd | (0b11)  # open drain multiplexed sdo  cause error with inc and dec cmd or cmderr bit

        # 16 bit commands
        if data != None:
            buf = bytearray(2)
            out = bytearray([cmd, data])
        # 8 bit commands
        else:  
            buf = bytearray(1)
            out = bytearray([cmd])

        # print("sending 0x{:X} (0b{:b})".format(int.from_bytes(out, "big"), int.from_bytes(out, "big")))

        self.spi.write_readinto(out, buf)

        # bit 9 is CMDERR bit. High is valid cmd, low is invalid cmd
        # not working
        if data != None:
            self.cmderr = extract_bit( int.from_bytes(buf, "big"), 9)
        else:
            self.cmderr = extract_bit( int.from_bytes(buf, "big"), 1)

        # print("sent 0x{:X} (0b{:b}), cmderr:{}".format(int.from_bytes(buf, "big"), int.from_bytes(buf, "big"), self.cmderr))

        return self.cmderr
    

    def read(self, reg):
        self.cs_pin(0)
        time.sleep_us(60)

        cmd = (reg<<4) | (CMD_READ<<2)
        self.send(cmd)

        # open drain multiplexed sdo set mosi to high when reading
        buf = self.spi.read(1, 0xFF)

        # print("received 0x{:X} (0b{:b})".format(int.from_bytes(buf, "big"), int.from_bytes(buf, "big")))

        self.cs_pin(1)

        return int.from_bytes(buf, "big")


    def inc(self, wiper=ADDR_WPR_0):
        self.cs_pin(0)
        time.sleep_us(60)

        cmd = (wiper<<4) | (CMD_INCR<<2)
        self.send(cmd)

        self.cs_pin(1)

    
    def dec(self, wiper=ADDR_WPR_0):
        self.cs_pin(0)
        time.sleep_us(60)

        cmd = (wiper<<4) | (CMD_DECR<<2)
        self.send(cmd)

        self.cs_pin(1)
        

    def tcon(self, data=None):
        if data != None:
            self.write(ADDR_TCON, data)
        return self.read(ADDR_TCON)
    
    # IC only has one pot, resistor 1 not supported
    def term_con(self, term, con=-1):
        tmp = self.tcon()
        if con == 1:
            tmp = tmp | (1<<term)
            self.tcon(tmp)
        elif con == 0:
            tmp = tmp & ~(1<<term)
            self.tcon(tmp)
        return extract_bit(self.tcon(), term)


    # IC doesn't have shutdown pin, control shutdown through TCON register
    # 1 is shutdown, 0 is not in shutdown (opp of value in TCON register)
    def shutdown(self, s=-1):
        if s == -1:
            pass
        elif s:
            s = 0
        else:
            s = 1
        return not self.term_con(TERM_SHUTDOWN, s)
        
