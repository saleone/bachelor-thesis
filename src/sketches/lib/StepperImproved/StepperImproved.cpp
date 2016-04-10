#include "Arduino.h"
#include "StepperImproved.h"

/*
 * Constructor for 4 wire stepper motor.
 */
StepperImproved::StepperImproved (int steps_number, short pin1, short pin2, short pin3, short pin4) {
    this->rev_steps = steps_number; // Number of steps for one full revolution.
    this->position  = 0;            // Current angle position of Stepper.

    // Pins used for stepping.
    this->pin1 = pin1;
    this->pin2 = pin2;
    this->pin3 = pin3;
    this->pin4 = pin4;

    // Set stepping pins into output mode.
    pinMode(this->pin1, OUTPUT);
    pinMode(this->pin2, OUTPUT);
    pinMode(this->pin3, OUTPUT);
    pinMode(this->pin4, OUTPUT);

    // Number of pins.
    this->pinCount = 4;

    // Steps per degree ratio.
    this->ratio = this->rev_steps / 360;  

    // Last time we moved a step.
    this->last_step_time = 0; 

    // Last coil position we've been on.
    this->last_coil;
}

/*
 * Moves the stepper to specified angle position.
 */
void StepperImproved::write(short angle) {
    short angleDelta = this->position - angle;
    if (angleDelta > 0 && abs(angleDelta) <= 180) {
        // Step the motor in clockwise direction.
        this->cw = true;
    } else if (angleDelta < 0 && abs(angleDelta) > 180) {
        // Step the motor in counter clockwise direction.
        this->cw = false;
    } else {
        // angleDelta is 0.
        return;
    }
    
    // Steps to move.
    int steps = (int) (angleDelta * ratio);
    step(steps);

    // Update the position.
    this->position = angle;
}

/*
 * Generates pulses to step the motor.
 */
void StepperImproved::step(int steps) {
    // Move while we still have steps to move.
    while (steps > 0) { 
        unsigned long now = micros();

        if (this->cw) {
            this->last_coil += 1;
        } else {
            this->last_coil -= 1;
        }
        
        // Calculate which step to activate. 
        this->last_coil =  this->last_coil % 4;
        if (this->last_coil < 0) {
            this->last_coil += 4;
        } else if (this->last_coil > 3) {
            this->last_coil -= 4;
        }
        
        // Move only if we waited for the required delay.
        if (now - this->last_step_time >= this->delay)
        {
            switch(this->last_coil) {
                case 0:
                    digitalWrite(this->pin1, HIGH);
                    digitalWrite(this->pin2, LOW);
                    digitalWrite(this->pin3, LOW);
                    digitalWrite(this->pin4, LOW);
                    break;
                case 1:
                    digitalWrite(this->pin1, LOW);
                    digitalWrite(this->pin2, HIGH);
                    digitalWrite(this->pin3, LOW);
                    digitalWrite(this->pin4, LOW);
                    break;
                case 2:
                    digitalWrite(this->pin1, LOW);
                    digitalWrite(this->pin2, LOW);
                    digitalWrite(this->pin3, HIGH);
                    digitalWrite(this->pin4, LOW);
                    break;
                case 3:
                    digitalWrite(this->pin1, LOW);
                    digitalWrite(this->pin2, LOW);
                    digitalWrite(this->pin3, LOW);
                    digitalWrite(this->pin4, HIGH);
                    break;
            }
            steps--;

            // Last time we stepped.
            this->last_step_time = now;
        }
    }
    
}

