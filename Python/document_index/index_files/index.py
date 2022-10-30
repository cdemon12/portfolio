import subprocess
from whoosh.fields import Schema, ID, KEYWORD, TEXT, DATETIME
from whoosh.index import create_in, open_dir
import os
from contextlib import contextmanager
from os import listdir
import re
from connect import connect
import traceback

# Creates index of all files using Whoosh

# all file paths for index, pdfs, text
index_path = 'C:/Users/Cole Schnell/Desktop/Summer/Learn/project-2/CPS_meeting_index'
pdfs_path = f'{index_path}/pdfs'
text_path = f'{index_path}/text'

#create directory files lists
pdfs_dir = listdir(pdfs_path)
text_dir = listdir(text_path)


def main():
    #create text for all pdfs
    for path in pdfs_dir:
        removepdf = re.split("\.", path)
        subprocess.call(['pdftotext', 
                        '-enc', 
                        'UTF-8', 
                        f'{pdfs_path}/{path}', 
                        f'{text_path}/{removepdf[0]}.txt'])
    
    #create schema for index
    pdf_schema = Schema(id = ID(unique=True, stored=True),
                    meeting_id = ID(unique=True, stored=True),
                    path = ID(stored=True),
                    source = ID(stored=True),
                    url = ID(stored=True),
                    date = DATETIME(stored=True),
                    type = ID(stored=True),
                    text = TEXT
                    )

    
    #create index
    if not os.path.exists(index_path):
        os.mkdir(index_path)
    
    index = create_in(index_path, pdf_schema)

    #open index
    index = open_dir(index_path)
    writer = index.writer()
    for path in text_dir:
        scrap_path = re.split('-', path)
        month = scrap_path[-4]
        day = scrap_path[-3]
        year = scrap_path[-2]
        file_date = f"{year}-{month}-{day}"


        #open sql connection
        with connect() as conn:
            try:
                cur = conn.cursor()
                cur.execute(get_info % file_date)
                ans = cur.fetchall()
            except Exception as e:
                conn.rollback()
                print(e)
                traceback.print_exc()

        sql_id = str(ans[0][0]).encode('utf-8').decode('utf-8')
        sql_type = ans[0][1]
        sql_url = ans[0][2]

        removetxt = re.split("\.", path)

        writer.add_document(
            id = sql_id,
            path = f'{text_path}/{path}',
            source = f'{pdfs_path}/{removetxt[0]}.pdf',
            url = sql_url,
            date = file_date,
            type = sql_type,
            text = open(f'{text_path}/{path}', encoding='utf-8').read()
        )
    writer.commit()



#create sql command
get_info = '''
    SELECT meeting_id, type, url FROM meetings
    WHERE date LIKE '%s%%';
'''

if __name__ == '__main__':
    main()