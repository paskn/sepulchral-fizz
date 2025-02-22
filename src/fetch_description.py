from string import ascii_uppercase
from urllib.parse import urljoin

import requests

from waybackpy import WaybackMachineCDXServerAPI

import time
from bs4 import BeautifulSoup
import pandas as pd


def get_wayb(url):
    user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"
    print(f'Respectfully asking for {url}...')
    oldest_url = WaybackMachineCDXServerAPI(url, user_agent).oldest().archive_url

    time.sleep(15)
    return oldest_url


def get_char_names(char_names, novel_name):
    # get the page
    page = requests.get(char_names)
    # find the table with chars
    soup = BeautifulSoup(page.content, "html.parser")
    section_id = soup.find(
        lambda tag: tag.name == "h3" and novel_name in tag.get_text()
    )
    section_id = section_id.get("id")
    # get the table with char names
    novel_section = soup.find("h3", id=section_id)
    novel_char_list = novel_section.find_next("table")
    return novel_char_list


def get_char_targets(novel_char_list):
    chars = { a.get_text(strip=True): a.get("href") for a in novel_char_list.find_all("a") }
    return chars


def collect_descriptions(char_names, target_base):
    char_link = [get_wayb(target_base + link) for link in char_names.values()]
    
    char_targets = {}
    for name, link in zip(char_names.keys(), char_link):
        char_targets[name] = {"page_tag": char_names[name],
                 "page_link": link}

    page_targets = list(
        set([inner["page_link"] for inner in char_targets.values()])
    )

    def fetch_kindly(url):
        print(f"Kindly asking for {url}...")
        page = requests.get(url)
        time.sleep(15)
        return page.content

    
    scraped_targets = {}
    for target in page_targets:
        scraped_targets[target] = fetch_kindly(target)

        
    def extract_description(pages, url, tag):
        soup = BeautifulSoup(pages[url], "html.parser")
        id = tag.split("#")[1]
        desc = soup.find("a",{"name": id}).find_next("p").get_text()
        return desc

    char_descriptions = {}
    for name in char_targets:
        char_descriptions[name] = extract_description(
            scraped_targets,
            char_targets[name]['page_link'],
            char_targets[name]['page_tag'])

    return char_descriptions


if __name__ == '__main__':
    novel_name = "Our Mutual Friend"

    target_base = "https://m.charlesdickenspage.com/"
    target_chars_novel = "charles-dickens-characters-by-novel.html"

    char_list = get_wayb(target_base + target_chars_novel)
    char_names = get_char_names(char_list, novel_name)
    char_names = get_char_targets(char_names)

    char_descriptions = collect_descriptions(char_names, target_base)
    data = pd.DataFrame(char_descriptions.items(), columns=["Name", "Description"])
    data.to_csv("char_descs.csv", index=False)
