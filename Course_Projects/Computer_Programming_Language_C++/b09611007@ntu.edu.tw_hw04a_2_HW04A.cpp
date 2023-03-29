
//================================================================
//  PROGRAMMER :B09611007
//  DATE       : 2020-11-15
//  FILENAME   : HW04AB09611007.CPP 
//  DESCRIPTION: This is a program to find the largest perfect number less than 10000 .
//================================================================

#include <iostream>
using namespace std;

int answer1;   // Store the largest perfect number less than 10000 in this global variable
int sum=0;  // Store the sum of all its factors excluding itself

void PerfectNumber(long int Num) ;

int main() 
{
  for(int t=1;t<10000;t++)
  {
    PerfectNumber(t);
  }
  cout<<"The largest perfect number less than 10000 is "<<answer1;
}

void PerfectNumber(long int Num)   // Examine whether Num is a perfect number. If Num is a perfect number, store Num into answer1
{
  sum=0;   // initialize sum 
  for(int i=1 ; i < Num ; i++)  // calculate the sum of all its factors excluding itself
  {
    if(Num%i==0)
    {
      sum+=i;  // add sum by i if i is a factor of Num
    }
  }
  if(sum==Num)  // if the sum is equal to Num, Num is a perfect number
  {
    answer1=Num;
  }
}