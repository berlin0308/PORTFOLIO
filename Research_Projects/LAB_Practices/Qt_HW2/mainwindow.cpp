#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QFileDialog>
#include <QPixmap>
#include <QDebug>
#include <QFile>
#include <QTextStream>
#include <QString>
#include <QFileInfo>
#include <QTextEdit>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_pushButton_select_image_clicked()
{
    QString filepath = QFileDialog::getOpenFileName(this,tr("Open a file"),"",tr("image (*.png *.jpg *.jepg )"));
    QPixmap pix(filepath);
    int w = pix.width();
    int h = pix.height();

    int w_scaled;
    int h_scaled;

    if(w>h){
        w_scaled = 200;
        h_scaled = 200*h/w;
    }
    else{
        w_scaled = 200*w/h;
        h_scaled = 200;
    }
    qDebug() << w_scaled << h_scaled;

    ui->label_show_image->setPixmap(pix.scaled(w_scaled,h_scaled,Qt::KeepAspectRatio));
    ui->label_show_image->setAlignment(Qt::AlignCenter);
}

void MainWindow::on_pushButton_openfile_clicked()
{
    QString filepath = QFileDialog::getOpenFileName(this,tr("Open a file"),"",tr("Text (*.txt )"));
    QFile fileRead(filepath);
    QFileInfo info(filepath);

    QString browserTitle = "File Name: ";
    QString FileName = info.fileName();
    QString Title = browserTitle+FileName;
    ui->label_Browser->setText(Title);
    ui->textBrowser_Browser->setText("");
    if(fileRead.open(QIODevice::ReadOnly)){
        QTextStream input(&fileRead);
        input.setCodec("UTF-8");
        while(!input.atEnd()){
            QString line = input.readLine();
            ui->textBrowser_Browser->append(line.toStdString().data());

        }
        fileRead.close();
    }
}

void MainWindow::on_pushButton_clear_clicked()
{
    ui->textBrowser_Browser->setText("");
}

void MainWindow::on_pushButton_writefile_clicked()
{
    QString UserInput = ui->textEdit_put_text->toPlainText();
    qDebug() << "Text Edited:" << UserInput;
    QString filepath = QFileDialog::getOpenFileName(this,tr("Open a file"),"",tr("Text (*.txt )"));
    QFile fileWrite(filepath);

    if(fileWrite.open(QIODevice::WriteOnly | QIODevice::Text)){
        fileWrite.flush();
        QTextStream output(&fileWrite);
        output << UserInput << endl;
        fileWrite.close();
    }
}

void MainWindow::on_pushButton_add2file_clicked()
{
    QString UserInput = ui->textEdit_put_text->toPlainText();
    qDebug() << "Text Edited:" << UserInput;
    QString filepath = QFileDialog::getOpenFileName(this,tr("Open a file"),"",tr("Text (*.txt )"));
    QFile fileWrite(filepath);

    if(fileWrite.open(QIODevice::WriteOnly | QIODevice::Append | QIODevice::Text)){
        fileWrite.flush();
        QTextStream output(&fileWrite);
        output << UserInput << endl;
        fileWrite.close();
    }
}
