import time
import mcp41xx31 as mcp

pot1 = mcp.MCP4131("PB12", bus=2, res=mcp.RES_10K)
# pot1 = mcp.MCP41HV31("PB11", bus=2, res=mcp.RES_100K)

# write register function
#   input: register to write, data
#       values: ADDR_WPR_0
#               ADDR_TCON
#               ADDR_STATUS (not avaliable in HV version)
#   return: nothing
pot1.write(mcp.ADDR_WPR_0, 0x05)  # write 0x05 into register for resistor 0

# read register function
#   input: register to read
#       values: ADDR_WPR_0
#               ADDR_TCON
#               ADDR_STATUS (not avaliable in HV version)
#   return: value in register
print("ADDR_WPR_0", pot1.read(mcp.ADDR_WPR_0))  # print current value for resistor 0

# tcon function
#   input: data to write to TCON register (optional)
#   return: value in register
pot1.tcon(0x00)  # disconnect everything
print("TCON", hex(pot1.tcon()))
time.sleep(3)
pot1.tcon(0xFF)  # connect everything
print("TCON", hex(pot1.tcon()))