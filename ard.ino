#include <Arduino.h>
#include <Servo.h>

void setup() {
  Serial.begin(57600); // Initialize serial communication
}

void loop() {
  Serial.println("Hello");
  delay(1000); // Delay for 1 second
}
