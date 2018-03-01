"""Built upon the code given by Catapult
Author: Trevor Leung
Date: 01/03/2018"""

import serial
import time

iridium = serial.Serial("/dev/ttyUSB0", 19200, timeout=0)  # This is where you set up to talk to the device


class App():

    def __init__(self):
        self.rx_message = ""
        

    # Response function
    def response(self, confirmation, message):
        while (True):
            time.sleep(0.5)
            _read_line = iridium.readline().strip()
            if (_read_line != ""):
                _information = _read_line
                print(_information)
            if (_read_line == "ERROR"):
                iridium.flush()
                print("X: ERROR in Response. Try Again\n")
                break
            if (confirmation in _read_line):  # Confirmation code you should get from the device
                iridium.flush()
                print(message + "\r\n")
                return message

    # MT Function
    def receive(self):
        # Here we go again
        print("\n1. Query the device for registration status")
        command = "AT+SBDREG?"
        iridium.write(command + "\r\n")
        self.response("+SBDREG:2", "Read message code")
        "Reply is +SBDREG:SOMETHING"

        # Initiate an SBD session in answer to the automatic notification
        print("2. Initiating an SBD session")
        command = "AT+SBDIXA"
        iridium.write(command + "\r\n")
        self.response("+SBDIX:", "Read message code")  # No A apparently
        "Reply is +SBDIX:SOMETHING"

        # Getting the message
        print("3. Getting the message")
        command = "AT+SBDRB"
        iridium.write(command + "\r\n")
        self.rx_message = self.response("", "Message received")  # Whatever we have literally


    # MO Function
    def transmit(self, message):
        # Enabling indicator event reporting
        print("\n1. Enabling error indicator...\n")
        command = "AT+CIER=1,0,1,0"
        iridium.write(command + "\r\n")
        self.response("OK", "Indicator enabled\n")
        """Reply is OK"""

        # Initializing
        print("\n2. Load the message...\n")
        command = "AT+SBDWB=" + str(len(message))
        iridium.write(command + "\r\n")
        self.response("READY", "Trying to transmit")
        """Reply is READY"""

        # Load the message
        iridium.write(message)  # + "\r\n"
        checksum = 0
        for c in message:  # Message is specified in the TkInter as above
            checksum = checksum + ord(c)
        iridium.write(chr(checksum >> 8))  # Adding checksum... [Verified it's working]
        iridium.write(chr(checksum & 0xFF))
        self.response("0", "Loaded...")
        """Reply is 0 if successful"""

        # Send the message
        print("\n3. Transmit the message...")
        command = "AT+SBDIX"
        iridium.write(command + "\r\n")
        self.response("SBDIX:", "Replied")
        """Reply is +SBDIX: ?,?,?,?,?,?"""

        # Ending the transmission
        command = "AT+SBDD0"  # Clearing buffer
        iridium.write(command + "\r\n")  # Ending, don't care what it gave back to us...

    # PING FUNCTION - AT&K0
    def ping(self):
        print("\nCommand Sent. Awaiting Response\n")
        command = "AT"
        iridium.write(command + "\r\n")
        self.response("OK", "Response Received Successfully")

    # SIGNAL STRENGTH REQUEST
    def signal_strength(self):
        print("\nCommand Sent. Awaiting Response\n")
        command = "AT+CSQ"
        iridium.write(command + "\r\n")
        print("Awaiting for Signal Strength Response")
        time.sleep(0.5)
        self.response("OK", "Response Received Successfully")
        extra_read_line = iridium.readline().strip()
        print(extra_read_line.decode() + "\n")

    # POWER DOWN IRIDIUM
    def turn_off(self):
        print("\nCommand Sent. Awaiting Response\n")
        command = "AT*F"
        iridium.write(command + "\r")
        print("Turn off the device now")
        print("\n")
        iridium.flush()


test = App()
test.transmit("CSS:Hackathon!")
