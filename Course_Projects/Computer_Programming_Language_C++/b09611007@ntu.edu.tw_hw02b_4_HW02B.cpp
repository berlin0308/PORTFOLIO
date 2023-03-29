//=================================================================
//  PROGRAMMER : B09611007
//  DATE       : 2020-10-12
//  FILENAME   : HW02BB09611007.CPP 
//  DESCRIPTION: This is a program to encrypt a 4-digit integer.
//=================================================================

#include <iostream>
using namespace std;

int answer1,answer2,answer3,answer4,answer5=1;  // 4 digits of the encrypted integer   // answer5 represent if the input is valid
int p,a,b,c,d,e,f;

int main()
{
  cout<< "Please input a 4-digit integer : " ;
  cin>>p;  // input an unencrypted 4-digit integer
  if(p>999&&p<=9999) // if the input is valid
  {
    a=p/1000;  //the thousands place
    b=p/100-10*a; //the hundreds place
    c=p/10%10;  //the tens place
    d=p%10;  //the ones place
    
    a=(a+7)%10;
    b=(b+7)%10;
    c=(c+7)%10;
    d=(d+7)%10;  // plus them by 7 and get the ones place number to convert the digits 
    
    e=b;
    b=a;
    a=e;  // swap the first two digits
    
    f=d;
    d=c;
    c=f;  // swap the last two digits
    
    answer1=a;
    answer2=b;
    answer3=c;
    answer4=d;  // store the consequence of the encryption 
    
    cout<<"The encrypted message is "<<answer1<<answer2<<answer3<<answer4;  // output the encrypted number
    
  }
  else  
  answer5=0;  // if the input number is invalid
	
    return 0;
}
