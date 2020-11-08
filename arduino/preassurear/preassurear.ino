/* Simple example code for Force Sensitive Resistor (FSR) with Arduino. More info: https://www.makerguides.com */

// Define FSR pin:
#define fsrpin A0
#define fsrpin1 A1
//Define variable to store sensor readings:
int fsrreading; //Variable to store FSR value
int fsrreading1;

void setup() {
  // Begin serial communication at a baud rate of 9600:
  Serial.begin(9600);
}

void loop() {
  fsrreading = analogRead(fsrpin);
  fsrreading1 = analogRead(fsrpin1);
  Serial.print(fsrreading);
  Serial.print(", ");
  Serial.println(fsrreading1);


  delay(100); //Delay 500 ms.
}
