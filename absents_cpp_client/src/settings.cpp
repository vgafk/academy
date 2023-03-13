#include "settings.h"

Settings::Settings()
{

}

Q_GLOBAL_STATIC(Settings, global_inst)

Settings *Settings::instance(){
    return global_inst();
}

void Settings::setHostAddress(QString address, int port)
{
    setValue("host_address", address);
    setValue("host_port", port);
}

QPair<QString, int> Settings::getHostAddress()
{
    return qMakePair(getValue("host_address").toString(), getValue("host_port").toInt());
}

void Settings::setValue(QString key, QVariant value)
{
    QSettings settings("config.ini", QSettings::IniFormat);
    settings.setValue(key, value);
}

QVariant Settings::getValue(QString key)
{
    QSettings settings("config.ini", QSettings::IniFormat);
    return settings.value(key);
}
