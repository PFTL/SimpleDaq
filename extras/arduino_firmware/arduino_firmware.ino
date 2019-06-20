String Comm;

int output = DAC0;
int input;
int val;
String inData;
String tempValue;
String channel;
int sensorPin = A0;    // select the input pin for the potentiometer
int sensorValue;
bool isData = false;
int i = 0;
int ledPin = 13;

void setup() {
  Serial.begin(9600);
  while (!Serial);
  analogWriteResolution(12);
  analogWrite(DAC0, 0);
  analogWrite(DAC1, 0);
  pinMode(ledPin, OUTPUT);
}

void loop() {
  while (Serial.available() > 0 ) {
    char value = Serial.read();
    Comm += value;
    if (value == '\n') {
      isData = true;
    }
  }
  if (isData) {
    isData = false;
    if (Comm.startsWith("IDN\n")) {
      Serial.print("General DAQ Device built by Uetke. v.1.2017");
      Serial.print("\n");
    }
    else if (Comm.startsWith("OUT")) {
      channel = Comm[6];
      if (channel.toInt() == 1) {
        output = DAC1;
      }
      else if (channel.toInt() == 0) {
        output = DAC0;
      }
      tempValue = "";
      for (i = 8; i < Comm.length(); i++) {
        tempValue += Comm[i];
      }
      val = tempValue.toInt();
      analogWrite(output, val);
    }
    else if (Comm.startsWith("IN")) {
      channel = Comm[5];
      input = channel.toInt();
      val = analogRead(input);
      Serial.print(val);
      Serial.print("\n");
    }
    else if (Comm.startsWith("DI")){
      for(i = 0; i < 10; i++){
        digitalWrite(ledPin, HIGH);
        delay(300);
        digitalWrite(ledPin, LOW);
        delay(300);
      }
    }
    else {
      Serial.print("Command not known\n");
    }
    Comm = "";
  }
  delay(20);
}
