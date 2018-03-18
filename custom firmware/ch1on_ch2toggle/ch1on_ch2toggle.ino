int CH1 = 7;
int CH2 = 8;
int CH3 = 9;

void setup() {
  // put your setup code here, to run once:
  pinMode(CH1, OUTPUT);
  pinMode(CH2, OUTPUT);
  pinMode(CH3, OUTPUT);
  digitalWrite(CH1, HIGH);
  digitalWrite(CH2, HIGH);
  digitalWrite(CH3, HIGH);
  digitalWrite(CH1, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  int randomdelay1 = random(100,2000);
  int randomdelay2 = random(100,2000);
  digitalWrite(CH2, LOW);
  delay(randomdelay1);
  digitalWrite(CH2, HIGH);
  delay(randomdelay2);
}
