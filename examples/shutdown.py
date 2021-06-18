import time
import mcp4131 as mcp

pot1 = mcp.MCP4131("PA4")

# Enter shutdown mode
# wiper at position B, A disconnected
pot1.shutdown(1)

# read current shutdown status from registers
print( "Shutdown Status:", pot1.shutdown() )
time.sleep(3)

# Exit shutdown mode
pot1.shutdown(0)
print( "Shutdown Status:", pot1.shutdown() )