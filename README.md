# Tum Live Video Scraper

## Disclaimer

This README is out of date. I'm too lazy to update it now but maybe in the future. you can look in the code to see how it works. its pretty simple. 😅

## Overview

This project is a Python script for downloading VODs from <https://live.rbg.tum.de>. It records all downloaded files to prevent duplicates. Contributions in the form of code improvements and new features are welcome. Please submit pull requests to help improve the project.

## Setup

To use this project, follow these steps:

### Create a Virtual Environment (Optional)

It is recommended to create a virtual environment for this project. This helps keep the dependencies separate from the rest of your system. To create a virtual environment, run the following commands in the project folder:

#### Unix

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python3 -m venv venv
./venv/Scripts/activate
```

### Install Dependencies

Update pip and install the dependencies listed in the `requirements.txt` file:

#### Unix/Windows

```css
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

### Chrome and ffmpeg

This project requires both Google Chrome and ffmpeg.

#### Chrome

Download Google Chrome from the official website. You will also need the Chrome Driver, which can be downloaded from <https://chromedriver.chromium.org/downloads>.

#### ffmpeg

On Unix systems, you can install ffmpeg using a package manager. On Windows, you can download it from <https://ffmpeg.org/>. Ensure that ffmpeg is accessible on your system path.

## Usage

```md
Usage: python <script name> [options]

Options:
  -u, --username   Provide the username
  -p, --password   Provide the password
  -c, --config     Provide the path to the configuration file in YAML format
  -P, --path       Provide the path to save the files (default: ./) ending with '/'
  -C, --courses    Provide a list of courses in the format: "CourseName:CourseId" separated by spaces
  --help           Show this help message and exit

Either a configuration file (-c, --config) or username (-u, --username) and password (-p, --password) must be provided.
If both a configuration file and username and password are provided, the provided username and password will overwrite the information in the configuration file.
```

### Example Configuration File

```md
password: pass
username: user
path: path
courses: {
  EIDI: /course/2022/W/eidi,
  ERA: /course/2022/W/WiSe22ERA
}
```

### Warning

The program has been designed to allow you to finish the current lecture download before closing the program by pressing `Ctrl + C`. However, this means that you will no longer be able to kill the program using `Ctrl + C`. If you need to stop the program, you will have to wait for the current lecture download to finish.

I understand that this might not be the best solution and I welcome any suggestions for a better implementation of this feature.

## Disclaimer-2

This code is not guaranteed to work in all cases and may contain bugs. It was only tested on my system and may not work on other systems.

If you would like to improve the code, feel free to create a pull request or reach out to the me with a link to your own repository if you have created a working version. I would be happy to update the README to link to your repository if it is deemed to be a functional improvement.
