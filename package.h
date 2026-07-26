#include <Arduino.h>
#include <Servo.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>


const String PLACE_HOLDER = " ";


float MS = 1;
float SEC = 1000;
float US = 0.001;

const float NOTE_C1 = 32.70;
const float NOTE_CS1 = 34.65;
const float NOTE_DF1 = NOTE_CS1;
const float NOTE_D1 = 36.71;
const float NOTE_DS1 = 38.89;
const float NOTE_EF1 = NOTE_DS1;
const float NOTE_E1 = 41.20;
const float NOTE_F1 = 43.65;
const float NOTE_FS1 = 46.25;
const float NOTE_GF1 = NOTE_FS1;
const float NOTE_G1 = 49.00;
const float NOTE_GS1 = 51.91;
const float NOTE_AF1 = NOTE_GS1;
const float NOTE_A1 = 55.00;
const float NOTE_AS1 = 58.27;
const float NOTE_BF1 = NOTE_AS1;
const float NOTE_B1 = 61.74;
const float NOTE_C2 = 65.41;
const float NOTE_CS2 = 69.30;
const float NOTE_DF2 = NOTE_CS2;
const float NOTE_D2 = 73.42;
const float NOTE_DS2 = 77.78;
const float NOTE_EF2 = NOTE_DS2;
const float NOTE_E2 = 82.41;
const float NOTE_F2 = 87.31;
const float NOTE_FS2 = 92.50;
const float NOTE_GF2 = NOTE_FS2;
const float NOTE_G2 = 98.00;
const float NOTE_GS2 = 103.83;
const float NOTE_AF2 = NOTE_GS2;
const float NOTE_A2 = 110.00;
const float NOTE_AS2 = 116.54;
const float NOTE_BF2 = NOTE_AS2;
const float NOTE_B2 = 123.47;
const float NOTE_C3 = 130.81;
const float NOTE_CS3 = 138.59;
const float NOTE_DF3 = NOTE_CS3;
const float NOTE_D3 = 146.83;
const float NOTE_DS3 = 155.56;
const float NOTE_EF3 = NOTE_DS3;
const float NOTE_E3 = 164.81;
const float NOTE_F3 = 174.61;
const float NOTE_FS3 = 185.00;
const float NOTE_GF3 = NOTE_FS3;
const float NOTE_G3 = 196.00;
const float NOTE_GS3 = 207.65;
const float NOTE_AF3 = NOTE_GS3;
const float NOTE_A3 = 220.00;
const float NOTE_AS3 = 233.08;
const float NOTE_BF3 = NOTE_AS3;
const float NOTE_B3 = 246.94;
const float NOTE_C4 = 261.63;
const float NOTE_CS4 = 277.18;
const float NOTE_DF4 = NOTE_CS4;
const float NOTE_D4 = 293.66;
const float NOTE_DS4 = 311.13;
const float NOTE_EF4 = NOTE_DS4;
const float NOTE_E4 = 329.63;
const float NOTE_F4 = 349.23;
const float NOTE_FS4 = 369.99;
const float NOTE_GF4 = NOTE_FS4;
const float NOTE_G4 = 392.00;
const float NOTE_GS4 = 415.30;
const float NOTE_AF4 = NOTE_GS4;
const float NOTE_A4 = 440.00;
const float NOTE_AS4 = 466.16;
const float NOTE_BF4 = NOTE_AS4;
const float NOTE_B4 = 493.88;
const float NOTE_C5 = 523.25;
const float NOTE_CS5 = 554.37;
const float NOTE_DF5 = NOTE_CS5;
const float NOTE_D5 = 587.33;
const float NOTE_DS5 = 622.25;
const float NOTE_EF5 = NOTE_DS5;
const float NOTE_E5 = 659.26;
const float NOTE_F5 = 698.46;
const float NOTE_FS5 = 739.99;
const float NOTE_GF5 = NOTE_FS5;
const float NOTE_G5 = 783.99;
const float NOTE_GS5 = 830.61;
const float NOTE_AF5 = NOTE_GS5;
const float NOTE_A5 = 880.00;
const float NOTE_AS5 = 932.33;
const float NOTE_BF5 = NOTE_AS5;
const float NOTE_B5 = 987.77;
const float NOTE_C6 = 1046.50;
const float NOTE_CS6 = 1108.73;
const float NOTE_DF6 = NOTE_CS6;
const float NOTE_D6 = 1174.66;
const float NOTE_DS6 = 1244.51;
const float NOTE_EF6 = NOTE_DS6;
const float NOTE_E6 = 1318.51;
const float NOTE_F6 = 1396.91;
const float NOTE_FS6 = 1479.98;
const float NOTE_GF6 = NOTE_FS6;
const float NOTE_G6 = 1567.98;
const float NOTE_GS6 = 1661.22;
const float NOTE_AF6 = NOTE_GS6;
const float NOTE_A6 = 1760.00;
const float NOTE_AS6 = 1864.66;
const float NOTE_BF6 = NOTE_AS6;
const float NOTE_B6 = 1975.53;
const float NOTE_C7 = 2093.00;
const float NOTE_CS7 = 2217.46;
const float NOTE_DF7 = NOTE_CS7;
const float NOTE_D7 = 2349.32;
const float NOTE_DS7 = 2489.02;
const float NOTE_EF7 = NOTE_DS7;
const float NOTE_E7 = 2637.02;
const float NOTE_F7 = 2793.83;
const float NOTE_FS7 = 2959.96;
const float NOTE_GF7 = NOTE_FS7;
const float NOTE_G7 = 3135.96;
const float NOTE_GS7 = 3322.44;
const float NOTE_AF7 = NOTE_GS7;
const float NOTE_A7 = 3520.00;
const float NOTE_AS7 = 3729.31;
const float NOTE_BF7 = NOTE_AS7;
const float NOTE_B7 = 3951.07;
const float NOTE_C8 = 4186.01;

class RGB{
public:
    int r,g,b;
    RGB(int r, int g, int b){
        this->r = r;
        this->g = g;
        this->b = b;
    }

    String to_hash(int value){
        const char* digits = "0123456789ABCDEF";

        String s;
        s += digits[value / 16];
        s += digits[value % 16];

        return s;
    }
    
    String hash(){
        return ("#"+to_hash(r)+to_hash(g)+to_hash(b));
    }
};

//Classes

class Led{
public:
    byte pin;

    unsigned long interval;
    unsigned long times;

    bool is_blinking = false;
    bool is_fading = false;

    bool state = false;
    bool lastState = false;

    int lastFade;
    int step;

    unsigned long lastUpdate = 0;

    Led(byte pin){
        this->pin = pin;
        pinMode(pin, OUTPUT);
        digitalWrite(pin, LOW);
    }

    void on(){
        lastState = state;
        state = true;

    }

    void off(){
        lastState = state;
        state = false;
    }

    void toggle(){
        lastState = state;
        if (state){
            state = false;
        }
        else{
            state = true;
        }
    }

    bool returnState(){
        return state;
    }

    void blink(unsigned long speed, float unit = MS, unsigned long times = -1){
        this->interval = speed*unit;
        this->times = times;
        this->is_blinking = true;

    }

    void fade(unsigned long time, float unit = MS){
        this->is_fading = true;
        lastFade = 0;
        step = (time*unit)/255;

    }

    void update(){
        if (is_blinking){
            if (millis()-this->lastUpdate>=interval){
                if (times!=0){
                        lastUpdate = millis();
                        this->state = !state;
                        times--;
                }
                else{
                    is_blinking = false;
                }
            }
        }

        if (is_fading){
            if (millis()-lastUpdate>=step){
                lastUpdate = millis();
                lastFade++;
                if (lastFade>=255){
                    is_fading = false;
                }
                analogWrite(this->pin, lastFade);
            }
        }

        if (lastState != state){
            if (state){
                digitalWrite(this->pin, HIGH);
            }
            else{
                digitalWrite(this->pin, LOW);
            }
            lastState = state;
        }
    }



};

class Button{
public:
    byte pin;
    bool last;
    Button(byte pin){
        this->pin = pin;
        pinMode(this->pin, INPUT);
    }

   bool read(){
        bool reading = digitalRead(pin)==LOW;
        delay(1000);
        
        if (reading){
            last = reading;
            return (true);
        }
        
        last = reading;
        return (false);


        
    }
    bool update(){return(read());}

            
};

class RGBLed{
    public:
    byte pin1;
    byte pin2;
    byte pin3;

    unsigned long interval;
    unsigned long times;

    bool is_blinking = false;
    int blink1;
    int blink2;
    int blink3;

    bool is_fading = false;


    int state1;
    int state2;
    int state3;

    int lastState1;
    int lastState2;
    int lastState3;

    int lastFade1;
    int lastFade2;
    int lastFade3;

    int step;

    unsigned long lastUpdate = 0;

    RGBLed(byte p1, byte p2, byte p3){
        this->pin1 = p1;
        this->pin2 = p2;
        this->pin3 = p3;
        pinMode(pin1, OUTPUT);
        pinMode(pin2, OUTPUT);
        pinMode(pin3, OUTPUT);
        digitalWrite(pin1, LOW);
        digitalWrite(pin2, LOW);
        digitalWrite(pin3, LOW);
    }

    void set(int a, int b, int c){
        lastState1 = state1;
        lastState2 = state2;
        lastState3 = state3;

        state1 = (a*255)/100;
        state2 = (b*255)/100;
        state3 = (c*255)/100;

    }

    void off(){
        lastState1 = state1;
        lastState2 = state2;
        lastState3 = state3;

        state1 = 0;
        state2 = 0;
        state3 = 0;
    }

    RGB returnState(){
        return RGB(state1,state2,state3);
    }

    void blink(int r, int g, int b,unsigned long speed, float unit = MS, unsigned long times = -1){
        this->interval = speed*unit;
        this->times = times;
        this->is_blinking = true;
        this->blink1 = (r*255)/100;
        this->blink2 = (g*255)/100;
        this->blink3 = (b*255)/100;


    }

    void fade(unsigned long time, float unit = MS){
        this->is_fading = true;
        lastFade1 = 0;
        lastFade2 = 0;
        lastFade3 = 0;
        step = max(1UL, (unsigned long)((time * unit) / 255));

    }

    void update(){
        if (is_blinking){
            if (millis()-this->lastUpdate>=interval){
                if (times!=0){
                        lastUpdate = millis();
                        if (times%2==0){
                            this->state1=0;
                            this->state2=0;
                            this->state3=0;
                        }
                        else{
                            state1 = blink1;
                            state2 = blink2;
                            state3 = blink3;
                        }
                        times--;
                }
                else{
                    is_blinking = false;
                }
            }
        }

        if (is_fading){
            if (millis()-lastUpdate>=step){
                lastUpdate = millis();

                lastFade1++;
                lastFade2++;
                lastFade3++;

                if (lastFade1>=255||lastFade2>=255||lastFade3>=255){
                    is_fading = false;
                }

                state1 = lastFade1;
                state2 = lastFade2;
                state3 = lastFade3;
                
            }
        }

        if (lastState1 != state1||lastState2 != state2||lastState3 != state3){
            analogWrite(this->pin1, state1);
            analogWrite(this->pin2, state2);
            analogWrite(this->pin3, state3);
            
            lastState1 = state1;
            lastState2 = state2;
            lastState3 = state3;
        }
    }
};

class ActiveBuzzer{
public:
    byte pin;
    bool state;

    ActiveBuzzer(byte pin){
        this->pin = pin;
        pinMode(pin, OUTPUT);
    }

    void on(){digitalWrite(this->pin, HIGH);state=true;}
    void off(){digitalWrite(this->pin, LOW);state=false;}
    void toggle(){
        if (state){
            digitalWrite(pin, LOW); state = false;
        }
        else{
            digitalWrite(pin, HIGH); state = true;
        }
    }

    bool return_state(){return (state);}

};

class PassiveBuzzer{
public:
    byte pin;
    float state;
    PassiveBuzzer(byte pin){
        this->pin = pin;
        pinMode(pin, OUTPUT);
    }
    void write(float frequency, float time = 1, float unit = SEC){
        tone(pin, frequency);
        delay(time*unit);
        noTone(pin);
    }

    void write_note(float frequency = 0, float time = 1, float unit = SEC){
        tone(pin, frequency);
        delay(time*unit);
        noTone(pin);
    }
};

class ServoMotor{
public:
    Servo pin;
    int state;
    int is_moving;
    int current_moving_angle;
    int angle;
    int step;
    unsigned long  last_step;
    ServoMotor(byte pin){
        this->pin.attach(pin);
        this->pin.write(0);
    }

    void write(int angle){
        state=angle;
        this->pin.write(angle);
    }

    int return_state(){
        return (state);
    }

    void move_smooth(int angle, unsigned long speed, float unit = MS){
        step = max(1UL, (unsigned long)((speed * unit) / 180));
        this->angle = angle;
        is_moving = true;

    }

    void update(){
        if (is_moving){
            if (millis()-last_step>=step){
                last_step = millis();
                if (current_moving_angle < angle){
                            current_moving_angle++;
                }
                else if (current_moving_angle > angle){
                    current_moving_angle--;
                }
                else{
                    is_moving = false;
                }
                if (current_moving_angle>=angle){
                    is_moving = false;
                }
                pin.write(current_moving_angle);
            }
        }
    }
};

struct Message{
    String str;
    bool importance;
};
class I2C_LCD_Display{
public:
    LiquidCrystal_I2C dis;
    int width;
    Message messages[80];
    byte message_count = 0;
    bool is_scrolling;
    unsigned long interval;
    unsigned long lastUpdate;
    int position = 0;
    String current;
    String place;
    String savedCurrent;
    int savedPosition;
    bool interrupted = false;


    I2C_LCD_Display(int sda, int scl, int width, int height, int address = 0x27):dis(address, width,height){
        Wire.begin();
        dis.init();
        dis.backlight();
        this->width = width;
        this->place = "";

        for (int i = 0; i < width; i++)
        {
            this->place += ' ';
        }
    }

    void set_cursor(int x, int y){
        dis.setCursor(x,y);
    }

    void write(String str){
        dis.print(str);
    }

    void scroll_text(String str, unsigned long dely, float unit=MS){
        String string="                   "+str+"                   ";
        int newl=string.length();
        for(int i=0; i<newl-width; i++){
            String need= string.substring(i,i+width);
            dis.clear();
            dis.print(need);
            delay(dely*MS);
        }
    }

    void scroll_with_millis(const String str, unsigned long delay, float unit = MS){
        is_scrolling = true;
        interval = delay*unit;
        add(str, 0);
        current = messages[0].str;
    }

    void add(String str, int importance=0){
        if (message_count>=80){
            return;
        }
        
        if (importance==0){
            addFront(str);
            message_count+=1;
        }

        else if (importance==1){
            addBack(place+str+place, false);
            message_count+=1;
        }

        else{
            savedCurrent = current;
            savedPosition = position;
            interrupted = true;

            current = place + str + place;
            position = 0;

            dis.clear();
            dis.setCursor(0,0);
            dis.print(current.substring(0, width));

            lastUpdate = millis();
            return;
        }
    }

    void addFront(String str){
        messages[message_count].str = str;
        messages[message_count].importance = false;
    }

    void addBack(String str, bool importance){
        for (int i = message_count; i>0; i--){
            messages[i] = messages[i-1];
        }
        messages[0].str = str;
        messages[0].importance = importance;
    }

    void popFront(){
        if (message_count==0){
            return;
        }
        for (int i = 0; i<message_count-1; i++){
            messages[i] = messages[i+1];
        }
        message_count--;
    }

    void update(){
        if (is_scrolling){
            if (millis()-lastUpdate>=interval){
                lastUpdate = millis();
                dis.clear();
                dis.setCursor(0,0);
                dis.print(current.substring(position, position+width));
                position++;
                if (position>=current.length()-width){
                    if (interrupted){
                        current= savedCurrent;
                        position = savedPosition;
                        
                        interrupted = false;
                    }
                    else {
                        popFront();
                        current = messages[0].str;
                        position = 0;
                    }
                }
            }
        }
    }


};
