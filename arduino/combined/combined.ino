#include <Stepper.h>


#define RPWM 7
#define LPWM 6
int out1;
int out2;
int threshold = 150;
int goal = 0;
const int L1 = 4;
const int L2 = 2;
const int L3 = 3;
boolean L1Val = 0;
int state = -1;
int motor_enable = 1;
float current_position = 500.0;
const int stepsPerRevolution = 2038;
Stepper stepper(stepsPerRevolution, 30, 32, 31, 33);

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(2);
  analogReference(INTERNAL);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(LPWM, OUTPUT);
  pinMode(RPWM, OUTPUT);
  pinMode(L1, INPUT);
  pinMode(L2, INPUT);
  pinMode(L3, INPUT);
  pinMode(7, OUTPUT);
  stepper.setSpeed(15);
  digitalWrite(7, motor_enable);
  analogWrite(LPWM, 0);
  analogWrite(RPWM, 0);
  steer_to(500);
}

void driveForward(){
  int speed = analogRead(A1);
    if(speed>512){
    out1=map(speed,512,1023,0,255);
    analogWrite(LPWM,out1);
    analogWrite(RPWM,0);
  }
  if(speed<512){
    out2=map(speed,512,0,0,255);

    analogWrite(RPWM,out2);
    analogWrite(LPWM,0);
}
}

void turnRight(){
  digitalWrite(9, HIGH);
  digitalWrite(10, LOW);
}

void turnLeft(){
  digitalWrite(10, HIGH);
  digitalWrite(9, LOW);
}

void turnOff(){
  digitalWrite(9, LOW);
  digitalWrite(10, LOW);
}

void steer_to(int goal){
    int current = analogRead(A0);
    while (!(goal-threshold < current && current < goal+threshold)){
        current = analogRead(A0);
        Serial.println(current);
        if (current >= goal+threshold){turnLeft();}
        if (current <= goal-threshold){turnRight();}
     }
    turnOff();
}

void moveStepperMotor(int goal) {
    while (current_position < goal && motor == 1){
        stepper.step(1);
        current_position++;
    }
    while(current_position > goal && motor == 1){
        stepper.step(-1);
        current_position--;
    }
}

void loop() {
  driveForward();
  if (Serial.available() > 0){
    String buff = Serial.readStringUntil("\n");
    goal = buff.toInt();
    while (goal > 1005) {
    String numString = String(goal);
    numString.remove(numString.length() - 1);
    goal = numString.toInt();
  }
  if (goal>1000){goal=1000;};if(goal<10){goal=10;}
  int current = analogRead(A0);
  steer_to(goal);
  moveStepperMotor(goal);
  while(Serial.available()>0){Serial.read();}
  }
}