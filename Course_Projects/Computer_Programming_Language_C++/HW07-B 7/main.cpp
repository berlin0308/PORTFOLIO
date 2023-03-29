#include <iostream>
#include<string>
#include <fstream>
#include<cstdlib>
#include<iomanip>

using namespace std;

int answer1=0; // The total number of movies listed
int answer2=0; // The total number of ratings
string answer3; // The movie with the highest average rating

fstream list; // the input file

// declaration section
class MovieReview
{
  private:
    
    string movieTitle; // store the title as a string
    double totalScore; // store the total score
    int numRating; // store the number of ratings
    double aveScore; // store the average score
    int score;

  public:
  
    MovieReview(string mt =" ",int sc = 0)
    { movieTitle=mt; score=sc; numRating=0;};
    // accessor
    string getMovieTitle(){return movieTitle;} ;
    double getTotalScore(){return totalScore;};
    int getNumRating(){return numRating;};
    double getAveScore(){return aveScore;};
    // mutator
    void setMovieTitle(string mt){movieTitle=mt;};
    void setTotalScore(int ts){totalScore=ts;};
    void setNumRating(int num){numRating=num;};
    void setAveScore(int as){aveScore=as;};  
    void addScore(int,int);
    void calculateAveScore();
    };

// implementation section
void MovieReview::addScore(int s,int n)
{
  totalScore+=s;
  numRating+=n;
}

void MovieReview::calculateAveScore()
{
  aveScore=totalScore/numRating;
}

MovieReview A[20];
void readData(); // used to read the file

int main()
{
 readData();
 int i;
 A[0].calculateAveScore();
 double max=A[0].getAveScore();
 int highest;
 string ttt('=',32);
 cout<<endl<<"MovieTitle / TotalScore / NumRating / AveScore "<<endl<<ttt<<endl;
 for(i=0;i<20&&A[i].getTotalScore()!=0;i++)
 {
   A[i].calculateAveScore();
   cout<<A[i].getMovieTitle()<<setw(5)<<A[i].getTotalScore()<<setw(5)<<A[i].getNumRating()<<"  "<<A[i].getAveScore()<<endl;
   if(A[i].getAveScore()>max)
   {
     max=A[i].getAveScore();
     highest=i;
   }
 }
answer1=i;
answer3=A[highest].getMovieTitle();
  
 cout<<endl<<"The total number of movies listed : "<<answer1<<endl<<"The total number of ratings :"<<answer2<<endl<<"The movie with the highest average rating :"<<answer3;
 cout<<"("<<A[highest].getAveScore()<<")";
 return 0;
}


void readData()
{
  
  string aaa;
  int k;
  list.open("RatingList.txt");
  while(list.good())
  {
    string str;
    while(list>>aaa)
    {
      if(aaa!="|")
      {
        str=str+aaa+" ";
      }
      else if(aaa=="|")
      {
        list>>k;
        break;
      }
      
    }
  
    for(int i=0;i<20;i++)
    {
      if(str==A[i].getMovieTitle())
      {
        A[i].addScore(k,1);
        break;
      }
      if(i==19)
      {
        int b;
        MovieReview T(str,k);
        A[b]=T;
        A[b].addScore(k,1);
        cout<<A[b].getMovieTitle()<<b<<endl;
        b++;
      }
    }
    answer2++;
  }
  cout<<endl;
  list.close();
}
