//=================================================================
//  PROGRAMMER : B09611007
//  DATE       : 2020-10-12
//  FILENAME   : HW02AB09611007.CPP 
//  DESCRIPTION: This is a program to determine in which quadrant or axis the coordinate point lies.
//=================================================================
#include <iostream>
using namespace std;

int answer1;  // represent  in which quadrant or axis the coordinate point lies.

int main()
{
	
	double a=0.00,b=0.00; // x and y coordinates of the point
	cin >> a >> b ;  // input the x and y coordinates of the point
	
	if( a>0 && b>0 )
		answer1=1;  // the point lies in quadrant I 
		
	else if(a<0 && b>0 )
		answer1=2;  // the point lies in quadrant ll
		
	else if(a<0 && b<0 )
		answer1=3;  // the point lies in quadrant Ill
		
                 else if(a>0 && b<0 )
		answer1=4;  // the point lies in quadrant IV
		
	else if( a!=0 && b==0 )
		answer1=5;  // the point lies on the x axis
	
	else if( a==0 && b!=0 )
		answer1=6;  // the point lies on the y axis
		
	else if(a==0 && b==0 )
		answer1=7;  // the point is the origin point
	
	if( answer1==1 )
	{
		
		cout << '(' << a << ", " << b << ") is in quadrant I ";
	}
	else if( answer1==2 )
	{
		
		cout << '(' << a << ", " << b << ") is in quadrant II ";
	}
	else if( answer1==3 )
	{
		
		cout << '(' << a << ", " << b << ") is in quadrant III ";
	}
	else if( answer1==4 )
	{
		
		cout << '(' << a << ", " << b << ") is in quadrant IV ";
	}
	else if( answer1==5 )
	{
		
		cout << '(' << a << ", " << b << ") is on the x axis";
	}
	else if( answer1==6 )
	{
		
		cout << '(' << a << ", " << b << ") is on the y axis";
	}
		else if( answer1==7 )
	{
		
		cout << '('<< a << ", " << b << ") is the origin (0,0).";
	}
	
    return 0;
}