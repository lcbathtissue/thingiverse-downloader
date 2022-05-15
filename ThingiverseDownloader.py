import os
import time
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

hideBrowser = True

print("Enter URL's, enter 'exit' to exit..")
URL = input("Please enter a thiniverse.com URL: ")
if URL == "exit":
    exit(0)

seleBrowserPath = "C:\Program Files (x86)\chromedriver.exe"

if hideBrowser:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    seleDriver = webdriver.Chrome(seleBrowserPath, options=chrome_options)
else:
    seleDriver = webdriver.Chrome(seleBrowserPath)


def download_files(URL):
    print()
    if URL.find("/files") == -1:
        if URL[-1] == "/":
            URL = URL + "files"
        else:
            URL = URL + "/files"

    seleDriver.get(URL)
    time.sleep(5)

    page_contents = str(seleDriver.page_source.encode('utf-8'))
    page_contents = page_contents[page_contents.find("ThingFilesListHeader"):]
    name_position = page_contents.find("ThingFilesListHeader__fileName") + len("ThingFilesListHeader__fileName") + 9
    project_name = page_contents[name_position:]
    project_name = project_name[:project_name.find("</")]
    os.mkdir(project_name)
    end_of_files_position = page_contents.find("ThingFilePolicy__thingFilePolicyContainer") + len(
        "ThingFilePolicy__thingFilePolicyContainer") + 9
    files_contents = page_contents[:end_of_files_position]
    file_soup = BeautifulSoup(files_contents, features="lxml")
    for anchor_element in file_soup.find_all("a"):
        for href_tag in anchor_element:
            file_name = anchor_element.get('download')
            href = anchor_element.get('href')
            urllib.request.urlretrieve(href, f"{project_name}/{file_name}")

    policy_contents = page_contents[end_of_files_position:]
    policy_soup = BeautifulSoup(policy_contents, features="lxml")
    policy = policy_soup.text
    policy = policy.replace(r"\n", "")
    policy = policy.replace(r"\t", "")
    policy = policy.replace("Back to Top", "")
    policy = policy.replace("License", "License\n")
    policy = policy.replace(" by", "\nby ")
    policy = policy.replace(" licensed", "\nlicensed")
    policy = policy.replace("Non-Commerciallicense", "Non-Commercial license")
    policy = policy.replace("By downloading this thing,", "\nBy downloading this thing,")
    policy = policy.replace("by  the license", "by the license")
    policy = policy.replace("abide\nby", "abide by")
    policy = policy.replace(" by the license: ", " by the license:\n")
    if policy[policy.find("under the") + len("under the") + 1] != " " or policy[
        policy.find("under the") + len("under the") + 1] != "\n":
        policy = policy.replace("under the", "under the ")
    if policy[policy.find(".") + 2] != " " or policy[policy.find(".") + 2] != "\n":
        policy = policy.replace(".", ". ")
    policy = policy.strip()
    policy = policy.split("\n")
    reassembled_policy_string = ""
    while len(policy[-1]) <= 1:
        policy.pop(len(policy) - 1)
    for index, policy_part in enumerate(policy):
        if index == 0:
            reassembled_policy_string = reassembled_policy_string + policy_part + ":\n"
        elif index == 1:
            reassembled_policy_string = reassembled_policy_string + policy_part + f" ({URL})" + "\n"
        elif index == 2:
            reassembled_policy_string = reassembled_policy_string + policy_part + " (thingiverse.com)" + "\n\n"
        elif index == 3:
            reassembled_policy_string = reassembled_policy_string + policy_part[0].upper() + policy_part[1:] + "\n"
        else:
            reassembled_policy_string = reassembled_policy_string + policy_part + "\n"
    reassembled_policy_string = reassembled_policy_string[:-1]
    with open(f"{project_name}/LICENSE.TXT", "w", encoding="utf-8") as policy_file:
        policy_file.write(reassembled_policy_string)
    policy_file.close()
    print(reassembled_policy_string)


download_files(URL)
while URL != "exit":
    URL = input("\nPlease enter a thiniverse.com URL: ")
    download_files(URL)
    if URL == "exit":
        exit(0)

seleDriver.close()
