
#define RPWM 7
#define LPWM 6
int out1;
int out2;
int threshold = 150;
int goal = 0;
void setup() {
  Serial.begin(115200);
  Serial.setTimeout(2);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(LPWM, OUTPUT);
  pinMode(RPWM, OUTPUT);
  analogWrite(LPWM, 0);
  analogWrite(RPWM, 0);
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

void drive_test(int speed){
    analogWrite(LPWM,100);
    analogWrite(RPWM,00);
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
  while (!(goal-threshold < current && current < goal+threshold)){
    current = analogRead(A0);
    Serial.println(current);
    if (current >= goal+threshold){turnLeft();}
    if (current <= goal-threshold){turnRight();}
  }
  turnOff();
  while(Serial.available()>0){Serial.read();}
  }
}