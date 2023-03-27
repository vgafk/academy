#ifndef ABSENTTYPEBOX_H
#define ABSENTTYPEBOX_H

#include <QComboBox>
#include <QObject>
#include <QWidget>

class AbsentTypeBox : public QComboBox
{
    Q_OBJECT

public:
    enum AbnsetType{
        NotSet,
        Present,
        HaveReason,
        NotReason,
        LessonCanceled
    };

    AbsentTypeBox(int studentId, int lessonId);
    int getStudentId() const;
    int getLessonId() const;
    void setType(int type);
    void setId(int newId);
    int getId();
    int getType();

signals:
    void changet();
//    void updateAbsent(int, int);
//    void addAbsent(int, int);
//    void deleteAbsent(int);

private slots:
    void typeChanget(int newIndex);

private:
    void addAbsentTypes();
    const int studentId;
    const int lessonId;
    int id;
    int sourseType;
};

#endif // ABSENTTYPEBOX_H
