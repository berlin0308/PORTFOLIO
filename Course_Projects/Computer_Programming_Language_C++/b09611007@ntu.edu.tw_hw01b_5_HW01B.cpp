
//=================================================================
//  PROGRAMMER : B09611007
//  DATE       : 2020-10-01
//  FILENAME   : HW01BB09611007.CPP 
//  DESCRIPTION: This is a program to calculate the sum and average of the three numbers.
//=================================================================



#include <iostream>
using namespace std;
double answer1, answer2; //the two answers, the sum and the average

int main()
{
    double a, b, c;   // the three numbers included
    cin >> a >> b >> c;  // input the three numbers
    answer1 = a + b + c;  // caculate the sum of the numbers
    answer2 =answer1 / 3;  // divide the sum by 3 to caculate the average
    return 0;

}