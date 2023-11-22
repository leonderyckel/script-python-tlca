from argparse import ArgumentParser
from json import load
from os import listdir, mkdir, rename
from os.path import isfile, exists
from platform import system
from datetime import datetime


def readfile():
    """
    Read a file and allow final-user to manipulate the datas inside !
    :return: <dict>
    """
    with open('data.json', 'r') as file:
        return load(file)


def extension(filename: str):
    """
    Just return the extension of the file by split the <str> with the dot
    :param filename:
    :return: <str>
    """
    return filename.split('.')[-1]


def extensions(categ_name: str):
    """
    Just return all extensions known of the categories !
    :param categ_name:
    :return: <list>
    """
    return readfile()['categories'][f'{categ_name}']


def splitter():
    """
    Simply return the splitter needed by the current OS.
    Windows OS use \ as PATH splitter
    Linux and MacOS (recognized as Darwin) use / as PATH splitter
    :return: <str>
    """
    return "/" if system() in ['Darwin', 'Linux'] else "\\"


class Sort:
    def __init__(self, directory: str):
        self.files = None
        self.directory = directory
        self.log = {
            "files": [],
            "folders": []
        }

    def listfiles(self, verbose=False, path=True):
        """
        The listdir() method from os will list every file of the precised pathfile, and the isfile() method will return
        a boolean if the specified path is a file or a folder
        :param verbose: <bool> to set if you need to print each file found
        :param path: <bool> to set if we need to keep the PATH to the file as PATH value
        :return: <list> of all founded files inside the specified folder
        """
        files = []
        for item in listdir(path=self.directory):
            if isfile(f"{self.directory}{item}") and 'main.py' != item and "data.json" != item:
                if verbose:
                    if path:
                        print(f"{self.directory}{item}")
                    else:
                        print(item)
                if path:
                    files.append(f"{self.directory}{item}")
                else:
                    files.append(f"{item}")
        return files

    def sortfiles(self, configfile: dict):
        """
        This will work on two rounds:
        1. Create a <list> with all known categories
        2. Make 2 rounds:
            2.1. Checking if categories folder exists. Create a folder if not...
            2.2. Checking if the found file's extension are known. If yes, send it to the destination
            folder.
        Those operations are logged and printed !
        :param configfile: <dict> from data.json file
        :return: <bool>
        """
        categories = []
        for item in configfile['categories']:
            categories.append(item)
        for rnd in range(1, 3):
            if rnd == 1:
                print(f"Round {rnd}: Checking categories...")
                for item in categories:
                    if not exists(f"{self.directory}{item}"):
                        print(f"Creating the {item} folder inside {self.directory}...")
                        mkdir(f"{self.directory}{item}")
                        self.log['folders'].append(item)
            elif rnd == 2:
                print(f"\nRound {rnd}: Starting sort...")
                for file in self.listfiles(path=False):
                    for category in categories:
                        if extension(file) in extensions(
                                categ_name=f'{category}') and 'main.py' != file and "data.json" != file:
                            source = f"{self.directory}{file}"
                            destination = f'{self.directory}{category}{self.directory[-1]}{file}'
                            rename(
                                src=source,
                                dst=destination
                            )
                            self.log['files'].append([
                                destination.split(splitter())[-1],
                                category
                            ])
                            print(f"{source} ---> {destination} [Done]")
                return True

    def make_log(self):
        """
        This method will make a log:
        - The specified scanned directory
        - To recognize when has been made the action, the time is recorded when the scan has been made
        - The created folders are recorded
        - The moved files are also recorded
        :return: <bool>
        """
        var = f"Folder target: {self.directory}\n"
        date = datetime.now().strftime("%Y-%m-%d")
        time = datetime.now().strftime("%H:%M")
        var += f"Log created the {date} at {time}\n\n"
        var += "Category's folder created:\n"
        var += "--------------------------\n"
        for [index, line] in enumerate(self.log['folders'], start=1):
            var += f"{str(index).zfill(2)}) {line} has been created !"
        var += "\n\nSorted files:\n"
        var += "-------------\n"
        for [index, line] in enumerate(self.log['files'], start=1):
            var += f"{str(index).zfill(2)}) {line[0]} has been moved inside the {line[1]} folder..."

        with open('log.txt', 'a') as log:
            log.write(f"\n{var}\n")
        return True


config = readfile()
# ------- Arguments Declaration -----------------------------------------------------

arg = ArgumentParser(description=f"{config['title']} | Version: {config['version']}")
sm = arg.add_argument_group('Scan Methods')
mo = arg.add_argument_group('Main options')
mo.add_argument('--dir', '-d', help='Specify a PATH', required=True)
mo.add_argument('--relative-path', '-rp', help='relative PATH', action='store_true')
sm.add_argument('--list-files', '-lf', help="List files of the specified path", action='store_true')
sm.add_argument('--sort-files', '-sf', help="Sort files from categories (see data.json)", action='store_true')
arg = arg.parse_args()

# ------------------------------------------------------------------------------------
# ------- Just check what should be done ---------------------------------------------
if arg.dir[-1] not in ['\\' or '/']:
    arg.dir = f"{arg.dir}{splitter()}"

sorting = Sort(directory=arg.dir)
if arg.list_files:
    sorting.listfiles(verbose=True, path=arg.relative_path)
elif arg.sort_files:
    sorting.sortfiles(
        configfile=config
    )
    sorting.make_log()
