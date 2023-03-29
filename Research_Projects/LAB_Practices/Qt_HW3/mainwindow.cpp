#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QString>
#include <QMouseEvent>
#include <QLabel>
#include <QDebug>
#include <QPainter>
#include <QPaintEvent>
#include <QCursor>

static int init_x,init_y;
static int cur_x,cur_y;
static int final_x,final_y;


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    ui->label_press->setVisible(false);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::paintEvent(QPaintEvent *event){
    QPainter p;
    p.begin(this);

    QPen pen_preview;
    pen_preview.setWidth(3);
    pen_preview.setStyle(Qt::DashLine);
    pen_preview.setColor(QColor(255,0,0));

    QPen pen;
    pen.setWidth(5);
    pen.setColor(QColor(255,0,0));


    QBrush brush;
    brush.setStyle(Qt::NoBrush);
    p.setBrush(brush);

    if(ui->radioButton_line->isChecked()){
        p.setPen(pen_preview);
        p.drawLine(QPoint(init_x,init_y),QPoint(cur_x,cur_y));
        p.setPen(pen);
        p.drawLine(QPoint(init_x,init_y),QPoint(final_x,final_y));
    }
    else if (ui->radioButton_rect->isChecked()) {
        p.setPen(pen_preview);
        p.drawRect(init_x,init_y,cur_x-init_x,cur_y-init_y);
        p.setPen(pen);
        p.drawRect(init_x,init_y,final_x-init_x,final_y-init_y);
    }
    else if (ui->radioButton_circle->isChecked()) {
        p.setPen(pen_preview);
        //p.drawRect(init_x,init_y,cur_x-init_x,cur_y-init_y);
        p.drawEllipse(QPoint((init_x+cur_x)/2,(init_y+cur_y)/2),(cur_y-init_y)/2,(cur_y-init_y)/2);
        p.setPen(pen);
        p.drawEllipse(QPoint((init_x+final_x)/2,(init_y+final_y)/2),(final_y-init_y)/2,(final_y-init_y)/2);
    }
    else if (ui->radioButton_ellipse->isChecked()) {
        p.setPen(pen_preview);
        //p.drawRect(init_x,init_y,cur_x-init_x,cur_y-init_y);
        p.drawEllipse(QPoint((init_x+cur_x)/2,(init_y+cur_y)/2),(cur_x-init_x)/2,(cur_y-init_y)/2);
        p.setPen(pen);
        p.drawEllipse(QPoint((init_x+final_x)/2,(init_y+final_y)/2),(final_x-init_x)/2,(final_y-init_y)/2);
    }

    p.end();
    qDebug() << "painting...";
}

void MainWindow::mouseMoveEvent(QMouseEvent* event){

    cur_x = event->pos().x();
    cur_y = event->pos().y();

    QString x = QString::number(cur_x);
    QString y = QString::number(cur_y);
    QString coord = "(" + x +", " + y + ")";
    ui->label_position->setText(coord);
    QFont f( "Arial", 20, QFont::Bold);
    ui->label_position->setFont(f);
    update();

}

void MainWindow::mousePressEvent(QMouseEvent *event){
    this->setCursor(Qt::CrossCursor);
    if(event->button() == Qt::LeftButton){
        ui->label_press->setText("press");
        init_x = event->pos().x();
        init_y = event->pos().y();
        qDebug() << "initial pos: " << init_x << init_y;
        cur_x = final_x = init_x;
        cur_y = final_y = init_y;
    }

}

void MainWindow::mouseReleaseEvent(QMouseEvent *event){
    this->setCursor(Qt::ArrowCursor);
    if(event->button() == Qt::LeftButton){
        ui->label_press->setText("release");
        final_x = event->pos().x();
        final_y = event->pos().y();
        qDebug() << "final pos: " << final_x << final_y;
        update();
    }

}
