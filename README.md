# malak
Psychophysiology measurement via Arduino

# Hardware
Microcontroller: Elegoo Basic Starter Kit (really nice Uno R3 Arduino clone with jumper wires, breadboard, light
sensor, etc),
https://www.amazon.co.uk/gp/product/B01DGD2GAO/ref=od_aui_detailpages01?ie=UTF8&psc=1. Around 14
pounds.

Pulse Sensor for heart rate: Pulse Sensor’s pulse sensor,
https://www.amazon.co.uk/gp/product/B01CPP4QM0/ref=od_aui_detailpages01?ie=UTF8&psc=1. Around 20
pounds. This sensor provides a photoplethysmogram (PPG): A voltage signal that reflects the changes in
blood oxygen levels that occur as patterns between heart beats. The sensor exploits changes in light absorption measured at the skin on the finger, which occur due to subtle changes in the volume of blood vessels during the cardiac cycle.

Computer to present tasks and save data.

# Basic set-up
Elegoo has a tutorial for the microcontroller on elegoo.com. This goes through installing the Arduino
programming IDE for the Processing language (this doesn't appear to require admin rights). Working on Windows 10, I plugged the board into a USB port using the USB cable, before installing the software. When I first opened the IDE, I could select the
Port with the Arduino connected via Tools -> Port, and everything worked without any problems.
Lesson 1 of the Elegoo tutorial perhaps goes into technical details a little much for first use, which you
can skip; but it’s a good resource. Lesson 2 is the classic “blink” function: Do that for a first introduction
and test everything’s working.

Then do a pulse sensor tutorial: www.pulsesensor.com has a Getting Started project. Just follow the
video to get the very easy connections done and putting the velcro and vinyl stickers on. The video
explains how to get the necessary Processing code (the .ino file) from PulseSensor’s github repository.
Open the code and upload to the board. Using Tools -> Serial Plotter shows the pulse signal!

# Making it usable for experiments

So the data are already there! We just need to save them, and we might need to
synchronize the PPG to task events.

In preparation for this, we’re going to use the breadboard for connections instead of plugging into the microcontroller
directly. Use jumper cables to power the breadboard by connecting the microcontroller’s ground and 5V
pins to the – and + columns (on the side of the board; pick either side), respectively. Pick a row, or 
“line”, on the breadboard and connect any pin to the A0 pin on the microcontroller. Then attach the pins
of the pulse sensor to the breadboard: The 5V and ground to any line on the side-lines, and the purple
wire to a pin on the same line, and the same side of the line, as the pin connected to A0. (The lines are
“cut” down the middle so without, e.g., a resistor or button, pins on the left aren’t connected to pins on
the right.) Check whether the PPG is still coming through via Serial Plotter. Also have a look at the raw
numbers coming in with Serial Monitor.

# Using a light sensor to synchronize task events and data

The Elegoo basic kit includes a light sensor. Its wiring is given in its chapter in the Elegoo tutorial. Use A1 instead of A0 (since A0 is used for the pulse sensor). Make sure you use a suitable resistor, otherwise the signal values can be attenuated or become zero.

The file malak.ino in this repository contains the Processing code to measure the PPG and light sensor data. Upload this code to the microcontroller (make sure you're using the right type via Tools->Board, if you're using a Nano for instance) and open the Serial Monitor to see how sensitive the light sensor is. If we hold it up to some point of a black screen, it’s very clear if anything flashes white at that position. We can use that when programming tasks to synchronize the signal. For instance: The task lights up a rectangle or border at the start of every block and saves the exact time of the flash. If we save the light sensor signal together with the PPG signal, we can use the response to those flashes to synchronize the data. One nice thing is that this means we can use JavaScript tasks which wouldn’t allow triggers via a USB connection. Hence, we can use the same tasks for online and lab experiments. For an example online experiment with Javascript tasks, see https://github.com/thomasgladwin/onlineABM.

We do need to get the light sensor into position on the screen (at the time of synchronization at least) and program the task to send some suitable light signal via the screen. One possibility is to light up the border of the Javascript canvas at the
Introduction screen of the task, and save the time point when the border is removed and the edges turn
black. That would allow a procedure in which the task can start up, then wait at the Introduction screen
until the sensor is positioned, and then the participant can continue with the task.

# Using a Python program to save data

Install Python 3.x. If you use the Anaconda distribution, you don't need admin rights. Also install the libraries needed by malak.py and malak_sample.py. E.g., the pyserial library: From command line (search “cmd” or use Powershell or the Anaconda command line; make sure python.exe is in the path): python -m pip install pyserial. At the time of writing, the other libary not available by default is pygame, which you can install the same way.

Now you can use the Python program malak.py from this repository: python malak.py. You may need to go into malak_sample.py to adjust the COM port to match your hardware.

It will ask for a base filename to save data to (base.log), open a window, and then keep on reading in what the microcontroller is sending and saving it to file. You should see a visual representation of the signal values coming in, as well as the peak detection for the PPG. There's also a visual and auditory representation of the heart rate over the last few seconds, which could be useful for biofeedback purposes. Measurement stops when you close the window.

malak.py calls malak_sample.py, but you can also run malak_sample.py directly: This only reads and prints the values coming in.

So the procedure would be something like:

- Start the task, which must indicate where to hold the light sensor and wait for a response before continuing.
- Attach the PPG to the participant's finger.
- Start the measurement program.
- Hold the light sensor to the correct area of the screen.
- Press a button that changes the screen brightness at that location and then continues to the next instruction screen of the task.
- Put away the light sensor.
- The participant performs the task.
- After the task ends, close the malak window to stop measurement.

# Hardware design

The document Hardware_design.docx currently shows a probably useless photo of the wiring of a prototype. To be updated if I ever get round to making it nicer.
