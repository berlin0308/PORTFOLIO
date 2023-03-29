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

using namespace std;
using namespace cv;


MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_pushButton_clicked()
{
    QString filePath = QFileDialog::getOpenFileName(this,tr("Open File"),"",tr("image(*.png *.jpeg *.jpg)"));
    string fileName = filePath.toStdString();
    cout << fileName;
    Mat img,img_resized,img_gray,display,kernal;
    img = imread(fileName);
    cv::resize(img,img_resized,Size(img.cols*2,img.rows*2),0,0,INTER_LINEAR);

    cvtColor(img_resized,img_gray,COLOR_RGB2GRAY);
    cv::threshold(img_gray,img_gray,120,255,THRESH_BINARY);

    Mat kernel = getStructuringElement(MORPH_RECT,Size(11,11));
    cv::erode(img_gray,img_gray,kernel);

    cvtColor(img_gray,img_gray,COLOR_GRAY2RGB);
    hconcat(img_resized,img_gray,display);
    imshow("image",display);
    waitKey(0);

}

