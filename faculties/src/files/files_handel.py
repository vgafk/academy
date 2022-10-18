from db.resolvers import add_group


class FileHandler:

    @staticmethod
    async def add_batch_group(data_bytes: bytes):
        data = data_bytes.decode('utf8')
        for row in data.split('\n'):
            group_data = row.split(',')
            try:
                faculty_id = int(group_data[0])
                new_group = {
                    'faculty_id': faculty_id,
                    'name': group_data[1],
                    'full_name': group_data[2],
                }
                await add_group(new_group=new_group)
            except ValueError:
                continue
