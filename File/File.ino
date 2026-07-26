float MS = 1;
float SEC = 1000;
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
        digitalWrite(pin, HIGH);

    }

    void off(){
        lastState = state;
        state = false;
        digitalWrite(pin, LOW);
    }

    void toggle(){
        lastState = state;
        if (state){
            state = false;
            digitalWrite(pin, LOW);
        }
        else{
            state = true;
            digitalWrite(pin, HIGH);
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
    bool last = false;
    Button(byte pin){
        this->pin = pin;
        pinMode(this->pin, INPUT_PULLUP);
    }

    bool read(){
        bool reading = digitalRead(pin)==LOW;
		
		if (reading){
            last = true;
			return (true);
		}

        if (!reading){
            last = false;
        }
		return (false);


        
    }
    bool update(){return(read());}
};
#define A0 A0
#define A1 A1
#define A2 A2
#define A3 A3
#define A4 A4
#define A5 A5
#define A6 A6
#define A7 A7
#define SDA A4
#define SCL A5


Led l(8);
Button b(4 );
void h(bool e ){
l.toggle();
}
// void wait(unsigned long time, float unit){
// 	unsigned long end = millis() + (time*unit);

// 	while (millis() < end)
// 	{
// 		if (b.update() == true){
// h(true);
// }
// 		l.update();

// 	}
// }
// void setup(){ 


// //SetBoard

// }

// void loop() {

// if (b.update() == true){
// h(true);
// }
// l.update();
// }
// void setup() {
//     pinMode(3, OUTPUT);
//     pinMode(4, INPUT_PULLUP);
// }

// void loop() {
//     digitalWrite(3, digitalRead(4) == LOW);
// }
void setup() {
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
    digitalWrite(LED_BUILTIN, HIGH);
}


















