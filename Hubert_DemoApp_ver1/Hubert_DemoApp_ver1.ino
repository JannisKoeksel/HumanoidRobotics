
// #include <Arduino.h>
// #include <Servo.h>

// //Servos
// Servo body;
// Servo headPan;
// Servo headTilt;
// Servo shoulder;
// Servo elbow;
// Servo gripper;

// //Init position of all servos
// const int servo_pins[] = {3, 5, 6, 9, 10, 11};

// const int pos_init[] = {1700, 1500, 2000, 2127.5, 1485, 1600}; // E: 1650, S: 2200
// int curr_pos[6];
// int new_servo_val[6];
// int new_pos[] = {1700, 1500, 2000, 2127.5, 1485, 1600};

// const int pos_min[] = {560, 550, 950, 750, 550, 550};
// const int pos_max[] = {2330, 2340, 2400, 2200, 2400, 2150};

// const int pos_move[] = {2200, 1000, 1500, 1100, 2300, 1600};

// char body_parts[] = {'B','P', 'T', 'S', 'E', 'G'};

// int dv = 80;

// void servo_body_ex() {

//   int diff, steps, now, CurrPwm, NewPwm, delta = 6;

//   //current servo value
//   now = curr_pos[0];
//   CurrPwm = now;
//   NewPwm = new_pos[0];

//   /* determine interation "diff" from old to new position */
//   diff = (NewPwm - CurrPwm)/abs(NewPwm - CurrPwm); // Should return +1 if NewPwm is bigger than CurrPwm, -1 otherwise.
//   steps = abs(NewPwm - CurrPwm);
  

//   now = now + 1.5*diff;
//   body.writeMicroseconds(now);

//   curr_pos[0] = now;
// }

// void servo_neck_pan() {

//   int diff, steps, now, CurrPwm, NewPwm, delta = 6;

//   //current servo value
//   now = curr_pos[1];
//   CurrPwm = now;
//   NewPwm = new_pos[1];

//   /* determine interation "diff" from old to new position */
//   diff = (NewPwm - CurrPwm)/abs(NewPwm - CurrPwm); // Should return +1 if NewPwm is bigger than CurrPwm, -1 otherwise.
//   steps = abs(NewPwm - CurrPwm);


//   now = now + 1.5*diff;
//   headPan.writeMicroseconds(now);

//   curr_pos[1] = now;
// }

// void servo_neck_tilt() {

//   int diff, steps, now, CurrPwm, NewPwm, delta = 6;

//   //current servo value
//   now = curr_pos[2];
//   CurrPwm = now;
//   NewPwm = new_pos[2];

//   /* determine interation "diff" from old to new position */
//   diff = (NewPwm - CurrPwm)/abs(NewPwm - CurrPwm); // Should return +1 if NewPwm is bigger than CurrPwm, -1 otherwise.
//   steps = abs(NewPwm - CurrPwm);


//   now = now + 1.5*diff;
//   headTilt.writeMicroseconds(now);

//   curr_pos[2] = now;
// }

// void servo_shoulder() {

//   int diff, steps, now, CurrPwm, NewPwm, delta = 6;

//   //current servo value
//   now = curr_pos[3];
//   CurrPwm = now;
//   NewPwm = new_pos[3];

//   /* determine interation "diff" from old to new position */
//   diff = (NewPwm - CurrPwm)/abs(NewPwm - CurrPwm); // Should return +1 if NewPwm is bigger than CurrPwm, -1 otherwise.
//   steps = abs(NewPwm - CurrPwm);


//   now = now + 1.5*diff;
//   shoulder.writeMicroseconds(now);

//   curr_pos[3] = now;
// }

// void servo_elbow() {

//   int diff, steps, now, CurrPwm, NewPwm, delta = 6;

//   //current servo value
//   now = curr_pos[4];
//   CurrPwm = now;
//   NewPwm = new_pos[4];

//   /* determine interation "diff" from old to new position */
//   diff = (NewPwm - CurrPwm)/abs(NewPwm - CurrPwm); // Should return +1 if NewPwm is bigger than CurrPwm, -1 otherwise.
//   steps = abs(NewPwm - CurrPwm);


//   now = now + 1.5*diff;
//   elbow.writeMicroseconds(now);

//   curr_pos[4] = now;
// }

// void servo_gripper_ex() {

//   int diff, steps, now, CurrPwm, NewPwm, delta = 6;

//   //current servo value
//   now = curr_pos[5];
//   CurrPwm = now;
//   NewPwm = new_pos[5];

//   /* determine interation "diff" from old to new position */
//   diff = (NewPwm - CurrPwm)/abs(NewPwm - CurrPwm); // Should return +1 if NewPwm is bigger than CurrPwm, -1 otherwise.
//   steps = abs(NewPwm - CurrPwm);


//   now = now + 1.5*diff;
//   gripper.writeMicroseconds(now);

//   curr_pos[5] = now;
// }

// void setup() {

//   Serial.begin(57600); // Starts the serial communication

// 	//Attach each joint servo and write each init position
//   body.attach(servo_pins[0]);
//   body.writeMicroseconds(pos_init[0]);
  
//   headPan.attach(servo_pins[1]);
//   headPan.writeMicroseconds(pos_init[1]);
  
//   headTilt.attach(servo_pins[2]);
//   headTilt.writeMicroseconds(pos_init[2]);

//   shoulder.attach(servo_pins[3]);
// 	shoulder.writeMicroseconds(pos_init[3]);

// 	elbow.attach(servo_pins[4]);
// 	elbow.writeMicroseconds(pos_init[4]);
	
// 	gripper.attach(servo_pins[5]);
//   gripper.writeMicroseconds(pos_init[5]);

//   //Initilize curr_pos and new_servo_val vectors
//   byte i;
//   for (i=0; i<(sizeof(pos_init)/sizeof(int)); i++){
//     curr_pos[i] = pos_init[i];
//     new_servo_val[i] = curr_pos[i];
//   }

// 	delay(2000);
// }

// void move_to_init() {
//   // new_pos[6] = pos_init[6];
//   new_pos[0] = pos_init[0];
//   new_pos[1] = pos_init[1];
//   new_pos[2] = pos_init[2];
//   new_pos[3] = pos_init[3];
//   new_pos[4] = pos_init[4];
//   new_pos[5] = pos_init[5];
// }

// void shoot() {
//   new_pos[3] = 1990.0; // servo_shoulder(1990);
//   delay(dv);
//   new_pos[4] = 2217.0; // servo_elbow(2217);
//   delay(dv);
//   new_pos[5] = 1800.0; // servo_gripper_ex(1800); // change depending on laser pointer
//   delay(dv);
// }

// void move_one(const char X, const int position) {
//   if (X == 'B') { new_pos[0] = position; }
//   else if (X == 'P') { new_pos[1] = position; } 
//   else if (X == 'T') { new_pos[2] = position; } 
//   else if (X == 'S') { new_pos[3] = position; }
//   else if (X == 'E') { new_pos[4] = position; }
//   else if (X == 'G') { new_pos[5] = position; }
// }

// void loop() {
  
//   // if (Serial.available() > 0) {
//     String full_command = String("");
//     while (Serial.available() > 0)
//     {
//       String command = Serial.readStringUntil('\n');
//       full_command += String(command);
//       delay(10);
//     }
    
//     if(full_command.length() > 0){
//       char servo = full_command.charAt(0);
//       full_command.remove(0);
//       int position = full_command.toInt();
//       if (strchr(body_parts, servo)) { move_one(servo, position); }

//     }
//     // String command = Serial.readString();
    
//     // int position = Serial.parseInt();

//     String out = "";
//     for(int i = 0 ; i < 6; i++ ){
//       out.concat(String(new_pos[i]));
//       out.concat(" ");
//     }
//     Serial.println(out);
//     // Serial.println(full_command);
//   // }
//   if(new_pos[0] != curr_pos[0]){ servo_body_ex(); }
//   if(new_pos[1] != curr_pos[1]){ servo_neck_pan(); }
//   if(new_pos[2] != curr_pos[2]){ servo_neck_tilt(); }
//   if(new_pos[3] != curr_pos[3]){ servo_shoulder(); }
//   if(new_pos[4] != curr_pos[4]){ servo_elbow(); }
//   if(new_pos[5] != curr_pos[5]){ servo_gripper_ex(); }
 
//     // else if (command == 'q') { move_to_init(); }
//     // else if (command == 's') { shoot(); }
//     // // else if (command == 'i') { idle_behaviour(70); }
//     // else if (command == 'i') { idle_beha(position); }

  
// }

