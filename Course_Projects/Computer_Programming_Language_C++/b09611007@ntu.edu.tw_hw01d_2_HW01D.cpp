
//=================================================================
//  PROGRAMMER : B09611007
//  DATE       : 2020-10-01
//  FILENAME   : HW01DB09611007.CPP 
//  DESCRIPTION: Programming a mathematical formula to caculate the value of the maximum load in 1bs.
//=================================================================



#include <iostream>
using namespace std;

double answer1; // the value of the maximum load in 1bs

int main()
{
    int s=3000, d=96, c=2; // the stress, the moment arm, and one half of the height of the symmetricle beam
    double i=10.67;  // the rectangular moment
    answer1 = s * i / (d * c); // caculate the maximum load by the formula 
    cout<< answer1 << endl;  // output the answer -- the value of the maximum load in 1bs
    return 0;

}