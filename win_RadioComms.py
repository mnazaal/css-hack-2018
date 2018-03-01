"""Built upon the code given by Catapult
Author: Trevor Leung
====================
This is built for the lovely window instead"""

from tkinter import *
import tkinter as tk
# import threading
# import Image
from PIL import Image, ImageTk
# from gi.repository import Gtk
# import sys
# import glob
# import signal
# import sys
import serial
import time

iridium = serial.Serial("COM6", 19200, timeout=0)  # This is where you set up to talk to the device


class App():

    def __init__(self, master):
        self.rx_message = ""
        frame = Frame(master)
        frame.pack(fill=BOTH, expand=YES)
        self.button = Button(frame,
                             text="QUIT", fg="red",
                             command=frame.quit)
        self.button.pack(side=BOTTOM, anchor=W, fill=X, expand=YES)

        # Test AT command
        self.SBD = Button(frame,
                          text="AT Ping",
                          command=self.ping)
        self.SBD.pack(side=TOP, anchor=W, fill=X, expand=YES)

        # Check Signal Strength
        self.SBD = Button(frame,
                          text="Check Signal Strength",
                          command=self.signal_strength)
        self.SBD.pack(side=TOP, anchor=W, fill=X, expand=YES)

        # Transmit the data button!!
        self.SBD = Button(frame,
                          text="Tx",
                          command=lambda: self.transmit("CSS:Hackathon!"))
        self.SBD.pack(side=TOP, anchor=W, fill=X, expand=YES)

        # Receive the data button!!
        self.SBD = Button(frame,
                          text="Rx",
                          command=self.receive)
        self.SBD.pack(side=TOP, anchor=W, fill=X, expand=YES)

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
                print(message + "\r\n")
                return message  # get away from the while loop

    # Stupid Encode Function
    def s_en(self, stringToEncode):
        return stringToEncode.encode()

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
        self.response("+SBDIXA:", "Read message code")
        "Reply is +SBDIXA:SOMETHING"

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
        self.response("0", "Loaded successfully...")
        """Reply is 0"""

        # Send the message
        print("\n3. Transmit the message...")
        command = "AT+SBDIX"
        iridium.write(self.s_en(command + "\r\n"))
        while True:
            time.sleep(0.5)
            _read_line = iridium.readline().strip()
            if _read_line != b"":  # Whatever they give it back to us...
                _information = _read_line
                print(_information.decode())
            if "SBDIX: " in _read_line:  # Check for sequence +SBDIX
                iridium.flush()
                print(message.decode() + "\r\n")
                break  # get away from the while loop
        """Reply is +SBDIX: ?,?,?,?,?,?"""

        # Ending the transmission
        command = "AT+SBDD0"  # Clearing buffer
        iridium.write(self.s_en(command + "\r\n"))  # Ending, don't care what it gave back to us...

    # PING FUNCTION - AT&K0
    def ping(self):
        print("\nCommand Sent. Awaiting Response\n")
        command = "AT"
        iridium.write(self.s_en(command + "\r\n"))
        # i=0
        while (True):
            time.sleep(0.5)
            _read_line = iridium.readline().strip()
            if (_read_line != ""):
                _information = _read_line
                print (_information)
            if (_read_line == "ERROR"):
                iridium.flush()
                print("ERROR in Response. Try Again\n")
                break
            if (_read_line == "OK"):
                iridium.flush()
                print("Response Received Successfully\n")
                break

    # SIGNAL STRENGTH REQUEST
    def signal_strength(self):
        print("\nCommand Sent. Awaiting Response\n")
        command = "AT+CSQ"
        iridium.write(self.s_en(command + "\r\n"))
        print("Awaiting for Signal Strength Response")
        time.sleep(0.5)
        # i=0
        self.response("OK", "Response Received Successfully")
        extra_read_line = iridium.readline().strip()
        print(extra_read_line.decode() + "\n")  # Blanc??

    # POWER DOWN IRIDIUM
    def turn_off(self):
        print ("\nCommand Sent. Awaiting Response\n")
        command = "AT*F"
        iridium.write(command + "\r")
        print ("Turn off the device now")
        print("\n")
        iridium.flush()


root = Tk()
ment = StringVar()
root.title("Hackathon")
root.geometry("600x400")
imageFile = "sac.png"
image1 = ImageTk.PhotoImage(Image.open(imageFile))
image2 = ImageTk.PhotoImage(Image.open("sac.png"))
panel1 = tk.Label(root, image=image1)
display = image1
panel1.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
app = App(root)
root.mainloop()
