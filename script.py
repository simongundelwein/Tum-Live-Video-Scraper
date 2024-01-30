from datetime import datetime
import re
from typing import List, Optional, Tuple
import os
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import argparse


def login(username: str, password: str) -> webdriver:
    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument("--headless")
    if os.getenv("NO-SANDBOX") == "1":
        driver_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=driver_options)

    driver.get("https://live.rbg.tum.de/login")
    sleep(1)
    # all possible By. options
    driver.find_element(By.LINK_TEXT, "TUM Login").click()
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "btnLogin").click()
    sleep(1)
    if "Moin Simon" in driver.page_source:
        print("Login successful")
        return driver
    driver.close()
    raise argparse.ArgumentTypeError("Username or password incorrect")


load_dotenv()

WEB = login(os.getenv("USERNAME"), os.getenv("PASSWORD"))


def get_title_and_m3u8(lecture_url: str) -> Tuple[str, str]:
    WEB.get(lecture_url)
    sleep(1)
    title = WEB.find_element(By.TAG_NAME, "h1").text.strip()
    # if title in form "Lecture: December 05. 2024"
    try:
        title = datetime.strptime(title, "Lecture: %B %d. %Y").strftime("%Y-%m-%d")
    except ValueError:
        pass
    source = WEB.page_source
    middle_index = source.find("playlist.m3u8")
    start_index = source.rfind('"', 0, middle_index) + 1
    end_index = source.find('"', middle_index)
    m3u8_url = source[start_index:end_index]
    return title, m3u8_url


def get_lectures_per_course(
    course_url: str, start_date: Optional[datetime] = None
) -> List[str]:
    WEB.get(course_url)
    sleep(1)
    lecture_elements = WEB.find_elements(By.CLASS_NAME, "tum-live-stream")
    if start_date is not None:
        lecture_elements = [
            lecture
            for lecture in lecture_elements
            if datetime.strptime(
                lecture.find_element(By.CLASS_NAME, "date").text.split(", ")[1],
                "%m/%d/%Y",
            )
            >= start_date
        ]
    return [
        lecture.find_element(By.TAG_NAME, "a").get_attribute("href")
        for lecture in lecture_elements
    ]


def download_lecture(lecture_url: str, path: Optional[str] = None):
    title, m3u8 = get_title_and_m3u8(lecture_url)
    sanitized_title = re.sub(r'[\\/*?:. "<>|]', "_", title).strip("_")

    if path is None:
        path = os.getcwd()
    else:
        if not os.path.exists(path):
            os.makedirs(path)
    new_file_path = os.path.join(path, sanitized_title + ".mp4")
    os.system(
        f'ffmpeg -i {m3u8} -c copy -bsf:a aac_adtstoasc -loglevel error "{new_file_path}"'
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download lectures from TUM Live")
    parser.add_argument(
        "course",
        type=str,
        help="The URL of the course you want to download",
    )
    parser.add_argument(
        "path",
        type=str,
        help="The path where the lectures should be saved",
        default=os.getcwd(),
    )
    parser.add_argument(
        "--start-date",
        type=str,
        help="The start date of the lectures you want to download (format: YYYY-MM-DD)",
        default="",
    )
    args = parser.parse_args()
    if args.start_date:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
        lectures = get_lectures_per_course(args.course, start_date=start_date)
    else:
        lectures = get_lectures_per_course(args.course)
    for lecture in lectures:
        download_lecture(lecture, args.path)
