
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
from .widgets import pyqtSignal
from .widgets import QObject



class FMain(Frame):
    """
    Main frame that includes other frames
    and widgets.
    """
    def __init__(self) -> None:
        super().__init__(layout=Horizontal)
        self.setObjectName("fmain")
        self.init_widgets()
    
    def init_widgets(self) -> None:
        """
        Initializes the frames and widgets.
        """
        self.fresult = None
        self.fcriteria = FCriteria(self.clear_result)
        self.fresult = FResult()
    
    def clear_result(self) -> None:
        """
        Bridge method to call the clear result
        in fresult.
        """
        self.fresult.clear_result()

class FCriteria(Frame):
    """
    This frame is for showing the widgets
    to get the search targets and other
    configs for searching.
    """
    def __init__(self,
                 clear_result_callback: Callable) -> None:
        super().__init__(layout=Vertical)

        self.setup_frame()
        self.init_widgets(clear_result_callback)

    def setup_frame(self) -> None:
        """
        Setup frame configuration
        """
        self.setObjectName("fcriteria")
        self.setFixedWidth(250)

    def init_widgets(self,
                     clear_result_callback: Callable) -> None:
        """
        Initializes the widgets and frames.
        """
        self.clear_result_button = Button(label="Clear Result",
                                          callback_function=clear_result_callback,
                                          width=250)
        self.select_path_button = Button(label="SELECT PATH",
                                         callback_function=self.open_get_location,
                                         width=250)
        self.search_path_entry = LabelEntry(label="SEARCH PATH",
                                            effect_color="#009187",
                                            effect_blur_radius=10,
                                            object_name="criteria",
                                            max_length=10000)
        
        self.targets_entry = LabelEntry(label="TARGETS",
                                        effect_color="#009187",
                                        object_name="criteria",
                                        effect_blur_radius=10)
        
        self.add_stretch()

        self.search_in_files_checkbox = CheckBox(label="SEARCH IN FILES")

        self.maix_file_size_entry = LabelEntry(label="MAX FILE SIZE",
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
        
        self.search_button = Button(label="Search",
                                    callback_function=print,
                                    width=250)
        

    def open_get_location(self) -> None:
        """
        Open dialog window to get the path
        location.
        """

        res = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.search_path_entry.set_value(res)

class FResult(Frame):
    """
    This frame is for showing the result
    of the search.
    """

    def __init__(self) -> None:
        super().__init__(layout=Vertical)
        self.setup_frame()
        self.table_header = ["Directory","Names","In File"]

    def setup_frame(self) -> None:
        """
        Setup frame configuration
        """
        self.setObjectName("fresult")
    
    def show_data(self, data: dict) -> None:
        """
        Show the data in the table. It adds a
        row to show the data in the table and 
        if it not initialized, initialize new
        table.

        # self.table.insert_data(self.table_header,
        #                        [{"Directory": "E:\Test Directory\Another Test Directory\Test\Tests\Codes",
        #                          "Files": "main.py\ntest.py\ndata.json",
        #                          "In File": "readme.txt\nseeme.txt\nfindme.csv\nmoveme.json"}]*100)
        """
        try:
            rows_count = self.table.rowCount()
            self.table.setRowCount(rows_count+1)
        except AttributeError:
            self.table = HorizontalTable(editable=True)
            self.table.setup_view(h_headers=self.table_header,
                                  row_count=1,
                                  column_count=len(self.table_header))
        self.table.insert_row(data=data)

    
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