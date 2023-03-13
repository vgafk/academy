#include "baseworker.h"

#include "settings.h"

BaseWorker::BaseWorker(QObject *parent)
    : QObject{parent}
{
}

void BaseWorker::getFacultyList()
{
    makeReques("faculties");
}

void BaseWorker::slotReadyRead()
{
    qDebug() << reply->readAll();
}

void BaseWorker::slotError(QNetworkReply::NetworkError error)
{
    qCritical() << error;
}

QUrl BaseWorker::concatUrl(QString endpoint)
{
    QPair<QString, int> host = Settings::instance()->getHostAddress();
    QUrl url = QUrl(QString("http://%1:%2/%3").arg(host.first).arg(host.second).arg(endpoint));\
    return url;
}

void BaseWorker::makeReques(QString endpoint)
{
    request.setUrl(concatUrl(endpoint));
    reply = manager.get(request);


    qDebug() << reply->readAll();
//    connect(reply), &QNetworkReply::readyRead, this, &BaseWorker::slotReadyRead);
//    connect(reply.get(), &QNetworkReply::errorOccurred, this, &BaseWorker::slotError);

//
//    connect(manager, &QNetworkAccessManager::, this, &BaseWorker::slotError);
//    manager.get(request);
}
