from connect import connect
import pandas as pd
import traceback
from create_meetings import meetings_with_minutes

# Creates SQL database for meetings and files

def main():

    with connect() as conn:
        try:
            cur = conn.cursor()
            cur.execute(create_table)
            
            for meeting in meetings:
                cur.execute(insert_values, [meeting.id, meeting.date, meeting.type, meeting.url])

            conn.commit()
        except Exception as e:
            conn.rollback()
            print(e)
            traceback.print_exc()


meetings = meetings_with_minutes

table = 'meetings'

#SQL commands
create_table = f'''
    CREATE TABLE {table} (
        meeting_id int primary key,
        date varchar,
        type varchar,
        url varchar
        )
'''

insert_values = f'''
    INSERT INTO {table} (meeting_id, date, type, url)
    VALUES (%s, %s, %s, %s)
    '''

if __name__ == "__main__":
    main()
