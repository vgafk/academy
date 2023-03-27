#include "baseworker.h"

#include "settings.h"

#include <QEventLoop>
#include <QJsonObject>
#include <QUrlQuery>


BaseWorker::BaseWorker(QObject *parent)
    : QObject{parent}
{
}

BaseWorker::~BaseWorker()
{
}

void BaseWorker::init(const QString &host, int port)
{
    serverUrl.setScheme("http");
    serverUrl.setHost(host);
    serverUrl.setPort(port);
}


QList<Faculty> BaseWorker::getFaculties()
{
    QJsonDocument answer = QJsonDocument::fromJson(get("faculties/"));
    QJsonArray answerArray = answer.array();
    QList<Faculty> faculties;

    for(int i = 0; i < answerArray.size(); ++i){
        Faculty newFaculty;
        newFaculty.id = answerArray.at(i)["id"].toInt();
        newFaculty.fullName = answerArray.at(i)["full_name"].toString();
        newFaculty.name = answerArray.at(i)["name"].toString();
        faculties.append(newFaculty);
    }
    return faculties;
}

QList<Group> BaseWorker::getGroups()
{
    QJsonDocument answer = QJsonDocument::fromJson(get("groups/"));
    QJsonArray answerArray = answer.array();
    QList<Group> groups;

    for(int i = 0; i < answerArray.size(); ++i){
        Group newGroup;
        newGroup.id = answerArray.at(i)["id"].toInt();
        newGroup.fullName = answerArray.at(i)["full_name"].toString();
        newGroup.name = answerArray.at(i)["name"].toString();
        newGroup.facultyId = answerArray.at(i)["faculty_id"].toInt();
        groups.append(newGroup);
    }
    return groups;
}

QList<Schedule*> BaseWorker::getSchedule(int group_id, int weekNumber)
{
    QList<QPair<QString, int>> parametrs;
    parametrs.append(QPair<QString, int>("group_id", group_id));
    parametrs.append(QPair<QString, int>("week_number", weekNumber));

    QJsonDocument answer = QJsonDocument::fromJson(get("schedule/", parametrs));
    QJsonArray answerArray = answer.array();
    QList<Schedule*> schedule;
    Schedule *newSchedule = nullptr;

    for(int i = 0; i < answerArray.size(); ++i){
        QDate date = QDate::fromString(answerArray.at(i)["date"].toString(), "yyyy-MM-dd");
        if(newSchedule == nullptr || newSchedule->date != date){
            newSchedule = new Schedule();
            newSchedule->date = date;
            schedule.append(newSchedule);
        }


        Lesson newLesson;
        newLesson.id = answerArray.at(i)["id"].toInt();
        newLesson.numberInDay = answerArray.at(i)["number_in_day"].toInt();
        newLesson.teachers = answerArray.at(i)["teachers"].toString();

        newSchedule->lesessons.insert(newLesson.numberInDay, newLesson);
    }
    return schedule;
}

bool BaseWorker::createWeekSchedule(int week, int groupId)
{
    QJsonObject param;
    param.insert("week_number", week);
    param.insert("group_id", groupId);
    post("schedule/", QJsonDocument(param));
    return true;
}

QList<Student> BaseWorker::getStudents(int groupId)
{
    QList<QPair<QString, int>> group;
    group.append(QPair<QString, int>("group_id", groupId));

    QJsonDocument answer = QJsonDocument::fromJson(get("students/", group));
    QJsonArray answerArray = answer.array();
    QList<Student> students;

    for(int i = 0; i < answerArray.size(); ++i){
        Student newStudent;
        newStudent.id = answerArray.at(i)["id"].toInt();
        newStudent.surname = answerArray.at(i)["surname"].toString();
        newStudent.name = answerArray.at(i)["name"].toString();
        newStudent.groupId = answerArray.at(i)["group_id"].toInt();
        students.append(newStudent);
    }
    return students;
}

QList<Absent> BaseWorker::getAbsents(int groupId, int weekNumber)
{

    QList<QPair<QString, int>> params;
    params.append(QPair<QString, int>("group_id", groupId));
    params.append(QPair<QString, int>("week_number", weekNumber));

    QJsonDocument answer = QJsonDocument::fromJson(get("attendance/", params));
    QJsonArray answerArray = answer.array();
    QList<Absent> absents;

    for(int i = 0; i < answerArray.size(); ++i){
        Absent newAbsent;
        newAbsent.id = answerArray.at(i)["id"].toInt();
        newAbsent.userId = answerArray.at(i)["student_id"].toInt();
        newAbsent.lessonId = answerArray.at(i)["schedule_id"].toInt();
        newAbsent.absentType = answerArray.at(i)["attendance_type_id"].toInt();
        absents.append(newAbsent);
    }
    return absents;
}

void BaseWorker::addAbsent(QList<Absent> absents)
{

    QJsonArray param;
    for(int i = 0; i < absents.count(); ++i){
        QJsonObject abs;
        abs.insert("student_id", absents.at(i).userId);
        abs.insert("schedule_id", absents.at(i).lessonId);
        abs.insert("attendance_type_id", absents.at(i).absentType);
        param.append(abs);
    }
    QJsonDocument doc;
    doc.setArray(param);
    post("attendance", doc);
}

void BaseWorker::updateAbsent(QList<Absent> absents)
{
    QJsonArray param;
    for(int i = 0; i < absents.count(); ++i){
        QJsonObject abs;
        abs.insert("id", absents.at(i).id);
        abs.insert("attendance_type_id", absents.at(i).absentType);
        param.append(abs);
    }
    QJsonDocument doc;
    doc.setArray(param);
    post("attendance/update", doc);
}

void BaseWorker::deleteAbsent(QList<int> absents)
{
    QJsonArray param;
    for(int i = 0; i < absents.count(); ++i){
        QJsonObject abs;
        abs.insert("id", absents.at(i));
        param.append(abs);
    }
    QJsonDocument doc;
    doc.setArray(param);
    post("attendance/delete", doc);
}


QByteArray BaseWorker::get(QString endpoint, QList<QPair<QString, int>> parametrs)
{

    serverUrl.setPath(QString("/api/%1").arg(endpoint));

    QUrlQuery query;

    QPair<QString, int> parametr;

    foreach(parametr, parametrs){
        qDebug() << parametr;
        query.addQueryItem(parametr.first, QString::number(parametr.second));
    }

    serverUrl.setQuery(query);

    qDebug()<<"GET " << serverUrl;

    QNetworkReply* reply = manager.get(QNetworkRequest(serverUrl));
    QEventLoop eventLoop;
    connect(reply, SIGNAL(finished()), &eventLoop, SLOT(quit()));
    eventLoop.exec();

    if (reply->error() != QNetworkReply::NoError)
        qDebug() << "Network error: " << reply->error();

    return reply->readAll();
}

QByteArray BaseWorker::post(QString endpoint,  QJsonDocument param) // QList<QPair<QString, QVariant>> parametrs)
{
    serverUrl.setPath(QString("/api/%1").arg(endpoint));
    serverUrl.setQuery(QUrlQuery());


    QNetworkRequest request;
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
    request.setUrl(serverUrl);

    qDebug()<<"POST " << serverUrl;

    QNetworkReply* reply = manager.post(request, param.toJson(QJsonDocument::Compact));

    QEventLoop eventLoop;
    connect(reply, SIGNAL(finished()), &eventLoop, SLOT(quit()));
    eventLoop.exec();

    if (reply->error() != QNetworkReply::NoError)
        qDebug() << "Network error: " << reply->error();

    return reply->readAll();
}

QByteArray BaseWorker::put(QString endpoint, QJsonDocument param)
{
    serverUrl.setPath(QString("/api/%1").arg(endpoint));
    serverUrl.setQuery(QUrlQuery());


    QNetworkRequest request;
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
    request.setUrl(serverUrl);

    qDebug()<<"PUT " << serverUrl;

    QNetworkReply* reply = manager.put(request, param.toJson(QJsonDocument::Compact));

    QEventLoop eventLoop;
    connect(reply, SIGNAL(finished()), &eventLoop, SLOT(quit()));
    eventLoop.exec();

    if (reply->error() != QNetworkReply::NoError)
        qDebug() << "Network error: " << reply->error();

    return reply->readAll();
}
