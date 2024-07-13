# from https://www.abelectronics.co.uk/kb/article/1094/i2c-part-4-programming-i2c-with-python

from smbus import SMBus
import time

# Define registers values from datasheet
IODIRA = 0x00  # IO direction A - 1= input 0 = output
IODIRB = 0x01  # IO direction B - 1= input 0 = output    
IPOLA = 0x02  # Input polarity A
IPOLB = 0x03  # Input polarity B
GPINTENA = 0x04  # Interrupt-onchange A
GPINTENB = 0x05  # Interrupt-onchange B
DEFVALA = 0x06  # Default value for port A
DEFVALB = 0x07  # Default value for port B
INTCONA = 0x08  # Interrupt control register for port A
INTCONB = 0x09  # Interrupt control register for port B
IOCON = 0x0A  # Configuration register
GPPUA = 0x0C  # Pull-up resistors for port A
GPPUB = 0x0D  # Pull-up resistors for port B
INTFA = 0x0E  # Interrupt condition for port A
INTFB = 0x0F  # Interrupt condition for port B
INTCAPA = 0x10  # Interrupt capture for port A
INTCAPB = 0x11  # Interrupt capture for port B
GPIOA = 0x12  # Data port A
GPIOB = 0x13  # Data port B
OLATA = 0x14  # Output latches A
OLATB = 0x15  # Output latches B

i2cbus = SMBus(1)
i2caddress = 0x20

# set sequencial mode (bit 5 to 0)
# set default interrupt pin level to LOW (bit 2 to 1)
i2cbus.write_byte_data(i2caddress, IOCON, 0x02)  # Update configuration register
i2cbus.write_word_data(i2caddress, IODIRA, 0x0000)  # Set Port A and B as outputs

counter = 0
shift = 1
while True:
    i2cbus.write_word_data(i2caddress, GPIOA, (~shift)&0xFFFF)
    time.sleep(0.1)  # Wait 500ms
    shift = shift * 2
    counter = counter + 1
    if counter == 15:
        counter = 0
        shift = 1
