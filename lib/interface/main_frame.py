
"""
Includes main frame and other frames to
show the widgets
"""

from .widgets import Frame
from .widgets import Horizontal
from .widgets import Vertical


class MainFrame(Frame):
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

class ResultFrame(Frame):
    pass

class CriteriaFrame(Frame):
    pass