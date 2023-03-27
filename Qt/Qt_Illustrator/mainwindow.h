#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPushButton>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:

    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();


    void new_file(); // white background
    void open_file(); // QFileDialog
    void save_as(); // QFileDialog
    void save();
    void undo(); // Stack
    void redo(); // Stack
    void clear(); // white rect
    void aboutQt(); // QMessageBox
    void aboutLab(); // QDesktopServices


    void setMenuBar();
    void setAppearance();
    void setWidgetFunc();


    void setButtonBackImage(QPushButton *button,QPixmap pixmap
                            ,int sizeW, int sizeH);


    void noFileWarning();

    void setDefualtTheme();
    void setDarkTheme();
    void setWhiteTheme();
    void setBlueTheme();
    void setWarmTheme();
    void settingDefault();


    void GaussianBlur();


private slots:
    void on_pushButton_color_ring_clicked();

    void on_pushButton_select_clicked();

    void on_comboBox_style_select_currentTextChanged(const QString &arg1);

    void on_spinBox_width_valueChanged(int arg1);

    void on_horizontalSlider_shape_select_valueChanged(int value);

    void on_radioButton_unfill_clicked();

    void on_radioButton_fill_clicked();



    void on_pushButton_red_clicked();

    void on_pushButton_ro_clicked();

    void on_pushButton_o_clicked();

    void on_pushButton_oy_clicked();

    void on_pushButton_y_clicked();

    void on_pushButton_yg_clicked();

    void on_pushButton_g_clicked();

    void on_pushButton_gb_clicked();

    void on_pushButton_b_clicked();

    void on_pushButton_bp_clicked();

    void on_pushButton_p_clicked();

    void on_pushButton_pr_clicked();



    void on_pushButton_fill_clicked();

    void on_pushButton_unfill_clicked();

    void on_pushButton_move_clicked();

    void on_pushButton_cut_clicked();

    void on_pushButton_copy_clicked();

    void on_pushButton_paste_clicked();

    void on_pushButton_delete_clicked();



    void on_pushButton_attach_open_file_clicked();

    void on_pushButton_import_clear_clicked();


    void on_pushButton_add_img_clicked();

    void on_pushButton_open_file_text_clicked();

    void on_fontComboBox_text_currentFontChanged(const QFont &f);

    void on_spinBox_size_valueChanged(int arg1);

    void on_pushButton_clear_text_clicked();

    void on_pushButton_add_text_clicked();

private:
    Ui::MainWindow *ui;

protected:

    void mousePressEvent(QMouseEvent *event); // initial point
    void mouseMoveEvent(QMouseEvent *event); // preview
    void mouseReleaseEvent(QMouseEvent *event); // final point, curStack.push()

    void paintEvent(QPaintEvent *event);

    void keyPressEvent(QKeyEvent *event);
};
#endif // MAINWINDOW_H
