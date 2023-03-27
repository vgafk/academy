#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QAction>
#include <baseworker.h>
#include <qmessagebox.h>
#include "settings.h"
#include "absenttypebox.h"

//#include <QJsonArray>
//#include <QJsonDocument>
//#include <QJsonObject>
//#include <QMessageBox>
//#include <QSettings>
//#include <QSqlQuery>
//#include  <QSqlError>
//#include <QMessageBox>



MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
    , emptyPage(1)
    , schedulePage(2)
    , workDayCount(5)
    , changet(false)
{
    ui->setupUi(this);
    //    Settings::instance()->setHostAddress("127.0.0.1", 9000);
    Settings::instance()->setDayLessonsCount(5);

    QPair<QString, int> host = Settings::instance()->getHostAddress();
    //    Settings::instance()->setDayLessonsCount(5);
    dayLessonsCount = Settings::instance()->getDayLessonsCount();
    //    qDebug() << "getDayLessonsCount = " << dayLessonsCount;
    baseWorker.init(host.first, host.second);

    groups = baseWorker.getGroups();

    setFaculties();
    setCourses();

    ui->tableWidget->verticalHeader()->setContextMenuPolicy(Qt::CustomContextMenu);

    connect(ui->tableWidget->verticalHeader(), &QTableWidget::customContextMenuRequested, this, &MainWindow::customHeaderMenuRequested);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::closeEvent(QCloseEvent *e)
{
    if(changet){
        int answer = QMessageBox::question(this, "Данные изменены", "Данные были изменены, сохранить перед закрытием?",
                                           QMessageBox::Yes|QMessageBox::No|QMessageBox::Cancel);
        if(answer == QMessageBox::Cancel){
            e->ignore();
            return;
        } else if(answer == QMessageBox::Yes) {
            saveData();
        }
        e->accept();
    }
}

void MainWindow::setFaculties()
{
    QList<Faculty> faculties = baseWorker.getFaculties();

    foreach(Faculty faculty, faculties){
        ui->cb_faculties->addItem(faculty.name, faculty.id);
    }
}

void MainWindow::setCourses()
{
    for(int i = 0; i < 6; ++i){
        QString course = i == 0 ? "Все" : QString("%1 курс").arg(i);
        ui->cb_cource->addItem(course, i);
    }
}

void MainWindow::setGroups()
{
    ui->lw_groupList->clear();
    int course = ui->cb_cource->currentData().toInt();

    foreach(Group group, groups){

        if( course != 0 && !group.name.startsWith(QString::number(course)))
            continue;

        if(group.facultyId != ui->cb_faculties->currentData().toInt())
            continue;

        QListWidgetItem *item = new QListWidgetItem(group.name);
        item->setData(Roles::GroupId, group.id);
        ui->lw_groupList->addItem(item);
    }
}


void MainWindow::getSchedule()
{
    if(ui->lw_groupList->currentItem() == nullptr)
        return;

    int groupId = ui->lw_groupList->currentItem()->data(Roles::GroupId).toInt();
    int weekNUmber = ui->calendarWidget->selectedDate().weekNumber();

    QList<Schedule*> schedule = baseWorker.getSchedule(groupId, weekNUmber);

    if(schedule.isEmpty())
        ui->stackedWidget->setCurrentIndex(emptyPage);
    else
        setSchedule(schedule);

}

void MainWindow::getAbsents()
{
    if(ui->lw_groupList->currentItem() == nullptr)
        return;

    int groupId = ui->lw_groupList->currentItem()->data(Roles::GroupId).toInt();
    int weekNUmber = ui->calendarWidget->selectedDate().weekNumber();

    QList<Absent> absents = baseWorker.getAbsents(groupId, weekNUmber);

    for( int row = TeacherRow + 1; row < ui->tableWidget->rowCount(); ++row){
        int studentId = ui->tableWidget->verticalHeaderItem(row)->data(Roles::StudentId).toInt();

        for( int column = 0; column < ui->tableWidget->columnCount(); ++column){
            int lessonId = ui->tableWidget->item(NumberInDayRow, column)->data(Roles::LessonId).toInt();

            AbsentTypeBox *box = new AbsentTypeBox(studentId, lessonId);

            Absent absent;
            foreach(absent, absents){
                if(absent.lessonId == lessonId && absent.userId == studentId){
                    box->setType(absent.absentType);
                    box->setId(absent.id);
                }
            }
            ui->tableWidget->setCellWidget(row, column, box);
            connect(box, &AbsentTypeBox::changet, this, &MainWindow::dataChenget);
        }

    }
}

void MainWindow::setSchedule(QList<Schedule*> schedule)
{
    Q_UNUSED(schedule)
    setScheduleHeadrows(schedule);
    //    setTeachers(schedule);
}

void MainWindow::setScheduleHeadrows(QList<Schedule*> schedule)
{
    int spanStartColumn = 0;
    int columnsBefore = 0;
    ui->stackedWidget->setCurrentIndex(schedulePage);

    ui->tableWidget->setRowCount(0);
    ui->tableWidget->insertRow(RowsName::DateRow);
    ui->tableWidget->setVerticalHeaderItem(RowsName::DateRow, new QTableWidgetItem("Дата"));
    ui->tableWidget->insertRow(RowsName::NumberInDayRow);
    ui->tableWidget->setVerticalHeaderItem(RowsName::NumberInDayRow, new QTableWidgetItem("Пара"));
    ui->tableWidget->insertRow(RowsName::TeacherRow);
    ui->tableWidget->setVerticalHeaderItem(RowsName::TeacherRow, new QTableWidgetItem(""));

    int columnsCount = workDayCount * dayLessonsCount;

    ui->tableWidget->setColumnCount(columnsCount);
    QDate startDate = getWeekStartDate();

    for( int dateColumn = 0; dateColumn < workDayCount; ++dateColumn){
        ui->tableWidget->setSpan(RowsName::DateRow, spanStartColumn, 1, dayLessonsCount);
        QDate newDate = startDate.addDays(dateColumn);
        ui->tableWidget->setItem(RowsName::DateRow, dateColumn * dayLessonsCount + columnsBefore, new QTableWidgetItem(newDate.toString("dd.MM.yyyy")));
        spanStartColumn += dayLessonsCount;

        for( int numberInDayColumn = 0; numberInDayColumn < dayLessonsCount; ++numberInDayColumn){

            int val = numberInDayColumn % dayLessonsCount + 1;
            QTableWidgetItem *lessonItem = new QTableWidgetItem(QString::number(val));
            QTableWidgetItem *teacherItem = new QTableWidgetItem();

            ui->tableWidget->setItem(RowsName::NumberInDayRow, numberInDayColumn + (dayLessonsCount * dateColumn), lessonItem);
            ui->tableWidget->setItem(RowsName::TeacherRow, numberInDayColumn + (dayLessonsCount * dateColumn), teacherItem);

            Schedule *scheduleRecord;
            foreach(scheduleRecord, schedule){
                if(scheduleRecord->date == newDate){
                    lessonItem->setData(Roles::LessonId, scheduleRecord->lesessons.value(val).id);
                                        teacherItem->setText(QString::number(scheduleRecord->lesessons.value(val).id));
                    break;
                }
            }
        }
    }

    ui->tableWidget->resizeColumnsToContents();

}

QDate MainWindow::getWeekStartDate()
{
    int currentWeekDay = ui->calendarWidget->selectedDate().dayOfWeek() - 1;
    QDate weekStartDate = ui->calendarWidget->selectedDate().addDays(-currentWeekDay);
    return weekStartDate;
}

void MainWindow::createSchedule()
{
    int groupId = ui->lw_groupList->currentItem()->data(Roles::GroupId).toInt();
    int weekNUmber = ui->calendarWidget->selectedDate().weekNumber();

    int answer = int(baseWorker.createWeekSchedule(weekNUmber, groupId));
    qDebug() << answer;
    selectData();

}

void MainWindow::getStudents()
{
    if(ui->lw_groupList->currentItem() == nullptr)
        return;

    int groupId = ui->lw_groupList->currentItem()->data(Roles::GroupId).toInt();

    QList<Student> students = baseWorker.getStudents(groupId);

    Student student;
    foreach(student, students){
        int row = ui->tableWidget->rowCount();
        ui->tableWidget->insertRow(row);
        QTableWidgetItem * item = new QTableWidgetItem(QString("%1 %2").arg(student.surname, student.name));
        item->setData(Roles::GroupId, student.groupId);
        item->setData(Roles::StudentId, student.id);
        ui->tableWidget->setVerticalHeaderItem(row, item);
    }
}

void MainWindow::saveData()
{
    addedAbsent.clear();
    updatedAbsent.clear();
    deletedAbsent.clear();

    for(int row = TeacherRow + 1; row < ui->tableWidget->rowCount(); ++row){
        for( int column = 0; column < ui->tableWidget->columnCount(); ++column){
            AbsentTypeBox *box = qobject_cast<AbsentTypeBox*>(ui->tableWidget->cellWidget(row, column));
            if(box->getId() == 0){
                if(box->getType() == 1){
                    continue;
                } else {
                    Absent absent;
                    absent.lessonId = ui->tableWidget->item(NumberInDayRow, column)->data(Roles::LessonId).toInt();
                    absent.userId = ui->tableWidget->verticalHeaderItem(row)->data(Roles::StudentId).toInt();
                    absent.absentType = box->getType();
                    addedAbsent.append(absent);
                }
            } else {
                if(box->getType() == 1){
                    deletedAbsent.append(box->getId());
                } else {
                    Absent absent;
                    absent.id = box->getId();
                    absent.absentType = box->getType();
                    updatedAbsent.append(absent);
                }
            }
        }
    }
    baseWorker.addAbsent(addedAbsent);
    baseWorker.updateAbsent(updatedAbsent);
    baseWorker.deleteAbsent(deletedAbsent);
}

QMenu *MainWindow::createMenu()
{
    QMenu *menu = new QMenu(this);
    menu->addAction(new QAction("Проставить диапазоном ", this));
    return menu;
}

void MainWindow::on_cb_faculties_currentIndexChanged(int index)
{
    Q_UNUSED(index)
    setGroups();
}


void MainWindow::on_cb_cource_currentIndexChanged(int index)
{
    Q_UNUSED(index)
    setGroups();
}


void MainWindow::on_lw_groupList_currentItemChanged(QListWidgetItem *current, QListWidgetItem *previous)
{
    Q_UNUSED(previous)
    if(current == nullptr)
        return;

    selectData();
}

void MainWindow::on_calendarWidget_clicked(const QDate &date)
{
    Q_UNUSED(date)
    selectData();
}


void MainWindow::on_btn_createSchedule_clicked()
{
    createSchedule();
}

void MainWindow::dataChenget()
{
    changet = true;
}

void MainWindow::selectData()
{
    getSchedule();
    getStudents();
    getAbsents();
    changet = false;

    ui->tableWidget->resizeColumnsToContents();
}


void MainWindow::on_btn_reset_clicked()
{
    selectData();
}


void MainWindow::on_btn_save_clicked()
{
    saveData();
    selectData();
    changet = false;
}

void MainWindow::customHeaderMenuRequested(QPoint pos)
{
    int row = ui->tableWidget->verticalHeader()->logicalIndexAt(pos);

    QMenu *menu = createMenu();
    menu->popup(ui->tableWidget->verticalHeader()->viewport()->mapToGlobal(pos));

}

