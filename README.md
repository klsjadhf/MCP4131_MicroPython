# MCP4131_MicroPython
MicroPython library for MCP4131 & MCP41HV31 digital potentiometer from Microchip  

## Connections  
![image](https://user-images.githubusercontent.com/56586471/122552094-71d6a280-d068-11eb-92e0-08d198e242d2.png)  
For MCP4131 with multiplexed SDI/SDO. Using 240 ohms for STM32F407VET board  

SPI pins for STM32f407:    
Bus  |  1  |  2   |  3  
---- |-----|------|-----  
SCK  | PA5 | PB13 | PB3  
MISO | PA6 | PB14 | PB4  
MOSI | PA7 | PB15 | PB5  

## Problems
CMDERR bit not working properly  
Math not fully checked might be off by 1 bit, etc
