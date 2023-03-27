#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include "opencv2/core/mat.hpp"
#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    QImage cvMat_to_QImage(const cv::Mat &mat ) ;


private slots:
    void on_pushButton_openfile_clicked();

    void on_pushButton_erode_clicked();

    void on_pushButton_canny_clicked();

    void on_pushButton_hl_clicked();

private:
    Ui::MainWindow *ui;
};
#endif // MAINWINDOW_H
