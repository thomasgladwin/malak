//  Variables
int PulseSensorPurplePin = 0;   // Pulse Sensor PURPLE WIRE connected to ANALOG PIN 0
int LightSensorPin = 1;         // Analog trigger via light code
int manualTriggerPin = 2;       // Digital trigger via COM
int LED13 = 13;                 // The on-board Arduion LED

int lightTrigger = 0;
int manualTrigger = 0;
int USBTrigger = 0;
int Signal;                     // holds the incoming raw data. Signal value can range from 0-1024

int loop_delay = 5;

int capturing_on = 0;
int waiting_for_trigger = 1;

// The SetUp Function:
void setup() {
  pinMode(LED13, OUTPUT);
  digitalWrite(LED13,LOW);
  pinMode(manualTrigger, INPUT_PULLUP);
  Serial.begin(9600);           // Sets up Serial Communication at certain speed.
}

// The Main Loop Function
void loop() {

  Signal = analogRead(PulseSensorPurplePin);  // Read the PulseSensor's value. 
                                              // Assign this value to the "Signal" variable.
  //manualTrigger = digitalRead(manualTriggerPin);
  //USBTrigger = Serial.read();
  lightTrigger = analogRead(LightSensorPin);  // Read the light sensor's value. 

  if (1 == 1 || capturing_on == 1) {
    Serial.print(Signal);
    Serial.print('\t');
    Serial.print(lightTrigger);
    Serial.print('\n');
    //Serial.print('\t');
    //Serial.print(manualTrigger);
    //Serial.print('\t');
    //Serial.println(USBTrigger);
  }

  delay(loop_delay);
   
}

