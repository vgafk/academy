#ifndef SETTINGS_H
#define SETTINGS_H

#include <QObject>
#include <QSettings>

class Settings : public QObject
{
    Q_OBJECT

public:
    explicit Settings();
    static Settings *instance();

    void setHostAddress(QString address, int port);
    QPair<QString, int> getHostAddress();


private:
    void setValue(QString key, QVariant value);
    QVariant getValue(QString key);
};

#endif // SETTINGS_H
