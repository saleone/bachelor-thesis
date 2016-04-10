#fndef StepperImproved_h
#define StepperImproved_h

class StepperImproved {
    public:

        // Constructor for 4 coil steppers.
        StepperImproved(int steps_number, int pin1, int pin2, int pin3, int pin4);  
        
        // Set Stepper position.
        void write(int angle); 
        
        // Defines movement speed in degrees per second.
        void setSpeed(double speed);

    private:
        
        // Current angle position of the motor.
        int position;         

        // Pins for stepping.
        int pin1;
        int pin2;
        int pin3;
        int pin4;

        // Number of pins.
        int pinCount;

        // Steps per degree ratio.
        double ratio;

        // Direction to step in true:clockwise, false:counter-clockwise.
        bool cw;

        // Delay between steps in miliseconds.
        int delay;

        // Last time we moved a step.
        unsigned long last_step_time;
}

#endif
