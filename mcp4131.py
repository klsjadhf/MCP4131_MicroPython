# MicroPython library for MCP4131 digital potentiometer from Microchip（7 bit)
# Reading requires proper values of limiting and pullup resistors

import time
from micropython import const
from machine import Pin, SPI

MODE_00 = const(0)
MODE_11 = const(1)

ADDR_WPR_0 =  const(0x00)
ADDR_WPR_1 =  const(0x01)
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

def limit(num, min, max):
    if num < min:
        return min
    elif num > max:
        return max
    else:
        return num

class MCP4131:
    used_cs_pins = []

    def __init__(self, bus, cs, res=RES_10K):
        self.spi_bus = bus
        self.baud = 10000  # 250kHz
        self.set_mode(MODE_00)
        self.crc = 0

        self.wiper_pos = 0.5  # default 50% on power on (0 is at position B, 1 at pos A)
        self.max_resistance = res 

        self.cs_pin = Pin(cs)
        if self.cs_pin.name() not in self.used_cs_pins:
            self.cs_pin.init(mode=Pin.OUT)
            self.cs_pin(1)  # active low
            self.used_cs_pins.append(self.cs_pin.name())
        else:
            raise Exception("Pin {} is already in use!".format(cs))

        # Pin('PA5', Pin.OUT)
        # Pin('PA6', Pin.IN)
        # Pin('PA7', Pin.OUT)

        self.init_bus(bus)

    def init_bus(self, bus=None):
        if bus:
            self.spi_bus = bus

        if self.spi_bus:
            # print("using spi bus", self.spi_bus)
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


    # resistance btwn wiper and b
    def set_res(self, resistance):
        # self.r_step = self.resistance / 128  # resistance of each resistor in ladder
        # self.r_wiper = int( self.wiper_pos * 128) + 75  #wiper resistance is 75 ohm
        self.set_pos(resistance/self.max_resistance)


    # set wiper position away from terminal B (0 at B, 1 at A)
    def set_pos(self, pos):
        data = limit(int(128 * pos), 0, 128)
        self.write(ADDR_WPR_0, data)


    def write(self, reg, data):
        self.cs_pin(0)

        msb = (reg<<4) | (CMD_WRITE<<2)
        lsb = data

        out = bytearray([msb, lsb])
        print("sending", out)
        self.spi.write(out)

        self.cs_pin(1)

    # int to bin str (encoded)
    def i2bStr(self, n):
        buf = "{:b}".format(n)
        buf.encode()
        return buf

    # string to integer
    def str2bin(self, s):
        s.decode()
        v = int(s, 2)
        return v
    
    # def get_status(self):
        
    #     self.cs_pin.value(0)

    #     # time.sleep(0.01)
    #     # buf = self.spi.recv(5)
    #     # print(buf)
    #     self.spi.send(0b00001100)
    #     buf = self.spi.recv(1)
    #     # self.spi.send(bytearray([0, 0]))
    #     # buf = self.spi.recv(5)

    #     # out = bytearray([0,0])  # MSB LSB
    #     # buf = self.spi.send_recv(send=out)
    #     # print(self.spi.read(3))
    #     # buf = self.spi.recv(5)
    #     # time.sleep(1)
        
    #     self.cs_pin.value(1)

    #     return buf
        
        

# spi 1 for stm32f407
# pa4 spi_nss brown (slave select not needed in master mode)
# pa5 spi_sck yellow
# pa6 spi_miso orange
# pa7 spi_mosi green

# pin max current is 25 mA (min 132 ohms)

spi_bus = 1
cs_pin = 'PA4'

def testing():
    print("testing")
    pot1 = MCP4131(spi_bus, cs_pin)
    print(pot1.i2bStr(5))
    print(pot1.str2bin(b"101"))
    pot1.deinit()

# dosent work because of multiplexed data lines
def read_status_test():
    print("read_status_test")
    pot1 = MCP4131(spi_bus, cs_pin)
    print(pot1.get_status())
    pot1.deinit()

def write_reg_test():
    print("write_reg_test")
    pot1 = MCP4131(spi_bus, cs_pin)
    pot1.write(ADDR_WPR_0, 0)  # pos b
    time.sleep(3)
    pot1.write(ADDR_WPR_0, 128)  # pos a
    time.sleep(3)
    pot1.deinit()

def write_position_test():
    print("write_position_test")
    pot1 = MCP4131(spi_bus, cs_pin)
    pot1.set_pos(0) # at terminal b
    time.sleep(3)
    pot1.set_pos(1) # at terminal a
    time.sleep(3)
    pot1.set_pos(0.5) # halfway
    time.sleep(3)
    pot1.deinit()

# resistance from wiper to term b
def write_reistance_test():
    print("write_reistance_test")
    pot1 = MCP4131(spi_bus, cs_pin)
    pot1.set_res(0)
    time.sleep(3)
    pot1.set_res(7000)
    time.sleep(3)
    pot1.set_res(10000)
    time.sleep(3)
    pot1.deinit()

def used_pins_test():
    print("used_pins_test")
    pot1 = MCP4131(spi_bus, cs_pin)
    print("pot1")
    try:
        pot2 = MCP4131(spi_bus, cs_pin)
    except Exception as e:
        print(e)
    print("pot2")
    pot1.deinit()

def test_limit():
    print("test_limit")
    print(limit(100, 0, 128))  # expect 100
    print(limit(0, 0, 128))  # expect 0
    print(limit(128, 0, 128))  # expect 128
    print(limit(-1, 0, 128))  # expect 0
    print(limit(129, 0, 128))  # expect 128

# testing()
# read_status_test()
write_reg_test()
write_position_test()
write_reistance_test()
# used_pins_test()
# test_limit()

# a4 = Pin("A4")
# print("A4", a4.af_list(), a4.af())

# a5 = Pin("A5")
# print("A5", a5.af_list(), a5.af())

# a6 = Pin("A6")
# print("A6", a6.af_list(), a6.af())

# a7 = Pin("A7")
# print("A7", a7.af_list(), a7.af())

