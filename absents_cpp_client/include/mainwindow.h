#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QCloseEvent>
#include <QDate>
#include <QListWidgetItem>
#include <QMainWindow>
#include <QSqlDatabase>
#include <QMenu>

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
    virtual void closeEvent(QCloseEvent *e);

private slots:
    //    void setFacultiesList(QList<Faculty> faculties);
    void on_cb_faculties_currentIndexChanged(int index);
    void on_cb_cource_currentIndexChanged(int index);
    void on_lw_groupList_currentItemChanged(QListWidgetItem *current, QListWidgetItem *previous);
    void on_calendarWidget_clicked(const QDate &date);
    void on_btn_createSchedule_clicked();

    void dataChenget();
//    void deleteAbsent(int absentId);
//    void addAbsent(int lessonId, int userId, int absentType);
//    void updateAbsent(int absentId, int absentType);
    void on_btn_reset_clicked();
    void on_btn_save_clicked();
    void customHeaderMenuRequested(QPoint pos);

private:
    Ui::MainWindow *ui;

    enum Roles{
        GroupId = Qt::UserRole,
        StudentId,
        LessonId
    };

    enum RowsName{
        DateRow,
        NumberInDayRow,
        TeacherRow
    };

    const int emptyPage;
    const int schedulePage;
    const int workDayCount;
    int dayLessonsCount;

    BaseWorker baseWorker;

    QList<Group> groups;

    bool changet;

    QList<int> deletedAbsent;
    QList<Absent> updatedAbsent;
    QList<Absent> addedAbsent;


    void selectData();
    void setFaculties();
    void setCourses();
    void setGroups();
    void getSchedule();
    void getAbsents();
    void setSchedule(QList<Schedule *> schedule);
    void setScheduleHeadrows(QList<Schedule *> schedule);
    QDate getWeekStartDate();
    void createSchedule();
    void getStudents();
    void saveData();
    QMenu *createMenu();
};
#endif // MAINWINDOW_H
