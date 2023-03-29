#include <iostream>
using namespace std;
int answer1;
int main() 
{
  int b,r[4999], found=0, thelongest=0, deno;
  for(b=1;b<5000;b++)
  {
    int a=1;  // a is the fraction
    int t=0;  // t stands for times of the division
    r[0]=1;   // r array stands for the remainder
    int len=0;  // len stands for the length of the rucurring cycle
    while(1)  // under every circumstances
    {
      found=0;  // the recurring cycle hasn't been found
      t+=1;  
      a=(a*10)%b;  // the remainder of each division
      r[t]=a;  // store the remainder of each division
      if(r[t]==0)  
      break;    // pause if it doesn't have recurring cycle
      for(int i=0;i<t;i++) // check if there are same values of remainders from different part
      {
        if(r[i]==r[t])
        {
          found=1; // found==1 stands for the recurring cycle is found
          len=t-i; // the length of the recurring cycle
          break;  // break if the recurring cycle is found
        }
      }
      if(found==1)
       break;
    }
  
    if(len>thelongest)
    {
      thelongest=len;  // replace the longest length if there is a larger value of length
      deno=b;  // note the denominator if there is a larger value of length
    }
  }
  answer1=deno;  // store the denominator
  cout<<answer1<<' '<<thelongest;
}