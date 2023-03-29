#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_pushButton_select_image_clicked();

    void on_pushButton_openfile_clicked();

    void on_pushButton_clear_clicked();

    void on_pushButton_writefile_clicked();

    void on_pushButton_add2file_clicked();

private:
    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
