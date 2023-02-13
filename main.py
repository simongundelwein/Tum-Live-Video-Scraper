from functions import start
import sys
import yaml
import os

USAGE_MESSAGE = """
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
"""

def checkUsage(cond, message=None):
    if not cond:
        if message != None:
            print(message)
        else:
            print(USAGE_MESSAGE)
        sys.exit()

def extractArgument(args: list[str]) -> list[str]:
    checkUsage(len(args) > 1 and args[0].startswith('-'))
    result = []
    result.append(args.pop(0))
    while len(args) != 0 and not args[0].startswith('-'):
        result.append(args.pop(0))
    return result



arguments = sys.argv
arguments.pop(0)

checkUsage(len(arguments) > 0)

username = ''
password = ''
path = ''
courseList = {}
config = {
    "path": "./",
    "courses": {}
}


while len(arguments) != 0:
    current = extractArgument(arguments)
    identifier = current.pop(0)
    match identifier:
        case '-u' | '--username':
            checkUsage(len(current) == 1)
            username = current[0]
        case '-p' | '--password':
            checkUsage(len(current) == 1)
            password = current[0]
        case '-C' | '--courses':
            for course in current:
                currentCourse = course.split(':')
                checkUsage(len(currentCourse) == 2, message="Usage: CourseName:CourseId")
                courseList[currentCourse[0]] = currentCourse[1]
        case '-P' | '--path':
            checkUsage(len(current) == 1 and current[0].endswith('/'))
            path = current[0]
        case '-c' | '--config':
            checkUsage(len(current) == 1)
            checkUsage(os.path.isfile(current[0]), message="File does not Exists!")
            with open(current[0], "r") as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
        case '--help':
            print(USAGE_MESSAGE)
            sys.exit()
        case other:
            checkUsage(False, message='{} is not a valid argument!'.format(identifier))

if password != '':
    config["password"] = password
if username != '':
    config["username"] = username
if path != '':
    config["path"] = path
if courseList != {}:
    config["path"] = courseList

checkUsage(all(k in config.keys() for k in ("password", "username", "path", "courses")))

start(courses=config["courses"], url='https://live.rbg.tum.de', username=config["username"], 
        password=config["password"], tmpPath="tmp/", path=config["path"])