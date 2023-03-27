QT       += core gui sql network

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++17

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    src/absenttypebox.cpp \
    src/baseworker.cpp \
    src/main.cpp \
    src/mainwindow.cpp \
    src/settings.cpp

HEADERS += \
    include/absenttypebox.h \
    include/apistructs.h \
    include/baseworker.h \
    include/mainwindow.h \
    include/settings.h

FORMS += \
    ui/mainwindow.ui

TRANSLATIONS += \
    tr/Absents_ru_RU.ts

INCLUDEPATH +=\
    include


CONFIG += lrelease
CONFIG += embed_translations

LD_LIBRARY_PATH= 3rdparty/openssl-1.1.1q/

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

RESOURCES += \
    res.qrc
