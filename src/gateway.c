#define sr Serial
#define A 65
#define B 66
#define C 67
#define D 68
#define E 69
#define F 70
#define G 71
#define H 72
#define I 73
#define J 74
#define K 75
#define L 76
#define M 77
#define N 78
#define O 79
#define P 80
int bufferofinps[64];

void setup() {
  sr.begin(9600); // opens sr port, sets data rate to 9600 bps
  for (int i=2; i<14; i++) {
     pinMode(i, OUTPUT); digitalWrite(i,LOW);
  }
  sr.println("Ready.");  
}

int hold() {
  bool inloop = true; while(inloop) {
  if (sr.available()) { int incomingByte = sr.read();return incomingByte;}}}



void loop() {
  int incomingByte = hold();
  if (incomingByte == 67) {
    int ticker = 0; bool go = true; int bufferofinps[64]; sr.println("Writing all future inputs (until C) to buffer..."); while (go) {
      int icc = hold(); if (icc != 67) { bufferofinps[ticker] = icc; ticker++; } else { go = false;} sr.println(bufferofinps[0]); }
   //comment out on non debug
      sr.println("Buffer: ");
    for (int i=0; i < ticker; i++) {
      sr.println(bufferofinps[i]);
    }

    
   //conditional code goes here
int execpin;
int dir = LOW;
switch(bufferofinps[0]) {
  case A:
    dir = HIGH;
    break;
  case B:
    dir = LOW;
    break;
  default:
    dir = LOW;
}

switch(bufferofinps[1]) {
  case D: execpin = 2; break;
  case E: execpin = 3; break;
  case F: execpin = 4; break;
  case G: execpin = 5; break;
  case H: execpin = 6; break;
  case I: execpin = 7; break;
  case J: execpin = 8; break;
  case K: execpin = 9; break;
  case L: execpin = 10; break;
  case M: execpin = 11; break;
  case N: execpin = 12; break;
  default: execpin = 13;
  /*
   C + Direction + Port + C
   CADC = turn port 2 ON
   CBDC = turn port 2 OFF
   CANC = turn port 12 ON
   CBNC = turn port 12 OFF
   */
}
sr.println(execpin);
digitalWrite(execpin, dir);

   //conditional code ends here
  }

}