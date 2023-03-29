//

//================================================================
//  PROGRAMMER :B09611007
//  DATE       : 2018-10-29
//  FILENAME   : HW03BB09611007.CPP 
//  DESCRIPTION: This is a program to recognize whether the number between 2 to 999 is prime number or not
//================================================================

	
#include <iostream>
#include<math.h>
using namespace std;

int answer1;   // Store the largest prime number less than 1000 in this global variable

int main()
{
	int k,n; //declare k,n as the intergers
	n = 0;  //give n value
	
	for (k = 2; k < 1000; k++)  //test prime numbers between 2 to 999
	{
		for (n = 2; n < k; n++)  //test whether when n<k can be divided with no remainder
		{
			if (k%n == 0)  //calculate the remainder
			{
				break;
			}
			if (k == n + 1) //if k have no remainder, it's prime number
			{
				answer1 = k;  //when loop done ,answer1 is largest prime number between 2 to 999
			}

		}

	}
	cout << answer1 << " is the biggest prime number less than 1000. " << endl;  //display largest prime number between 2 to 999
        return 0;
}