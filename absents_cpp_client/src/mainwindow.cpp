#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>
#include <QMessageBox>
#include <QSettings>
#include <QSqlQuery>
#include  <QSqlError>
#include <QMessageBox>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
    , m_columnCount(26)
{
    ui->setupUi(this);


    loadSettings();
    setBase();

    getGroups();

}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::loadSettings()
{
    QSettings settings("settings.ini", QSettings::IniFormat);
    m_gatewayIp = settings.value("getewayIp", "http://10.0.2.18").toString();
    m_gatewayPort = settings.value("getewayPort", 4000).toInt();
}


void MainWindow::getGroups()
{
    disconnect(ui->cb_group, SIGNAL(currentIndexChanged(int)), this, SLOT(selectStudents(int)));
    disconnect(ui->cb_week, SIGNAL(currentIndexChanged(int)), this, SLOT(selectStudents(int)));

    ui->cb_group->clear();
    ui->cb_group->addItem("-");

    if(!m_base.isOpen())
        m_base.open();

    QSqlQuery query(m_base);
    QString queryText = "SELECT id, name FROM a_groups WHERE active = 1";
    query.exec(queryText);
    if(query.lastError().isValid())
        qDebug()<<query.lastError().text();

    while (query.next()) {
        ui->cb_group->addItem(query.value("name").toString(), query.value("id"));
    }
    m_base.close();

    connect(ui->cb_group, SIGNAL(currentIndexChanged(int)), this, SLOT(selectStudents(int)));
    connect(ui->cb_week, SIGNAL(currentIndexChanged(int)), this, SLOT(selectStudents(int)));
}


void MainWindow::selectStudents(int index)
{
    Q_UNUSED(index)

    setTableColumnHeaders();

    if(!index || !ui->cb_week->currentIndex())
        return;

    if(!m_base.isOpen())
        m_base.open();

    QSqlQuery query(m_base);
    QString queryText = QString("SELECT id, surname, name, middle_name "
                                "FROM a_students "
                                "WHERE group_id = %1 "
                                "ORDER BY surname")
            .arg(ui->cb_group->currentData().toInt());

    query.exec(queryText);

    if(query.lastError().isValid())
        qDebug()<<query.lastError().text();

    while (query.next()) {
        int row = ui->tableWidget->rowCount();
        ui->tableWidget->insertRow(row);
        QTableWidgetItem * item = new QTableWidgetItem(QString("%1 %2 %3")
                                                       .arg(query.value("surname").toString(),
                                                            query.value("name").toString(),
                                                            query.value("middle_name").toString()));
        item->setData(Fields::UserId, query.value("id"));
        ui->tableWidget->setItem(row, 0, item);
        setAbsents(query.value("id").toInt(), row);
    }

    ui->tableWidget->resizeColumnsToContents();
}


void MainWindow::setTableColumnHeaders()
{
    ui->tableWidget->setRowCount(0);
    ui->tableWidget->insertRow(0);
    ui->tableWidget->setColumnCount(m_columnCount);


    QTableWidgetItem * item = new QTableWidgetItem("");
    ui->tableWidget->setItem(0, 0, item);

    QList<QPair<QString, QDate>> weekDays = getWeekDays();

    int startColumn = 1;
    for(int i = 0; i < weekDays.count(); ++i){
        ui->tableWidget->setSpan(0, startColumn, 1, 5);
        item = new QTableWidgetItem(weekDays.at(i).first);
        item->setTextAlignment(Qt::AlignHCenter|Qt::AlignVCenter);
        item->setData(Fields::Date, weekDays.at(i).second);
        ui->tableWidget->setItem(0, startColumn, item);
        startColumn += 5;
    }

    int row = 1;
    ui->tableWidget->insertRow(row);
    for(int i = 1; i < m_columnCount; ++i){
        int index = i % 5;
        item = new QTableWidgetItem(QString::number(index?index:5));
        item->setTextAlignment(Qt::AlignHCenter|Qt::AlignVCenter);
        ui->tableWidget->setItem(row, i, item);
    }

}

QList<QPair<QString, QDate>> MainWindow::getWeekDays()
{
    QList<QPair<QString, QDate>> weekDays;

    QStringList days = ui->cb_week->currentText().split("-");
    QDate startDate = QDate::fromString(QString("%1.2022").arg(days.at(0).trimmed()), "dd.MM.yyyy");

    weekDays.append(qMakePair("Понедельник" + startDate.toString("(dd.MM.yyyy)"), startDate));
    weekDays.append(qMakePair("Вторник" + startDate.addDays(1).toString("(dd.MM.yyyy)"),startDate.addDays(1)));
    weekDays.append(qMakePair("Среда" + startDate.addDays(2).toString("(dd.MM.yyyy)"), startDate.addDays(2)));
    weekDays.append(qMakePair("Четверг" + startDate.addDays(3).toString("(dd.MM.yyyy)"), startDate.addDays(3)));
    weekDays.append(qMakePair("Пятница" + startDate.addDays(4).toString("(dd.MM.yyyy)"), startDate.addDays(4)));

    return weekDays;
}

bool MainWindow::checkAbsents(QDate date, int number, QList<AbsentStr> *absents)
{
    for(int i = 0; i < absents->count(); ++i){
        if(absents->at(i).date == date &&
                absents->at(i).number == number){
            return true;
        }
    }
    return false;
}

void MainWindow::saveAbsents()
{
    for(int row = 2; row < ui->tableWidget->rowCount(); ++row){
        for(int column = 1; column < ui->tableWidget->columnCount(); ++column ){
            if(ui->tableWidget->item(row, column)->data(Fields::State) == States::Absent &&
                    ui->tableWidget->item(row, column)->checkState() == Qt::Unchecked){
                deleteAbsents(row, column);
            } else if (ui->tableWidget->item(row, column)->data(Fields::State) == States::Present &&
                       ui->tableWidget->item(row, column)->checkState() == Qt::Checked){
                addAbsents(row, column);
            }
        }
    }
}

void MainWindow::addAbsents(int row, int column)
{
    if(!m_base.isOpen())
        m_base.open();

    QSqlQuery query(m_base);
    query.prepare("INSERT INTO a_absents(user_id, `date`, `number`) VALUES(:user_id, :date, :number)");
    query.bindValue(":user_id", ui->tableWidget->item(row, column)->data(Fields::UserId).toInt());
    query.bindValue(":date", ui->tableWidget->item(row, column)->data(Fields::Date).toDate());
    query.bindValue(":number", ui->tableWidget->item(row, column)->data(Fields::Number).toInt());
    query.exec();

    if(query.lastError().isValid())
        QMessageBox::critical(this, "Ошибка добавления", query.lastError().text());

    ui->tableWidget->item(row, column)->setData(Fields::State, States::Absent);
    m_base.close();
}

void MainWindow::deleteAbsents(int row, int column)
{
    if(!m_base.isOpen())
        m_base.open();

    QSqlQuery query(m_base);
    query.prepare("DELETE FROM a_absents WHERE user_id = :user_id AND date = :date AND number = :number");
    query.bindValue(":user_id", ui->tableWidget->item(row, column)->data(Fields::UserId).toInt());
    query.bindValue(":date", ui->tableWidget->item(row, column)->data(Fields::Date).toDate());
    query.bindValue(":number", ui->tableWidget->item(row, column)->data(Fields::Number).toInt());
    query.exec();

    if(query.lastError().isValid())
        QMessageBox::critical(this, "Ошибка добавления", query.lastError().text());

    ui->tableWidget->item(row, column)->setData(Fields::State, States::Absent);
    m_base.close();
}

void MainWindow::setAbsents(int student_id, int row)
{
    if(!m_base.isOpen())
        m_base.open();

    QSqlQuery query(m_base);
    QString queryText = QString("SELECT id, `date`, `number` FROM a_absents WHERE user_id = %1").arg(student_id);
    query.exec(queryText);
    if(query.lastError().isValid())
        qDebug()<<query.lastError().text();

    QList<AbsentStr> absents;
    while (query.next()) {
       AbsentStr abs;
       abs.date = query.value("date").toDate();
       abs.number = query.value("number").toInt();
       abs.student_id = student_id;
       absents.append(abs);
    }

    for(int column = 1; column < m_columnCount; ++column){
        int index = 0;
        if(column >= 1 && column < 6){
            index = 1;
        } else if(column >= 6 && column < 11){
            index = 6;
        }else if(column >= 11 && column < 16){
            index = 11;
        }else if(column >= 16 && column < 21){
            index = 16;
        }else {
            index = 21;
        }

        QTableWidgetItem * item = new QTableWidgetItem();
        item->setData(Fields::UserId, student_id);
        item->setData(Fields::Number, ui->tableWidget->item(1, column)->text());
        item->setData(Fields::Date, ui->tableWidget->item(0, index)->data(Fields::Date));
        if(checkAbsents(item->data(Fields::Date).toDate(),
                        item->data(Fields::Number).toInt(),
                        &absents)){
            item->setCheckState(Qt::Checked);
            item->setData(Fields::State, States::Absent);
        } else{
            item->setCheckState(Qt::Unchecked);
            item->setData(Fields::State, States::Present);
        }

        ui->tableWidget->setItem(row, column, item);
    }

    m_base.close();
}


void MainWindow::on_btn_save_clicked()
{
    saveAbsents();
}

void MainWindow::setBase()
{
    m_base = QSqlDatabase::addDatabase("QMYSQL");
    m_base.setDatabaseName("Diplomas");
    m_base.setHostName("10.0.2.18");
    m_base.setUserName("diplomas");
    m_base.setPassword("Diplomas");
}

