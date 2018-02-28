from Tkinter import *
import Tkinter as tk
import threading
# import Image
from PIL import Image, ImageTk
from gi.repository import Gtk
import sys
import glob
import signal
import sys
import serial
import time

iridium = serial.Serial("/dev/ttyUSB0", 19200, timeout=0)  # This is where you set up to talk to the device


class App():

    def __init__(self, master):
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
                          text="Transmit data!",
                          command=self.transmit("CSS:Hackathon Rocks!"))
        self.SBD.pack(side-TOP, anchor=W, fill=X, expand=YES)

    # Response function
    def response(self, confirmation, message):
        while (True):
            time.sleep(0.5)
            _read_line = iridium.readline().strip()
            if (_read_line != ""):
                _information = _read_line
                print ("X" + _information)
            if (_read_line == "ERROR"):
                iridium.flush()
                print("X: ERROR in Response. Try Again\n")
                break
            if (_read_line == confirmation):  # Confirmation code you should get from the device
                iridium.flush()
                print("X: " + message)
                break  # get away from the while loop

    # MO Function
    def transmit(self, message):
        # Enabling indicator event reporting
        print("\nEnabling error indicator event reporting command sent. Awaiting Response\n")
        command = "AT+CIER=1,0,1,0"
        iridium.write(command + "\r\n")
        self.response("OK", "Error indicator enabled\n")
        """Reply is OK"""

        # Initializing
        print("\nTransmitting message\n")
        command = "AT+SBDWB=" + str(len(message))
        iridium.write(command + "\r\n")
        self.response("READY", "Beginning transmission...")
        """Reply is READY"""

        # Load the message
        iridium.write(message + "\r")  # + "\r\n"
        checksum = 0
        for c in message:  # Message is specified in the TkInter as above
            checksum = checksum + ord(c)
        iridium.write(chr(checksum >> 8))  # Adding checksum... [Verified it's working]
        iridium.write(chr(checksum & 0xFF))
        self.response("0", "Message is loaded...")
        """Reply is 0"""

        # Send the message
        command = "AT+SBDIX"
        iridium.write(command + "\r\n")
        while (True):
            time.sleep(0.5)
            _read_line = iridium.readline().strip()
            if (_read_line != ""):  # Whatever they give it back to us...
                _information = _read_line
                print(_information)
                break
        """Reply is +SBDIX: ?,?,?,?,?,?"""

        # Ending the transmission
        command = "AT+SBDD0"  # Clearing buffer
        iridium.write(command + "\r\n")  # Ending, don't care what it gave back to us...

    # PING FUNCTION - AT&K0
    def ping(self):
        print ("\nCommand Sent. Awaiting Response\n")
        command = "AT"
        iridium.write(command + "\r\n")
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
        print ("\nCommand Sent. Awaiting Response\n")
        command = "AT+CSQ"
        iridium.write(command + "\r\n")
        print ("Awaiting for Signal Strength Response")
        time.sleep(0.5)
        # i=0
        while (True):
            time.sleep(0.1)
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
        extra_read_line = iridium.readline().strip()
        print (extra_read_line + "\n")  # Blanc??

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
