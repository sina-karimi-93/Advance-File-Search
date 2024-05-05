"""
This module is for searching through files, folders
for the result.
"""
import os
from time import sleep
from typing import Callable
from typing import Generator
from threading import Thread
from threading import Lock

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
            full_path = f"{dir_path}/{file_name}"
            file_size = self.get_file_size(full_path)
            if self.compare(file_name, target):
                yield {"file_name": full_path.replace("\\","/")}
            
            # Check in files
            if not self.in_file_search:
                continue
            if file_size > self.file_size_limit:
                continue
            if not self.is_valid_extension(file_name):
                continue
            try:
                with open(full_path, "r") as file:
                    if target.lower() in file.read().lower():
                        yield {"in_file": full_path}   
            except UnicodeDecodeError:
                pass
            sleep(0.01)

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
                 finish_search_callback: Callable,
                 threads_count: int = 16) -> None:
        self.is_searching = False
        self.is_finished = False
        self.threads_count = threads_count
        self.lock = Lock()
        self.signal_callback = signal_callback
        self.finish_search_callback = finish_search_callback
    
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
        self.is_finished = True
        self.threads = [Thread(target=self.worker,
                  args=[search_handler, targets, paths])
                  for _ in range(self.threads_count)]
        for thread in self.threads:
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
        self.stop_working()
    
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
    
    def stop_working(self) -> None:
        """
        To prevent all threads call the finish
        callback this method checks to call it
        just once.
        """
        with self.lock:
            if self.is_finished:
                self.finish_search_callback()
                self.is_finished = False

    def stop_searching(self) -> None:
        """
        Change the value of is_searching attribute
        to false to stop the threads working.
        """
        self.is_searching = False
            

class SearchProcess:
    """
    Search for the targets in the given paths
    from up to down of the directories and files
    and inside the files with specific criteria
    such as the maximum file size or its extension.
    """
    def __init__(self,
                 signal_callback: Callable,
                 finish_search_callback: Callable,
                 in_file_search:bool = False,
                 max_file_size: float = 20,
                 extensions: list = [],
                 threads_count: int = 16) -> None:
        """
        -----------------------------------------------
        -> Params
            finds_container: dict
            max_file_size: float
            extensions: list of string
            threads_count: int
            number of threads spawn
        """
        self.search_handler = Search(in_file_search=in_file_search,
                                     file_size_limit=max_file_size,
                                     extensions=extensions)
        self.workers = SearchWorkers(threads_count=threads_count,
                                     signal_callback=signal_callback,
                                     finish_search_callback=finish_search_callback)
    
    def search(self,
               targets: list,
               paths: list) -> None:
        """
        ----------------------------------------
        -> Params
            targets: list of string,
            paths: list of string
        """
        paths = self.search_handler.get_paths(paths=paths)
        self.workers.search(targets=targets,
                            search_handler=self.search_handler.search_directory,
                            paths=paths)
    
    def stop_searching(self) -> None:
        """
        Stop searching process.
        """
        self.workers.stop_searching()