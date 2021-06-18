# ignore everything here. not used anymore

import mcp4131
import time
# spi 1 for stm32f407
# pa4 spi_nss brown (slave select not needed in master mode)
# pa5 spi_sck yellow
# pa6 spi_miso orange
# pa7 spi_mosi green

# pin max current is 25 mA (min 132 ohms)

spi_bus = 1
cs_pin = 'PA4'

# def testing():
#     print("\n\ntesting")
#     pot1 = MCP4131(spi_bus, cs_pin)
#     print(pot1.i2bStr(5))
#     print(pot1.str2bin(b"101"))
#     pot1.deinit()

# def read_status_test():
#     print("\n\nread_status_test")
#     pot1 = MCP4131(spi_bus, cs_pin)
#     # print(pot1.get_status())
#     print(hex(pot1.read(ADDR_STATUS)))
#     pot1.deinit()

# def write_reg_test():
#     print("\n\nwrite_reg_test")
#     pot1 = MCP4131(spi_bus, cs_pin)
#     pot1.write(ADDR_WPR_0, 0)  # pos b
#     time.sleep(3)
#     pot1.write(ADDR_WPR_0, 128)  # pos a
#     time.sleep(3)
#     pot1.deinit()

# def write_position_test():
#     print("\n\nwrite_position_test")
#     pot1 = MCP4131(spi_bus, cs_pin)
#     pot1.set_pos(0) # at terminal b
#     time.sleep(3)
#     pot1.set_pos(1) # at terminal a
#     time.sleep(3)
#     pot1.set_pos(0.5) # halfway
#     time.sleep(3)
#     pot1.deinit()

# # resistance from wiper to term b
# def write_reistance_test():
#     print("\n\nwrite_reistance_test")
#     pot1 = MCP4131(spi_bus, cs_pin)
#     pot1.set_res(0)
#     time.sleep(3)
#     pot1.set_res(7000)
#     time.sleep(3)
#     pot1.set_res(10000)
#     time.sleep(3)
#     pot1.deinit()

# def used_pins_test():
#     print("\n\nused_pins_test")
#     pot1 = MCP4131(spi_bus, cs_pin)
#     print("pot1")
#     try:
#         pot2 = MCP4131(spi_bus, cs_pin)
#     except Exception as e:
#         print(e)
#     print("pot2")
#     pot1.deinit()

# def test_limit():
#     print("\n\ntest_limit")
#     print(limit(100, 0, 128))  # expect 100
#     print(limit(0, 0, 128))  # expect 0
#     print(limit(128, 0, 128))  # expect 128
#     print(limit(-1, 0, 128))  # expect 0
#     print(limit(129, 0, 128))  # expect 128

# def read_write_test():
#     print("\n\n read_write_test")
#     pot1 = MCP4131(spi_bus, cs_pin)

#     pot1.write(ADDR_WPR_0, 11)
#     print(pot1.read(ADDR_WPR_0))

#     pot1.deinit()

# def extract_bit_test():
#     print("\n\n extract_bit_test")

#     print(extract_bit(0b00000001, 0) == 1)
#     print(extract_bit(0b00000001, 1) == 0)
#     print(extract_bit(0b00000010, 1) == 1)
#     print(extract_bit(0b11111101, 1) == 0)
#     print(extract_bit(0b10111111, 6) == 0)
#     print(extract_bit(0b10110110, 5) == 1)
#     print(extract_bit(0b0110101010110110, 9) == 1)
#     print(extract_bit(0b0110101010110110, 10) == 0)

# def cmderr_test():
#     print("\n\n cmderr_test")
#     pot1 = MCP4131(spi_bus, cs_pin)
    
#     print(pot1.write(ADDR_WPR_0, 0))  # no error (1)
#     print(pot1.write(ADDR_STATUS, 0))  # error (0)

#     print(pot1.read(ADDR_WPR_0))  # no error (1)
#     # print(pot1.read(ADDR_WPR_1))  # error (0)

#     # print(pot1.read(0x02))  # error (0)
#     # print(pot1.write(0x02, 0))  # error (0)

#     pot1.deinit()

# def increment_test():
#     print("\n\n increment_test")
#     pot1 = MCP4131(spi_bus, cs_pin)

#     print(pot1.read(ADDR_WPR_0))
#     pot1.inc()
#     print(pot1.read(ADDR_WPR_0))

#     pot1.deinit()

# def decrement_test():
    # print("\n\n decrement_test")
    # pot1 = MCP4131(spi_bus, cs_pin)

    # print(pot1.read(ADDR_WPR_0))
    # pot1.dec()
    # print(pot1.read(ADDR_WPR_0))

    # pot1.deinit()

def shutdown_test():
    print("\n\n shutdown_test")
    pot1 = mcp4131.MCP4131(spi_bus, cs_pin)

    print(pot1.shutdown())
    pot1.shutdown(1)
    print(pot1.shutdown())
    time.sleep(3)
    pot1.shutdown(0)
    print(pot1.shutdown())
    time.sleep(3)

    pot1.deinit()

def tcon_test():
    print("\n\n tcon_test")
    pot1 = mcp4131.MCP4131(spi_bus, cs_pin)

    print(pot1.tcon())

    # print("shutdown res 0")
    # pot1.tcon(0b11110111)
    # print(pot1.read(ADDR_STATUS))
    # time.sleep(3)

    # print("disconnect term a")
    # pot1.tcon(0b11111011)
    # time.sleep(3)

    # print("disconnect wiper")
    # pot1.tcon(0b11111101)
    # time.sleep(3)

    print("disconnect term b")
    pot1.tcon(0b11111110)
    time.sleep(3)

    pot1.deinit()

def term_con_test():
    print("\n\n term_con_test")
    pot1 = mcp4131.MCP4131(spi_bus, cs_pin)

    print("term a", pot1.term_con(mcp4131.TERM_A))
    pot1.term_con(mcp4131.TERM_A, mcp4131.DISCONNECT)
    print(pot1.term_con(mcp4131.TERM_A))
    time.sleep(3)
    # pot1.term_con(TERM_A, CONNECT)
    # print(pot1.term_con(TERM_A))
    # time.sleep(3)

    print("term b", pot1.term_con(mcp4131.TERM_B))
    pot1.term_con(mcp4131.TERM_B, mcp4131.DISCONNECT)
    print(pot1.term_con(mcp4131.TERM_B))
    # time.sleep(3)
    # pot1.term_con(TERM_B, CONNECT)
    # print(pot1.term_con(TERM_B))
    # time.sleep(3)

    # print("wiper", pot1.term_con(TERM_WPR))
    # pot1.term_con(TERM_A, DISCONNECT)
    # print(pot1.term_con(TERM_WPR))
    # time.sleep(3)
    # pot1.term_con(TERM_A, CONNECT)
    # print(pot1.term_con(TERM_WPR))
    # time.sleep(3)

    pot1.deinit()

# micropython.mem_info()
# testing()
# read_status_test()
# write_reg_test()
# write_position_test()
# write_reistance_test()
# used_pins_test()
# test_limit()
# read_write_test()
# extract_bit_test()
# cmderr_test()
# increment_test()
# decrement_test()
shutdown_test()
# tcon_test()
# term_con_test()