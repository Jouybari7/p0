void initMotorController()
{
    R = new SOLOMotorControllersCanopen(200, 9); 
    delay(1000);
    L = new SOLOMotorControllersCanopen(100, 9); 
    delay(1000);
//    Serial.println("\n Trying to Connect To SOLOs");
    delay(1000);
     while(R->CommunicationIsWorking() == false || L->CommunicationIsWorking() == false )
        {delay(500);}
//     Serial.println("\n Both Communications Established succuessfully!");
  R->SetOutputPwmFrequencyKhz(20);
  R->SetCurrentLimit(10.0);
  R->SetMotorPolesCounts(4);
  R->SetCommandMode(SOLOMotorControllers::CommandMode::digital);
  R->SetMotorType(SOLOMotorControllers::MotorType::bldcPmsm);
  R->SetFeedbackControlMode(SOLOMotorControllers::FeedbackControlMode::hallSensors);
  R->SetSpeedControllerKp(0.1199951);
  R->SetSpeedControllerKi(0.0049972);
  R->SetControlMode(SOLOMotorControllers::ControlMode::speedMode);
  
  L->SetOutputPwmFrequencyKhz(20);
  L->SetCurrentLimit(10.0);
  L->SetMotorPolesCounts(4);
  L->SetCommandMode(SOLOMotorControllers::CommandMode::digital);
  L->SetMotorType(SOLOMotorControllers::MotorType::bldcPmsm);
  L->SetFeedbackControlMode(SOLOMotorControllers::FeedbackControlMode::hallSensors);
  L->SetSpeedControllerKp(0.1199951);
  L->SetSpeedControllerKi(0.0049972);
  L->SetControlMode(SOLOMotorControllers::ControlMode::speedMode);
  R->MotorParametersIdentification(SOLOMotorControllers::Action::start);
  delay(2000);
  L->MotorParametersIdentification(SOLOMotorControllers::Action::start);
  delay(2000);
  }

  void setMotorSpeed(int i, int spd) {
    unsigned char reverse = 0;
    unsigned int spd2=0;
    
    if (spd < -255)
        spd = -255;

    if (spd > 255)
        spd = 255;
      
    if (spd < 0)
    {
      spd = -spd;
      reverse = 1;
    }

    if(spd!=0){  
    spd2=map(spd,0, 255, 300, 3000);}
    
    if (i == LEFT) { 
      if      (reverse == 0) { L->SetMotorDirection(SOLOMotorControllers::Direction::counterclockwise);L->SetSpeedReference(spd2);}
      else if (reverse == 1) { L->SetMotorDirection(SOLOMotorControllers::Direction::clockwise);L->SetSpeedReference(spd2);}
    }
    else /*if (i == RIGHT) //no need for condition*/ {
      if      (reverse == 0) {R->SetMotorDirection(SOLOMotorControllers::Direction::clockwise);R->SetSpeedReference(spd2);}
      else if (reverse == 1) {R->SetMotorDirection(SOLOMotorControllers::Direction::counterclockwise);R->SetSpeedReference(spd2);}
    }
  }



  void setMotorSpeeds(int leftSpeed, int rightSpeed) {
    setMotorSpeed(LEFT, leftSpeed);
    setMotorSpeed(RIGHT, rightSpeed);
  }
