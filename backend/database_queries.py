from __future__ import print_function

import locale

import bcrypt
import mysql.connector
from mysql.connector import errorcode, MySQLConnection

from time import time

locale.setlocale(locale.LC_ALL, str('sv_SE.UTF-8'))
DB_NAME = 'getProspectus'


def create_database():
    cnx = MySQLConnection(user='root', password='getprospectus', host='127.0.0.1',
                                  charset='utf8mb4', collation='utf8mb4_swedish_ci', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    tables = {}
    tables['allpdfs'] = (
        "CREATE TABLE IF NOT EXISTS `allpdfs` ("
        "  `registration_number` varchar(30) NOT NULL,"
        "  `date` varchar(20) NOT NULL,"
        "  `company` varchar(50) NOT NULL,"
        "  `type` varchar(30) NOT NULL,"
        "  `file_name` varchar(150) NOT NULL,"
        "  `id` varchar(150) NOT NULL,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB")

    tables['users'] = (
        "CREATE TABLE IF NOT EXISTS `users` ("
        "  `username` varchar(60) NOT NULL,"
        "  `password` varchar(60) NOT NULL,"
        "  PRIMARY KEY (`username`)"
        ") ENGINE=InnoDB")

    tables['stopwords'] = (
        "CREATE TABLE IF NOT EXISTS `stopwords` ("
        "  `word` char(50) NOT NULL,"
        "  PRIMARY KEY (`word`)"
        ") ENGINE=InnoDB")
    try:
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8mb4' DEFAULT COLLATE 'utf8mb4_swedish_ci'".format(
                DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database()
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)
    for table_name in tables:
        table_description = tables[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    cursor.close()
    cnx.close()


def insert_user(username, password):
    cnx = MySQLConnection(user='root', password='getprospectus', host='127.0.0.1', database=DB_NAME,
                          charset='utf8mb4', collation='utf8mb4_swedish_ci', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    statement = """INSERT INTO users (username, password) VALUES (%s, %s)"""
    values = (username, hashed)
    success = False
    try:
        cursor.execute(statement, values)
        success = True
    except mysql.connector.Error as err:
        print(err)
        success = False
    cnx.commit()
    cursor.close()
    cnx.close()
    return success


def verify_user(username, password):
    cnx = MySQLConnection(user='root', password='getprospectus', host='127.0.0.1', database=DB_NAME,
                          charset='utf8mb4', collation='utf8mb4_swedish_ci', auth_plugin='mysql_native_password')
    cursor = cnx.cursor(dictionary=True)

    statement = "SELECT username, password FROM users WHERE username = '{}'".format(username)

    try:
        cursor.execute(statement)
    except mysql.connector.Error as err:
        print(err.msg)
    result = cursor.fetchone()
    cnx.commit()
    cursor.close()
    cnx.close()
    if result:
        return bcrypt.checkpw(password.encode('utf-8'), result['password'].encode('utf-8'))
    return False


def insert_stopwords():
    cnx = MySQLConnection(user='root', password='getprospectus', host='127.0.0.1', database=DB_NAME,
                          charset='utf8mb4', collation='utf8mb4_swedish_ci', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()

    add_words = "INSERT IGNORE INTO stopwords (word) VALUES "
    with open("../backend/stopwords.txt", "r") as file:
        for word in file:
            add_words += "(\"" + word.replace("\n", "") + "\"),"

    statement = (add_words[:-1])

    try:
        cursor.execute(statement)
        print("Stopwords inserted successfully")
    except mysql.connector.Error as err:
        print(err.msg)
    cnx.commit()

    cursor.close()
    cnx.close()


def insert_allpdfs(pdf, cnx):

    cursor = cnx.cursor()

    dic = {}
    splitted = pdf.split(":")
    dic["registration_number"] = splitted[0]
    dic["date"] = splitted[1]
    dic["company"] = splitted[2]
    dic["type"] = splitted[3]
    dic["id"] = splitted[4]

    statement = "INSERT INTO allpdfs (registration_number, date, company, type, file_name, id) VALUES "

    statement += "(\"" + dic["registration_number"] + "\",\"" + dic["date"] + "\",\"" + dic["company"] + "\",\"" + \
                 dic["type"] + "\",\"" + pdf + "\",\"" + dic["id"] + "\")"

    try:
        cursor.execute(statement)
        print("Pdf inserted successfully")
    except mysql.connector.Error as err:
        print(err.msg)
    cnx.commit()

    cursor.close()


def insert_words_from_pdf(tokens, pdf, cnx):
    start = time()

    cnx.autocommit = False
    cursor = cnx.cursor()
    token_word_count = {}
    for token in tokens:
        if token in token_word_count:
            token_word_count[token] += 1
        else:
            token_word_count[token] = 1
    create_table_list = []
    insert_statement_list = []
    for word, count in token_word_count.items():
        if word.isalnum():
            insert_statement = "INSERT INTO `" + word + "` (pdf, count) values (\"" + pdf + "\"," + str(count) + ")"
            try:
                # First, try to insert the pdf in the word table
                cursor.execute(insert_statement)
                cnx.commit()
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_NO_SUCH_TABLE:
                    statement = ("CREATE TABLE `" + word + "` ("
                                                           " `pdf` varchar(100) NOT NULL,"
                                                           " `count` int(20) NOT NULL,"
                                                           "  PRIMARY KEY (`pdf`)"
                                                           ") ENGINE=InnoDB")
                    create_table_list.append(statement)
                    insert_statement_list.append(insert_statement)
                    # cursor.execute(statement)
                    # cursor.execute(insert_statement)
                else:
                    print(err.msg)
        # else: # TODO --- Do better filtering of words here
        # print("Word is not alpha-numerical: " + token)
        # print("Size of token is: " + len(token))
    commit_start = time()
    cnx.start_transaction()
    for i in range(0, len(create_table_list)):
        if i % 500 == 0:
            cnx.commit()
            cnx.start_transaction()
            print("Commit of 500 tokens took " + str(time() - commit_start) + " seconds")
            commit_start = time()
        cursor.execute(create_table_list[i])
        cursor.execute(insert_statement_list[i])

    cnx.commit()
    cursor.close()

    print(pdf + " with " + str(len(tokens)) + " words took " + str(time() - start) + " seconds" + "\n")


def find_filename_from_words(words):
    cnx = MySQLConnection(user='root', password='getprospectus', host='127.0.0.1', database=DB_NAME,
                                  charset='utf8mb4', collation='utf8mb4_swedish_ci', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()

    if len(words) == 1:
        statement = "SELECT file_name FROM allpdfs WHERE id in (SELECT " + words[0] + ".pdf FROM " + \
                    words[0]
    else:
        statement = "SELECT file_name FROM allpdfs WHERE id in (SELECT " + words[0] + ".pdf FROM " + \
                    words[0] + " inner join " + words[1] + " on " + words[0] + ".pdf=" + words[1] + ".pdf"

        for i in range(2, len(words)):
            statement += " inner join " + words[i] + " on " + words[i - 1] + ".pdf=" + words[i] + ".pdf"
    statement += ")"
    try:
        cursor.execute(statement)
    except mysql.connector.Error:
        cnx.commit()
        cursor.close()
        return []
    result = cursor.fetchall()
    cnx.commit()

    cursor.close()
    cnx.close()
    return result


def find_prospects(file_list):
    cnx = MySQLConnection(user='root', password='getprospectus', host='127.0.0.1', database=DB_NAME,
                                  charset='utf8mb4', collation='utf8mb4_swedish_ci', auth_plugin='mysql_native_password')

    cursor = cnx.cursor()
    statement = "SELECT * FROM allpdfs WHERE file_name in ("
    for file in file_list:
        statement += "\"" + file + "\","
    statement = statement[:-1] + ")"

    try:
        cursor.execute(statement)
    except mysql.connector.Error:
        cnx.commit()
        cursor.close()
        return {}
    result = cursor.fetchall()
    cnx.commit()
    cursor.close()
    prospects = []
    for res in result:
        dic = {}
        dic["download_link"] = res[4]
        dic["date"] = res[1]
        dic["type"] = res[3]
        dic["company_name"] = res[2]
        dic["open_in_browser"] = ""
        prospects.append(dic)
    cnx.close()
    return prospects

