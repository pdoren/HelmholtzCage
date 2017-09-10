#include "Wire.h"
#include "I2Cdev.h"
#include "HMC5883L.h"

#define LED_PIN 13
#define MAG 0x55
#define ERR 0x21

HMC5883L mag;
char cmd;
int16_t mx, my, mz;
String error;

void setup() {

    Wire.begin();

    Serial.begin(38400);

    mag.initialize();

    // verify connection
    if(mag.testConnection())
    {
      error = "HMC5883L connection failed";
    }

    pinMode(LED_PIN, OUTPUT);
}

void loop() {
    // send data only when you receive data:
    if (Serial.available() > 0) {

      Serial.readBytes(&cmd, 1);

      if(cmd == MAG)
      {
        mag.getHeading(&mx, &my, &mz);
        Serial.print(mx); Serial.print(";");
        Serial.print(my); Serial.print(";");
        Serial.println(mz);

        digitalWrite(LED_PIN, true);
      }
      else if(cmd == ERR)
      {
        Serial.println(error);
        
        digitalWrite(LED_PIN, true);
      }
      else
      {
        digitalWrite(LED_PIN, false);
      }
    }
}
