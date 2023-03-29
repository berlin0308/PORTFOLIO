#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <qdebug.h>
#include <string>
#include <iostream>
using namespace std;

static int payment = 0;

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    this->setWindowTitle("Ordering System");
}

MainWindow::~MainWindow()
{
    delete ui;
}



void MainWindow::on_buttonBox_rejected()
{
    qDebug() << "ButtonBox rejected";
    payment = 0;
    ui->label_TotalPrice->setText("Total: $0");
    ui->checkBox_A->setChecked(false);
    ui->checkBox_B->setChecked(false);
    ui->checkBox_C->setChecked(false);
    ui->checkBox_D->setChecked(false);
    ui->checkBox_E->setChecked(false);
    ui->checkBox_F->setChecked(false);
}

void MainWindow::on_buttonBox_accepted()
{

    qDebug() << "ButtonBox accepted";

    payment = 0;
    if(ui->checkBox_A->checkState()==Qt::Checked){
        payment += 200;
    }
    if(ui->checkBox_B->checkState()==Qt::Checked){
        payment += 180;
    }
    if(ui->checkBox_C->checkState()==Qt::Checked){
        payment += 160;
    }
    if(ui->checkBox_D->checkState()==Qt::Checked){
        payment += 60;
    }
    if(ui->checkBox_E->checkState()==Qt::Checked){
        payment += 50;
    }
    if(ui->checkBox_F->checkState()==Qt::Checked){
        payment += 40;
    }

    if(ui->button_Cash->isChecked()){
        payment -= 30;
    }
    else if(ui->button_CreditCard->isChecked()){
        payment *= 0.9;
    }
    else{
        qDebug() << "the payment method hasn't be determined";
        ui->label_TotalPrice->setText("the payment method!");
        return;
    }

    qDebug() << "Total Price:" << payment;
    string str;
    str = to_string(payment);
    QString Qstr = QString::fromStdString(str);
    ui->label_TotalPrice->setText("Total: $"+Qstr);
}
