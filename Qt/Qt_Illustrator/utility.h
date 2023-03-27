#ifndef UTILITY_H
#define UTILITY_H

#include "qcolor.h"
#endif // UTILITY_H

#include <QString>
#include <QPoint>
#include <stack>
#include <iostream>
#include <QFileDialog>
#include <QString>
#include <QFile>
#include <QTextStream>
#include <QImage>
#include <qdebug.h>
#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgcodecs.hpp>

using namespace std;

stack<QPoint>emptyStack;
QImage emptyImg;
QFont F;

class Move
{
public:
    Move(QString ="", QColor=QColor(0,0,0), int=0, QString="", bool=false
            , int=0, int=0, int=0, int=0, stack<QPoint> =emptyStack, QString=""
            , QImage=emptyImg, QString="",QFont=F,int=0) ;
    QString Shape;
    QColor Color;
    int Width;
    QString Style;
    bool Fill;
    int X1;
    int X2;
    int Y1;
    int Y2;
    QString selectAction;
    stack<QPoint>pencilPoints; // pencil only
    QImage importImage;
    QString importText;
    QFont importTextFont;
    int importTextSize;

    bool checkMoveIdentical(Move B);
    bool checkIfMoveSelected(Move A,stack<Move> MoveStack);
};

Move::Move(QString sh,QColor col,int wid,QString sty,bool fill,int x1,int y1,int x2,int y2,stack<QPoint> points,QString action,QImage img,QString text,QFont f,int s){
    Shape = sh;
    Color = col;
    Width = wid;
    Style = sty;
    Fill = fill;
    X1 = x1;
    X2 = x2;
    Y1 = y1;
    Y2 = y2;
    selectAction = action;
    pencilPoints = points;
    importImage = img;
    importText = text;
    importTextFont = f ;
    importTextSize = s;
}



stack<Move>curStack;
stack<Move>temStack;
stack<Move>selStack;
stack<Move>selStackCopy;

stack<Move>selectedFillMoves;
stack<Move>selectedUnfillMoves;
stack<Move>selectedMoveMoves;


int selectedMoveMoves_Up_count;
int selectedMoveMoves_Down_count;
int selectedMoveMoves_Left_count;
int selectedMoveMoves_Right_count;

stack<Move> StackInverse(stack<Move>origStack){
    stack<Move> invStack;
    while(!origStack.empty()){
        invStack.push(origStack.top());
        origStack.pop();
    }

    return invStack;
}

stack<Move> findMoveSelected(QPoint A, QPoint B){ // to identify which Moves are selected
    stack<Move>curStackCopy = curStack;
    stack<Move>selected;
    while(!curStackCopy.empty()){
        Move aMove = curStackCopy.top();
        curStackCopy.pop();
        double X_max,Y_max,X_min,Y_min;
        bool REACH;

        if(A.x()>B.x()){
            X_max = A.x();
            X_min = B.x();
        }
        else{
            X_max = B.x();
            X_min = A.x();
        }

        if(A.y()>B.y()){
            Y_max = A.y();
            Y_min = B.y();
        }
        else{
            Y_max = B.y();
            Y_min = A.y();
        }

        if(aMove.Shape=="pencil"){

            REACH = false;
            stack<QPoint> points = aMove.pencilPoints;
            while(!points.empty()){
                QPoint p = points.top();
                points.pop();

                if(p.x()>=X_min && p.x()<=X_max && p.y()>=Y_min && p.y()<=Y_max){
                    REACH = true;
                    break;
                }

            }

            if(REACH==true){
                selected.push(aMove);
                qDebug() << "pencil path selected";
            }

        }
        if(aMove.Shape=="line"){
            if((aMove.X1>X_max && aMove.X2>X_max) || (aMove.X1<X_min && aMove.X2<X_min)){
                REACH = false;
            }
            else if((aMove.Y1>Y_max && aMove.Y2>Y_max) || (aMove.Y1<Y_min && aMove.Y2<Y_min)){
                REACH = false;
            }
            else{
                int count = 0; // count how many vertices is on the right side of y=mx+k
                double m = double(aMove.Y2-aMove.Y1)/double(aMove.X2-aMove.X1);
                double k = double(aMove.Y1)-m*double(aMove.X1); //(aMove.X2*aMove.Y1-aMove.X1*aMove.Y2)/(aMove.X2-aMove.X1);
                // qDebug() << m << k;
                if(Y_max-m*X_max-k>0){
                    count ++;
                }
                if(Y_max-m*X_min-k>0){
                    count ++;
                }
                if(Y_min-m*X_max-k>0){
                    count ++;
                }
                if(Y_min-m*X_min-k>0){
                    count ++;
                }

                // qDebug() << "count:" << count;
                if(count==4||count==0){
                    REACH = false;
                }
                else{
                    REACH = true;
                }
            }

            if(REACH==true){
                selected.push(aMove);
                qDebug() << "A line selected";
            }
        }
        if(aMove.Shape=="circle"){
            double CX = (aMove.X1+aMove.X2)/2;
            double CY = (aMove.Y1+aMove.Y2)/2;
            double R = (aMove.Y2-aMove.Y1)/2;
            double D;

            qDebug() << CX << CY << R;

            if(CX>X_min && CX<X_max && CY>Y_min && CY<Y_max){
                REACH = true;
            }

            else if(CX>X_max && CY>Y_min && CY<Y_max){
                D = CX-X_max;
                if(D<R){
                    REACH = true;
                }
                else{
                    REACH = false;
                }
            }
            else if(CX<X_min && CY>Y_min && CY<Y_max){
                D = X_max-CX;
                if(D<R){
                    REACH = true;
                }
                else{
                    REACH = false;
                }
            }

            else if(CY>Y_max && CX>X_min && CX<X_max){
                D = CY-Y_max;
                if(D<R){
                    REACH = true;
                }
                else{
                    REACH = false;
                }
            }
            else if(CY<Y_min && CX>X_min && CX<X_max){
                D = Y_min-CY;
                if(D<R){
                    REACH = true;
                }
                else{
                    REACH = false;
                }
            }

            else if(CX<=X_min && CY>=Y_max){
                D = sqrt(pow((CX-X_min),2)+pow((CY-Y_max),2));
                if(D<R){
                    REACH = true;
                }
                else{
                    REACH = false;
                }
            }
           else if(CX<=X_min && CY<=Y_min){
                D = sqrt(pow((CX-X_min),2)+pow((CY-Y_min),2));
                if(D<R){
                    REACH = true;
                }
                else{
                    REACH = false;
                }
            }
            else if(CX>=X_max && CY<=Y_min){
                D = sqrt(pow((CX-X_max),2)+pow((CY-Y_min),2));
                if(D<R){
                    REACH = true;
                }
                else{
                    REACH = false;
                }
            }
            else if(CX>=X_max && CY>=Y_max){
                D = sqrt(pow((CX-X_max),2)+pow((CY-Y_max),2));
                if(D<R){
                    REACH = true;
                }
                else{
                    REACH = false;
                }
            }
            else{
                REACH = false;
            }

            if(REACH==true){
                selected.push(aMove);
                qDebug() << "A circle selected";
            }

        }
        if(aMove.Shape=="rect" || aMove.Shape=="image"
                || aMove.Shape=="text"){
            if((aMove.X1>X_max && aMove.X2>X_max) || (aMove.X1<X_min && aMove.X2<X_min)){
                REACH = false;
            }
            else if((aMove.Y1>Y_max && aMove.Y2>Y_max) || (aMove.Y1<Y_min && aMove.Y2<Y_min)){
                REACH = false;
            }
            else{
                REACH = true;
            }

            if(REACH==true){
                selected.push(aMove);
                qDebug() << "A rect or image selected";
            }
        }
        if(aMove.Shape=="ellipse"){
            double OX = (aMove.X1+aMove.X2)/2;
            double OY = (aMove.Y1+aMove.Y2)/2;

            if(abs(aMove.X2-aMove.X1)>abs(aMove.Y2-aMove.Y1)){ // lying ellipse
                double a = abs((aMove.X2-aMove.X1)/2);
                double b = abs((aMove.Y2-aMove.Y1)/2);
                double c = sqrt(pow(a,2)-pow(b,2));
                // F1,F2 = (OX+-c,OY);
                double D;
                double PF1;
                double PF2;

                qDebug() << OX << OY;

                if(OX>X_min && OX<X_max && OY>Y_min && OY<Y_max){
                    REACH = true;
                }
                else if(OX>X_max && OY>Y_min && OY<Y_max){
                    D = OX-X_max;
                    if(D<a){
                        REACH = true;
                    }
                    else{
                        REACH = false;
                    }
                }
                else if(OX<X_min && OY>Y_min && OY<Y_max){
                    D = X_min-OX;
                    if(D<a){
                        REACH = true;
                    }
                    else{
                        REACH = false;
                    }
                }

                else if(OY>Y_max && OX>X_min && OX<X_max){
                    D = OY-Y_max;
                    if(D<b){
                        REACH = true;
                    }
                    else{
                        REACH = false;
                    }
                }
                else if(OY<Y_min && OX>X_min && OX<X_max){
                    D = Y_min-OY;
                    if(D<b){
                        REACH = true;
                    }
                    else{
                        REACH = false;
                    }
                }

                else if(OX<=X_min && OY>=Y_max){
                    PF1 = sqrt(pow(((OX+c)-X_min),2)+pow((OY-Y_max),2));
                    PF2 = sqrt(pow(((OX-c)-X_min),2)+pow((OY-Y_max),2));
                    //qDebug() << PF1+PF2 << 2*a;
                    if(PF1+PF2<=2*a){
                        REACH = true;
                    }
                    else{
                        REACH = false;
                    }
                }
                else if(OX<=X_min && OY<=Y_min){
                    PF1 = sqrt(pow(((OX+c)-X_min),2)+pow((OY-Y_min),2));
                    PF2 = sqrt(pow(((OX-c)-X_min),2)+pow((OY-Y_min),2));
                    //qDebug() << PF1+PF2 << 2*a;
                    if(PF1+PF2<=2*a){
                        REACH = true;
                    }
                    else{
                        REACH = false;
                    }
                }
                else if(OX>=X_max && OY<=Y_min){
                    PF1 = sqrt(pow(((OX+c)-X_max),2)+pow((OY-Y_min),2));
                    PF2 = sqrt(pow(((OX-c)-X_max),2)+pow((OY-Y_min),2));
                    //qDebug() << PF1+PF2 << 2*a;
                    if(PF1+PF2<=2*a){
                        REACH = true;
                    }
                    else{
                        REACH = false;
                    }

                }
                else if(OX>=X_max && OY>=Y_max){
                    PF1 = sqrt(pow(((OX+c)-X_max),2)+pow((OY-Y_max),2));
                    PF2 = sqrt(pow(((OX-c)-X_max),2)+pow((OY-Y_max),2));
                    //qDebug() << PF1+PF2 << 2*a;
                    if(PF1+PF2<=2*a){
                        REACH = true;
                    }
                    else{
                        REACH = false;
                    }
                }
                else{
                    REACH = false;
                }


            }else{ // standing ellipse
                double a = abs((aMove.Y2-aMove.Y1)/2);
                double b = abs((aMove.X2-aMove.X1)/2);
                double c = sqrt(pow(a,2)-pow(b,2));
                // F1,F2 = (OX,OY+-c);
                double D;
                double PF1;
                double PF2;

                qDebug() << OX << OY;

                if(OX>X_min && OX<X_max && OY>Y_min && OY<Y_max){
                    REACH = true;
                }
                else if(OX>X_max && OY>Y_min && OY<Y_max){
                    D = OX-X_max;
                    if(D<b){
                        REACH = true;
                    }
                    else{
                        REACH = false;
                    }
                }
                else if(OX<X_min && OY>Y_min && OY<Y_max){
                    D = X_min-OX;
                    if(D<b){
                        REACH = true;
                    }
                    else{
                        REACH = false;
                    }
                }

                else if(OY>Y_max && OX>X_min && OX<X_max){
                    D = OY-Y_max;
                    if(D<a){
                        REACH = true;
                    }
                    else{
                        REACH = false;
                    }
                }
                else if(OY<Y_min && OX>X_min && OX<X_max){
                    D = Y_min-OY;
                    if(D<a){
                        REACH = true;
                    }
                    else{
                        REACH = false;
                    }
                }

                else if(OX<=X_min && OY>=Y_max){
                    PF1 = sqrt(pow((OX-X_min),2)+pow(((OY+c)-Y_max),2));
                    PF2 = sqrt(pow((OX-X_min),2)+pow(((OY-c)-Y_max),2));
                    if(PF1+PF2<=2*a){
                        REACH = true;
                    }
                    else{
                        REACH = false;
                    }
                }
                else if(OX<=X_min && OY<=Y_min){
                    PF1 = sqrt(pow((OX-X_min),2)+pow(((OY+c)-Y_min),2));
                    PF2 = sqrt(pow((OX-X_min),2)+pow(((OY-c)-Y_min),2));
                    if(PF1+PF2<=2*a){
                        REACH = true;
                    }
                    else{
                        REACH = false;
                    }
                }
                else if(OX>=X_max && OY<=Y_min){
                    PF1 = sqrt(pow((OX-X_max),2)+pow(((OY+c)-Y_min),2));
                    PF2 = sqrt(pow((OX-X_max),2)+pow(((OY-c)-Y_min),2));
                    if(PF1+PF2<=2*a){
                        REACH = true;
                    }
                    else{
                        REACH = false;
                    }

                }
                else if(OX>=X_max && OY>=Y_max){
                    PF1 = sqrt(pow((OX-X_max),2)+pow(((OY+c)-Y_max),2));
                    PF2 = sqrt(pow((OX-X_max),2)+pow(((OY-c)-Y_max),2));
                    if(PF1+PF2<=2*a){
                        REACH = true;
                    }
                    else{
                        REACH = false;
                    }
                }
                else{
                    REACH = false;
                }

            }


            if(REACH==true){
                selected.push(aMove);
                qDebug() << "An ellipse selected";
            }

        }

    }
    return selected;
}


bool Move::checkMoveIdentical(Move B){
    if(Shape==B.Shape && Color==B.Color && Style==B.Style && Width==B.Width && Fill==B.Fill
            && X1==B.X1 && X2==B.X2 && Y1==B.Y1 && Y2==B.Y2){
        return true;
    }
    else
        return false;
}

bool Move::checkIfMoveSelected(Move A,stack<Move> MoveStack){

    bool sel=false;
    while(!MoveStack.empty()){
        Move B = MoveStack.top();

        if(A.checkMoveIdentical(B)){
            sel=true;
        }

        MoveStack.pop();

    }
      //qDebug() << sel;
    return sel;

}


QImage cvMat_to_QImage(const cv::Mat &mat );


