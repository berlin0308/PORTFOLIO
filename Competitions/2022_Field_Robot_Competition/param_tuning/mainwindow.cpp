#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <iostream>
#include <QFileDialog>
#include <QString>
#include <QFile>
#include <QTextStream>
#include <QImage>
#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgcodecs.hpp>
#include <cmath>

using namespace std;
using namespace cv;

Mat img,img_cannied,img_lined;
vector<Vec4i>img_lines;

String fileName;

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    ui->spinBox_erode->setMaximum(1001);
    ui->spinBox_hl_minLineGap->setMaximum(1000);
    ui->spinBox_hl_minLineLength->setMaximum(1000);
    ui->spinBox_hl_threshold->setMaximum(1000);

    ui->spinBox_erode->setValue(3);
    ui->spinBox_hl_threshold->setValue(40);

    ui->spinBox_hl_minLineLength->setValue(40);

    ui->spinBox_hl_minLineGap->setValue(40);
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_pushButton_openfile_clicked()
{
    QString filePath = QFileDialog::getOpenFileName(this,tr("Open File"),"",tr("image(*.png *.jpeg *.jpg)"));
    fileName = filePath.toStdString();
    //fileName = "C:\\Users\\BERLIN CHEN\\Desktop\\DDLAB\\PRO\\OpenCV_HW3\\color_ring_processed.jpg";

    //qDebug() << filePath;
    img = imread(fileName);
    cvtColor(img,img,COLOR_BGR2GRAY);


    const int label_w = ui->label->width();
    const int label_h = ui->label->height();
    ui->label->setPixmap(QPixmap::fromImage(cvMat_to_QImage(img).scaled(label_w,label_h,Qt::KeepAspectRatio)));

}

QImage MainWindow::cvMat_to_QImage(const cv::Mat &mat ) {
  switch ( mat.type() )
  {
     // 8-bit, 4 channel
     case CV_8UC4:
     {
        QImage image( mat.data, mat.cols, mat.rows, mat.step, QImage::Format_RGB32 );
        return image;
     }

     // 8-bit, 3 channel
     case CV_8UC3:
     {
        QImage image( mat.data, mat.cols, mat.rows, mat.step, QImage::Format_RGB888 );
        return image.rgbSwapped();
     }

     // 8-bit, 1 channel
     case CV_8UC1:
     {
        static QVector<QRgb>  sColorTable;
        // only create our color table once
        if ( sColorTable.isEmpty() )
        {
           for ( int i = 0; i < 256; ++i )
              sColorTable.push_back( qRgb( i, i, i ) );
        }
        QImage image( mat.data, mat.cols, mat.rows, mat.step, QImage::Format_Indexed8 );
        image.setColorTable( sColorTable );
        return image;
     }

     default:
        qDebug("Image format is not supported: depth=%d and %d channels\n", mat.depth(), mat.channels());
        break;
  }
  return QImage();
}




void MainWindow::on_pushButton_erode_clicked()
{

    int k = ui->spinBox_erode->value();
    Mat kernel_er = getStructuringElement(MORPH_RECT,Size(k,k));
    cv::erode(img,img,kernel_er);

    const int label_w = ui->label_2->width();
    const int label_h = ui->label_2->height();
    ui->label_2->setPixmap(QPixmap::fromImage(cvMat_to_QImage(img).scaled(label_w,label_h,Qt::KeepAspectRatio)));

}


void MainWindow::on_pushButton_canny_clicked()
{
    cv::Canny(img,img_cannied,100,200);

    const int label_w = ui->label_3->width();
    const int label_h = ui->label_3->height();
    ui->label_3->setPixmap(QPixmap::fromImage(cvMat_to_QImage(img_cannied).scaled(label_w,label_h,Qt::KeepAspectRatio)));

}


void MainWindow::on_pushButton_hl_clicked()
{
    cv::HoughLinesP(img_cannied,img_lines,1,0.017444,ui->spinBox_hl_threshold->value(),ui->spinBox_hl_minLineLength->value(),ui->spinBox_hl_minLineGap->value());

    img_lined=img;
    cv::cvtColor(img_lined,img_lined,COLOR_GRAY2BGR);


    for(size_t i=0;i<img_lines.size();i++){
        Vec4i l = img_lines[i];
        cv::line(img_lined,Point(l[0],l[1]),Point(l[2],l[3]),Scalar(255,0,0),3,LINE_AA);
    }

    const int label_w = ui->label_4->width();
    const int label_h = ui->label_4->height();
    ui->label_4->setPixmap(QPixmap::fromImage(cvMat_to_QImage(img_lined).scaled(label_w,label_h,Qt::KeepAspectRatio)));
}

