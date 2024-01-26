from typing import Dict, List
import requests
import os
from bs4 import BeautifulSoup
import json
import threading
import imageio_ffmpeg

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import argparse


def getUrlList(url: str, web: webdriver) -> List[str]:
    web.get(url)
    sleep(1)
    lectures = web.find_elements(By.CLASS_NAME, "tum-live-stream")
    return [lecture.find_element(By.TAG_NAME, "a").get_attribute("href") for lecture in lectures]


def getSegments(url: str, web: webdriver) -> List[str]:
    web.get(url)
    playlist = BeautifulSoup(web.page_source, features="html.parser").find("video-js")
    playlist = playlist.source["src"]
    groundUrl = playlist[: playlist.find("playlist.m3u8") - 1]
    segments = requests.get(playlist).text.split(",\n")
    if len(segments) == 1:
        key = segments[0][segments[0].rindex("_") + 1 : segments[0].rindex(".")]
        segments.append(groundUrl + "/" + "media_" + key + "_")
        segments.pop(0)
    else:
        segments.pop(0)
        for i in range(len(segments)):
            segments[i] = segments[i].split("#")[0]
            segments[i] = groundUrl + "/" + segments[i]
    return segments


def findSegmentName(url: str) -> str:
    first = url.find("segment") + 7
    if first == 6:
        first = url.rindex("_") + 1
    last = url.find(".", first)
    return url[first:last] + ".ts"


def findName(url: str) -> str:
    last = url.find(".mp4")
    first = url.rindex("/", 0, last) + 1
    name = url[first:last]
    name = name.split("_")
    name.pop()
    name.pop()
    return "_".join(name)


def downloadSegment(segment: str, tmpPath: str) -> bool:
    response = requests.get(segment)
    if response.status_code != 200:
        return False

    open(tmpPath + findSegmentName(segment), "wb").write(response.content)
    return True


def writeTsList(tmpPath: str) -> None:
    path = tmpPath  # specify the path to the directory containing the .ts files
    ts_files = [f for f in os.listdir(path) if f.endswith(".ts")]

    ts_files.sort()

    with open(f"{tmpPath}mylist.txt", "w") as f:
        for file in ts_files:
            f.write("file '" + file + "'\n")


def downloadLecture(url: str, web: webdriver, path: str, tmpPath: str) -> str:
    segments = getSegments(url, web)
    name = findName(segments[0])
    print("--- " + name + " ---")

    # print("Downloading Segments . . . ", end="", flush=True)
    # if len(segments) == 1:
    #     available = True
    #     counter = 0
    #     while available:
    #         available = downloadSegment(
    #             segments[0] + str(counter).zfill(4) + ".ts", tmpPath
    #         )
    #         counter = counter + 1
    # else:
    #     for segment in segments:
    #         downloadSegment(segment, tmpPath)

    # print("done!")

    print("Merging . . . ", end="", flush=True)
    writeTsList(tmpPath)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    os.system(
        f"{ffmpeg} -hide_banner -loglevel error -f concat -i "
        + tmpPath
        + "mylist.txt -c copy "
        + tmpPath
        + "all.ts"
    )
    print("done!")
    print("Converting . . . ", end="", flush=True)
    os.system(
        f"{ffmpeg} -hide_banner -loglevel error -i "
        + tmpPath
        + "all.ts -acodec copy -vcodec copy "
        + path
        + name
        + ".mp4"
    )
    print("done!\n")
    tmpPath = (
        tmpPath.replace("/", "\m").removesuffix("m") if os.name == "nt" else tmpPath
    )
    remove = "del" if os.name == "nt" else "rm"
    os.system(f"{remove} {tmpPath}*.ts")
    os.system(f"{remove} {tmpPath}mylist.txt")
    return path + name + ".mp4"


def login(username: str, password: str) -> webdriver:
    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument("--headless")
    if os.getenv("NO-SANDBOX") == "1":
        driver_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=driver_options)

    driver.get("https://live.rbg.tum.de/login")
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


def appendLockFile(id: str, new_data: str, filename: str = "lock.json") -> None:
    if os.path.isfile(filename):
        with open(filename, "r") as f:
            data = json.load(f)
        if new_data not in data.get(id, []):
            data.setdefault(id, []).append(new_data)
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
    else:
        data = {id: [new_data]}
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)


def locked(id: str, lecture: str, filename: str = "lock.json") -> bool:
    if not os.path.isfile(filename):
        return False
    with open(filename, "r") as f:
        data = json.load(f)
        return lecture in data.get(id, [])


class Downloader:
    def __init__(self):
        self.stop: bool = False
        self.running: bool = True

    def downloadCourseList(
        self,
        courses: dict,
        url: str,
        username: str,
        password: str,
        tmpPath: str,
        path: str,
    ):
        web = login(username, password)
        os.system("cls" if os.name == "nt" else "clear")
        os.path.isdir(tmpPath) or os.mkdir(tmpPath)
        for courseName, info in courses.items():
            if self.stop:
                break
            print("*** " + courseName + " ***")
            try:
                if not os.path.isdir(os.path.join("./", path, courseName)):
                    os.makedirs(os.path.join("./", path, courseName))
            except FileNotFoundError:
                print("The specified directory could not be found or created.")
            urls = getUrlList(url + f"?year={info["year"]}&term={info["semester"]}&slug={info["title"]}&view=3", web)
            for lecture in urls:
                if self.stop:
                    break
                if not locked(info, lecture):
                    downloadedPath = downloadLecture(
                        lecture, web, path + courseName + "/", tmpPath
                    )
                    if os.path.isfile(downloadedPath):
                        appendLockFile(info, lecture)
                else:
                    print("Already Downloaded: " + lecture + " ✅\n")
        os.rmdir(tmpPath)
        self.running = False


def start(
    courses: Dict[str, str],
    url: str,
    username: str,
    password: str,
    tmpPath: str,
    path: str,
) -> None:
    downloader = Downloader()
    loop_thread = threading.Thread(
        target=downloader.downloadCourseList,
        args=(courses, url, username, password, tmpPath, path),
    )
    loop_thread.start()
    while downloader.running:
        try:
            loop_thread.join(0.1)
        except KeyboardInterrupt:
            downloader.stop = True
