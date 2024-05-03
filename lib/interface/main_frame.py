
"""
Includes main frame and other frames to
show the widgets
"""

from typing import Callable
from .widgets import Frame
from .widgets import Horizontal
from .widgets import Vertical
from .widgets import LabelEntry
from .widgets import Button
from .widgets import HorizontalTable
from .widgets import CheckBox
from .widgets import QFileDialog
from .widgets import QGraphicsDropShadowEffect
from .widgets import QColor
from .widgets import pyqtSignal
from .widgets import QObject
from .widgets import MessageBox
from lib.logic.search_algorithm import SearchProcess



class FMain(Frame):
    """
    Main frame that includes other frames
    and widgets.
    """
    def __init__(self) -> None:
        super().__init__(layout=Horizontal)
        self.setObjectName("fmain")
        self.init_widgets()

        self.provider = Provider(self.fresult.show_data)
    
    def init_widgets(self) -> None:
        """
        Initializes the frames and widgets.
        """
        self.fresult = None
        self.fcriteria = FCriteria(self.search, self.clear_result)
        self.fresult = FResult()
    
    def clear_result(self) -> None:
        """
        Bridge method to call the clear result
        in fresult.
        """
        self.fresult.clear_result()

    def search(self, criteria: dict) -> None:
        """
        Extract criteria, start searching for
        the targets and show result in result
        frame.
        --------------------------------------
        -> Params
            criteria: dict
        """
        targets = criteria.pop("targets")
        paths = criteria.pop("paths")
        self.search_process = SearchProcess(signal_callback=self.provider.get_search_result,
                                            **criteria)
        self.search_process.search(targets=targets,
                                   paths=paths)
    
    def stop_search(self) -> None:
        """
        Stop searching process.
        """

class FCriteria(Frame):
    """
    This frame is for showing the widgets
    to get the search targets and other
    configs for searching.
    """
    def __init__(self,
                 search_callback: Callable,
                 clear_result_callback: Callable) -> None:
        super().__init__(layout=Vertical)
        self.search_callback = search_callback
        self.clear_result_callback = clear_result_callback
        self.setup_frame()
        self.init_widgets(clear_result_callback)

    def setup_frame(self) -> None:
        """
        Setup frame configuration
        """
        self.setObjectName("fcriteria")
        self.setFixedWidth(250)
        effect = QGraphicsDropShadowEffect(self)
        effect.setColor(QColor("#006f68"))
        effect.setBlurRadius(15)
        effect.setOffset(0,0)
        self.setGraphicsEffect(effect)

    def init_widgets(self,
                     clear_result_callback: Callable) -> None:
        """
        Initializes the widgets and frames.
        """
        self.clear_result_button = Button(label="CLEAR RESULT",
                                          callback_function=clear_result_callback,
                                          width=250)
        self.select_path_button = Button(label="SELECT PATH",
                                         callback_function=self.open_get_location,
                                         width=250)
        self.search_path_entry = LabelEntry(label="SEARCH PATH",
                                            effect_color="#009187",
                                            effect_blur_radius=10,
                                            object_name="criteria",
                                            max_length=10000,
                                            
                                            default_value="E:/")
        
        self.targets_entry = LabelEntry(label="TARGETS",
                                        effect_color="#009187",
                                        object_name="criteria",
                                        effect_blur_radius=10,
                                        
                                        default_value="aera")
        
        self.search_in_files_checkbox = CheckBox(label="SEARCH IN FILES")

        self.max_file_size_entry = LabelEntry(label="MAX FILE SIZE",
                                               validator="int",
                                               default_value=10,
                                               tool_tip="Size in megabyte. Note that specifying large file size can slow the machine.",
                                               effect_color="#009187",
                                               object_name="criteria",
                                               effect_blur_radius=10)
        
        self.extensions_entry = LabelEntry(label="EXTENSIONS",
                                           place_holder="txt, json, csv",
                                           effect_color="#009187",
                                           object_name="criteria",
                                           effect_blur_radius=10)
        self.add_stretch()
        
        self.search_button = Button(label="SEARCH",
                                    callback_function=self.search_button_callback,
                                    width=250)
        

    def open_get_location(self) -> None:
        """
        Open dialog window to get the path
        location.
        """

        res = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.search_path_entry.set_value(res)

    def search_button_callback(self) -> None:
        """
        Collects entries data and pass them to
        the search_callback to start searching.
        """
        criteria = dict()
        targets = self.targets_entry.get_value()
        if not targets:
            MessageBox(self, "high", "Error",
                       "Please insert your targets for searching.")
            return
        criteria["targets"] = targets.split(",")
        paths = self.search_path_entry.get_value()
        criteria["paths"] = paths.split(",")

        in_file_search = self.search_in_files_checkbox.get_value()
        if in_file_search:
            criteria["in_file_search"] = in_file_search
            max_file_size = self.max_file_size_entry.get_value()
            if max_file_size > 100:
                MessageBox(self, "high", "Error",
                       "Max file size couldn't reach 100 Megabytes.")
                return
            criteria["max_file_size"] = max_file_size
            extensions = self.extensions_entry.get_value()
            if extensions:
                extensions = extensions.split(",")
                criteria["extensions"] = extensions
        self.clear_result_callback()
        self.search_callback(criteria)


class FResult(Frame):
    """
    This frame is for showing the result
    of the search.
    """

    def __init__(self) -> None:
        super().__init__(layout=Horizontal)
        self.setup_frame()
        self.init_widgets()

    def setup_frame(self) -> None:
        """
        Setup frame configuration
        """
        self.setObjectName("fresult")
        effect = QGraphicsDropShadowEffect(self)
        effect.setColor(QColor("#006f68"))
        effect.setBlurRadius(15)
        effect.setOffset(0,0)
        self.setGraphicsEffect(effect)

    def init_widgets(self) -> None:
        """
        Initializes the tables for each group
        of data.
        """
        self.dir_name = HorizontalTable(editable=True)
        self.dir_name.setup_view(h_headers=["Directory Name"],
                                 row_count=0,
                                 column_count=1)
        
        self.file_name = HorizontalTable(editable=True)
        self.file_name.setup_view(h_headers=["File Name"],
                                 row_count=0,
                                 column_count=1)
        
        self.in_file = HorizontalTable(editable=True)
        self.in_file.setup_view(h_headers=["In File"],
                                 row_count=0,
                                 column_count=1)
        
    def show_data(self, data: dict) -> None:
        """
        Show the data in the table. It adds a
        row to show the data in the table and 
        if it not initialized, initialize new
        table.
        """
        header,value = tuple(data.items())[0]
        if not self.widgets:
            self.init_widgets()
        table = getattr(self, header)
        rows_count = table.rowCount()
        table.setRowCount(rows_count+1)
        table.insert_row(value=[value], row=rows_count)


    def clear_result(self) -> None:
        """
        Clears the table data.
        """
        self.remove_all_widgets()


class Provider(QObject):
    """
    This class helps to gets the data from
    the search algorithm and pass it to the
    interface to show the search result.
    """
    
    search_result = pyqtSignal(dict)

    def __init__(self,
                 provider_callback: Callable) -> None:
        super().__init__()
        self.search_result.connect(provider_callback)
    
    def get_search_result(self, result: dict) -> None:
        """
        Bridge method to get the search result
        and pass it to the signal to send it to
        the interface.
        ---------------------------------------
        -> Params
            result: dict
        """
        self.search_result.emit(result)