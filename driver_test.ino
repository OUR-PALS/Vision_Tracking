#include <Encoder.h>



int in1=2;
int in2=3;
Encoder myEnc(4, 5);


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  
}`

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("moving forward");
  moveforward();
  for(int i=0;i<1000;i++){
    delay(1);
    Serial.println(myEnc.read());
    }
  
  stopmove();
  delay(300);
  movebackward();
  for(int i=0;i<1000;i++){
    delay(1);
    Serial.println(myEnc.read());
    }
}

void stopmove(){
  digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
  }
void moveforward(){
  digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
  }

void movebackward(){
  digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
  }

