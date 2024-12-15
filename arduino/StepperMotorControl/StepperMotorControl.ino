#include <Stepper.h>

const int L1 = 2;
const int L2 = 0;
const int L3 = 1;
boolean L1Val = 0;
int mode = -1;
int motor = 0;
float current_position = 500.0;
int goal = 100;
const unsigned char PS_128 = (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0);
const int stepsPerRevolution = 2038;
Stepper stepper(stepsPerRevolution, 8, 10, 9, 11);


void setup() {
  ADCSRA &= ~PS_128;
  ADCSRA |= (1 << ADPS1) | (1 << ADPS0);
  Serial.begin(115200);
  analogReference(INTERNAL);
  pinMode(L1, INPUT);
  pinMode(L2, INPUT);
  pinMode(L3, INPUT);
  pinMode(7, OUTPUT);
  stepper.setSpeed(15);
  digitalWrite(7, motor);
}


void loop() {

  while (current_position < goal && motor == 1){
    stepper.step(1);
    current_position++;
  }
  while(current_position > goal && motor == 1){
    stepper.step(-1);
    current_position--;
  }

  while (mode == 0 && motor==0){
  Serial.println(current_position);
  if((analogRead(L1) > 700) && (L1Val == 0)){
    L1Val = 1;
  }
  if ((L1Val == 1) && (analogRead(L2) > 700)){
    mode = 1;
    L1Val = 0;
  }

  if ((L1Val == 1) && (analogRead(L3) > 700)) {
    mode = 2;
    L1Val = 0;
  }
  }
  if (mode == 1){
    current_position = current_position - 0.0025;
  }
  if (mode == 2){
    current_position = current_position + 0.0025;
  }
  if (analogRead(L1) < 700 && analogRead(L2) < 700 && analogRead(L3) < 700 && motor == 0){
    mode = 0;
  }

}