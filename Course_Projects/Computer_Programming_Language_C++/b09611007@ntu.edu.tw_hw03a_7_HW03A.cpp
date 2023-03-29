//=================================================================
//  PROGRAMMER : B09611007
//  DATE       : 2020-10-28
//  FILENAME   : HW03AB09611007.CPP 
//  DESCRIPTION: This is a program to calculate an arithmetic series and get the error that should be less then 1.0*10^3
//=================================================================
#include <iostream>
#include <math.h>

using namespace std;

double answer1; // Store the smallest value of n that makes the error less than 1.0×10-3
int i; //normal value

//write Fibonacci number
int a(int i)
{
    if(i == 1 || i == 2)
    {
        return 1;
    }
    else if (i >= 3)
    {
        return a(i - 1) + a(i - 2);
    }
    else
    return -1;
}

//calculate the answer
int main()
{
    double total = 0;
    double error;
    while(total <= 1.999)
    {
        i = i + 1;
        total = total + a(i) * pow(0.5, i);
        error = 2 - total;
    }
    answer1 = i;
  cout << i<<'\n'<<error;
  
}








