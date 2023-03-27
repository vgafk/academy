#ifndef APISTRUCTS_H
#define APISTRUCTS_H

#include <QDate>
#include <QString>

struct Faculty{
    int id;
    QString fullName;
    QString name;
};

struct Group{
    int id;
    QString name;
    QString fullName;
    int facultyId;
};

struct SubGroup{
    int id;
    QString name;
    QString comments;
    int groupId;
};

struct Student{
    int id;
    QString surname;
    QString name;
    QString middleName;
    int groupId;
    int subgroupId;
};

struct Lesson{
    int id;
     int numberInDay;
     QString teachers;
};

struct Schedule{
    QDate date;
//    int numberInDay;
//    int weekNumber;
//    int groupId;
//    QString groupName;
//    QString teachers;
    QMap<int, Lesson> lesessons;
};


struct Absent{
    int id;
    int lessonId;
    int userId;
    int absentType;
};


#endif // APISTRUCTS_H
