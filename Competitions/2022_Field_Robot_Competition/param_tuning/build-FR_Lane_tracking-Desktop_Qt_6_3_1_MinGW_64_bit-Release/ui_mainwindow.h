/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 6.3.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpinBox>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralwidget;
    QWidget *widget;
    QGridLayout *gridLayout_2;
    QLabel *label;
    QLabel *label_2;
    QLabel *label_3;
    QLabel *label_4;
    QPushButton *pushButton_openfile;
    QVBoxLayout *verticalLayout;
    QSpinBox *spinBox_erode;
    QPushButton *pushButton_erode;
    QPushButton *pushButton_canny;
    QVBoxLayout *verticalLayout_2;
    QGridLayout *gridLayout;
    QLabel *label_5;
    QLabel *label_6;
    QLabel *label_7;
    QSpinBox *spinBox_hl_threshold;
    QSpinBox *spinBox_hl_minLineLength;
    QSpinBox *spinBox_hl_minLineGap;
    QPushButton *pushButton_hl;
    QMenuBar *menubar;
    QStatusBar *statusbar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(800, 600);
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName(QString::fromUtf8("centralwidget"));
        widget = new QWidget(centralwidget);
        widget->setObjectName(QString::fromUtf8("widget"));
        widget->setGeometry(QRect(50, 41, 601, 261));
        gridLayout_2 = new QGridLayout(widget);
        gridLayout_2->setObjectName(QString::fromUtf8("gridLayout_2"));
        gridLayout_2->setContentsMargins(0, 0, 0, 0);
        label = new QLabel(widget);
        label->setObjectName(QString::fromUtf8("label"));

        gridLayout_2->addWidget(label, 0, 0, 1, 1);

        label_2 = new QLabel(widget);
        label_2->setObjectName(QString::fromUtf8("label_2"));

        gridLayout_2->addWidget(label_2, 0, 1, 1, 1);

        label_3 = new QLabel(widget);
        label_3->setObjectName(QString::fromUtf8("label_3"));

        gridLayout_2->addWidget(label_3, 0, 2, 1, 1);

        label_4 = new QLabel(widget);
        label_4->setObjectName(QString::fromUtf8("label_4"));

        gridLayout_2->addWidget(label_4, 0, 3, 1, 1);

        pushButton_openfile = new QPushButton(widget);
        pushButton_openfile->setObjectName(QString::fromUtf8("pushButton_openfile"));

        gridLayout_2->addWidget(pushButton_openfile, 1, 0, 1, 1);

        verticalLayout = new QVBoxLayout();
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        spinBox_erode = new QSpinBox(widget);
        spinBox_erode->setObjectName(QString::fromUtf8("spinBox_erode"));

        verticalLayout->addWidget(spinBox_erode);

        pushButton_erode = new QPushButton(widget);
        pushButton_erode->setObjectName(QString::fromUtf8("pushButton_erode"));

        verticalLayout->addWidget(pushButton_erode);


        gridLayout_2->addLayout(verticalLayout, 1, 1, 1, 1);

        pushButton_canny = new QPushButton(widget);
        pushButton_canny->setObjectName(QString::fromUtf8("pushButton_canny"));

        gridLayout_2->addWidget(pushButton_canny, 1, 2, 1, 1);

        verticalLayout_2 = new QVBoxLayout();
        verticalLayout_2->setObjectName(QString::fromUtf8("verticalLayout_2"));
        gridLayout = new QGridLayout();
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        label_5 = new QLabel(widget);
        label_5->setObjectName(QString::fromUtf8("label_5"));

        gridLayout->addWidget(label_5, 0, 0, 1, 1);

        label_6 = new QLabel(widget);
        label_6->setObjectName(QString::fromUtf8("label_6"));

        gridLayout->addWidget(label_6, 0, 1, 1, 1);

        label_7 = new QLabel(widget);
        label_7->setObjectName(QString::fromUtf8("label_7"));

        gridLayout->addWidget(label_7, 0, 2, 1, 1);

        spinBox_hl_threshold = new QSpinBox(widget);
        spinBox_hl_threshold->setObjectName(QString::fromUtf8("spinBox_hl_threshold"));

        gridLayout->addWidget(spinBox_hl_threshold, 1, 0, 1, 1);

        spinBox_hl_minLineLength = new QSpinBox(widget);
        spinBox_hl_minLineLength->setObjectName(QString::fromUtf8("spinBox_hl_minLineLength"));

        gridLayout->addWidget(spinBox_hl_minLineLength, 1, 1, 1, 1);

        spinBox_hl_minLineGap = new QSpinBox(widget);
        spinBox_hl_minLineGap->setObjectName(QString::fromUtf8("spinBox_hl_minLineGap"));

        gridLayout->addWidget(spinBox_hl_minLineGap, 1, 2, 1, 1);


        verticalLayout_2->addLayout(gridLayout);

        pushButton_hl = new QPushButton(widget);
        pushButton_hl->setObjectName(QString::fromUtf8("pushButton_hl"));

        verticalLayout_2->addWidget(pushButton_hl);


        gridLayout_2->addLayout(verticalLayout_2, 1, 3, 1, 1);

        MainWindow->setCentralWidget(centralwidget);
        menubar = new QMenuBar(MainWindow);
        menubar->setObjectName(QString::fromUtf8("menubar"));
        menubar->setGeometry(QRect(0, 0, 800, 17));
        MainWindow->setMenuBar(menubar);
        statusbar = new QStatusBar(MainWindow);
        statusbar->setObjectName(QString::fromUtf8("statusbar"));
        MainWindow->setStatusBar(statusbar);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "MainWindow", nullptr));
        label->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_2->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_3->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_4->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        pushButton_openfile->setText(QCoreApplication::translate("MainWindow", "Open gray file", nullptr));
        pushButton_erode->setText(QCoreApplication::translate("MainWindow", "erode", nullptr));
        pushButton_canny->setText(QCoreApplication::translate("MainWindow", "Canny", nullptr));
        label_5->setText(QCoreApplication::translate("MainWindow", "threshold", nullptr));
        label_6->setText(QCoreApplication::translate("MainWindow", "minLineLength", nullptr));
        label_7->setText(QCoreApplication::translate("MainWindow", "minLineGap", nullptr));
        pushButton_hl->setText(QCoreApplication::translate("MainWindow", "HoughLines", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
