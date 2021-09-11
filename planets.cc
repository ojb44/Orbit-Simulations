//planets.cc
//Single planet moving in an arbitrary central potential in 2 dimensions

#include <iostream>
#include <cmath>
#include <fstream>
using namespace std;

#define dt 0.001
#define n -2   //parameter for the force law r^n
#define k -1   //proportionality constant for force law k*r^n*e_r, negative for attractive (e_r is unit vector in radial direction)
#define mass 1    //mass of the planets

// class to deal with the vectors for position, velocity, acceleration etc.
class vec2d{ 
    public:
    float x;
    float y;

    vec2d(){
        x=0.0; y=0.0;
    }

    vec2d(float a, float b){
        x=a; y=b;
    }

    friend ostream &operator<<(ostream &os, vec2d const &v) { 
        return os << v.x << " " << v.y;
    }

    vec2d operator+ (const vec2d &v) const {
        return vec2d(x+v.x, y+v.y);
    }

    vec2d operator* (const float &a) const {
        return vec2d(x*a, y*a);
    }

    float mag();
};

//class for the planet

class planet{
    public:
    vec2d position;
    vec2d velocity;

    planet(vec2d pos, vec2d vel){
        position = pos;
        velocity = vel;
    }

    //functions associated with the planet
    void showState();
    float squareDist();
    vec2d accel();
    void PositionStep(float timeStep);
    void VelocityStep(float timeStep);
    float energy();
    float angMom();
    void Leapfrog(int steps, float timeStep);
    void simulate(int steps, float timeStep, int stepsPerWrite, string simName, string fileName);
    void openStateFile(string name);
    void closeStateFile(string name);
    void writeState(float time);
    void Verlet(int steps, float timeStep);
    void impulse(vec2d imp);
};


int main(){
    vec2d pos(1,0);
    vec2d vel(0,1);

    planet Mercury(pos,vel);
    planet Venus(pos,vel);
    planet Earth(pos,vel);
    planet Mars(pos,vel);
    planet Jupiter(pos,vel);
    
    ofstream fout;
    fout.open("mercury.dat", ofstream::trunc);  //clears the output file
    fout.open("venus.dat", ofstream::trunc);
    fout.open("earth.dat", ofstream::trunc);
    fout.open("mars.dat", ofstream::trunc);
    fout.open("jupiter.dat", ofstream::trunc);
    fout.close();


    /*cout<<"Energy: "<<Uranus.energy()<<endl;
    cout<<"L: "<<Uranus.angMom()<<endl;
    Uranus.simulate(10000,dt,1,1);
    cout<<"Energy: "<<Uranus.energy()<<endl;
    cout<<"L: "<<Uranus.angMom()<<endl;*/
    //plot 'planetOutput.dat' u 4:5:6 with l palette

    
    vec2d imp1(pos*(0.1));
    vec2d imp2(pos*(-0.1));
    vec2d imp3(vel*0.1);
    vec2d imp4(vel*(-0.1));


    Mercury.simulate(10000,dt,1,"mercury", "mercury.dat");   // add setting so that it can be plotted as different colour after the impulse
    Venus.impulse(imp1);
    Venus.simulate(10000,dt,1,"venus", "venus.dat");
    Earth.impulse(imp2);
    Earth.simulate(10000,dt,1,"earth", "earth.dat");
    Mars.impulse(imp3);
    Mars.simulate(10000,dt,1,"mars","mars.dat");
    Jupiter.impulse(imp4);
    Jupiter.simulate(10000,dt,1,"jupiter","jupiter.dat");

}

//computes magnitude of the vector
float vec2d::mag(){
    float m = sqrt(x*x+y*y);
    return m;
}
//prints the state of the planet
void planet::showState(){
    cout<<"Position: "<<position<<" Velocity: "<<velocity;
}
//gives square distance from the origin
float planet::squareDist(){
    float dsqu = position.x*position.x+position.y*position.y;
    return dsqu;
}
//returns acceleration of the planet
vec2d planet::accel(){
    float dist = position.mag();
    float a = k*pow(dist, n-1); //n-1 because one power is included in the position itself
    return position*a;
}
//updates position by one step
void planet::PositionStep(float timeStep){
    position = position + velocity*timeStep;
}
//updates velocity by one step
void planet::VelocityStep(float timeStep){
    velocity = velocity + accel()*timeStep;
}
//gives the energy of the planet
float planet::energy(){
    float ke=0.5*mass*pow(velocity.mag(),2);
    float pe=k*mass/position.mag(); //note this currently only works for the inverse square law!
    return ke+pe;
}

//angular momentum about the origin
float planet::angMom(){
    float L = position.x*velocity.y-position.y*velocity.x;
    return L;
}

//leapfrog update
void planet::Leapfrog(int steps, float timeStep){
    for (int i=0; i<steps; i++){
        PositionStep(timeStep/2);
        VelocityStep(timeStep);
        PositionStep(timeStep/2);
    }
}

//verlet update
void planet::Verlet(int steps, float timeStep){
    vec2d init_accel;
    for (int i=0; i<steps; i++){
        init_accel=accel();
        position=position+velocity*dt+init_accel*0.5*dt*dt;
        velocity=velocity+(init_accel+accel())*0.5*dt;
    }
}

//function to open the file (so don't re-open for every write)
/*void planet::openStateFile(string name){
    ofstream fout;
    fout.open(name);
}

void planet::closeStateFile(string name){
    fout.close();
}

//function to write state to the file (must be already open)
void planet::writeState(float time){
    
}*/

//simulate function, repeatedly updates position of planet and writes to file with columns time, x, y, vx, vy
void planet::simulate(int steps, float timeStep, int stepsPerWrite, string simName, string fileName){
    ofstream fout;
    fout.open(fileName, ofstream::trunc);

    float time=0;

    for (int j=0;j<steps;j++){
        fout<<time<<"\t"<<position.x<<"\t"<<position.y<<"\t"<<velocity.x<<"\t"<<velocity.y<<"\t"<<simName<<"\n";
        Verlet(stepsPerWrite, timeStep);
        time+=timeStep;
    }

    cout<<"Simulation done"<<endl;
    fout.close();
}

//apply an impulse to the planet
void planet::impulse(vec2d imp){
    velocity=velocity + imp*(1/mass);
}
