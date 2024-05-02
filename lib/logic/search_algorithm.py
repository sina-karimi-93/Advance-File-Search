"""
This module is for searching through files, folders
for the result.
"""
import os
import time
from typing import Callable
from typing import Generator
from traceback import print_tb
from pprint import pprint
from time import strftime
from threading import Thread, Lock

class Logger:
    """
    act as advance print function for debugging the code
    ----------------------------------------------------
    @properties
            debug: activate and deactivate output
            level: level of printing details
    @methods

    """
    colors = {
        "default": '\033[0m',
        "red": '\033[91m',
        "green": '\033[92m',
        "blue": '\033[94m',
        "yellow": '\033[93m',
        "purple": '\033[95m',
        "cyan": '\033[96m',
    }
    debug = True
    level = 1
    time_stamp_format = "[%H:%M:%S]:"

    def __init__(self) -> None:
        self.levels = {1: self.level_one,
                       2: self.level_two,
                       3: self.level_three}
        self.pretty_printer = pprint
    
    def __call__(self,
                 *args,
                 pretty: bool = False,
                 level: str = 1,
                 color: str = "default",
                 **kwargs):
        """
        debug print the args and error traceback base on the detail level
        -------------------------------------------------------------------
        -> Params:
                prrety:
                        pprint the args
                level:
                        level_one:
                                normal print with time stamp
                        level_two:
                                details of the catched error
                                with line and cause of error
        """
        if not self.debug:
            return
        try:
            self.levels[level](pretty=pretty, color=color, *args, **kwargs)
        except KeyError as err:
            print(self.colors["default"], err)
            raise SystemError("Invalid Level name for debugging")

    def level_one(self,
                  *args,
                  pretty: bool,
                  color: str,
                  **kwargs) -> None:
        """
        print given argument with time stamp
        """
        time_stamp = strftime(self.time_stamp_format)
        if pretty:
            print(self.colors[color], time_stamp, end="\t")
            self.pretty_printer(*args)
            print(self.colors["default"], end="")
            return
        print(self.colors[color],
              time_stamp,
              *args,
              self.colors["default"])

    def level_two(self,
                  *args,
                  error: object,
                  pretty: bool,
                  color: str) -> None:
        """
        print traceback of the catched error from try,
        except block
        ----------------------------------------------
        -> Params:
                *args
                 error: object,
                 pretty: bool,
                 color: str
        """
        self.level_one(*args, error, pretty=pretty, color=color)
        print_tb(error.__traceback__)

    def level_three(self,
                    *args,
                    pretty: bool,
                    color: str,
                    **kwargs) -> None:
        """
        Print debugging messages
        -------------------------------------------------
        -> Params:
                *args
                 error
        """
        self.level_one(*args, pretty=pretty, color=color, **kwargs)

    def disable_logger(self) -> None:
        """
        disable the debug mode
        """
        self.debug = False

    def disable_log_level(self, level: int) -> None:
        """
        disable logger base on the give level
        --------------------------------------
        -> Params:
                level
        @raises:
             InvalidLogLevel
        """
        if not self.levels.get(level):
            raise ValueError(f"invalid level -> <{level}>")
        self.levels[level]
        self.levels[level] = self.void_function

    def void_function(self, *args, **kwargs) -> None:
        """
        replace function for log leves when
        we want to disable logger base on function levels
        """

    def compile_mode(self) -> None:
        """
        change default ouput to normal print fucntion.
        there is bug with python pprint module, which is
        cause program crash after compilation
        """
        self.pretty_printer = print


log = Logger()



class Search:
    
    def __init__(self,
                 in_file_search: bool,
                 file_size_limit: float = 30,
                 extensions: list = []) -> None:
        """
        ---------------------------------------
        -> Params
            file_size_limit: float
                Limit of file size that it should search
                inside the file. It's in Megabyte
        """
        self.in_file_search = in_file_search
        self.file_size_limit = file_size_limit
        self.extensions = extensions
    
    def get_paths(self,
                  paths: tuple = None) -> Generator:
        """
        Run os.walk method on the given paths and
        yield the output of the walk method.
        If didn't provided any paths, it uses all
        partitions names like C:/, E:/ ,...
        -----------------------------------------
        -> Params
            paths: list of str
        <- Return
            Generator
        """
        if not paths:
            paths = self.get_partitions()
        for path in paths:
            if self.is_dir(path):
                yield from os.walk(path)

    def is_dir(self, path: str) -> bool:
        """
        Checks the given input path is a valid
        path or not.
        --------------------------------------
        -> Params
            path: str
        <- Return
            bool
        """
        return os.path.isdir(path)

    def get_partitions(self) -> list:
        """
        Returns all defined partitions in
        the system.
        -----------------------------------
        <- Return
            list of strings
        """
        partitions = [f"{chr(i)}:\\" for i in range(65, 91)
                      if self.is_dir(f"{chr(i)}:/")]
        return partitions

    def search_directory(self,
                         dir_path: str,
                         file_names: list,
                         targets: list) -> Generator:
        """
        Search targets in the given directory address
        and the files in the directory.
        ---------------------------------------------
        -> Params
            dir_path: str
            file_names: list of str
            targets: list of str
        <- Return
            Generator
        """
        if ".git" in dir_path:
            return
        for target in targets:
            if self.compare(dir_path, target):
                yield {"dir_name": dir_path.replace("\\","/")}
            yield from self.check_files(dir_path, file_names, target)

    def compare(self, path: str, target: str) -> bool:
        """
        Checks the given target is in the
        path or not.
        ------------------------------------
        -> Params
            path: str
            target: str
        <- Return
            bool
        """
        if target.lower() in path.lower():
            return True
        return False

    def check_files(self,
                    dir_path: str,
                    file_names: list,
                    target: str) -> Generator:
        """
        Loop through file names, create a full
        valid path, and check the target is in
        the path and in the file or not.
        --------------------------------------
        -> Params
            dir_path: str,
            file_names: list
            target: str
        <- Return
            Generator
        """
        for file_name in file_names:
            if not self.is_valid_extension(file_name):
                continue
            full_path = f"{dir_path}/{file_name}"
            file_size = self.get_file_size(full_path)
            if file_size > self.file_size_limit:
                continue
            if self.compare(file_name, target):
                yield {"file_name": full_path.replace("\\","/")}
            if not self.in_file_search:
                continue
            try:
                with open(full_path, "r") as file:
                    if target.lower() in file.read().lower():
                        yield {"in_file": full_path}
            except UnicodeDecodeError:
                pass

    def is_valid_extension(self, file_name: str):
        """
        Checks the given file has the desired
        extension or not.
        -------------------------------------
        -> Params
            file_name: str
        <- Return
            bool
        """
        if not self.extensions:
            return True
        for extension in self.extensions:
            if file_name.endswith(extension):
                return True
        return False

    def get_file_size(self, path: str) -> float:
        """
        Calculates a file size in Megabyte and
        return the size.
        ---------------------------------------
        -> Params
            path: str
        <- Return
            float: Megabyte
        """
        return os.stat(path).st_size / (1024 * 1024)


class SearchWorkers:

    def __init__(self,
                 signal_callback: Callable,
                 threads_count: int = 16) -> None:
        self.is_searching = False
        self.threads_count = threads_count
        self.lock = Lock()
        self.signal_callback = signal_callback
    
    def search(self,
               targets: list,
               search_handler: Callable,
               paths: Generator) -> list:
        """
        Generate threads to do the search process
        on the provided paths.
        -----------------------------------------
        -> Params
            targets: list of str
            search_handler:
        """
        self.is_searching = True
        threads = [Thread(target=self.worker,
                  args=[search_handler, targets, paths])
                  for _ in range(self.threads_count)]
        for thread in threads:
            thread.daemon = True
            thread.start()
    
    def worker(self,
               search_handler: Callable,
               targets: list,
               paths: Generator) -> None:
        """
        Worker function that first gets a list of
        directories and file names, then search in
        the directories and files for the desired
        targets and add the results to a provided
        list.
        -----------------------------------------
        -> Params
            search_handler: Callable
            targets: list of strings
            paths: Generator
                includes dirname and file names
        """
        while self.is_searching:
            try:
                with self.lock:
                    dir_path, _, file_names = next(paths)
                result = search_handler(dir_path, file_names, targets)
                self.add_to_finds(result)
            except StopIteration:
                break
    
    def add_to_finds(self, result: Generator) -> None:
        """
        Adds the search result to the finds
        container.
        -----------------------------------
        -> Params
            result: tuple
                (find type, path)
        """
        try:
            result = dict(next(result))
            self.signal_callback(result)
        except StopIteration:
            pass

    def stop_searching(self) -> None:
        """
        Change the value of is_searching attribute
        to false to stop the threads working.
        """
        self.is_searching = False


def search(targets: list,
           paths: list,
           signal_callback: Callable,
           in_file_search:bool = False,
           max_file_size: float = 20,
           extensions: list = [],
           threads_count: int = 16) -> dict:
    """
    Search for the targets in the given paths
    from up to down of the directories and files
    and inside the files with specific criteria
    such as the maximum file size or its extension.
    -----------------------------------------------
    -> Params
        targets: list of string,
        paths: list of string
        finds_container: dict
        max_file_size: float
        extensions: list of string
        threads_count: int
            number of threads spawn
    <- Return
        dict
    """
    search = Search(in_file_search=in_file_search,
                    file_size_limit=max_file_size,
                    extensions=extensions)
    paths = search.get_paths(paths=paths)
    workers = SearchWorkers(threads_count=threads_count,
                            signal_callback=signal_callback)
    result = workers.search(targets=targets,
                            search_handler=search.search_directory,
                            paths=paths)
    return result