#ifndef APISTRUCTS_H
#define APISTRUCTS_H

#include <QString>

struct Faculty{
    int id;
    QString name;
};

struct Group{
    int id;
    QString name;
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


#endif // APISTRUCTS_H
