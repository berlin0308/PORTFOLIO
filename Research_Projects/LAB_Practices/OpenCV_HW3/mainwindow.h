#ifndef MAINWINDOW_H
#define MAINWINDOW_H

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

private slots:
    void Update_Image();

    void NoFile_Warning();

    void Settings();

    void on_pushButton_file_clicked();

    void on_horizontalSlider_adjust_B_valueChanged(int value);


    void on_horizontalSlider_adjust_G_valueChanged(int value);

    void on_horizontalSlider_adjust_R_valueChanged(int value);

    void on_horizontalSlider_adjust_H_valueChanged(int value);

    void on_horizontalSlider_adjust_S_valueChanged(int value);

    void on_horizontalSlider_adjust_V_valueChanged(int value);


    void on_pushButton_undo_clicked();

    void on_pushButton_redo_clicked();

    void on_pushButton_reset_clicked();

    void on_comboBox_select_filter_currentTextChanged(const QString &arg1);

    void on_horizontalSlider_filter_valueChanged(int value);

    void on_horizontalSlider_range_H_lower_valueChanged(int value);

    void on_horizontalSlider_range_S_lower_valueChanged(int value);

    void on_horizontalSlider_range_V_lower_valueChanged(int value);

    void on_horizontalSlider_range_H_upper_valueChanged(int value);

    void on_horizontalSlider_range_S_upper_valueChanged(int value);

    void on_horizontalSlider_range_V_upper_valueChanged(int value);

    void on_pushButton_flip_H_clicked();

    void on_pushButton_flip_V_clicked();

    void on_pushButton_rotate_clicked();


    void on_pushButton_rotate_L_clicked();

    void on_pushButton_save_clicked();

private:
    Ui::MainWindow *ui;

};
#endif // MAINWINDOW_H
