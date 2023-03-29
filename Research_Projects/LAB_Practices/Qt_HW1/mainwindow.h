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


    void on_buttonBox_rejected();

    void on_buttonBox_accepted();

private:
    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
