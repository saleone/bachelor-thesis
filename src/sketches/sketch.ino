#include <CheapStepper.h>

CheapStepper stepper1(10, 11, 12, 13);
CheapStepper stepper2(6, 7, 8, 9);
CheapStepper stepper3(2, 3, 4, 5);

// Rotation on the shoulder joint
int shoulderAngle = 0;

// Lift of the arm (angle from the shoulder rotation plane)
int armAngle = 0;

// Rotation of the elbow joint
int elbowAngle = 0;

// Do we have a complete command:
//     B is for begin, so we just began getting the command
//     F is for finished, we have all values for command
//
// !!!
// Be carefull when setting these constants as they can interfere
// with angle specifiers (SHOULDER, ARM and ELBOW)
// !!!
#define BEGIN_COMMAND_FLAG 'B'
#define END_COMMAND_FLAG 'F'
char haveCommand = 'B';

// Used to help parseCommand determine which angle to set.
#define SHOULDER 'S'
#define ARM 'A'
#define ELBOW 'E'
char angleSpecifier = SHOULDER;

void setup()
{
  stepper1.setRpm(15);
  stepper2.setRpm(15);
  stepper1.setRpm(15);

  Serial.begin(9600);
  Serial.println("Initialized. Starting...");
}

void loop()
{
  stepper1.run();
  stepper2.run();
  stepper3.run();

  // only change values for angles when we have a complete command
  if (haveCommand != 'F')
    return;

  Serial.print("Moving shoulder to: ");
  Serial.println(shoulderAngle);

  Serial.print("Moving arm to: ");
  Serial.println(armAngle);

  Serial.print("Moving elbow to: ");
  Serial.println(elbowAngle);

  haveCommand = 'I';
}

// Handle data on the serial connection
void serialEvent()
{
  while (Serial.available())
  {
    char input = (char)Serial.read();

    Serial.print("Received character: ");
    Serial.print(input);
    Serial.print(" -> ");
    Serial.println((int)input);

    if (input == BEGIN_COMMAND_FLAG || input == END_COMMAND_FLAG)
    {
      Serial.println("Changing command flag to input.");
      haveCommand = input;
    }
    else if (input == SHOULDER || input == ARM || input == ELBOW)
    {
      Serial.println("Changing angle specifier to input.");
      angleSpecifier = input;
    }
    else if ((int)input >= 48 && (int)input <= 57)
    {
      Serial.print("Setting angle value for ");
      Serial.println(angleSpecifier);
      writeAngle((int)input);
    }
  }
}

// Parse the command string and fill angle values
void writeAngle(int digit)
{
  if (angleSpecifier == SHOULDER)
  {
    Serial.print(" from ");
    Serial.print(shoulderAngle);
    Serial.print(" to ");
    shoulderAngle = calculateAngle(shoulderAngle, digit);
    Serial.println(shoulderAngle);
  }
  else if (angleSpecifier == ARM)
  {
    Serial.print(" from ");
    Serial.print(armAngle);
    Serial.print(" to ");
    armAngle = calculateAngle(armAngle, digit);
    Serial.println(armAngle);
  }
  else if (angleSpecifier == ELBOW)
  {
    Serial.print(" from ");
    Serial.print(elbowAngle);
    Serial.print(" to ");
    elbowAngle = calculateAngle(elbowAngle, digit);
    Serial.println(elbowAngle);
  }
}

// Calculate angle based on previous value and new digit.
int calculateAngle(int value, int digit)
{
  digit = digit - 48;

  value = value * 10 + digit;

  if (value >= 360)
    value = digit;

  return value;
}
