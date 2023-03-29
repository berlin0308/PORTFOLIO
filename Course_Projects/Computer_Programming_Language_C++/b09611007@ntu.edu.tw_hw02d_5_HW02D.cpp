//=================================================================
//  PROGRAMMER : B09611007
//  DATE       : 2020-10-12
//  FILENAME   : HW02DB09611007.CPP 
//  DESCRIPTION: This is a program to calculate the total value of the hand, and the sum of the three cards.
//=================================================================

#include <iostream>
using namespace std;

int answer1,answer2,a,b,c;  // the total value and the sum  // the numbers of three cards

int main()
{
  cin>>a>>b>>c;  // input the numbers of three cards
  answer2=a+b+c;  // calculate the sum
  if(a>=11)
  a=10;
  if(b>=11)
  b=10;
  if(c>=11)
  c=10;
  if(a==1)
  a=11;
  if(b==1)
  b=11;
  if(c==1)
  c=11;      // set the ACE card to 11 points
  
  if(a!=11&&b!=11&&c!=11)
  answer1=a+b+c;   // the no-ACE situation
  
  else if(a==11&&b!=11&&c!=11)  // a is ACE but the others are not
  {
    if(a+b+c>21)
    answer1=a+b+c-10;  // if the total value exceeds 21, substrate it by 10 ( the ACE stands for 1 )
    else
    answer1=a+b+c;  // if the total value doesn’t exceed 21 ( the ACE remains 11 )
  }
  else if(a!=11&&b==11&&c!=11)  // b is ACE but the others are not
  {
    if(a+b+c>21)
    answer1=a+b+c-10;
    else
    answer1=a+b+c;
  }
  else if(a!=11&&b!=11&&c==11)  // c is ACE but the others are not
  {
    if(a+b+c>21)
    answer1=a+b+c-10;
    else
    answer1=a+b+c;
  }
  
  
  else if(a==11&&b==11&&c!=11)  // a and b are ACEs but c isn’t 
  {
    if(a+b+c>31)
    answer1=a+b+c-20;  // if the total value exceeds 31, substrate it by 20 ( both ACEs stand for 1 )
    else
    answer1=a+b+c-10;  // the total value must exceed 21( 11+11+c>22), so substrate it by 10 ( one ACE stands for 1 but the other stands for 11)
  }
  else if(a!=11&&b==11&&c==11)   // b and c are ACEs but a isn’t 
  {
    if(a+b+c>31)
    answer1=a+b+c-20;
    else
    answer1=a+b+c-10;
  }
  else if(a==11&&b!=11&&c==11)   // a and c are ACEs but b isn’t 
  {
    if(a+b+c>31)
    answer1=a+b+c-20;
    else
    answer1=a+b+c-10;
  }
  else
  answer1=13;  // all three cards are ACEs, one stands for 11 and the others stand for 1
  
  cout<<"The total value of the hand is "<<answer1;  // output the total value
  if(answer1>21)
  cout<<"(bust)";  // if the total value exceed 21

  return 0;
  
}
