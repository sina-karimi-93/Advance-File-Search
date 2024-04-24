
"""
Includes main frame and other frames to
show the widgets
"""

from .widgets import Frame
from .widgets import Horizontal
from .widgets import Vertical
from .widgets import LabelEntry
from .widgets import Button
from .widgets import CheckBox
from .widgets import QFileDialog


class FMain(Frame):
    """
    Main frame that includes other frames
    and widgets.
    """
    def __init__(self) -> None:
        super().__init__(layout=Horizontal)

        self.init_widgets()
    
    def init_widgets(self) -> None:
        """
        Initializes the frames and widgets.
        """

        self.fcriteria = FCriteria()
        self.fresult = FResult()

class FCriteria(Frame):
    """
    This frame is for showing the widgets
    to get the search targets and other
    configs for searching.
    """
    def __init__(self) -> None:
        super().__init__(layout=Vertical)

        self.setup_frame()
        self.init_widgets()

    def setup_frame(self) -> None:
        """
        Setup frame configuration
        """
        self.setObjectName("fcriteria")
        self.setFixedWidth(250)

    def init_widgets(self) -> None:
        """
        Initializes the widgets and frames.
        """
        self.targets_entry = LabelEntry(label="TARGETS",
                                        effect_color="#009187",
                                        effect_blur_radius=20)
        
        self.search_path_entry = LabelEntry(label="SEARCH PATH",
                                            effect_color="#009187",
                                            effect_blur_radius=20,
                                            max_length=10000)
        
        self.select_path_button = Button(label="SELECT PATH",
                                         callback_function=self.open_get_location,
                                         width=250)
        
        self.add_stretch()

        self.search_in_files_checkbox = CheckBox(label="SEARCH IN FILES")

        self.maix_file_size_entry = LabelEntry(label="MAX FILE SIZE",
                                               validator="int",
                                               default_value=10,
                                               tool_tip="Size in megabyte. Note that specifying large file size can slow the machine.",
                                               effect_color="#009187",
                                               effect_blur_radius=20)
        
        self.extensions_entry = LabelEntry(label="EXTENSIONS",
                                           place_holder="txt, json, csv",
                                           effect_color="#009187",
                                           effect_blur_radius=20)

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
        self.init_widgets()

    def setup_frame(self) -> None:
        """
        Setup frame configuration
        """
        self.setObjectName("fresult")

    def init_widgets(self) -> None:
        """
        Initializes the widgets and frames.
        """
