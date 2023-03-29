#include <iostream>
#include<string>
#include <fstream>
#include<cstdlib>
#include<iomanip>

using namespace std;

int bjbj()
{
  fstream list;
  list.open("RatingList.txt");
  if (list.fail())  //if file can not be opened successfully, exit
  {
    cout << "The file can not be opened successfully." << endl;
    exit(1);
  }
  return 0;
}