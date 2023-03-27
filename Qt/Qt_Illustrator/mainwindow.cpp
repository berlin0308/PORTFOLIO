#include "mainwindow.h"
#include "qmenubar.h"
#include "ui_mainwindow.h"
#include "utility.h"
#include <QAction>
#include <QColorDialog>
#include <QColor>
#include <iostream>
#include <stack>
#include <QDebug>
#include <QString>
#include <QMouseEvent>
#include <QLabel>
#include <QDebug>
#include <QPainter>
#include <QPaintEvent>
#include <QCursor>
#include <QPainterPath>
#include <QEvent>
#include <QKeyEvent>
#include <QFileDialog>
#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgcodecs.hpp>
#include <QImage>
#include <QMessageBox>
#include <QDesktopServices>
#include <QUrl>



using namespace std;
using namespace cv;

static int init_x,init_y;
static int cur_x,cur_y;
static int final_x,final_y;

stack<Move> emptyMoveStack;
stack<QPoint>pencilTemStack;
static bool PencilState = false;
static bool select_mode=false;
static bool move_mode = false;

static bool add_image_mode = false;
static bool add_text_mode = false;

QString SHAPE = "pencil";
QColor COLOR;
int WIDTH = 3;
QString STYLE = "Solid";
bool FILL = false;

string fileName;
string fileName_save;
Mat img_read;
Mat img_import;
bool new_background;
QImage img_painted;
QFont import_text_font("Microsoft JhengHei UI");
int import_text_size=12;


MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    setMenuBar();
    setAppearance();
    setWidgetFunc();
    setFocusPolicy(Qt::StrongFocus);
    ui->tabWidget->raise();
    this->setWindowTitle("Illustrator");
    setDefualtTheme();
    //setDarkTheme();
    //setWhiteTheme();
    //setBlueTheme();
    //setWarmTheme();
}

MainWindow::~MainWindow()
{
    delete ui;
}



void MainWindow::paintEvent(QPaintEvent *event){


    // 1. process select actions, change values in Moves in curStack
    // 2. display Moves in curStack


    /*
    qDebug() << "\n\nselect mode:" << select_mode;
    qDebug() << "\nSHAPE:" << SHAPE;
    qDebug() << "COLOR:" << COLOR;
    qDebug() << "WIDTH:" << WIDTH;
    qDebug() << "STYLE:" << STYLE;
    qDebug() << "FILL:" << FILL;
    */

    /*
    if(temStack.empty())
       ui->pushButton_redo->setEnabled(false);
    }
    else{
        ui->pushButton_redo->setEnabled(true);
    }

    if(curStack.empty()){
       ui->pushButton_undo->setEnabled(false);
       ui->checkBox_select->setEnabled(false);
    }
    else{
        ui->pushButton_undo->setEnabled(true);
        ui->checkBox_select->setEnabled(true);
    }
    */

    if(!select_mode || selStack.empty()){
        ui->pushButton_move->setEnabled(false);
        ui->pushButton_fill->setEnabled(false);
        ui->pushButton_unfill->setEnabled(false);
        ui->pushButton_delete->setEnabled(false);
        ui->pushButton_copy->setEnabled(false);
        ui->pushButton_paste->setEnabled(false);
        ui->pushButton_cut->setEnabled(false);

     }
    else{
        ui->pushButton_move->setEnabled(true);
        ui->pushButton_fill->setEnabled(true);
        ui->pushButton_unfill->setEnabled(true);
        ui->pushButton_delete->setEnabled(true);
        ui->pushButton_copy->setEnabled(true);
        ui->pushButton_paste->setEnabled(true);
        ui->pushButton_cut->setEnabled(true);
    }


    /* PROCESS SELECTED ACTIONS */

    stack<Move>curStack_processed;

    stack<Move>curStackCopy = StackInverse(curStack);


    setFocusPolicy(Qt::StrongFocus);


    while(!curStackCopy.empty()){

        Move theMove = curStackCopy.top();
        // check if the Move is in the selected fill stack

        //qDebug() << theMove.checkIfMoveSelected(theMove,selectedFillMoves);


        if(theMove.checkIfMoveSelected(theMove,selectedFillMoves)){
            theMove.Fill = true;
        }
        if(theMove.checkIfMoveSelected(theMove,selectedUnfillMoves)){
            theMove.Fill = false;
        }


        if(theMove.Shape=="pencil"){
            if(theMove.checkIfMoveSelected(theMove,selectedMoveMoves)){
                int add_up=20*(selectedMoveMoves_Up_count-selectedMoveMoves_Down_count);
                int add_right=20*(selectedMoveMoves_Right_count-selectedMoveMoves_Left_count);
                stack<QPoint> points = theMove.pencilPoints;
                stack<QPoint> newpoints;
                while(!points.empty()){
                    QPoint p = points.top();
                    points.pop();
                    p.setX(p.x() + add_right);
                    p.setY(p.y() - add_up);
                    newpoints.push(p);
                }
                theMove.pencilPoints = newpoints;

            }

        }
        else if(theMove.checkIfMoveSelected(theMove,selectedMoveMoves)){
            int add_up=20*(selectedMoveMoves_Up_count-selectedMoveMoves_Down_count);
            theMove.Y1 = theMove.Y1 - add_up;
            theMove.Y2 = theMove.Y2 - add_up;
            qDebug() << "change: Up-Down";

            int add_right=20*(selectedMoveMoves_Right_count-selectedMoveMoves_Left_count);
            theMove.X1 = theMove.X1 + add_right;
            theMove.X2 = theMove.X2 + add_right;
            qDebug() << "change: Right-Left";

        }


        curStack_processed.push(theMove);

        curStackCopy.pop();

    }

    //curStack = curStack_processed;
    //curStack_processed = StackInverse(curStack_processed);

    QPainter p;
    //QPixmap map(2000,1000);
    QImage image(QSize(700,600),QImage::Format_ARGB32);

    //image.fill("white");
    p.begin(&image);


    //map.fill(Qt::transparent);
    //p.begin(&map);
    //p->begin();

    if(!img_read.empty()){
        //qDebug() << "read img";
        ui->label_canva->setText("");
        const int label_w = ui->label_canva->width();
        const int label_h = ui->label_canva->height();
        //ui->label_canva->setPixmap(QPixmap::fromImage(cvMat_to_QImage(img_read).scaled(label_w,label_h,Qt::KeepAspectRatio)));
        QRect region(0,180,700,600);
        p.drawImage(region,cvMat_to_QImage(img_read).scaled(label_w,label_h,Qt::KeepAspectRatio));
    }
    else if(new_background){

        //qDebug() << "white bg";
        ui->label_canva->setText("");
        //ui->label_canva->setStyleSheet("QLabel { color : white; }");
        p.fillRect(0,200,2000,1000,QColor(255,255,255)); // background
    }
    else{
        //qDebug() << "No file!";
        ui->label_canva->setText("Put the File here");
        ui->label_canva->setStyleSheet("QLabel { background-color : light gray; color : white; }");
    }


    QString Filter = "None";

    /* DISPLAY ALL MOVES */
    stack<Move>curStackInverse = StackInverse(curStack_processed);
    while(!curStackInverse.empty()){

        Move theMove = curStackInverse.top();

        QPen pen;
        pen.setWidth(theMove.Width);
        pen.setColor(theMove.Color);

        if(theMove.Style=="Solid")
            pen.setStyle(Qt::SolidLine);

        if(theMove.Style=="Dash")
            pen.setStyle(Qt::DashLine);

        if(theMove.Style=="Dot")
            pen.setStyle(Qt::DotLine);

        if(theMove.Style=="Dash-Dot")
            pen.setStyle(Qt::DashDotLine);

        p.setPen(pen);

        QBrush brush;

        //qDebug() << "Fill:" <<theMove.Fill;
        if(theMove.Fill){
            brush.setStyle(Qt::SolidPattern);
            brush.setColor(theMove.Color);
        }
        else{
            brush.setStyle(Qt::NoBrush);
        }
        p.setBrush(brush);

        if(theMove.Shape=="clear"){
            if(!img_read.empty()){
                const int label_w = ui->label_canva->width();
                const int label_h = ui->label_canva->height();
                QRect region(0,180,700,600);
                p.drawImage(region,cvMat_to_QImage(img_read).scaled(label_w,label_h,Qt::KeepAspectRatio));
            }
            else{
                p.fillRect(0,200,750,500,QColor(255,255,255));
            }
            update();
             qDebug() << "clear";
        }
        if(theMove.Shape=="line"){
            p.drawLine(QPoint(theMove.X1,theMove.Y1),QPoint(theMove.X2,theMove.Y2));
            //qDebug() << "line";
        }
        if(theMove.Shape=="rect"){
            p.drawRect(theMove.X1,theMove.Y1,theMove.X2-theMove.X1,theMove.Y2-theMove.Y1);
            //qDebug() << "rect";
        }
        if(theMove.Shape=="circle"){
            p.drawEllipse(QPoint((theMove.X1+theMove.X2)/2,(theMove.Y1+theMove.Y2)/2),(theMove.Y2-theMove.Y1)/2,(theMove.Y2-theMove.Y1)/2);
            //qDebug() << "circle";
        }
        if(theMove.Shape=="ellipse"){
            p.drawEllipse(QPoint((theMove.X1+theMove.X2)/2,(theMove.Y1+theMove.Y2)/2),(theMove.X2-theMove.X1)/2,(theMove.Y2-theMove.Y1)/2);
            //qDebug() << "ellipse";
        }
        if(theMove.Shape=="pencil"){
            // qDebug() << "draw pencil points";
            // draw lines by reading theMove.pencilPoints
            stack<QPoint>pencilPointsCopy = theMove.pencilPoints;
            // qDebug() << pencilPointsCopy.size();

            if(pencilPointsCopy.size()!=0){
                QPainterPath path;
                path.moveTo(pencilPointsCopy.top());
                pencilPointsCopy.pop();
                while(!pencilPointsCopy.empty()){
                    path.lineTo(pencilPointsCopy.top());
                    pencilPointsCopy.pop();
                 }
                 p.drawPath(path);
            }

        }
        if(theMove.Shape=="image"){
            qDebug() << "show import image";
            //ui->label_canva->setPixmap(QPixmap::fromImage(theMove.importImage).scaled(ui->label_canva->width(),ui->label_canva->height(),Qt::KeepAspectRatio));
            p.drawImage(QRect(theMove.X1,theMove.Y1,theMove.X2-theMove.X1,theMove.Y2-theMove.Y1),theMove.importImage);
        }
        if(theMove.Shape=="text"){
            qDebug() << "show import text";
            QFont font = theMove.importTextFont;
            font.setPointSize(theMove.importTextSize);
            p.setFont(font);
            p.drawText(QRect(theMove.X1,theMove.Y1,theMove.X2-theMove.X1,theMove.Y2-theMove.Y1),theMove.importText);

        }
        if(theMove.Shape=="Gaussian"){
            qDebug() << "Gaussian Blur";
            Filter = "Gaussian";

        }


        curStackInverse.pop();
    }


    /* PREVIEW */
    QPen pen_preview;
    pen_preview.setWidth(2);
    pen_preview.setStyle(Qt::DashLine);
    pen_preview.setColor(QColor(0,0,0));
    p.setPen(pen_preview);

    QBrush brush;
    brush.setStyle(Qt::NoBrush);
    p.setBrush(brush);

    if(select_mode || add_image_mode || add_text_mode){
        p.drawRect(init_x,init_y,cur_x-init_x,cur_y-init_y);
    }
    else{
        if(SHAPE=="pencil"){
            // draw lines by reading pencilTemStack
            // but it always crashes...
        }
        if(SHAPE=="line"){
            p.drawLine(QPoint(init_x,init_y),QPoint(cur_x,cur_y));
        }
        if(SHAPE=="rect") {
            p.drawRect(init_x,init_y,cur_x-init_x,cur_y-init_y);
        }
        if(SHAPE=="circle") {
            //p.drawRect(init_x,init_y,cur_x-init_x,cur_y-init_y);
            p.drawEllipse(QPoint((init_x+cur_x)/2,(init_y+cur_y)/2),(cur_y-init_y)/2,(cur_y-init_y)/2);
        }
        if(SHAPE=="ellipse") {
            //p.drawRect(init_x,init_y,cur_x-init_x,cur_y-init_y);
            p.drawEllipse(QPoint((init_x+cur_x)/2,(init_y+cur_y)/2),(cur_x-init_x)/2,(cur_y-init_y)/2);
        }

    }

    //p.save();
    p.end();
    //image.save("C:/Users/BERLIN CHEN/Desktop/DDLAB/PRO/Qt_Illustrator/123.png","PNG");
    //ui->label_canva->setPixmap(QPixmap::fromImage(image).scaled(this->width(),this->height())); //,Qt::KeepAspectRatio));

    QRect rect(0, 260, 700, 320);
    QImage cropped = image.copy(rect);

    ui->label_canva->setPixmap(QPixmap::fromImage(cropped).scaled(ui->label_canva->width(),ui->label_canva->height())); //,Qt::KeepAspectRatio));
    img_painted = cropped;
    //qDebug() << "painting...";
}



void MainWindow::mousePressEvent(QMouseEvent *event){

    noFileWarning();

    this->setCursor(Qt::PointingHandCursor);
    if(event->button() == Qt::LeftButton){
        init_x = event->pos().x();
        init_y = event->pos().y();
        // qDebug() << "initial pos: " << init_x << init_y;

        if(select_mode || add_image_mode || add_text_mode){
            this->setCursor(Qt::CrossCursor);
        }
        else if(ui->horizontalSlider_shape_select->value()==0){
            PencilState = true;
            QPoint initPoint;
            initPoint.setX(init_x);
            initPoint.setY(init_y);
            pencilTemStack.push(initPoint);
            // qDebug() << pencilTemStack.size();
            // qDebug() << initPoint.x() << initPoint.y();
        }


        cur_x = final_x = init_x;
        cur_y = final_y = init_y;
    }

}

void MainWindow::mouseMoveEvent(QMouseEvent* event){

    cur_x = event->pos().x();
    cur_y = event->pos().y();

    /*
    QString x = QString::number(cur_x);
    QString y = QString::number(cur_y);
    QString coord = "(" + x +", " + y + ")";
    ui->label_position->setText(coord);
    QFont f( "Arial", 20, QFont::Bold);
    ui->label_position->setFont(f);
    */

    if(select_mode==true){

    }
    else if(PencilState==true){
        QPoint curPoint;
        curPoint.setX(cur_x);
        curPoint.setY(cur_y);
        pencilTemStack.push(curPoint);
        // qDebug() << curPoint.x() << curPoint.y();
        // qDebug() << "pencilTemStack size:" << pencilTemStack.size();
    }
    update();
}

void MainWindow::mouseReleaseEvent(QMouseEvent *event){
    this->setCursor(Qt::ArrowCursor);
    if(event->button() == Qt::LeftButton){
        final_x = event->pos().x();
        final_y = event->pos().y();
        // qDebug() << "final pos: " << final_x << final_y;
    }

    if(select_mode==true){ // select
        QPoint A;
        A.setX(init_x);
        A.setY(init_y);
        QPoint B;
        B.setX(final_x);
        B.setY(final_y);

        selStack = findMoveSelected(A,B);
        qDebug() << "Moves selected:" << selStack.size();
    }
    else if(add_text_mode){

        if(final_x<init_x)
            swap(final_x,init_x);
        if(final_y<init_y)
            swap(final_y,init_y);

        QString Text = ui->textEdit_import->toPlainText();
        QFont Font = import_text_font;
        int Size = import_text_size;

        Move T("text",QColor(0,0,0),0,"",false,init_x,init_y,final_x,final_y,emptyStack,"",emptyImg,Text,Font,Size);
        curStack.push(T);
        add_text_mode = false;
    }
    else if(add_image_mode){

        if(final_x<init_x)
            swap(final_x,init_x);
        if(final_y<init_y)
            swap(final_y,init_y);
        QImage Add = cvMat_to_QImage(img_import);
        Move Img("image",QColor(0,0,0),0,"",false,init_x,init_y,final_x,final_y,emptyStack,"",Add);
        curStack.push(Img);
        qDebug() << "import image";
        update();
    }
    else{ // line, rect, circle, ellipse, pencil
        if(PencilState==true){
            PencilState = false;
        }

        //qDebug() << "\nTotal pencilTemStack size:" << pencilTemStack.size();
        Move LastMove(SHAPE,COLOR,WIDTH,STYLE,FILL,init_x,init_y,final_x,final_y,pencilTemStack);
        curStack.push(LastMove);

    }



    qDebug() << "\ncurStack:" << curStack.size();
    qDebug() << "temStack:" << temStack.size();

    update();

    init_x=init_y=cur_x=cur_y=final_x=final_y=0;
    pencilTemStack = emptyStack;
}





void MainWindow::new_file(){ // click "new file" on menu
    qDebug() << "new file";
    new_background = true;
}

void MainWindow::open_file(){ // click "open file" on menu
    qDebug() << "open file";
    QString filePath = QFileDialog::getOpenFileName(this,tr("Open File"),"",tr("image(*.png *.jpeg *.jpg)"));
    fileName = filePath.toStdString();
    //fileName = "C:\\Users\\BERLIN CHEN\\Desktop\\DDLAB\\PRO\\OpenCV_HW3\\color_ring.jpg";

    qDebug() << filePath;
    img_read = cv::imread(fileName);


}


void MainWindow::save(){ // click "save" on menu
    qDebug() << "save";

    if(fileName_save.empty()){
        MainWindow::save_as();
    }
    else{
        img_painted.save(QString::fromStdString(fileName_save),"PNG");
    }


}

void MainWindow::save_as(){ // click "save as..." on menu
    qDebug() << "save as...";
    QString dir = QFileDialog::getExistingDirectory(this, tr("Open Directory"),
                                                 "/Desktop",
                                                 QFileDialog::ShowDirsOnly
                                                 | QFileDialog::DontResolveSymlinks);
     qDebug() << dir;
     fileName_save = dir.toStdString() + "/picture.png";
     img_painted.save(QString::fromStdString(fileName_save),"PNG");

     QString content = "The File has been saved!\n";
     content += "File path:";
     content += QString::fromStdString(fileName_save);

     QMessageBox::about(this,"File saved",content);
}

void MainWindow::undo(){ // click "undo" on menu
    qDebug() << "undo";
    if(!curStack.empty()){
        Move Last = curStack.top();
        curStack.pop();
        temStack.push(Last);
        update();
    }

}


void MainWindow::redo(){ // click "redo" on menu
    qDebug() << "redo";
    if(!temStack.empty()){
        Move Last = temStack.top();
        temStack.pop();
        curStack.push(Last);
        update();
    }
}

void MainWindow::clear(){ // click "clear" on menu
    qDebug() << "clear";
    Move Clear("clear");
    curStack.push(Clear);
}



void MainWindow::on_pushButton_color_ring_clicked()
{
    QColor color = QColorDialog::getColor(Qt::white,this);
    //qDebug() << "Color:"<<color.red() << color.green() << color.blue();
    COLOR = color;

    QPixmap R(200,200);
    R.fill(COLOR);
    setButtonBackImage(ui->pushButton_color_ring,R,200,200);
}

void MainWindow::setButtonBackImage(QPushButton *button,QPixmap pixmap,int sizeW, int sizeH)
{
//QPixmap pixmap(image);
QPixmap fitpixmap=pixmap.scaled(163,163).scaled(sizeW, sizeH, Qt::IgnoreAspectRatio, Qt::SmoothTransformation);
button->setIcon(QIcon(fitpixmap));
button->setIconSize(QSize(sizeW,sizeH));
//button->setFlat(false);
//button->setStyleSheet("QLineEdit { background-color: yellow }");
}

void MainWindow::setMenuBar(){

    QMenuBar *bar = menuBar();
    this->QMainWindow::setMenuBar(bar);

    QPixmap arrow_pix(":/new/arrow/arrow_icon.png");
    QIcon arrow_right(arrow_pix);
    QMenu *menu_file = bar->addMenu("File");
    QAction *newAction = menu_file->addAction(arrow_right,"new file");
    connect(newAction,&QAction::triggered,this, &MainWindow::new_file);
    menu_file->addSeparator();
    QAction *openAction = menu_file->addAction(arrow_right,"open file");
    connect(openAction,&QAction::triggered,this, &MainWindow::open_file);


    QMenu *menu_edit = bar->addMenu("Edit");
    QAction *undoAction = menu_edit->addAction(arrow_right,"undo");
    connect(undoAction,&QAction::triggered,this, &MainWindow::undo);
    menu_file->addSeparator();
    QAction *redoAction = menu_edit->addAction(arrow_right,"redo");
    connect(redoAction,&QAction::triggered,this, &MainWindow::redo);
    menu_file->addSeparator();
    QAction *clearAction = menu_edit->addAction(arrow_right,"clear");
    connect(clearAction,&QAction::triggered,this, &MainWindow::clear);

    QMenu *menu_save = bar->addMenu("Save");
    QAction *saveAction = menu_save->addAction(arrow_right,"save");
    connect(saveAction,&QAction::triggered,this, &MainWindow::save);
    menu_file->addSeparator();
    QAction *saveasAction = menu_save->addAction(arrow_right,"save as...");
    connect(saveasAction,&QAction::triggered,this, &MainWindow::save_as);

    QMenu *menu_setting = bar->addMenu("Setting");
    QAction *defaultAction = menu_setting->addAction(arrow_right,"default");
    connect(defaultAction,&QAction::triggered,this, &MainWindow::settingDefault);

    QMenu *themeAction = menu_setting->addMenu(arrow_right,"theme");
    QAction *defaultTheme = themeAction->addAction("default theme");
    connect(defaultTheme,&QAction::triggered,this, &MainWindow::setDefualtTheme);

    QPixmap pixmap(100,100);
    pixmap.fill(QColor("black"));
    QIcon BlackIcon(pixmap);
    QAction *darkTheme = themeAction->addAction(BlackIcon,"dark theme");
    connect(darkTheme,&QAction::triggered,this, &MainWindow::setDarkTheme);

    pixmap.fill(QColor("white"));
    QIcon WhiteIcon(pixmap);
    QAction *whiteTheme = themeAction->addAction(WhiteIcon,"white theme");
    connect(whiteTheme,&QAction::triggered,this, &MainWindow::setWhiteTheme);

    pixmap.fill(QColor("aliceblue"));
    QIcon BlueIcon(pixmap);
    QAction *blueTheme = themeAction->addAction(BlueIcon,"blue theme");
    connect(blueTheme,&QAction::triggered,this, &MainWindow::setBlueTheme);


    pixmap.fill(QColor("moccasin"));
    QIcon WarmIcon(pixmap);
    QAction *warmTheme = themeAction->addAction(WarmIcon,"warm theme");
    connect(warmTheme,&QAction::triggered,this, &MainWindow::setWarmTheme);

    QMenu *menu_about = bar->addMenu("About");
    QAction *aboutQtAction = menu_about->addAction(arrow_right,"about Qt");
    connect(aboutQtAction,&QAction::triggered,this, &MainWindow::aboutQt);

    QAction *aboutLabAction = menu_about->addAction(arrow_right,"about BBLab");
    connect(aboutLabAction,&QAction::triggered,this, &MainWindow::aboutLab);

}

void MainWindow::setAppearance(){

    this->setAutoFillBackground(true);


    QPixmap pencil(":/new/shapes/pencil.png");
    ui->label_pencil->setPixmap(pencil.scaled(ui->label_pencil->width(),ui->label_pencil->height(),Qt::KeepAspectRatio));
    QPixmap line(":/new/shapes/line.png");
    ui->label_line->setPixmap(line.scaled(ui->label_line->width(),ui->label_line->height(),Qt::KeepAspectRatio));
    QPixmap rect(":/new/shapes/rect.png");
    ui->label_rect->setPixmap(rect.scaled(ui->label_rect->width(),ui->label_rect->height(),Qt::KeepAspectRatio));
    QPixmap circle(":/new/shapes/circle.png");
    ui->label_circle->setPixmap(circle.scaled(ui->label_circle->width(),ui->label_circle->height(),Qt::KeepAspectRatio));
    QPixmap ellipse(":/new/shapes/ellipse.png");
    ui->label_ellipse->setPixmap(ellipse.scaled(ui->label_ellipse->width(),ui->label_ellipse->height(),Qt::KeepAspectRatio));


    QPixmap colorRing(":/new/image/color_ring.jpg");
    setButtonBackImage(ui->pushButton_color_ring,colorRing,200,200);

    QPixmap R(200,200);
    R.fill(QColor::fromHsv(2,230,255));
    setButtonBackImage(ui->pushButton_red,R,200,200);

    R.fill(QColor::fromHsv(10,230,255));
    setButtonBackImage(ui->pushButton_ro,R,200,200);

    R.fill(QColor::fromHsv(20,230,255));
    setButtonBackImage(ui->pushButton_o,R,200,200);

    R.fill(QColor::fromHsv(30,230,255));
    setButtonBackImage(ui->pushButton_oy,R,200,200);

    R.fill(QColor::fromHsv(45,230,255));
    setButtonBackImage(ui->pushButton_y,R,200,200);

    R.fill(QColor::fromHsv(60,230,255));
    setButtonBackImage(ui->pushButton_yg,R,200,200);

    R.fill(QColor::fromHsv(90,230,255));
    setButtonBackImage(ui->pushButton_g,R,200,200);

    R.fill(QColor::fromHsv(135,230,255));
    setButtonBackImage(ui->pushButton_gb,R,200,200);

    R.fill(QColor::fromHsv(180,230,255));
    setButtonBackImage(ui->pushButton_b,R,200,200);

    R.fill(QColor::fromHsv(200,230,255));
    setButtonBackImage(ui->pushButton_bp,R,200,200);

    R.fill(QColor::fromHsv(230,230,255));
    setButtonBackImage(ui->pushButton_p,R,200,200);

    R.fill(QColor::fromHsv(254,230,255));
    setButtonBackImage(ui->pushButton_pr,R,200,200);

    QPixmap move(":/new/select/move.png");
    setButtonBackImage(ui->pushButton_move,move,70,80);
    QPixmap cut(":/new/select/cut.png");
    setButtonBackImage(ui->pushButton_cut,cut,70,80);
    QPixmap paste(":/new/select/paste.png");
    setButtonBackImage(ui->pushButton_paste,paste,70,80);
    QPixmap copy(":/new/select/copy.png");
    setButtonBackImage(ui->pushButton_copy,copy,70,80);
    QPixmap fill(":/new/select/fill.png");
    setButtonBackImage(ui->pushButton_fill,fill,70,80);
    QPixmap unfill(":/new/select/unfill.png");
    setButtonBackImage(ui->pushButton_unfill,unfill,70,80);
    QPixmap select(":/new/select/select.png");
    setButtonBackImage(ui->pushButton_select,select,70,80);
    QPixmap del(":/new/select/delete.png");
    setButtonBackImage(ui->pushButton_delete,del,70,80);

}

void MainWindow::setWidgetFunc(){

    // SHAPE
    ui->horizontalSlider_shape_select->setMinimum(0);
    ui->horizontalSlider_shape_select->setMaximum(4);
    ui->horizontalSlider_shape_select->setSingleStep(1);
    ui->horizontalSlider_shape_select->setTickInterval(1);
    ui->horizontalSlider_shape_select->setTickPosition(QSlider::TicksAbove);
    ui->horizontalSlider_shape_select->setValue(0);

    // WIDTH
    ui->horizontalSlider_width->setMinimum(1);
    ui->horizontalSlider_width->setMaximum(11);
    ui->horizontalSlider_width->setSingleStep(1);
    connect(ui->horizontalSlider_width,SIGNAL(valueChanged(int)),ui->spinBox_width,SLOT(setValue(int)));
    connect(ui->spinBox_width,SIGNAL(valueChanged(int)),ui->horizontalSlider_width,SLOT(setValue(int)));
    ui->spinBox_width->setValue(3);

    // STYLE
    ui->comboBox_style_select->clear();
    QStringList styleList;
    styleList << "Solid" << "Dash" << "Dot" << "Dash-Dot";
    ui->comboBox_style_select->addItems(styleList);
    ui->comboBox_style_select->setCurrentIndex(0);

    // FILL
    ui->radioButton_unfill->setChecked(true);


    ui->spinBox_size->setMinimum(3);
    ui->spinBox_size->setMaximum(33);
    ui->spinBox_size->setValue(12);

}

void MainWindow::on_pushButton_select_clicked()
{
    if(select_mode){

        select_mode = false;
    }
    else{
        select_mode = true;
        selStack = emptyMoveStack;
        selectedFillMoves = emptyMoveStack;
        selectedUnfillMoves = emptyMoveStack;
    }

}




void MainWindow::on_comboBox_style_select_currentTextChanged(const QString &arg1)
{
    QString changedStyle = ui->comboBox_style_select->currentText();
    STYLE = changedStyle;
}


void MainWindow::on_spinBox_width_valueChanged(int arg1)
{
    WIDTH = arg1;
}


void MainWindow::on_horizontalSlider_shape_select_valueChanged(int value)
{
    qDebug() << value;
    switch(value){
    case 0:
        SHAPE = "pencil";
        //PencilState = true;
        break;
    case 1:
        SHAPE = "line";
        break;
    case 2:
        SHAPE = "rect";
        break;
    case 3:
        SHAPE = "circle";
        break;
    case 4:
        SHAPE = "ellipse";
        break;
    }
}


void MainWindow::on_radioButton_unfill_clicked()
{
    FILL = false;
}


void MainWindow::on_radioButton_fill_clicked()
{
    FILL = true;
}



void MainWindow::on_pushButton_fill_clicked()
{
    selectedFillMoves = selStack;
    //Move fill("fill");
    //curStack.push(fill);
    qDebug() << "\n--------------\nfill, Moves:" << selectedFillMoves.size();
    update();
}




void MainWindow::on_pushButton_unfill_clicked()
{
    selectedUnfillMoves = selStack;
    //Move unfill("unfill");
    //curStack.push(unfill);
    qDebug() << "\n--------------\nunfill, Moves:" << selectedUnfillMoves.size();
    update();
}


void MainWindow::on_pushButton_move_clicked()
{
    move_mode = !move_mode;
    if(move_mode)
        this->setCursor(Qt::SizeAllCursor);
    selectedMoveMoves = selStack;
    qDebug() << "\n--------------\nmove, Moves:" << selectedMoveMoves.size();
    update();
}

void MainWindow::keyPressEvent(QKeyEvent *event){

    setFocusPolicy(Qt::StrongFocus);

    qDebug() << "count:" << selectedMoveMoves_Up_count << selectedMoveMoves_Down_count << selectedMoveMoves_Left_count << selectedMoveMoves_Right_count;

    if(move_mode){
        if(((event->modifiers()& Qt::ControlModifier)) != 0 && event->key()==Qt::Key_N) {

            setFocusPolicy(Qt::StrongFocus);
            qDebug() << "Down";
            selectedMoveMoves_Down_count ++;
        }


        if(((event->modifiers()& Qt::ControlModifier)) != 0 && event->key()==Qt::Key_J){

            setFocusPolicy(Qt::StrongFocus);
            qDebug() << "Up";
            selectedMoveMoves_Up_count ++;
        }

        if(((event->modifiers()& Qt::ControlModifier)) != 0 && event->key()==Qt::Key_B){

            qDebug() << "Left";
            selectedMoveMoves_Left_count ++;
        }

        if(((event->modifiers()& Qt::ControlModifier)) != 0 && event->key()==Qt::Key_M){
            qDebug() << "Right";
            selectedMoveMoves_Right_count ++;
        }
    }



    if(((event->modifiers()& Qt::ControlModifier)) != 0 && event->key()==Qt::Key_S){
        qDebug() << "Select";
        ui->pushButton_select->setChecked(!ui->pushButton_select->isChecked());
        MainWindow::on_pushButton_select_clicked();
    }

    if(((event->modifiers()& Qt::ControlModifier)) != 0 && event->key()==Qt::Key_F){
        qDebug() << "Fill";
        MainWindow::on_pushButton_fill_clicked();
    }
    if(((event->modifiers()& Qt::ControlModifier)) != 0 && event->key()==Qt::Key_U){
        qDebug() << "Unfill";
        MainWindow::on_pushButton_unfill_clicked();
    }

    if(((event->modifiers()& Qt::ControlModifier)) != 0 && event->key()==Qt::Key_X){
        qDebug() << "Cut";
        MainWindow::on_pushButton_cut_clicked();
    }
    if(((event->modifiers()& Qt::ControlModifier)) != 0 && event->key()==Qt::Key_C){
        qDebug() << "Copy";
        MainWindow::on_pushButton_copy_clicked();
    }
    if(((event->modifiers()& Qt::ControlModifier)) != 0 && event->key()==Qt::Key_V){
        qDebug() << "Paste";
        MainWindow::on_pushButton_paste_clicked();
    }
    if(((event->modifiers()& Qt::ControlModifier)) != 0 && event->key()==Qt::Key_Delete){
        qDebug() << "Delete";
        MainWindow::on_pushButton_delete_clicked();
    }

    update();

}


void MainWindow::on_pushButton_red_clicked()
{
    QPixmap R(200,200);
    QColor Col = QColor::fromHsv(2,230,255);
    COLOR = Col;
    R.fill(Col);
    setButtonBackImage(ui->pushButton_color_ring,R,200,200);
}


void MainWindow::on_pushButton_ro_clicked()
{
    QPixmap R(200,200);
    QColor Col = QColor::fromHsv(10,230,255);
    COLOR = Col;
    R.fill(Col);
    setButtonBackImage(ui->pushButton_color_ring,R,200,200);
}


void MainWindow::on_pushButton_o_clicked()
{
    QPixmap R(200,200);
    QColor Col = QColor::fromHsv(20,230,255);
    COLOR = Col;
    R.fill(Col);
    setButtonBackImage(ui->pushButton_color_ring,R,200,200);
}


void MainWindow::on_pushButton_oy_clicked()
{
    QPixmap R(200,200);
    QColor Col = QColor::fromHsv(30,230,255);
    COLOR = Col;
    R.fill(Col);
    setButtonBackImage(ui->pushButton_color_ring,R,200,200);
}


void MainWindow::on_pushButton_y_clicked()
{
    QPixmap R(200,200);
    QColor Col = QColor::fromHsv(45,230,255);
    COLOR = Col;
    R.fill(Col);
    setButtonBackImage(ui->pushButton_color_ring,R,200,200);
}


void MainWindow::on_pushButton_yg_clicked()
{
    QPixmap R(200,200);
    QColor Col = QColor::fromHsv(60,230,255);
    COLOR = Col;
    R.fill(Col);
    setButtonBackImage(ui->pushButton_color_ring,R,200,200);
}


void MainWindow::on_pushButton_g_clicked()
{
    QPixmap R(200,200);
    QColor Col = QColor::fromHsv(90,230,255);
    COLOR = Col;
    R.fill(Col);
    setButtonBackImage(ui->pushButton_color_ring,R,200,200);
}


void MainWindow::on_pushButton_gb_clicked()
{
    QPixmap R(200,200);
    QColor Col = QColor::fromHsv(135,230,255);
    COLOR = Col;
    R.fill(Col);
    setButtonBackImage(ui->pushButton_color_ring,R,200,200);
}


void MainWindow::on_pushButton_b_clicked()
{
    QPixmap R(200,200);
    QColor Col = QColor::fromHsv(180,230,255);
    COLOR = Col;
    R.fill(Col);
    setButtonBackImage(ui->pushButton_color_ring,R,200,200);
}


void MainWindow::on_pushButton_bp_clicked()
{
    QPixmap R(200,200);
    QColor Col = QColor::fromHsv(200,230,255);
    COLOR = Col;
    R.fill(Col);
    setButtonBackImage(ui->pushButton_color_ring,R,200,200);
}


void MainWindow::on_pushButton_p_clicked()
{
    QPixmap R(200,200);
    QColor Col = QColor::fromHsv(230,230,255);
    COLOR = Col;
    R.fill(Col);
    setButtonBackImage(ui->pushButton_color_ring,R,200,200);
}


void MainWindow::on_pushButton_pr_clicked()
{
    QPixmap R(200,200);
    QColor Col = QColor::fromHsv(254,230,255);
    COLOR = Col;
    R.fill(Col);
    setButtonBackImage(ui->pushButton_color_ring,R,200,200);
}




void MainWindow::on_pushButton_copy_clicked()
{
    selStackCopy = selStack;
    qDebug() << "selStackCopy:" << selStackCopy.size();
}


void MainWindow::on_pushButton_paste_clicked()
{
    stack<Move> pasteStack = selStackCopy;
    stack<Move> pasted = emptyMoveStack;
    while(!pasteStack.empty()){
        Move theMove = pasteStack.top();
        pasteStack.pop();

        if(theMove.Shape=="pencil"){
                int add_up=-40;
                int add_right=40;
                stack<QPoint> points = theMove.pencilPoints;
                stack<QPoint> newpoints;
                while(!points.empty()){
                    QPoint p = points.top();
                    points.pop();
                    p.setX(p.x() + add_right);
                    p.setY(p.y() - add_up);
                    newpoints.push(p);
                }
                theMove.pencilPoints = newpoints;

        }
        else{
            theMove.X1 += 40;
            theMove.X2 += 40;
            theMove.Y1 += 40;
            theMove.Y2 += 40;

        }
        pasted.push(theMove);
    }

    stack<Move> pastedCopy = pasted;
    while(!pastedCopy.empty()){
        curStack.push(pastedCopy.top());
        pastedCopy.pop();
    }
    update();

}

void MainWindow::on_pushButton_cut_clicked()
{
    MainWindow::on_pushButton_delete_clicked();
    MainWindow::on_pushButton_copy_clicked();
}


void MainWindow::on_pushButton_delete_clicked()
{

    stack<Move> delStack = selStack;
    stack<Move> curStackCopy = curStack;
    stack<Move> deleted;

    while(!curStackCopy.empty()){
        qDebug() << curStackCopy.size();
        Move theMove = curStackCopy.top();
        curStackCopy.pop();
        if(!theMove.checkIfMoveSelected(theMove,delStack)){
            deleted.push(theMove);
            qDebug() << "push Move";
        }
        else{
            qDebug() << "delete Move";
        }
    }

    qDebug() << "deleted size:" << deleted.size();
    curStack = StackInverse(deleted);
    //curStack = deleted;
    update();
}

void MainWindow::noFileWarning(){

    if(!curStack.empty() && img_read.empty() && !new_background){
        QMessageBox::critical(this,"No File warning","Please open a file");
    }
}



void MainWindow::on_pushButton_attach_open_file_clicked()
{
    QString filePath = QFileDialog::getOpenFileName(this,tr("Open File"),"",tr("image(*.png *.jpeg *.jpg)"));
    string imgName = filePath.toStdString();
    //fileName = "C:\\Users\\BERLIN CHEN\\Desktop\\DDLAB\\PRO\\OpenCV_HW3\\color_ring.jpg";

    //qDebug() << filePath;
    img_import = cv::imread(imgName);
    ui->label_import_img->setPixmap(QPixmap::fromImage(cvMat_to_QImage(img_import)).scaled(ui->label_import_img->width(),ui->label_import_img->height(),Qt::KeepAspectRatio));

}



void MainWindow::on_pushButton_import_clear_clicked()
{
    img_import = QChar::Null;
    ui->label_import_img->clear();
}




void MainWindow::on_pushButton_add_img_clicked()
{
    add_image_mode = true;
}


void MainWindow::on_pushButton_open_file_text_clicked()
{
    QString filePath = QFileDialog::getOpenFileName(this,tr("Open File"),"",tr("textFile(*.txt)"));
    QFile fileRead(filePath);
    ui->textEdit_import->setText("");
    if(fileRead.open(QIODevice::ReadOnly)){
        QTextStream input(&fileRead);
        //input.setCodec("UTF-8");
        while(!input.atEnd()){
            QString line = input.readLine();
            ui->textEdit_import->append(line.toStdString().data());
        }
        fileRead.close();
    }

}


void MainWindow::on_fontComboBox_text_currentFontChanged(const QFont &f)
{
    import_text_font = f;
    ui->textEdit_import->setFont(import_text_font);
}



void MainWindow::on_spinBox_size_valueChanged(int arg1)
{
    import_text_size = arg1;
    ui->textEdit_import->setFontPointSize(import_text_size);
}


void MainWindow::on_pushButton_clear_text_clicked()
{
    ui->textEdit_import->setText("");
}




void MainWindow::on_pushButton_add_text_clicked()
{
    add_text_mode = true;

}

void MainWindow::aboutQt(){

    QMessageBox::aboutQt(this,"About Qt");

}

void MainWindow::aboutLab(){

    QString link = "http://ttlin.bime.ntu.edu.tw/ttlin/";
    QDesktopServices::openUrl(QUrl(link));

}

void MainWindow::setDefualtTheme(){

    this->setStyleSheet("background-color: light gray");
    ui->label_canva->setStyleSheet("background-color: light gray");
    ui->tabWidget->setStyleSheet("background-color: light gray; color: black");
    ui->menubar->setStyleSheet("color: black");


}

void MainWindow::setDarkTheme(){

    this->setStyleSheet("background-color: rgb(65,65,65)");
    //ui->label_canva->setStyleSheet("background-color: silver");
    ui->tabWidget->setStyleSheet("background-color: lightgray");
    ui->menubar->setStyleSheet("color: white; border: 2px solid white");

}

void MainWindow::setWhiteTheme(){

    this->setStyleSheet("background-color: ghostwhite");
    ui->tabWidget->setStyleSheet("background-color: whitesmoke; color: black");
    ui->menubar->setStyleSheet("color: black");


}

void MainWindow::setBlueTheme(){
    this->setStyleSheet("background-color: lightsteelblue");
    ui->tabWidget->setStyleSheet("background-color: aliceblue; color: midnightblue");
    ui->menubar->setStyleSheet("color: midnightblue");

}

void MainWindow::setWarmTheme(){
    this->setStyleSheet("background-color: papayawhip");
    ui->tabWidget->setStyleSheet("background-color: floralwhite; color: rgb(53,0,0); padding: 0px  4px");
    ui->menubar->setStyleSheet("background-color:wheat ;color: rgb(53,0,0)");

}

void MainWindow::settingDefault(){

    setAppearance();
    setWidgetFunc();
    setFocusPolicy(Qt::StrongFocus);
    ui->tabWidget->raise();
    this->setWindowTitle("Illustrator");
    setDefualtTheme();

}

void MainWindow::GaussianBlur(){

    Move G("Gaussian");
    curStack.push(G);
    update();
}




