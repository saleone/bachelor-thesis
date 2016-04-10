#ifndef StepperImproved_h
#define StepperImproved_h

class StepperImproved {
    public:

        // Constructor for 4 coil steppers.
        StepperImproved(int steps_number, short pin1, short pin2, short pin3, short pin4);  
        
        // Set Stepper position.
        void write(short angle); 
        
        // Defines movement speed in degrees per second.
        void setSpeed(double speed);

    private:

        // Number of steps per full revolution.
        int rev_steps;
        
        // Current angle position of the motor.
        short position;         

        // Pins for stepping.
        short pin1;
        short pin2;
        short pin3;
        short pin4;

        // Number of pins.
        short pinCount;

        // Steps per degree ratio.
        double ratio;

        // Direction to step in true:clockwise, false:counter-clockwise.
        bool cw;

        // Delay between steps in miliseconds.
        int delay;

        // Last time we moved a step.
        unsigned long last_step_time;

        // Coil which was activated last.
        short last_coil;
}

#endif
