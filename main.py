import argparse
from functions import start
import yaml

parser = argparse.ArgumentParser(description='Download lectures from TUM Live')
parser.add_argument('-u', '--username', type=str, help='Provide the username')
parser.add_argument('-p', '--password', type=str, help='Provide the password')
parser.add_argument('-c', '--config', type=str, help='Provide the path to the configuration file in YAML format')
parser.add_argument('-P', '--path', type=str, help='Provide the path to save the files (default: ./) ending with /')
parser.add_argument('-C', '--courses', type=str, nargs='+', help='Provide a list of courses in the format: "CourseName:CourseId" separated by spaces')

args = parser.parse_args()

username = args.username
password = args.password
path = args.path
courses = args.courses
config_file = args.config

if config_file:
    with open(config_file, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise argparse.ArgumentTypeError("Configuration file is not in YAML format") from exc
    username = config["username"]
    print(username)
    password = config["password"]
    print(password)
    path = config["path"]
    courses = config["courses"]

start(courses=config["courses"], url='https://live.rbg.tum.de', username=config["username"], 
        password=config["password"], tmpPath="tmp/", path=config["path"])