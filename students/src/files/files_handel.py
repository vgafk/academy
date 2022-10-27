from enum import Enum
from loguru import logger
from db.resolvers import add_student


class StudentDataFields(Enum):
    SURNAME = 0
    NAME = 1
    MIDDLE_NAME = 2
    SNILS = 3
    INN = 4
    EMAIL = 5
    PHONE = 6
    STUDY_YEAR = 7
    GROUP_ID = 8


class FileHandler:

    @staticmethod
    async def add_batch_students(data_bytes: bytes):
        data = data_bytes.decode('utf8')
        for row in data.split('\n'):
            student_data = row.split(',')
            if student_data[StudentDataFields.SURNAME.value] == 'surname':
                continue
            try:
                new_student = {
                    'surname': student_data[StudentDataFields.SURNAME.value],
                    'name': student_data[StudentDataFields.NAME.value],
                    'middle_name': student_data[StudentDataFields.MIDDLE_NAME.value],
                    'snils': student_data[StudentDataFields.SNILS.value],
                    'inn': student_data[StudentDataFields.INN.value],
                    'email': student_data[StudentDataFields.EMAIL.value],
                    'phone': student_data[StudentDataFields.PHONE.value],
                    'study_year': student_data[StudentDataFields.STUDY_YEAR.value],
                    'group_id': student_data[StudentDataFields.GROUP_ID.value],
                }
                await add_student(student=new_student)
            except ValueError as ex:
                logger.warning(f'При добавлении студента: {ex}')
                continue
            except IndexError as ex:
                logger.info(ex)
