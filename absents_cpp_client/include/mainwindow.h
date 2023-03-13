#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QDate>
#include <QListWidgetItem>
#include <QMainWindow>
#include <QSqlDatabase>
#include "apistructs.h"
#include "baseworker.h"

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
//    void selectStudents(int index);

//    void on_btn_save_clicked();

    void on_calendarWidget_clicked(const QDate &date);
    void on_lw_groupList_currentRowChanged(int currentRow);

    void setFacultiesList(QList<Faculty> faculties);

private:
    Ui::MainWindow *ui;

    enum Roles{
        GroupId = Qt::UserRole
    };

    BaseWorker baseWorker;

    void getFacultyList();

    void selectAbsets();
    void selectAbsets(int groupId, int weekNumber);

//    struct AbsentStr{
//        int student_id;
//        QDate date;
//        int number;
//    };

//    enum Fields{
//        UserId = Qt::UserRole,
//        Number,
//        Date,
//        State,
//        Id
//    };

//    enum States{
//        Absent,
//        Present
//    };

//    QString m_gatewayIp;
//    int m_gatewayPort;
//    const int m_columnCount;

//    QSqlDatabase m_base;

//    void setBase();

//    void loadSettings();


//    void getGroups();

//    void setTableColumnHeaders();

//    QList<QPair<QString, QDate> > getWeekDays();
//    bool checkAbsents(QDate date, int number, QList<AbsentStr> *absents);

//    void saveAbsents();
//    void addAbsents(int row, int column);
//    void deleteAbsents(int row, int column);


//    void setAbsents(int student_id, int row);

};
#endif // MAINWINDOW_H
