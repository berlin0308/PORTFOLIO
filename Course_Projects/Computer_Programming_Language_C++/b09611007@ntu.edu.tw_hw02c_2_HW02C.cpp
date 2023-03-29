#include <iostream>
using namespace std;

int answer1;

int main()
{
	
	
    double a,b;
	cin >> a >> b ;
	
	if( a>0 && b>0 )
	{
		
		answer1=1;
	}
	else if(a<0 && b>0 )
	{
		answer1=2;
	}
		else if(a<0 && b<0 )
	{
		answer1=3;
	}
		else if(a>0 && b<0 )
	{
		answer1=4;
	}
		else if( a!=0 && b==0 )
	{
		answer1=5;
	}
		else if( a==0 && b!=0 )
	{
		answer1=6;
	}
		else if(a==0 && b==0 )
	{
		answer1=7;
	}
	
	
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

]