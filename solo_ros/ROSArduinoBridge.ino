#include "SOLOMotorControllersCanopen.h" 
#include "commands.h"
#include "motor_driver.h"

#define BAUDRATE     57600
#define MAX_PWM        255

SOLOMotorControllers *R; 
SOLOMotorControllers *L;

/* Variable initialization */

// A pair of varibles to help parse serial commands (thanks Fergs)
int arg = 0;
int index = 0;

// Variable to hold an input character
char chr;

// Variable to hold the current single-character command
char cmd;

// Character arrays to hold the first and second arguments
char argv1[16];
char argv2[16];

// The arguments converted to integers
long arg1;
long arg2;

/* Clear the current command parameters */
void resetCommand() {
  cmd = NULL;
  memset(argv1, 0, sizeof(argv1));
  memset(argv2, 0, sizeof(argv2));
  arg1 = 0;
  arg2 = 0;
  arg = 0;
  index = 0;
}

/* Run a command.  Commands are defined in commands.h */
int runCommand() {
  int i = 0;
  char *p = argv1;
  char *str;
  int pid_args[4];
  arg1 = atoi(argv1);
  arg2 = atoi(argv2);
  
  switch(cmd) {
    
  case GET_BAUDRATE:
    Serial.println(BAUDRATE);
    break;
    
  case READ_ENCODERS:
    Serial.print(L->GetPositionCountsFeedback());
    Serial.print(" ");
    Serial.println(-R->GetPositionCountsFeedback());
    break;
    
  case RESET_ENCODERS:
    L->ResetPositionToZero();
    R->ResetPositionToZero();
    Serial.println("OK"); 
    break;
    
  case MOTOR_SPEEDS:
    setMotorSpeeds(arg1, arg2);
    Serial.println("OK"); 
    break;
  
  }
}

/* Setup function--runs once at startup. */
void setup() {
  
  Serial.begin(BAUDRATE);
  initMotorController();
  
}

/* Enter the main loop.  Read and parse input from the serial port
   and run any valid commands. Run a PID calculation at the target
   interval and check for auto-stop conditions.
*/
void loop() {
  while (Serial.available() > 0) {
    
    // Read the next character
    chr = Serial.read();

    // Terminate a command with a CR
    if (chr == 13) {
      if (arg == 1) argv1[index] = NULL;
      else if (arg == 2) argv2[index] = NULL;
      runCommand();
      resetCommand();
    }
    // Use spaces to delimit parts of the command
    else if (chr == ' ') {
      // Step through the arguments
      if (arg == 0) arg = 1;
      else if (arg == 1)  {
        argv1[index] = NULL;
        arg = 2;
        index = 0;
      }
      continue;
    }
    else {
      if (arg == 0) {
        // The first arg is the single-letter command
        cmd = chr;
      }
      else if (arg == 1) {
        // Subsequent arguments can be more than one character
        argv1[index] = chr;
        index++;
      }
      else if (arg == 2) {
        argv2[index] = chr;
        index++;
      }
    }
  }
  

}
