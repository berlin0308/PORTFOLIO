#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "utilities.h"
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
#include <stack>
#include <QMouseEvent>
#include <cstddef>
#include <QMessageBox>

using namespace std;
using namespace cv;

// Adjust unittest
// stack
// QImage ProcessImage(image,execStack) 讀取stack 執行
// undo, redo, reset
// HSV range, bitwise image
// QMessageBox if img empty
// Filter
// flip, crop, rotation
// save
// label

string fileName;


Mat img_read;
Mat img_after;

stack<Process>ExecStack;
stack<Process>TemStack;

int Adjust_B,Adjust_G,Adjust_R,Adjust_H,Adjust_S,Adjust_V;
int Range_H_lower,Range_H_upper,Range_S_lower,Range_S_upper,Range_V_lower,Range_V_upper;
QString Filter;
int kernel;
bool flip_H;
bool flip_V;
int rotation;


MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    setWindowTitle("Image Processing Widget");
    Settings();
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::Update_Image(){

    qDebug() << "\nExecStack:" << ExecStack.size();
    qDebug() << "TemStack:" << TemStack.size();

    if(ExecStack.empty())
        ui->pushButton_undo->setEnabled(false);
    else
         ui->pushButton_undo->setEnabled(true);

    if(TemStack.empty())
        ui->pushButton_redo->setEnabled(false);
    else
        ui->pushButton_redo->setEnabled(true);

    if(ExecStack.empty()&&TemStack.empty())
        ui->pushButton_reset->setEnabled(false);
    else
        ui->pushButton_reset->setEnabled(true);

    /* initialization */

    Adjust_B=Adjust_G=Adjust_R=Adjust_H=Adjust_S=Adjust_V=0;
    Range_H_lower=Range_S_lower=Range_V_lower=0;
    Range_H_upper=Range_S_upper=Range_V_upper=255;

    Filter = "None";
    kernel = 7;
    flip_H = false;
    flip_V = false;
    rotation = 0;
    const int label_w = ui->label_Image->width();
    const int label_h = ui->label_Image->height();

    if(ExecStack.empty()&& !img_read.empty()){
        ui->label_Image->setPixmap(QPixmap::fromImage(cvMat_to_QImage(img_read).scaled(label_w,label_h,Qt::KeepAspectRatio)));
    }

    stack<Process>EXEC;
    stack<Process>ExecStackCopy = ExecStack;
    while(!ExecStackCopy.empty()){  // stack inversion
        EXEC.push(ExecStackCopy.top());
        ExecStackCopy.pop();
    }

    while(!EXEC.empty()){
        Process aProcess = EXEC.top();
        EXEC.pop();

        if(aProcess.Category=="Adjust"){
            if(aProcess.Type=="B"){
                Adjust_B = aProcess.key_value;
            }
            if(aProcess.Type=="G"){
                Adjust_G = aProcess.key_value;
            }
            if(aProcess.Type=="R"){
                Adjust_R = aProcess.key_value;
            }
            if(aProcess.Type=="H"){
                Adjust_H = aProcess.key_value;
            }
            if(aProcess.Type=="S"){
                Adjust_S = aProcess.key_value;
            }
            if(aProcess.Type=="V"){
                Adjust_V = aProcess.key_value;
            }
        }
        if(aProcess.Category=="Range"){
            if(aProcess.Type=="H_lower"){
                Range_H_lower = aProcess.key_value;
            }
            if(aProcess.Type=="H_upper"){
                Range_H_upper = aProcess.key_value;
            }
            if(aProcess.Type=="S_lower"){
                Range_S_lower = aProcess.key_value;
            }
            if(aProcess.Type=="S_upper"){
                Range_S_upper = aProcess.key_value;
            }
            if(aProcess.Type=="V_lower"){
                Range_V_lower = aProcess.key_value;
            }
            if(aProcess.Type=="V_upper"){
                Range_V_upper = aProcess.key_value;
            }
        }

        if(aProcess.Category=="Filter"){
            Filter = aProcess.Type;
            kernel = aProcess.key_value;
        }
        if(aProcess.Category=="Else"){
            if(aProcess.Type=="Flip_H"){
                flip_H = !flip_H;
                //qDebug() << "flip_H:" << flip_H;
            }
            if(aProcess.Type=="Flip_V"){
                flip_V = !flip_V;
                //qDebug() << "flip_V:" << flip_V;
            }
            if(aProcess.Type=="Rotate"){
                rotation ++ ;
            }
            if(aProcess.Type=="Rotate_L"){
                rotation -- ;
            }

        }
    }
        ui->spinBox_adjust_B->setValue(Adjust_B);
        ui->spinBox_adjust_G->setValue(Adjust_G);
        ui->spinBox_adjust_R->setValue(Adjust_R);
        ui->spinBox_adjust_H->setValue(Adjust_H);
        ui->spinBox_adjust_S->setValue(Adjust_S);
        ui->spinBox_adjust_V->setValue(Adjust_V);




        img_after = img_read.clone();
        double ratio = double(img_after.cols)/double(img_after.rows);
        Mat img_new;
        if(!img_after.empty())
        cv::resize(img_after,img_new,Size(int(200*ratio),200));

        //qDebug() << img_new.cols << img_new.rows;
        //qDebug() << img_new.channels() << img_new.depth();

        // Adjust 像素尋訪
        if(Adjust_B!=0 ||Adjust_G!=0 || Adjust_R!=0){
            int B,G,R;
            for(int i=0;i<img_new.rows;i++){
                for(int j=0;j<img_new.cols;j++){

                        //qDebug() << i << j;
                        B = int(img_new.at<cv::Vec3b>(i,j)[0])+Adjust_B;
                        G = int(img_new.at<cv::Vec3b>(i,j)[1])+Adjust_G;
                        R = int(img_new.at<cv::Vec3b>(i,j)[2])+Adjust_R;

                        //qDebug() << B << G << R;

                        if(B>255)
                            B=255;
                        if(B<0)
                            B=0;
                        if(G>255)
                            G=255;
                        if(G<0)
                            G=0;
                        if(R>255)
                            R=255;
                        if(R<0)
                            R=0;

                        img_new.at<cv::Vec3b>(i,j)[0] = B;
                        img_new.at<cv::Vec3b>(i,j)[1] = G;
                        img_new.at<cv::Vec3b>(i,j)[2] = R;

                }
            }

            ui->label_Image->setPixmap(QPixmap::fromImage(cvMat_to_QImage(img_new).scaled(label_w,label_h,Qt::KeepAspectRatio)));

        }

        if(Adjust_H!=0 ||Adjust_S!=0 || Adjust_V!=0){
            cvtColor(img_new,img_new,40,cv::COLOR_BGR2HSV);
            //qDebug() << "!!!";
            int H,S,V;
            for(int i=0;i<img_new.rows;i++){
                for(int j=0;j<img_new.cols;j++){
                       try {
                        qDebug() << i << j;
                        H = int(img_new.at<cv::Vec3b>(i,j)[0])+Adjust_H;
                        S = int(img_new.at<cv::Vec3b>(i,j)[1])+Adjust_S;
                        V = int(img_new.at<cv::Vec3b>(i,j)[2])+Adjust_V;

                        //qDebug() << H << S << V;

                        if(H>255)
                            H=255;
                        if(H<0)
                            H=0;
                        if(S>255)
                            S=255;
                        if(S<0)
                            S=0;
                        if(V>255)
                            V=255;
                        if(V<0)
                            V=0;

                        img_new.at<cv::Vec3b>(i,j)[0] = H;
                        img_new.at<cv::Vec3b>(i,j)[1] = S;
                        img_new.at<cv::Vec3b>(i,j)[2] = V;

                    } catch (...) {
                    }

                }
            }

            cvtColor(img_new,img_new,cv::COLOR_HSV2BGR);
            ui->label_Image->setPixmap(QPixmap::fromImage(cvMat_to_QImage(img_new).scaled(label_w,label_h,Qt::KeepAspectRatio)));

        }



        // Filter
        if(Filter!="None"){
            qDebug() << "Filter:" << Filter;
            if(Filter=="Box"){
                cv::blur(img_new,img_new,Size(kernel,kernel),Point(-1,-1));
                ui->label_Image->setPixmap(QPixmap::fromImage(cvMat_to_QImage(img_new).scaled(label_w,label_h,Qt::KeepAspectRatio)));
            }
            if(Filter=="Gaussian"){
                cv::GaussianBlur(img_new,img_new,Size(kernel,kernel),0,0);
                ui->label_Image->setPixmap(QPixmap::fromImage(cvMat_to_QImage(img_new).scaled(label_w,label_h,Qt::KeepAspectRatio)));
            }
            if(Filter=="Median"){
                cv::medianBlur(img_new,img_new,kernel);
                ui->label_Image->setPixmap(QPixmap::fromImage(cvMat_to_QImage(img_new).scaled(label_w,label_h,Qt::KeepAspectRatio)));
            }
            if(Filter=="Sharpen"){
                Mat img_blurred;
                cv::GaussianBlur(img_new,img_blurred,Size(kernel,kernel),0,0);
                cv::addWeighted(img_new,1.5,img_blurred,-0.6,0.0,img_new);
                ui->label_Image->setPixmap(QPixmap::fromImage(cvMat_to_QImage(img_new).scaled(label_w,label_h,Qt::KeepAspectRatio)));
            }
            if(Filter=="Noise"){
                img_new = gaussian_noise(img_new,kernel);
                ui->label_Image->setPixmap(QPixmap::fromImage(cvMat_to_QImage(img_new).scaled(label_w,label_h,Qt::KeepAspectRatio)));
            }

        }



        // Range
        if(Range_H_lower!=0 ||Range_S_lower!=0 || Range_V_lower!=0 || Range_H_upper!=255 || Range_S_upper!=255 || Range_V_upper!=255){
            Mat mask;
            cvtColor(img_new,mask,cv::COLOR_BGR2HSV);
            inRange(mask,Scalar(Range_H_lower,Range_S_lower,Range_V_lower),Scalar(Range_H_upper,Range_S_upper,Range_V_upper),mask);
            for(int i=0;i<mask.rows;i++){
                for(int j=0;j<mask.cols;j++){
                        //qDebug() << i << j;
                        int m = mask.at<uchar>(i,j);
                        //qDebug() << "m:" << m;
                        if(m==0){
                            //qDebug() << "m==0";
                            img_new.at<cv::Vec3b>(i,j)[0]=0;
                            img_new.at<cv::Vec3b>(i,j)[1]=0;
                            img_new.at<cv::Vec3b>(i,j)[2]=0;
                        }
                 }
            }
            //bitwise_and(img_new,mask,img_new); failed...
            ui->label_Image->setPixmap(QPixmap::fromImage(cvMat_to_QImage(img_new).scaled(label_w,label_h,Qt::KeepAspectRatio)));
        }


        // Else
        if(flip_H==true){
            //qDebug() << "flip H once";
            cv::flip(img_new,img_new,1);
            ui->label_Image->setPixmap(QPixmap::fromImage(cvMat_to_QImage(img_new).scaled(label_w,label_h,Qt::KeepAspectRatio)));
        }else{
            ui->label_Image->setPixmap(QPixmap::fromImage(cvMat_to_QImage(img_new).scaled(label_w,label_h,Qt::KeepAspectRatio)));
        }

        if(flip_V==true){
            //qDebug() << "flip V once";
            cv::flip(img_new,img_new,0);
            ui->label_Image->setPixmap(QPixmap::fromImage(cvMat_to_QImage(img_new).scaled(label_w,label_h,Qt::KeepAspectRatio)));
        }else{
            ui->label_Image->setPixmap(QPixmap::fromImage(cvMat_to_QImage(img_new).scaled(label_w,label_h,Qt::KeepAspectRatio)));
        }

        if(rotation!=0){
            cv::Point2f pc(img_new.cols/2.,img_new.rows/2.);
            cv::Mat r = cv::getRotationMatrix2D(pc,rotation*-90,1.0);
            cv::warpAffine(img_new,img_new,r,img_new.size());
            ui->label_Image->setPixmap(QPixmap::fromImage(cvMat_to_QImage(img_new).scaled(label_w,label_h,Qt::KeepAspectRatio)));
        }

        img_after = img_new;

}

void MainWindow::NoFile_Warning(){
    if(img_read.empty()){
        QMessageBox::warning(this,"No File Warning","Image not found \nPlease open a file");
    }
}

void MainWindow::on_pushButton_file_clicked()
{
    QString filePath = QFileDialog::getOpenFileName(this,tr("Open File"),"",tr("image(*.png *.jpeg *.jpg)"));
    fileName = filePath.toStdString();
    //fileName = "C:\\Users\\BERLIN CHEN\\Desktop\\DDLAB\\PRO\\OpenCV_HW3\\color_ring.jpg";

    qDebug() << filePath;
    img_read = imread(fileName);

    const int label_w = ui->label_Image->width();
    const int label_h = ui->label_Image->height();
    ui->label_Image->setPixmap(QPixmap::fromImage(cvMat_to_QImage(img_read).scaled(label_w,label_h,Qt::KeepAspectRatio)));
    Update_Image();
}

void MainWindow::on_pushButton_save_clicked()
{
    NoFile_Warning();
    //QString filePath = QFileDialog::getSaveFileUrl(this,tr("Select path"),img_after,"","");
    //string fileName = filePath.toStdString();

    size_t find = fileName.find_last_of(".");
    qDebug() << find;

    if(find==string::npos){

        qDebug() << "npos";
    }
    else{
        string output_file = fileName.substr(0,find);
        QString qstr = QString::fromStdString(output_file);
        qDebug() << qstr;

        output_file+="_processed.jpg";
        imwrite(output_file,img_after);

        string content = "The image has been saved:\n "+output_file;
        content += "\n\nImage Process info:";
        if(Adjust_B!=0 ||Adjust_G!=0 || Adjust_R!=0){
            content += "\nBGR Adjust: ";
            content.append(" B").append(to_string(Adjust_B));
            content.append(" G").append(to_string(Adjust_G));
            content.append(" R").append(to_string(Adjust_R));
        }
        if(Adjust_H!=0 ||Adjust_S!=0 || Adjust_V!=0){
            content += "\nHSV Adjust: ";
            content.append(" H").append(to_string(Adjust_H));
            content.append(" S").append(to_string(Adjust_S));
            content.append(" V").append(to_string(Adjust_V));
        }
        if(Range_H_lower!=0 ||Range_S_lower!=0 || Range_V_lower!=0 || Range_H_upper!=255 || Range_S_upper!=255 || Range_V_upper!=255){
            content += "\nHSV Range: ";
            content.append(" H").append(to_string(Range_H_lower)).append("~").append(to_string(Range_H_upper));
            content.append(" S").append(to_string(Range_S_lower)).append("~").append(to_string(Range_S_upper));
            content.append(" V").append(to_string(Range_V_lower)).append("~").append(to_string(Range_V_upper));
        }
        if(Filter!="None"){
            content += "\nFilter: ";
            content.append(Filter.toStdString()).append(" with kernel size: ").append(to_string(kernel));
        }
        if(flip_H==true){
            content += "\nHorizontal flip";
        }
        if(flip_V==true){
            content += "\nVertical flip";
        }
        if(rotation!=0){
            if(rotation%4==1)
                content += "\nRight rotation: 90 degree";
            if(rotation%4==2)
                content += "\n180 degree rotation";
            if(rotation%4==3)
                content += "\nLeft rotation: 90 degree";
        }


        QString qcontent = QString::fromStdString(content);
        QMessageBox::about(this,"Image saved",qcontent);

    }

}


void MainWindow::on_horizontalSlider_adjust_B_valueChanged(int value)
{
    NoFile_Warning();
    //qDebug() << "value changed:" << value;
    static int previous_value=0;
    if(abs(value-previous_value)>5){
        qDebug() << "value change";
        previous_value = value;

        Process change("Adjust","B",value);
        ExecStack.push(change);
        Update_Image();
    }
}



void MainWindow::on_horizontalSlider_adjust_G_valueChanged(int value)
{
    NoFile_Warning();
    //qDebug() << "value changed:" << value;
    static int previous_value=0;
    if(abs(value-previous_value)>5){
        qDebug() << "value change";
        previous_value = value;

        Process change("Adjust","G",value);
        ExecStack.push(change);
        Update_Image();
    }

}


void MainWindow::on_horizontalSlider_adjust_R_valueChanged(int value)
{
    NoFile_Warning();
    //qDebug() << "value changed:" << value;
    static int previous_value=0;
    if(abs(value-previous_value)>5){
        qDebug() << "value change";
        previous_value = value;

        Process change("Adjust","R",value);
        ExecStack.push(change);
        Update_Image();
    }
}


void MainWindow::on_horizontalSlider_adjust_H_valueChanged(int value)
{
    NoFile_Warning();
    //qDebug() << "value changed:" << value;
    static int previous_value=0;
    if(abs(value-previous_value)>5){
        qDebug() << "value change";
        previous_value = value;

        Process change("Adjust","H",value);
        ExecStack.push(change);
        Update_Image();
    }
}


void MainWindow::on_horizontalSlider_adjust_S_valueChanged(int value)
{
    NoFile_Warning();
    //qDebug() << "value changed:" << value;
    static int previous_value=0;
    if(abs(value-previous_value)>5){
        qDebug() << "value change";
        previous_value = value;

        Process change("Adjust","S",value);
        ExecStack.push(change);
        Update_Image();
    }
}


void MainWindow::on_horizontalSlider_adjust_V_valueChanged(int value)
{
    NoFile_Warning();
    //qDebug() << "value changed:" << value;
    static int previous_value=0;
    if(abs(value-previous_value)>5){
        qDebug() << "value change";
        previous_value = value;

        Process change("Adjust","V",value);
        ExecStack.push(change);
        Update_Image();
    }
}


void MainWindow::on_pushButton_undo_clicked()
{
    NoFile_Warning();
    Process Last = ExecStack.top();
    ExecStack.pop();
    TemStack.push(Last);
    Update_Image();
}


void MainWindow::on_pushButton_redo_clicked()
{
    NoFile_Warning();
    if(!TemStack.empty()){
    Process Last = TemStack.top();
    TemStack.pop();
    ExecStack.push(Last);
    ui->pushButton_redo->setEnabled(true);
    }

    Update_Image();
}


void MainWindow::on_pushButton_reset_clicked()
{
    NoFile_Warning();
    stack<Process>empty;
    ExecStack = empty;
    TemStack = empty;
    Settings();
    Update_Image();

}


void MainWindow::on_comboBox_select_filter_currentTextChanged(const QString &arg1)
{
    //NoFile_Warning();
    ui->horizontalSlider_filter->setValue(7);
}




void MainWindow::on_horizontalSlider_filter_valueChanged(int value)
{
    //NoFile_Warning();
    int k_size;
    if(value%2==0)
        k_size=value-1;
    else
        k_size=value;

    if(ui->comboBox_select_filter->currentText()=="Box filter"){
        Process Filt("Filter","Box",k_size);
        ExecStack.push(Filt);
        Update_Image();
    }
    if(ui->comboBox_select_filter->currentText()=="Gaussian"){
        Process Filt("Filter","Gaussian",k_size);
        ExecStack.push(Filt);
        Update_Image();
    }
    if(ui->comboBox_select_filter->currentText()=="Median"){
        Process Filt("Filter","Median",k_size);
        ExecStack.push(Filt);
        Update_Image();
    }
    if(ui->comboBox_select_filter->currentText()=="Sharpen"){
        Process Filt("Filter","Sharpen",k_size);
        ExecStack.push(Filt);
        Update_Image();
    }
    if(ui->comboBox_select_filter->currentText()=="Noise"){
        Process Filt("Filter","Noise",k_size);
        ExecStack.push(Filt);
        Update_Image();
    }

}


void MainWindow::Settings(){

    ui->label_Image->setAlignment(Qt::AlignCenter);

    // Adjust
    ui->spinBox_adjust_B->setMinimum(-255);
    ui->spinBox_adjust_B->setMaximum(255);
    ui->spinBox_adjust_B->setSingleStep(1);

    ui->horizontalSlider_adjust_B->setMinimum(-255);
    ui->horizontalSlider_adjust_B->setMaximum(255);
    ui->horizontalSlider_adjust_B->setSingleStep(5);

    connect(ui->spinBox_adjust_B, SIGNAL(valueChanged(int)),ui->horizontalSlider_adjust_B, SLOT(setValue(int)));
    connect(ui->horizontalSlider_adjust_B, SIGNAL(valueChanged(int)),ui->spinBox_adjust_B, SLOT(setValue(int)));
    ui->spinBox_adjust_B->setValue(0);

    ui->spinBox_adjust_G->setMinimum(-255);
    ui->spinBox_adjust_G->setMaximum(255);
    ui->spinBox_adjust_G->setSingleStep(1);

    ui->horizontalSlider_adjust_G->setMinimum(-255);
    ui->horizontalSlider_adjust_G->setMaximum(255);
    ui->horizontalSlider_adjust_G->setSingleStep(5);

    connect(ui->spinBox_adjust_G, SIGNAL(valueChanged(int)),ui->horizontalSlider_adjust_G, SLOT(setValue(int)));
    connect(ui->horizontalSlider_adjust_G, SIGNAL(valueChanged(int)),ui->spinBox_adjust_G, SLOT(setValue(int)));
    ui->spinBox_adjust_G->setValue(0);

    ui->spinBox_adjust_R->setMinimum(-255);
    ui->spinBox_adjust_R->setMaximum(255);
    ui->spinBox_adjust_R->setSingleStep(1);

    ui->horizontalSlider_adjust_R->setMinimum(-255);
    ui->horizontalSlider_adjust_R->setMaximum(255);
    ui->horizontalSlider_adjust_R->setSingleStep(5);

    connect(ui->spinBox_adjust_R, SIGNAL(valueChanged(int)),ui->horizontalSlider_adjust_R, SLOT(setValue(int)));
    connect(ui->horizontalSlider_adjust_R, SIGNAL(valueChanged(int)),ui->spinBox_adjust_R, SLOT(setValue(int)));
    ui->spinBox_adjust_R->setValue(0);

    ui->spinBox_adjust_H->setMinimum(-255);
    ui->spinBox_adjust_H->setMaximum(255);
    ui->spinBox_adjust_H->setSingleStep(1);

    ui->horizontalSlider_adjust_H->setMinimum(-255);
    ui->horizontalSlider_adjust_H->setMaximum(255);
    ui->horizontalSlider_adjust_H->setSingleStep(5);

    connect(ui->spinBox_adjust_H, SIGNAL(valueChanged(int)),ui->horizontalSlider_adjust_H, SLOT(setValue(int)));
    connect(ui->horizontalSlider_adjust_H, SIGNAL(valueChanged(int)),ui->spinBox_adjust_H, SLOT(setValue(int)));
    ui->spinBox_adjust_H->setValue(0);

    ui->spinBox_adjust_S->setMinimum(-255);
    ui->spinBox_adjust_S->setMaximum(255);
    ui->spinBox_adjust_S->setSingleStep(1);

    ui->horizontalSlider_adjust_S->setMinimum(-255);
    ui->horizontalSlider_adjust_S->setMaximum(255);
    ui->horizontalSlider_adjust_S->setSingleStep(5);

    connect(ui->spinBox_adjust_S, SIGNAL(valueChanged(int)),ui->horizontalSlider_adjust_S, SLOT(setValue(int)));
    connect(ui->horizontalSlider_adjust_S, SIGNAL(valueChanged(int)),ui->spinBox_adjust_S, SLOT(setValue(int)));
    ui->spinBox_adjust_S->setValue(0);

    ui->spinBox_adjust_V->setMinimum(-255);
    ui->spinBox_adjust_V->setMaximum(255);
    ui->spinBox_adjust_V->setSingleStep(1);

    ui->horizontalSlider_adjust_V->setMinimum(-255);
    ui->horizontalSlider_adjust_V->setMaximum(255);
    ui->horizontalSlider_adjust_V->setSingleStep(5);

    connect(ui->spinBox_adjust_V, SIGNAL(valueChanged(int)),ui->horizontalSlider_adjust_V, SLOT(setValue(int)));
    connect(ui->horizontalSlider_adjust_V, SIGNAL(valueChanged(int)),ui->spinBox_adjust_V, SLOT(setValue(int)));
    ui->spinBox_adjust_V->setValue(0);

    // Filter
    ui->comboBox_select_filter->clear();
    QStringList filterList;
    filterList << "None" << "Box filter" << "Gaussian" << "Median" << "Sharpen"  << "Noise";
    ui->comboBox_select_filter->addItems(filterList);
    ui->comboBox_select_filter->setCurrentIndex(0);

    ui->horizontalSlider_filter->setMinimum(1);
    ui->horizontalSlider_filter->setMaximum(21);
    ui->horizontalSlider_filter->setSingleStep(2);
    ui->spinBox_kernel_size->setSingleStep(2);
    connect(ui->spinBox_kernel_size, SIGNAL(valueChanged(int)),ui->horizontalSlider_filter, SLOT(setValue(int)));
    connect(ui->horizontalSlider_filter, SIGNAL(valueChanged(int)),ui->spinBox_kernel_size, SLOT(setValue(int)));
    ui->spinBox_kernel_size->setValue(7);

    // HSV range
    ui->horizontalSlider_range_H_lower->setMinimum(0);
    ui->horizontalSlider_range_H_lower->setMaximum(255);
       ui->spinBox_range_H_lower->setMaximum(255);
    ui->horizontalSlider_range_H_lower->setSingleStep(1);
    connect(ui->spinBox_range_H_lower, SIGNAL(valueChanged(int)),ui->horizontalSlider_range_H_lower, SLOT(setValue(int)));
    connect(ui->horizontalSlider_range_H_lower, SIGNAL(valueChanged(int)),ui->spinBox_range_H_lower, SLOT(setValue(int)));
    ui->horizontalSlider_range_H_lower->setValue(0);

    ui->horizontalSlider_range_H_upper->setMinimum(0);
    ui->horizontalSlider_range_H_upper->setMaximum(255);
      ui->spinBox_range_H_upper->setMaximum(255);
    ui->horizontalSlider_range_H_upper->setSingleStep(1);
    connect(ui->spinBox_range_H_upper, SIGNAL(valueChanged(int)),ui->horizontalSlider_range_H_upper, SLOT(setValue(int)));
    connect(ui->horizontalSlider_range_H_upper, SIGNAL(valueChanged(int)),ui->spinBox_range_H_upper, SLOT(setValue(int)));
    ui->horizontalSlider_range_H_upper->setValue(255);

    ui->horizontalSlider_range_S_lower->setMinimum(0);
    ui->horizontalSlider_range_S_lower->setMaximum(255);
       ui->spinBox_range_S_lower->setMaximum(255);
    ui->horizontalSlider_range_S_lower->setSingleStep(1);
    connect(ui->spinBox_range_S_lower, SIGNAL(valueChanged(int)),ui->horizontalSlider_range_S_lower, SLOT(setValue(int)));
    connect(ui->horizontalSlider_range_S_lower, SIGNAL(valueChanged(int)),ui->spinBox_range_S_lower, SLOT(setValue(int)));
    ui->horizontalSlider_range_S_lower->setValue(0);

    ui->horizontalSlider_range_S_upper->setMinimum(0);
    ui->horizontalSlider_range_S_upper->setMaximum(255);
      ui->spinBox_range_S_upper->setMaximum(255);
    ui->horizontalSlider_range_S_upper->setSingleStep(1);
    connect(ui->spinBox_range_S_upper, SIGNAL(valueChanged(int)),ui->horizontalSlider_range_S_upper, SLOT(setValue(int)));
    connect(ui->horizontalSlider_range_S_upper, SIGNAL(valueChanged(int)),ui->spinBox_range_S_upper, SLOT(setValue(int)));
    ui->horizontalSlider_range_S_upper->setValue(255);

    ui->horizontalSlider_range_V_lower->setMinimum(0);
    ui->horizontalSlider_range_V_lower->setMaximum(255);
       ui->spinBox_range_V_lower->setMaximum(255);
    ui->horizontalSlider_range_V_lower->setSingleStep(1);
    connect(ui->spinBox_range_V_lower, SIGNAL(valueChanged(int)),ui->horizontalSlider_range_V_lower, SLOT(setValue(int)));
    connect(ui->horizontalSlider_range_V_lower, SIGNAL(valueChanged(int)),ui->spinBox_range_V_lower, SLOT(setValue(int)));
    ui->horizontalSlider_range_V_lower->setValue(0);

    ui->horizontalSlider_range_V_upper->setMinimum(0);
    ui->horizontalSlider_range_V_upper->setMaximum(255);
      ui->spinBox_range_V_upper->setMaximum(255);
    ui->horizontalSlider_range_V_upper->setSingleStep(1);
    connect(ui->spinBox_range_V_upper, SIGNAL(valueChanged(int)),ui->horizontalSlider_range_V_upper, SLOT(setValue(int)));
    connect(ui->horizontalSlider_range_V_upper, SIGNAL(valueChanged(int)),ui->spinBox_range_V_upper, SLOT(setValue(int)));
    ui->horizontalSlider_range_V_upper->setValue(255);

    stack<Process>empty;
    ExecStack = empty;

    Update_Image();

}


void MainWindow::on_horizontalSlider_range_H_lower_valueChanged(int value)
{
    NoFile_Warning();
    //qDebug() << "value changed:" << value;
    Process change("Range","H_lower",value);
    ExecStack.push(change);
    Update_Image();
}


void MainWindow::on_horizontalSlider_range_S_lower_valueChanged(int value)
{
    NoFile_Warning();
    //qDebug() << "value changed:" << value;
    Process change("Range","S_lower",value);
    ExecStack.push(change);
    Update_Image();
}


void MainWindow::on_horizontalSlider_range_V_lower_valueChanged(int value)
{
    NoFile_Warning();
    //qDebug() << "value changed:" << value;
    Process change("Range","V_lower",value);
    ExecStack.push(change);
    Update_Image();
}


void MainWindow::on_horizontalSlider_range_H_upper_valueChanged(int value)
{
    //NoFile_Warning();
    //qDebug() << "value changed:" << value;
    Process change("Range","H_upper",value);
    ExecStack.push(change);
    Update_Image();
}


void MainWindow::on_horizontalSlider_range_S_upper_valueChanged(int value)
{
    //NoFile_Warning();
    //qDebug() << "value changed:" << value;
    Process change("Range","S_upper",value);
    ExecStack.push(change);
    Update_Image();
}


void MainWindow::on_horizontalSlider_range_V_upper_valueChanged(int value)
{
    //NoFile_Warning();
    //qDebug() << "value changed:" << value;
    Process change("Range","V_upper",value);
    ExecStack.push(change);
    Update_Image();
}


void MainWindow::on_pushButton_flip_H_clicked()
{
    NoFile_Warning();
    qDebug() << "flip H";
    Process change("Else","Flip_H");
    ExecStack.push(change);
    Update_Image();
}


void MainWindow::on_pushButton_flip_V_clicked()
{
    NoFile_Warning();
    qDebug() << "flip V";
    Process change("Else","Flip_V");
    ExecStack.push(change);
    Update_Image();
}


void MainWindow::on_pushButton_rotate_clicked()
{
    NoFile_Warning();
    qDebug() << "rotate";
    Process change("Else","Rotate");
    ExecStack.push(change);
    Update_Image();
}



void MainWindow::on_pushButton_rotate_L_clicked()
{
    NoFile_Warning();
    qDebug() << "rotate";
    Process change("Else","Rotate_L");
    ExecStack.push(change);
    Update_Image();
}



