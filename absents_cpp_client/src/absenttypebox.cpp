#include "absenttypebox.h"

AbsentTypeBox::AbsentTypeBox(int studentId, int lessonId):
    studentId(studentId)
  , lessonId(lessonId)
  , id(0)
{
    addAbsentTypes();
    connect(this, qOverload<int>(&AbsentTypeBox::currentIndexChanged), this, &AbsentTypeBox::typeChanget);
    //    setCurrentIndex(type);
}

void AbsentTypeBox::addAbsentTypes()        //TODO сделать загрузку названий и иконок из базы
{
    //    addItem("-----");
    //    addItem(QIcon(":/icons/button_ok_4514.png"), "Прис.", 1);
    //    addItem(QIcon(":/icons/dialog-error_3549.png"), "Прогул", 3);
    //    addItem(QIcon(":/icons/status_unknown_5125.png"), "Уваж.", 2);
    //    addItem(QIcon(":/icons/button_cancel_8964.png"), "Отмена", 4);

    addItem(QIcon(":/icons/button_ok_4514.png"), "", 1);
    addItem(QIcon(":/icons/dialog-error_3549.png"), "", 3);
    addItem(QIcon(":/icons/status_unknown_5125.png"), "", 2);
}

int AbsentTypeBox::getLessonId() const
{
    return lessonId;
}

void AbsentTypeBox::setType(int type)
{
    for(int index = 0; index < count(); ++index )
        if(itemData(index) == type){
            setCurrentIndex(index);
            break;
        }
}

void AbsentTypeBox::setId(int newId)
{
    id = newId;
}

int AbsentTypeBox::getId()
{
    return id;
}

int AbsentTypeBox::getType()
{
    return currentData().toInt();
}

void AbsentTypeBox::typeChanget(int newIndex)
{
    Q_UNUSED(newIndex)

    emit changet();
    //    if(id){
    //        if(!newIndex){
    //            emit deleteAbsent(id);
    //       } else {
    //            emit updateAbsent(id, currentData().toInt());
    //        }
    //    } else {
    //       emit addAbsent(lessonId, currentData().toInt());
    //    }
}

int AbsentTypeBox::getStudentId() const
{
    return studentId;
}
