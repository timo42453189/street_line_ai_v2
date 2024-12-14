int L1 = 2;
int L2 = 0;
int L3 = 1;
boolean L1Val = 0;
int mode = 0;
const unsigned char PS_128 = (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0);

void setup() {
  ADCSRA &= ~PS_128;
  ADCSRA |= (1 << ADPS1) | (1 << ADPS0);
  Serial.begin(115200);
  analogReference(INTERNAL);
  pinMode(L1, INPUT);
  pinMode(L2, INPUT);
  pinMode(L3, INPUT);

}

void loop() {
  Serial.println(analogRead(L3));
  while (mode == 0){
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
    Serial.println("Anticlockwise");
  }
  if (mode == 2){
    Serial.println("Clockwise");
  }
  if (analogRead(L1) < 600 && analogRead(L2) < 600 && analogRead(L3) < 600){
    mode = 0;
  }

}
