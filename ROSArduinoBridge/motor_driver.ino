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
  R->SetCommandMode(SOLOMotorControllers::CommandMode::DIGITAL);
  R->SetMotorType(SOLOMotorControllers::MotorType::BLDC_PMSM);
  R->SetFeedbackControlMode(SOLOMotorControllers::FeedbackControlMode::HALL_SENSORS);
  R->SetSpeedControllerKp(0.1199951);
  R->SetSpeedControllerKi(0.0049972);
  R->SetControlMode(SOLOMotorControllers::ControlMode::SPEED_MODE);
  
  L->SetOutputPwmFrequencyKhz(20);
  L->SetCurrentLimit(10.0);
  L->SetMotorPolesCounts(4);
  L->SetCommandMode(SOLOMotorControllers::CommandMode::DIGITAL);
  L->SetMotorType(SOLOMotorControllers::MotorType::BLDC_PMSM);
  L->SetFeedbackControlMode(SOLOMotorControllers::FeedbackControlMode::HALL_SENSORS);
  L->SetSpeedControllerKp(0.1199951);
  L->SetSpeedControllerKi(0.0049972);
  L->SetControlMode(SOLOMotorControllers::ControlMode::SPEED_MODE);
  R->MotorParametersIdentification(SOLOMotorControllers::Action::START);
  delay(2000);
  L->MotorParametersIdentification(SOLOMotorControllers::Action::START);
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
      if      (reverse == 0) { L->SetMotorDirection(SOLOMotorControllers::Direction::COUNTERCLOCKWISE);L->SetSpeedReference(spd2);}
      else if (reverse == 1) { L->SetMotorDirection(SOLOMotorControllers::Direction::CLOCKWISE);L->SetSpeedReference(spd2);}
    }
    else /*if (i == RIGHT) //no need for condition*/ {
      if      (reverse == 0) {R->SetMotorDirection(SOLOMotorControllers::Direction::CLOCKWISE);R->SetSpeedReference(spd2);}
      else if (reverse == 1) {R->SetMotorDirection(SOLOMotorControllers::Direction::COUNTERCLOCKWISE);R->SetSpeedReference(spd2);}
    }
  }



  void setMotorSpeeds(int leftSpeed, int rightSpeed) {
    setMotorSpeed(LEFT, leftSpeed);
    setMotorSpeed(RIGHT, rightSpeed);
  }
