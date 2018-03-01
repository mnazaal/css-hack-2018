"""Built upon the code given by Catapult
It does not implement the TkInter approach
Author: Trevor Leung
Date: 01/03/2018
====================
This is built for the lovely window instead"""

import serial
import time

iridium = serial.Serial("COM6", 19200, timeout=0)  # This is where you set up to talk to the device
# Look at what your COM port is first

class Irc():

    def __init__(self):
        self.rx_message = ""

    # Response function
    def response(self, confirmation, message):
        while True:
            time.sleep(0.5)
            _read_line = iridium.readline().strip()
            if _read_line != b"":
                _information = _read_line
                print(_information)
            if _read_line == b"ERROR":
                iridium.flush()
                print("X: ERROR in Response. Try Again\n")
                break
            if confirmation.encode() in _read_line:  # Confirmation code you should get from the device
                iridium.flush()
                # print(_read_line.decode() + "\r\n")
                print(message + "\r\n")
                return _read_line.decode()  # get away from the while loop

    # Stupid Encode Function
    def s_en(self, stringToEncode):
        return stringToEncode.encode()

    # MT Function
    def receive(self):
        # Here we go again
        print("\n1. Query the device for registration status")
        command = "AT+SBDREG?"
        iridium.write(self.s_en(command + "\r\n"))
        self.response("+SBDREG:2", "Read message code")
        "Reply is +SBDREG:SOMETHING"

        # Initiate an SBD session in answer to the automatic notification
        print("2. Initiating an SBD session")
        command = "AT+SBDIXA"
        iridium.write(self.s_en(command + "\r\n"))
        self.response("+SBDIX:", "Read message code")  # No A apparently
        "Reply is +SBDIX:SOMETHING"

        # Getting the message
        print("3. Getting the message")
        command = "AT+SBDRB"
        iridium.write(self.s_en(command + "\r\n"))
        self.rx_message = self.response("", "Message received")  # Whatever we have literally

    # MO Function
    def transmit(self, message):
        # Enabling indicator event reporting
        print("\n1. Enabling error indicator...\n")
        command = "AT+CIER=1,0,1,0"
        iridium.write(self.s_en(command + "\r\n"))
        self.response("OK", "Indicator enabled\n")
        """Reply is OK"""

        # Initializing
        print("\n2. Load the message...\n")
        command = "AT+SBDWB=" + str(len(message))
        iridium.write(self.s_en(command + "\r\n"))
        self.response("READY", "Trying to transmit")
        """Reply is READY"""

        # Load the message
        iridium.write(self.s_en(message))  # + "\r\n"
        checksum = 0
        for c in message:  # Message is specified in the TkInter as above
            checksum = checksum + ord(c)
        iridium.write(self.s_en(chr(checksum >> 8)))  # Adding checksum... [Verified it's working]
        iridium.write(self.s_en(chr(checksum & 0xFF)))
        self.response("", "Loaded...")
        """Reply is 0 if successful"""

        # Send the message
        print("\n3. Transmit the message...")
        command = "AT+SBDIX"
        iridium.write(self.s_en(command + "\r\n"))
        self.response("SBDIX:", "Replied")
        """Reply is +SBDIX: ?,?,?,?,?,?"""

        # Ending the transmission
        command = "AT+SBDD0"  # Clearing buffer
        iridium.write(self.s_en(command + "\r\n"))  # Ending, don't care what it gave back to us...

    # PING FUNCTION - AT&K0
    def ping(self):
        print("\nCommand Sent. Awaiting Response\n")
        command = "AT"
        iridium.write(self.s_en(command + "\r\n"))
        self.response("OK", "Response Received Successfully")

    # SIGNAL STRENGTH REQUEST
    def signal_strength(self):
        print("\nCommand Sent. Awaiting Response\n")
        command = "AT+CSQ"
        iridium.write(self.s_en(command + "\r\n"))
        print("Awaiting for Signal Strength Response")
        time.sleep(0.5)
        self.response("OK", "Response Received Successfully")
        extra_read_line = iridium.readline().strip()
        print(extra_read_line.decode() + "\n")

    # POWER DOWN IRIDIUM
    def turn_off(self):
        print("\nCommand Sent. Awaiting Response\n")
        command = "AT*F"
        iridium.write(self.s_en(command + "\r"))
        print("Turn off the device now")
        iridium.flush()

