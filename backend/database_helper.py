from __future__ import print_function
from backend.database_queries import *
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')


def initialize():
    create_database()
    insert_stopwords()


def sign_up_user(username, password):
    if insert_user(username, password):
        return_message = {"success": True, "message": "successfully signed up user"}
    else:
        return_message = {"success": False, "message": "user already exists"}
    return return_message 


def verify_user_exists(username, password):
    if verify_user(username, password):
        return_message = {"success": True, "message": "correct username and password"}
    else:
        return_message = {"success": False, "message": "username or password incorrect"}
    return return_message


def searchDB(search_string, exact_search=False):
    res_list = []
    search_words = search_string.split()

    temp_list = find_filename_from_words(search_words)
    for result in temp_list:
        res_list.append(result[0])
    if exact_search:
        res_list = find_exact_match(search_string, res_list)

    prospects = find_prospects(res_list)

    return prospects


def find_exact_match(searchString, file_list):
    path = "../backend/files/txts/"
    res = []
    for file in file_list:
        file_path = path + file[:-4] + ".txt"
        with open(file_path, 'r') as f:
            for line in f:
                if searchString in line:
                    res.append(file)
                    break
    return res


def get_message(exact_search, best_match, res_list, removed_words,
                search_string):
    if exact_search:
        if res_list:
            return ("success", "Found exact search")
        else:
            return ("danger", "Didn't find an exact search")

    elif best_match:
        if removed_words:
            return ("warning", "No matches found for all words, showing result with '"
                    + ", ".join(removed_words) + "' removed")

        elif not res_list:
            return ("danger", "No matches found for: " + search_string)

    elif removed_words:
        return ("danger", "No matches found for: " + ", ".join(removed_words))

    return ("success", "Found matches for all words")


def find_company_name(search_string, res_list):
    new_list = []
    for name in res_list:
        append_name = name
        name = name.lower()
        name = name.split(",")
        name = name[0:-1]
        name = " ".join(name)
        if (search_string in name):
            new_list.append(append_name)

    return new_list
