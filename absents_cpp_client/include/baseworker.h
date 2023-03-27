#ifndef BASEWORKER_H
#define BASEWORKER_H

#include <QObject>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QJsonDocument>
#include <QJsonArray>
#include <QSslConfiguration>

#include "apistructs.h"

class BaseWorker : public QObject
{
    Q_OBJECT
public:
    typedef std::function<void(const QJsonObject &)> handleFunc;

    explicit BaseWorker(QObject *parent = nullptr);
    ~BaseWorker();

    void init(const QString &host, int port);

    QList<Faculty> getFaculties();
    QList<Group> getGroups();
    QList<Schedule *> getSchedule(int group_id, int weekNumber);
    bool createWeekSchedule(int week, int groupId);
    QList<Student> getStudents(int groupId);
    QList<Absent> getAbsents(int groupId, int weekNumber);
    void addAbsent(QList<Absent> absents);
    void updateAbsent(QList<Absent> absents);
    void deleteAbsent(QList<int>);

signals:

private slots:


private:
    QUrl serverUrl;
    QSslConfiguration *sslConfig;

    QNetworkAccessManager manager;

    QByteArray get(QString endpoint, QList<QPair<QString, int> > parametrs = QList<QPair<QString, int>>());
//    QByteArray post(QString endpoint, QList<QPair<QString, QVariant> > parametrs);
    QByteArray post(QString endpoint,  QJsonDocument param);
//    QUrl concatUrl(QString endpoint);
    QByteArray put(QString endpoint,  QJsonDocument param);
    QByteArray deleteFromBase(QString endpoint, int id);
};

#endif // BASEWORKER_H
