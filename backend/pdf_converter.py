import os
import traceback
import textract
from nltk.tokenize import word_tokenize

from backend.database_queries import *
locale.setlocale(locale.LC_ALL, str('sv_SE.UTF-8'))


def converter():
    global path

    path = 'files/downloaded/'
    cnx = MySQLConnection(user='root', password='getprospectus', host='127.0.0.1', database=DB_NAME,
                          charset='utf8mb4', collation='utf8mb4_swedish_ci', auth_plugin='mysql_native_password')
    for filename in os.listdir(path):
        if filename != 'temp':
            try:
                convert(filename, cnx)
            except:
                traceback.print_exc()
                command = "mv '" + path + filename + "'" + " files/faulty/"
                os.system(command)


def convert(filename, cnx):
    command1 = "cp '" + path + filename + "'" + " " + path + "temp; "
    command2 = "qpdf --password='' --decrypt " + path + "temp '"
    command3 = path + filename + "'"
    command = command1 + command2 + command3
    os.system(command)
    text = ''
    text = textract.process(path + filename)
    text = text.decode('utf-8')
    insert_allpdfs(filename, cnx)

    if text == "":
        print("Testing tesseract")
        text = textract.process(path + filename, method='tesseract',
                                language='swe')
        text = text.decode('utf-8')

    if text == "":
        raise ValueError("No text was extracted")

    text = text.lower()
    text = text.replace("\n", " ")
    text = text.replace("  ", " ")
    tokens = word_tokenize(text)


    """
    stop_words = [] # ignore stop words ? have function for it in database_queries.py anyways
    with open("/var/www/FlaskApps/prospect/frontend/stopwords.txt", "r") as file:
        for word in file:
            stop_words.append(word)
    """

    txt_filename = "files/txts/" + filename[:-4] + ".txt"
    with open(txt_filename, 'w+') as f:
        f.write(text)

    insert_words_from_pdf(tokens, filename.split(":")[4], cnx)

    command = "mv '" + path + filename + "'" + " files/pdfs/"
    os.system(command)


converter()