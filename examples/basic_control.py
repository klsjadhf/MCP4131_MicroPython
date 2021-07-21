import time
import mcp41xx31 as mcp

# required inputs: pin for chip select
# optional parameters:
#    bus = 1  default is bus 1
#    res = RES_10K (default) max resistance of the pot
#          RES_5K
#          RES_50K
#          RES_100K
#    mode = MODE_11 (default) spi mode 
#           MODE_00
#    baud = 250000 (baud rate may not be same as what you set. depends on clock dividers)
pot1 = mcp.MCP4131("PB12", bus=2, res=mcp.RES_10K)
pot2 = mcp.MCP41HV31("PB11", bus=2, res=mcp.RES_100K)

r_list = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
for i in range(11):
    # res function 
    #   input: resistance measured from wiper to terminal B
    #   return: current resistance from registers
    pot1.res(r_list[i])  # set resistance from list
    print(r_list[i], pot1.res())

    # pos function
    #   input: postion from terminal B (0 is at B, 1 is at A, 0.5 is mid position)
    #   return: current position calcuated from register value
    print( 1-(i/10), pot2.pos( 1-(i/10) ) )  # decreasing resistance

    time.sleep(3)

pot1.pos(0)  # wiper at terminal B
pot2.pos(1)  # wiper at terminal A
for i in range(130):
    # inc/dec functions
    #   increase/decrease register values by 1
    pot1.inc()
    pot2.dec()
    time.sleep(0.05)