import time
import mcp4131 as mcp
from machine import Pin

pot1 = mcp.MCP4131(1, "PA4")
pot2 = mcp.MCP4131(1, "PA3")

r_list = [x*1000 for x in range(11)]  # 0 to 10k
print(r_list)
i = 0

while True:
    print("\n", i, r_list[i], 1-(i/11))
    print(pot1.res(r_list[i]))
    print(pot2.pos( 1-(i/11) ))

    if i == 10:
        i = 0
    else:
        i += 1

    time.sleep(3)