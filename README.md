# MCP4131_MicroPython
MicroPython library for MCP4131 digital potentiometer from Microchip  

## Connections  
![image](https://user-images.githubusercontent.com/56586471/122552094-71d6a280-d068-11eb-92e0-08d198e242d2.png)  
Using 240 ohms for STM32F407VET board  
SPI 1 for STM32f407
Pin | Function
--- |----  
PA5 | SCK  
PA6 | MISO  
PA7 | MOSI  

## Problems
CMDERR bit not working properly  
Math not fully checked might be off by 1 bit, etc
