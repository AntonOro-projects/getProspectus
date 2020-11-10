import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime

DATE_INDEX = 0
NAME_INDEX = 1
TYPE_INDEX = 2
ARCHIVE_HREF_INDEX = 3
REGISTRY_HREF_INDEX = 4


def main():
    archive_url = 'https://www.fi.se/sv/vara-register/prospektarkiv/?query=&vardepapper=&dokumenttyp=&year='
    registry_url = 'https://www.fi.se/sv/vara-register/prospektregistret/?query=&vardepapper=&dokumenttyp=&year='

    prospectus_finder(archive_url, datetime.now().year, ARCHIVE_HREF_INDEX)
    prospectus_finder(registry_url, datetime.now().year, REGISTRY_HREF_INDEX)


def prospectus_finder(prospectus_url, start_year, href_index):
    """ Finds the pages of prospectuses from the start year to current year"""
    for year in range(start_year, datetime.now().year+1):
        print(year)
        url = prospectus_url + str(year)
        website = urlopen(url)

        # Decode website into string string
        html = website.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')

        # Loop through all the individual prospectuses for the current year
        for prospect in soup.find_all('tr'):
            # Collect the link to the prospect
            for a in prospect.find_all('a', href=True):
                prospectus_downloader(a['href'], href_index)


def prospectus_downloader(url, href_index):
    """ Finds and downloads all prospectuses for the given link"""
    base_path = "https://www.fi.se/"
    full_path = base_path + url
    website = urlopen(full_path)

    # Decode website into string string
    html = website.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    headers = soup.find_all('h1')
    registration_number = ""

    # If the header contains the registration number, then extract that number
    for header in headers:
        if "Diarienummer" in header.contents[0]:
            registration_number = header.contents[0].split(": ")[1]
            break
    if not registration_number:  # TODO -- add some error message here
        print("No registration number found!")
        return

    prospect_info_list = soup.find('tbody').find('tr').find_all('td')

    date = prospect_info_list[DATE_INDEX].contents[0]
    name = prospect_info_list[NAME_INDEX].contents[0]
    try:
        type = prospect_info_list[TYPE_INDEX].contents[0]
    except IndexError:
        type = " "

    href = prospect_info_list[href_index].contents[0]['href'].split("&format")[0]

    id = href.split("?id=")[1]

    if check_if_string_in_file('downloaded_pdfs_links.txt', href):
        print("The file with link " + href + " has already been downloaded!")
        return
    else:
        sys_path = 'files/downloaded/'
        file_name = registration_number + ":" + date + ":" + name.replace('/', '') + ":" + type + ":" + id + ".pdf"
        download_url = "https://www.fi.se" + href
        command = 'wget'
        os.system("%s -q -O %s %s" % (command, "'" + sys_path + file_name + "'",
                                   download_url))
        with open('downloaded_pdfs_links.txt', 'a+') as file:
            file.write(str(href) + "\n")


def check_if_string_in_file(file_name, string_to_search):
    """ Check if any line in the file contains given string """
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if string_to_search in line:
                return True
    return False


main()
