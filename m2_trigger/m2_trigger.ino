int ledPin = 13;
int inPin = 2;
int val = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(ledPin, OUTPUT);
  pinMode(inPin, INPUT);
  digitalWrite(ledPin, LOW);
  Serial.begin(115200);
  }

void loop() {
  // put your main code here, to run repeatedly:
  val = digitalRead(inPin);
  digitalWrite(ledPin, LOW);
  if (val == HIGH){
    digitalWrite(ledPin, HIGH);
    Serial.print("Toggle command recognized!\n");
    while (val == HIGH){
      val = digitalRead(inPin);
    }
  }
}
