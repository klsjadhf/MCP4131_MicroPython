from mcp4131 import TERM_A
import time
import mcp4131 as mcp

pot1 = mcp.MCP4131("PA4")

# term_con() terminal connections
#   inputs: 
#       term: terminal to control
#       con: connect or disconnect
#   return:
#       current status of terminal
#   terminals:
#       TERM_WPR
#       TERM_A
#       TERM_B

# Disconnect terminal A
pot1.term_con(mcp.TERM_A, mcp.DISCONNECT)

# get current status of terminal A
if pot1.term_con(mcp.TERM_A) == mcp.CONNECT:
    print("Terminal A connected")
elif pot1.term_con(mcp.TERM_A) == mcp.DISCONNECT:
    print("Terminal A dicconnected")
time.sleep(3)

# Connect terminal A
pot1.term_con(mcp.TERM_A, mcp.CONNECT)
print("Term A: ", pot1.term_con(mcp.TERM_A) )