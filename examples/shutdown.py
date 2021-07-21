import time
import mcp41xx31 as mcp

pot1 = mcp.MCP4131("PB12", bus=2, res=mcp.RES_10K)
# pot1 = mcp.MCP41HV31("PB11", bus=2, res=mcp.RES_100K)

# Enter shutdown mode
# wiper at position B, A disconnected
pot1.shutdown(1)

# read current shutdown status from registers
print( "Shutdown Status:", pot1.shutdown() )
time.sleep(3)

# Exit shutdown mode
pot1.shutdown(0)
print( "Shutdown Status:", pot1.shutdown() )