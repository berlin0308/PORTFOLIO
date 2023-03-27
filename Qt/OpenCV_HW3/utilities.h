#include <QMainWindow>
#include <QFile>
#include <QTextStream>
#include <QImage>
#include <qdebug.h>
#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgcodecs.hpp>
#include <stack>


using namespace std;
using namespace cv;


class Process
{
public:
    Process(QString ="a",QString ="a",int=0);
    QString Category; // Adjust, HSVrange, Filter, Else
    QString Type; // B,G,R,H,S,V...
    int key_value;
};

Process::Process(QString category, QString type, int value){
    Category = category;
    Type = type;
    key_value = value;
}

QImage cvMat_to_QImage(const cv::Mat &mat );

Mat gaussian_noise(Mat img,int k);
