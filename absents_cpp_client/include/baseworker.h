#ifndef BASEWORKER_H
#define BASEWORKER_H

#include <QObject>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include "apistructs.h"

class BaseWorker : public QObject
{
    Q_OBJECT
public:
    explicit BaseWorker(QObject *parent = nullptr);

public slots:
    void getFacultyList();

signals:
    void facultyList(QList<Faculty>);

private slots:
    void slotReadyRead();
    void slotError(QNetworkReply::NetworkError error);

private:
    QNetworkAccessManager manager;
    QNetworkRequest request;
    QNetworkReply* reply;

    QUrl concatUrl(QString endpoint);
    void makeReques(QString endpoint);
};

#endif // BASEWORKER_H
