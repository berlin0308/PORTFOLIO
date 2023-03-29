
//================================================================
//  PROGRAMMER :B09611007
//  DATE       : 2020-11-15
//  FILENAME   : HW04CB09611007.CPP 
//  DESCRIPTION: This is a program to display the the greatest common divisor.
//================================================================

#include <iostream>
#include <iomanip>
using namespace std;

int answer1;     // Store the greatest common divisor of 5 and 15 in this global variable
int answer2;     // Store the greatest common divisor of 2 and 13 in this global variable
int answer3;     // Store the greatest common divisor of 6 and 12 in this global variable

int gcd(int a,int b);  //define a function to test greatest common divisor between two numbers

int main()
{
	int t[21][21];  //declare t as a two-dimension array
	int i , j , k;  //declare i,j,k as intergers
	cout << setw(7);  
	for (i = 1; i <= 20; i++)  
	{
		cout << i <<setw(3);
	}
	cout << endl << "==================================================================" << endl;
	
	for (j = 1; j <= 20; j++)  //output the table and calculate the greatest common divisor
	{
		cout << setw(2) << j  << setw(2) << "|";  //output the table
		for (k = 1; k <= 20; k++)  
		{
			t[j][k] = gcd(j, k);  //calculate the greatest common divisor
			cout << setw(3) << t[j][k];  //output the table
		}
		cout << endl;  //output the table
	}
	answer1 = t[5][15];  // Store the greatest common divisor of 5 and 15
	answer2 = t[2][13];  // Store the greatest common divisor of 2 and 13
	answer3 = t[6][12]; // Store the greatest common divisor of 6 and 12
	
	cout<<answer1<<" "<<answer2<<" "<<answer3;
	return 0;
}

int gcd(int a,int b)
{
	int p,r;  //declare p,r as intergers
	for (p = 1; p <= 20; p++)  //test iif p is greatest common divisor
	{
		if (a%p ==0 && b%p ==0 )  //if it's true
		{
			r = p;  //let greatest common divisor = r
		}
	}
	return r;  //return value
}
