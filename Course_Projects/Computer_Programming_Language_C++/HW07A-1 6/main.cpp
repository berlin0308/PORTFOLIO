#include <iostream>
#include <fstream>
#include <string>
using namespace std;
fstream words; // input file

int answer1; // store the total number of words
int answer2; // store the number of chars of the longest word
 string list[30][50000];
  int L[30]={0};
string Re(string); // the function to check if its reversed string is also in the list

int main() 
{
  int max;  // store the current maximum
  int t=0;  // count the number of words
  string longest; // store the current longest words
  words.open("words.txt"); // open the input file
 
  string aaa;
  
  // change uppercase char into lowwercase and count the number of words
  while(words>>aaa) 
  {
       // convert each line into string
      int len=aaa.size(); // the length of hhh[t]
      for(int y=0;y<len;y++) // turn to the lowercase
      {
        if(aaa[y]>='A'&&aaa[y]<='Z')
        aaa[y]+=32;
      }
      list[len][L[len]]=aaa;
      L[len]++;
      t++;  // count the number of words
  }
    words.close();
    int found=0;
  for(int i=30 ;i >0 ; i-- )
  {
    for(int j=0 ; j <= L[i] ; j++)
    {
      for(int k=0;k<j;k++)
       {
         if(list[i][j]==Re(list[i][k]))
       {
         cout<<list[i][k]<<endl;
         max=i;
         longest=list[i][j];
         found=1;
         break;
       }
       if(found==1)
       break;
       }
    }
      if(found==1)
       break;
  }
  answer1=t;
  answer2=max;
  cout<<endl<<answer1<<' '<<answer2;
  
  return 0;

}

string Re(string www)
{
   string rrr=www;
   int l=www.length();
   for(int i=l-1;i>=0;i--)
   {
     int j=l-i-1;
     rrr[j]=www[i];
   }
   return rrr ;
}