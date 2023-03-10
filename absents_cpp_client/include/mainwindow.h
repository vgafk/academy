#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QDate>
#include <QMainWindow>
#include <QSqlDatabase>

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
        void selectStudents(int index);

    void on_btn_save_clicked();

private:
    Ui::MainWindow *ui;

    struct AbsentStr{
        int student_id;
        QDate date;
        int number;
    };

    enum Fields{
        UserId = Qt::UserRole,
        Number,
        Date,
        State,
        Id
    };

    enum States{
        Absent,
        Present
    };

    QString m_gatewayIp;
    int m_gatewayPort;
    const int m_columnCount;

    QSqlDatabase m_base;

    void setBase();

    void loadSettings();


    void getGroups();

    void setTableColumnHeaders();

    QList<QPair<QString, QDate> > getWeekDays();
    bool checkAbsents(QDate date, int number, QList<AbsentStr> *absents);

    void saveAbsents();
    void addAbsents(int row, int column);
    void deleteAbsents(int row, int column);


    void setAbsents(int student_id, int row);

};
#endif // MAINWINDOW_H
