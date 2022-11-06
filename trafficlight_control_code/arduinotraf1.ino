// Include IR Remote Library by Ken Shirriff
#include <IRremote.h>
 
// Define sensor pin
const int RECV_PIN = 2;
 
// Define LED pin constants
const int red = 4; 
const int yellow = 5;
const int green = 6;

// Define integer to remember toggle state
int togglestate = 0;
 
// Define IR Receiver and Results Objects
IRrecv irrecv(RECV_PIN);
decode_results results;
 
 
void setup(){
  // Enable the IR Receiver
  irrecv.enableIRIn();
  // Set LED pins as Outputs
  pinMode(red, OUTPUT);
  pinMode(yellow, OUTPUT);
  pinMode(green, OUTPUT);
}
 


void loop(){
    if (irrecv.decode(&results)){
 
        switch(results.value){
         case 0xFFB04F://red Keypad Button
        // Toggle LED On or Off
        if(togglestate==0){
        digitalWrite(yellow, LOW);
        digitalWrite(green, LOW);
        digitalWrite(red, HIGH);
        togglestate=1;
        }
        else {
        digitalWrite(red, LOW);
        digitalWrite(yellow, LOW);
        digitalWrite(green, LOW);
        togglestate=0;
        }
        break;

        case 0xFF9867: //Yellow Keypad Button
        // Toggle LED On or Off
        if(togglestate==0){
        digitalWrite(green, LOW);
        digitalWrite(yellow, HIGH);
        delay(3000);
        digitalWrite(yellow, LOW);
        digitalWrite(red, HIGH);
        togglestate=1;
        }
        else {
        digitalWrite(red, LOW);
        digitalWrite(yellow, LOW);
        digitalWrite(green, LOW);
        togglestate=0;
        }
        break;

        case 0xFF6897://green Keypad Button
        // Toggle LED On or Off
        if(togglestate==0){
        digitalWrite(red, LOW);
        digitalWrite(yellow, LOW);
        digitalWrite(green, HIGH);
        togglestate=1;
        }
        else {
        digitalWrite(red, LOW);
        digitalWrite(yellow, LOW);
        digitalWrite(green, LOW);
        togglestate=0;
        }
        break;
        
        case 0xFF30CF: //green to yellow to red to green Keypad Button
        // Toggle LED On or Off
        if(togglestate==0){
        digitalWrite(green, HIGH);
        delay(6000);
        digitalWrite(green, LOW);
        digitalWrite(yellow, HIGH);
        delay(3000);
        digitalWrite(yellow, LOW);
        digitalWrite(red, HIGH);
        delay(6000);
        digitalWrite(red, LOW);
        digitalWrite(green, HIGH);
        togglestate=1;
        }
        else {
        digitalWrite(red, LOW);
        digitalWrite(yellow, LOW);
        digitalWrite(green, LOW);
        togglestate=0;
        }
        break;

        case 0xFF18E7: //red to green to yellow to red Keypad Button
        // Toggle LED On or Off
        if(togglestate==0){
        digitalWrite(red, HIGH);
        delay(6000);
        digitalWrite(red, LOW);
        digitalWrite(green, HIGH);
        delay(6000);
        digitalWrite(green, LOW);
        digitalWrite(yellow, HIGH);
        delay(3000);
        digitalWrite(yellow, LOW);
        digitalWrite(red, HIGH);
        togglestate=1;
        }
        else {
        digitalWrite(red, LOW);
        digitalWrite(yellow, LOW);
        digitalWrite(green, LOW);
        togglestate=0;
        }
        break;
        

    }
    irrecv.resume(); 
  }
 
}