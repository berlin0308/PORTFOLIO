#include <iostream>
using namespace std;
char answer1; // store the first character of the decode sentence
char answer2; // store the last character of the decode sentence

int main() 
{
 char letter[100]={'O',' ' ,'R','U','B','K',' ','I','U','S','V','A','Z','K','X',' ', 'V','X','U','M','X','G','S','S','O','T','M',' ','Y','U',' ','S','A','I','N'};
// the encrypted sentence
 char orig; // each character 
 int k=6;  // move 6 positions
 for(int i=0; letter[i]!='\0'; i++) // decode until end 
 {
   orig=letter[i]; // the i(th) character
   if(orig==' ')
   ;  // orig remains ' '(blank)
   else if(orig-k<'A')
   orig=orig-k+26; // +26 if the moved result < 'A'
   else
   orig-=k;  // move k positions
   letter[i]=orig;  // the result replaces the original character 
   cout<<letter[i]; // output the decoded sequence
 }
 answer1=letter[0]; // the first character
 answer2=orig; // the last character
 cout<<endl<<"the first character is "<<answer1<<endl<<"and the last character is "<<answer2;
 return 0;
}

