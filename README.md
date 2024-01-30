# TUM Live Lecture Downloader

## Overview

This Python script automates the process of downloading video lectures from TUM Live. It logs in using TUM credentials, navigates to specific course URLs, and downloads lectures in MP4 format. The script is equipped to handle lectures from a specified date onwards and saves them to a user-defined directory. The use of Selenium WebDriver and ffmpeg ensures a seamless download experience.

## Features

- **Automated TUM Login**: Logs in to TUM Live using provided credentials.
- **Selective Lecture Download**: Downloads lectures from a specific course URL, with an optional start date.
- **Title Extraction and Formatting**: Extracts and formats lecture titles for file naming.
- **Efficient Video Downloading**: Uses ffmpeg to download lectures in MP4 format.
- **Headless Browser Support**: Operates in a headless mode for background processing.

## Prerequisites

- **Python 3.x**: Ensure Python 3 is installed.
- **ffmpeg**: Required for video file processing.
- **Google Chrome**: Needed for the Chrome WebDriver.
- **Chrome WebDriver**: Must be compatible with the installed Chrome version.
- **Environment Variables**: USERNAME and PASSWORD for TUM Live login.

## Setup

1. **Clone the Repository**: Download the script from the GitHub repository.
2. **Create a Virtual Environment** (recommended):
   1. Unix: `python3 -m venv venv && source venv/bin/activate`
   2. Windows: `python3 -m venv venv && .\venv\Scripts\activate`
3. Install Dependencies: `pip install -r requirements.txt`
4. **Set Up Environment Variables**: Define `USERNAME` and `PASSWORD` in a .env file or export them directly.
5. **Download Chrome WebDriver**: Ensure it matches the Chrome version installed on your system.

## Usage

1. **Run the Script:**

```bash
python <script_name>.py "<course_url>" "<download_path>" [--start-date YYYY-MM-DD]
```

- `course_url`: URL of the TUM course.
- `download_path`: Path to save downloaded lectures.
- `--start-date`: Optional, to download lectures from a specific date up to now.

2. **Example Usage:**

```bash
python tum_live_downloader.py "https://live.rbg.tum.de/?year=2023&term=W&slug=GBS&view=3" "downloads/GBS" --start-date 2024-01-01
```

## Note

- **Configuration**: The script uses environment variables (`USERNAME` and `PASSWORD`) for authentication. Ensure they are set before running the script.
- **Headless Mode**: The script operates in headless mode by default. This can be changed in the code if necessary.
- **Disclaimer**: This script is provided "as is", and the author is not responsible for any misuse or issues arising from its use.

## Contributing

Contributions, bug reports, and feature requests are welcome. Please submit pull requests or open issues on the GitHub repository to collaborate and improve the script.
