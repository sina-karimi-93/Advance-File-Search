"""
Module contains all the widgets class to
create UI with Qt library
"""
from typing import Union
from typing import NewType
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QVBoxLayout as Vertical
from PyQt5.QtWidgets import QHBoxLayout as Horizontal
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5.QtGui import QCursor
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QIntValidator
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QRegExp
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject
from lib.errors import DataValidationFailed, RowNotExists, TableCellNotFoundError
from .utils import log
from .utils import void_function
from lib.constants import *

CSS = NewType("CSS", str)

def change_widget_status(widget: object, status: str = "normal") -> None:
    """
    Change the color of the widget to show the
    status of the widget.
    """
    states = {
        "normal": "",
        "warning": "#ffae00",
        "error": "#ff0048",
    }
    widget.setStyleSheet(f"border-color:{states[status]};")

class MessageBox(QMessageBox):
    """
    Custom subclass of QMessageBox
    """

    def __init__(self,
                 parent: object,
                 critical_level: str,
                 title: str,
                 message: str,
                 **kwargs) -> None:
        super().__init__(parent=parent, **kwargs)
        message = str(message)
        if critical_level == 'low':
            self.information(self, title, message)
        elif critical_level == 'medium':
            self.warning(self, title, message)
        elif critical_level == 'high':
            self.critical(self, title, message)
        else:
            self.setWindowTitle(title)
            self.setText(message)
            self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    def get_answer(self) -> bool:
        """
        Return the result of the message box
        in boolean.
        """
        result = self.exec()
        if result == QMessageBox.Ok:
            return True
        return False

class IntValidator(QIntValidator):

    def validate(self, a0: str, a1: int):
        """
        Overrite this method to add better restriction
        when user type a value.
        It checks if the value user inserted is not in
        the boundaries, then prevent typing more than of
        the boundaries.
        """

        res = super().validate(a0, a1)
        try:
            if not self.bottom() <= int(a0) <= self.top():
                res = (0, a0, a1)
        except ValueError:
            return res
        return res

class DoubleValidator(QDoubleValidator):

    def validate(self, a0: str, a1: int):
        """
        Overrite this method to add better restriction
        when user type a value.
        It checks if the value user inserted is not in
        the boundaries, then prevent typing more than of
        the boundaries.
        """
        res = super().validate(a0, a1)
        try:
            if not self.bottom() <= float(a0) <= self.top():
                res = (0, a0, a1)
        except ValueError:
            return res
        return res

class RegxpValidator(QRegExpValidator):
    """
    Sub class of QRegExpValidator, it will validate
    the widget value base on given regular expression
    pattern.
    ------------------------------------------------
    -> Params:
             pattern
    """

    def __init__(self, pattern: str) -> None:
        super().__init__(QRegExp(pattern))

class WidgetController:
    """
    its helper class(add extra functionalty to subclass).
    helps to keep track of the created widgets
    to make it get their data or removing them
    @methods
       __setattr__ = overridden
       get_widgets()
       remove_widgets()
       add_stretch()
    @usage:
         class Test(WidgetController):
             pass
    """

    def __init__(self) -> None:
        self.widgets = list()

    def add_grid_widget(self, widget: object) -> None:
        """
        Add grid widget when the main layout
        is QGridLayout, this method will override
        the add_widget
        -> Params:
                widget
        """
        grid_positions = widget.grid_positions
        self.main_layout.addWidget(widget, *grid_positions)

    def get_widget_object(self, index: int) -> object:
        """
        Return the widget object by index
        @args
            index:int

        @return
            object
        """
        return self.widgets[index][1]

    def get_widget_name(self, index: int) -> str:
        """
        Return the widget name by index
        @args
            index:int

        @return
            str
        """
        return self.widgets[index][0]

    def get_widget(self, index: int) -> tuple:
        """
        Return the widget name and object by index
        @args
            index:int

        @return
            tuple
        """

        return self.widgets[index]

    def add_widget(self, widget: object) -> None:
        """
        add non grid widget to the main layout
        this method will be replace with
        -> Params:
             widget
        """
        self.main_layout.addWidget(widget)

    def __setattr__(self, name: str, widget: object) -> None:
        """
        overriden __setattr__ to intercept
        object when setattr get called.
        we adding all widgets to widgets list
        by intercepting the coming objects
        -> Params:
                name: attribute name
                obj: attribute object
        """
        super().__setattr__(name, widget)
        try:
            # add to prevent qt log for none object
            # TODO: need to be tested
            if widget == None:
                return
            self.add_widget(widget)
            self.widgets.append((name, widget))
        except TypeError as error:
            log(error=error,
                level=3, 
                color="red")

        except AttributeError as error:
            log(error=error,
                level=3, 
                color="red")

    def get_widgets(self) -> list:
        """
        Return all widgets.
        return ->
            [(name,object),...]
        """
        return self.widgets

    def remove_widget(self, index: int = -1) -> None:
        """
        Remove the widget from layout and class.
        The default index is -1 to remove last widget added.
        params ->
            index: int
        """
        name, widget_obj = self.widgets[index]
        widget_obj.deleteLater()
        delattr(self, name)
        self.widgets.pop(index)
    
    def remove_widget_by_name(self, widget_name: str) -> None:
        """
        Based on the widget attribute name, remove
        it from the widget tree.
        """
        index = 0
        for name, widget_obj in self.widgets:
            if name == widget_name:
                widget_obj.deleteLater()
                delattr(self, name)
                break
            index += 1
        self.widgets.pop(index)

    def remove_all_widgets(self) -> None:
        """
        Remove all the widgests inside the widget list
        """
        for name, widget in self.widgets:
            widget.deleteLater()
            delattr(self, name)
        self.widgets.clear()

    def get_values(self) -> dict:
        """
        Return values of the all the widgets
        as dictionary
        """
        values = {
            name: widget.get_value()
            for name, widget in self.widgets if hasattr(widget, "get_value")
        }
        return values

    def add_stretch(self, strech_factor: int = 1) -> None:
        """
        Adds a stretchable space (a QSpacerItem)
        with zero minimum size and stretch factor
        stretch to the end of this box layout.
        -> params:
                 strech_factor
        """
        self.main_layout.addStretch(strech_factor)

    def validate_widgets(self) -> None:
        """
        iter over the widgets list and call widgets validate
        method.
        """
        for widget_name, widget in self.widgets:
            try:
                result = widget.validate()
                if result != True:
                    raise DataValidationFailed(
                        f"{widget_name.capitalize()} {result}")
            except AttributeError as error:
                log(error=error,
                    level=2, 
                    color="red")

    def get_layout(self) -> object:
        """
        return subclass layout manager class
        (QHBoxLayout or QVBoxLayout)
        """
        return self.main_layout

    def clear_cache(self) -> None:
        """
        Clear cached widgets inside the layout
        """
        self.main_layout.invalidate()

    def clear_values(self) -> None:
        """
        Clear all the widgets values
        """
        for _, widget in self.widgets:
            try:
                func = getattr(widget, "clear_value")
                func()
            except AttributeError as error:
                log(error=error,
                    level=2, 
                    color="red")

class Frame(QFrame, WidgetController):
    """
    Custom Frame class (Qwidget)
    """

    def __init__(self, layout: object, grid_positions: tuple = None, **kwargs):
        super().__init__(**kwargs)
        self.grid_positions = grid_positions
        self.main_layout = layout()

        self.adjustSize()
        self.setLayout(self.main_layout)

class LabelFrame(QGroupBox, WidgetController):
    """
    Custom widget contains a horizontal and vertical layout.
    for fewer code in upper level, each class that
    inherit from this class and add a widget, doesnt
    need to set the widget to layout.setattr of this
    class do this automatically when a attr set to class.
    """

    def __init__(self,
                 layout: object,
                 title: str = None,
                 object_name: str = None,
                 **kwargs):
        """
        params ->
            layout:object
            position:tuple -> using if this widget placed in a grid

        attr ->
            widgets: list
            grid_position: tuple
            main_layout: obj

        """
        super().__init__(**kwargs)
        self.setTitle(title)
        self.main_layout = layout()
        self.setLayout(self.main_layout)
        self.setObjectName(object_name)

    def set_title(self, value: str) -> None:
        """
        Set new title for the frame

        -> Params
            value:str
        """
        self.setTitle(value)

class Label(QLabel):
    """
    Custom sub class of QLabel
    """

    def __init__(self,
                 label=None,
                 object_name: str = None,
                 grid_positions: tuple = None,
                 *args,
                 **kwargs):
        super().__init__(str(label), *args, **kwargs)
        # self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setObjectName(object_name)
        self.setAlignment(Qt.AlignCenter)
        self.grid_positions = grid_positions

    def change_text(self, text: str) -> None:
        """
        Change text value of the label
        -> Params:
                text
        """
        try:
            self.setText(text)
        except TypeError:
            self.setText(str(text))

    def get_value(self) -> str:
        """
        Return the label text.

        @return
            str
        """
        return self.text()

    def set_image(self, file_name: str, scale: tuple = (300, 70)) -> None:
        """
        load and display given image file_name inside
        the label
        -> Params:
                filename: image must be inside imgaes folder
        """
        # path = check_image_exists(file_name)
        image = QPixmap(file_name)
        image = image.scaled(*scale,
                             transformMode=Qt.SmoothTransformation)
        self.setPixmap(image)

class Button(QPushButton):
    """
    Custom sub class of PushButton
    """

    def __init__(
        self,
        label: str,
        callback_function: object,
        icon: str = None,
        icon_size: tuple = (20, 20),
        tool_tip: str = None,
        min_width: int = 50,
        width=50,
        object_name: str = None,
        grid_positions: tuple = None,
        **kwargs,
    ):
        super().__init__(label, **kwargs)
        self.setObjectName(object_name)
        self.clicked.connect(callback_function)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        # self.setMinimumWidth(min_width)
        self.setFixedWidth(width)
        self.setToolTip(tool_tip)
        if icon:
            self.setIcon(QIcon(icon))
            self.setIconSize(QSize(*icon_size))
        self.grid_positions = grid_positions

class DigitValidator:
    """
    Mixing class helper to validato int and float entries
    """

    def get_value(self) -> int:
        """
        Return value of the entry
        """
        try:
            value = self._type(self.text())
            return value
        except (ValueError, TypeError):
            # self.set_value(0)
            return 0

    def validate(self) -> bool:
        """
        Validate this widget
        """
        value = self.text()

        if not value:
            self.on_invalid()
            return "should not be empty."

        if self.not_zero:
            if value == '0' or value == "0.0":
                self.on_invalid()
                return "should not be 0 ."

        self.on_valid()
        return True

class Entry(QLineEdit):
    """
    Customized QLineEdit Subclass
    -> Params:
          tool_tip
          validator: QtValidator
          widths

    @note:
         default event handler is on textChaged

    """

    def __init__(
        self,
        tool_tip: str = None,
        callback_func: object = void_function,
        default_value: str = "",
        place_holder: str = None,
        max_length: int = 50,
        width: int = 0,
        min_width: int = 0,
        max_width: int = 0,
        editable: bool = True,
        is_enable: bool = True,
        is_upper: bool = False,
        object_name: str = None,
        validator: str = None,
        value_limit: tuple = None,
        focus_out_callback: object = void_function,
        key_press_callback: callable = void_function,
        not_zero: bool = None,
        is_password: bool = False,
        grid_positions: tuple = None,
        use_effect: bool = True,
        effect_color: str = "#f89fa2",
        effect_blur_radius: int = 10,
                **kwargs,
            ):
        super().__init__(**kwargs)
        self.setObjectName(object_name)
        self.setToolTip(tool_tip)
        self.setAlignment(Qt.AlignCenter)
        self.setEnabled(is_enable)
        self.setMaxLength(max_length)
        self.setEnabled(editable)
        self.setPlaceholderText(place_holder)
        self.set_value(default_value)
        self.textChanged.connect(callback_func)
        if min_width:
            self.setMinimumWidth(min_width)
        if max_width:
            self.setMaximumWidth(max_width)
        if width:
            self.setFixedWidth(width)
        if is_upper:
            self.textChanged.connect(self.set_upper)
        if is_password:
            self.setEchoMode(QLineEdit.Password)
        self.focus_out_callback = focus_out_callback
        self.key_press_callback = key_press_callback
        self.grid_positions = grid_positions
        if use_effect:
            effect = QGraphicsDropShadowEffect(self)
            effect.setColor(QColor(effect_color))
            effect.setOffset(0, 0)
            effect.setBlurRadius(effect_blur_radius)
            self.setGraphicsEffect(effect)

    def set_callbacks(self, *callbacks) -> None:
        """
        Set new callback to the entry.

        @args
            callback:object
        """
        for callback in callbacks:
            self.textChanged.connect(callback)

    def set_upper(self) -> None:
        """
        Force the user input to be uppercase.
        """
        self.setText(self.text().upper())

    def on_invalid(self) -> None:
        """
        When something went wrong in this widget, for example
        user leave the widget empty or add invalid value, then
        change the widget status.
        """
        change_widget_status(self, status="error")

    def on_valid(self) -> None:
        """
        After an error fixed in this widget, this method
        change status of the widget to normal.
        """
        change_widget_status(self, status="normal")

    def get_value(self) -> str:
        """
        Get entry text.
        """
        value = self.text()
        return value

    def set_value(self, text: str) -> None:
        """
        Add text to entry.
        """
        try:
            self.setText(text)
        except TypeError:
            self.setText(str(text))

    def clear_value(self) -> None:
        """
        Clear the textbox value
        """
        self.clear()

    def focusOutEvent(self, event) -> None:
        self.focus_out_callback()
        return super().focusOutEvent(event)

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Return:
            self.key_press_callback(self.text())
        return super().keyPressEvent(event)

    def mousePressEvent(self, event) -> None:
        """
        Make widget valid when user click on it
        """
        self.on_valid()
        return super().mousePressEvent(event)

class DigitEntry(DigitValidator, Entry):
    """
    Mixing class of DigitValidator and Entry widget
    """

    def __init__(self, value_type: object, **kwargs) -> None:
        super().__init__(**kwargs)
        self.textChanged.connect(self.validate)
        self._type = value_type
        self.not_zero = kwargs["not_zero"]

class IntEntry(DigitEntry):
    """
    IntEntry will accept and return int value
    """

    def __init__(self, value_limit: tuple, **kwargs) -> None:
        super().__init__(value_type=int, **kwargs)
        self.setValidator(IntValidator(value_limit[0], value_limit[1]))

class LabelEntry(Frame):
    """
    Labeled Entry .is a frame contains entry
    with label
    -> Params:
          label
          tooltip
          layout: QBOXLAYOUT
          width
          place_hodler
          callback_func: default is void_function function
          **kwargs
    """

    widget_type = {
        "int": IntEntry,
    }

    def __init__(
        self,
        label: str,
        tool_tip: str = None,
        layout: object = Vertical,
        default_value: str = "",
        max_length: int = 20,
        validator: str = None,
        callback_func: object = void_function,
        width: int = None,
        min_width: int = 0,
        max_width: int = 0,
        frame_width:int= 0,
        place_holder: str = None,
        editable: bool = True,
        object_name: str = None,
        label_object_name: str = None,
        is_upper: bool = False,
        grid_positions: tuple = None,
        value_limit: tuple = (0, 2147483647),
        focus_out_callback: object = void_function,
        key_press_callback: callable = void_function,
        not_zero: bool = None,
        is_password: bool = False,
        align_center: bool = False,
        use_effect: bool = True,
        effect_color: str = "#f89fa2",
        effect_blur_radius: int = 15,
        **kwargs,
    ):
        super().__init__(layout, **kwargs)
        self.label = Label(label, object_name=label_object_name)
        self.label.setAlignment(Qt.AlignCenter)
        if align_center:
            self.main_layout.setAlignment(Qt.AlignCenter)
        self.entry = self.widget_type.get(validator, Entry)(
            width=width,
            min_width=min_width,
            max_width=max_width,
            tool_tip=tool_tip,
            validator=validator,
            default_value=default_value,
            callback_func=callback_func,
            place_holder=place_holder,
            editable=editable,
            max_length=max_length,
            object_name=object_name,
            value_limit=value_limit,
            focus_out_callback=focus_out_callback,
            key_press_callback=key_press_callback,
            is_upper=is_upper,
            not_zero=not_zero,
            is_password=is_password,
            use_effect=use_effect,
            effect_color=effect_color,
            effect_blur_radius=effect_blur_radius)
        self.grid_positions = grid_positions
        if frame_width:
            self.setFixedWidth(frame_width)
    def on_invalid(self) -> None:
        """
        When something went wrong in this widget, for example
        user leave the widget empty or add invalid value, then
        change the widget status.
        """
        self.entry.on_invalid()

    def on_valid(self) -> None:
        """
        After an error fixed in this widget, this method
        change status of the widget to normal.
        """
        self.entry.on_valid()

    def get_value(self) -> object:
        """
        return value of the entry
        """
        return self.entry.get_value()

    def set_value(self, value: str) -> None:
        """
        Set value of the entry
        """
        self.entry.set_value(value)

    def clear_value(self) -> None:
        """
        Clear value of the entry
        """
        self.entry.clear()

    def validate(self) -> bool:
        """
        Validate the entry
        """
        return self.entry.validate()

    def set_validator(self, validator: str) -> None:
        """
        Change validator of the entry.
        ------------------------------------------------
        -> Params
            validator: str
        """
        self.entry.set_validator(validator)

    def set_callbacks(self, *callbacks) -> None:
        """
        Connect a callback to the entry
        ------------------------------------------------
        -> Params
            callbacks: function, method
        """
        self.entry.set_callbacks(*callbacks)

    def disconnect_callbacks(self) -> None:
        """
        Disconnect all entry's callback.
        """
        self.entry.disconnect()

class Menu(QMenu):
    """
    This class is subclass of QMenu
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def add_action(self, icon_path: str, title: str,
                   callback_func: object) -> None:
        """
        Adds new action to the menu.

        @args
            icon_path:str
            title:str
            handler:object(method)
        """
        action = QAction(QIcon(icon_path), title, self)
        action.triggered.connect(callback_func)
        self.addAction(action)

class Table(QTableWidget):
    """
    Custom subclass from QTablewidget
    -> Params:
           headers: table header
           current_row
    """

    # horiznotalheadr
    H_HEADER = None
    # veticalHeader
    V_HEADER = None

    def __init__(self,
                 min_width: int = 600,
                 min_height: int = 200,
                 editable:bool=False,
                 table_number: int = 0,
                 selection_mode: object = QTableWidget.SingleSelection,
                 double_click_callback: callable = None,
                 **kwargs) -> None:

        super().__init__(**kwargs)
        edit_trigger=QTableWidget.NoEditTriggers
        if editable:
            edit_trigger=QTableWidget.DoubleClicked
        self.configure(edit_trigger=edit_trigger,
                       selection_mode=selection_mode)
        self.setMinimumSize(min_width, min_height)
        self.sizeIncrement()
        self.menu = Menu()
        self.table_number = table_number
        if double_click_callback:
            self.doubleClicked.connect(double_click_callback)

    def contextMenuEvent(self, event) -> None:
        """
        Overriting this method for showing a context menu
        by right click of the mouse on each row.
        """
        if self.currentRow() > -1:
            # A row is selected
            self.menu.popup(QCursor.pos())

    def configure(self,
                  edit_trigger: object = QTableWidget.NoEditTriggers,
                  selection_mode: object = QTableWidget.SingleSelection,
                  selection_behavior: object = QTableWidget.SelectRows,
                  ) -> None:
        """
        Change config of the widget, config object can be from
        QtableWidget or QAbstractItemView
        -------------------------------------------------------
        -> Params:
                 current_row
                 edit_trigger: Qt Triger object default is QTableWidget.DoubleClicked
                                (to make it ready only set edit_trigger to QTableWidget.NoEditTriggers)
                 selection_mode: Qt selection mode object default is SingleSelection
                 selection_behavior: Qt selection behavior default is SelectRows

        """
        self.setEditTriggers(edit_trigger)
        self.setSelectionMode(selection_mode)
        self.setSelectionBehavior(selection_behavior)
        self.setCurrentCell(0, 0)

    def get_headers(self) -> tuple:
        """
        Return the headers items
        """
        if self.H_HEADER:
            return self.H_HEADER
        return self.V_HEADER

    def is_vertical(self) -> bool:
        """
        Return the table type
        """
        if not self.H_HEADER:
            return True
        return False

    def _convert_item(self, item: str) -> type:
        """
        This method calls from _item_getter() to convert
        the data to its corresponding type.

        @return
            str, float, int
        """
        try:
            return int(item)
        except ValueError:
            try:
                return float(item)
            except ValueError:
                return item

    def _item_getter(self,
                     row: int,
                     column: int,
                     validate: bool = False) -> type:
        """
        This method calls from get_row() method to return an item from
        a row. If validator set to True, it will convert the item to its
        specific type.

        @args
            row: int
            column: int
            validator: bool
        @return
            type(str, float, int)
        """
        try:
            item = self.item(row, column).text()
        except AttributeError:
            raise TableCellNotFoundError(
                f"Couldn't find the item in row {row} and column {column}.")
        if validate:
            item = self._convert_item(item)
        return item

    def convert_before_insert(self, data: list) -> list:
        """
        Convert data from list of non-dict items to
        a list of a dict for inserting into the table.
        ----------------------------------------------
        -> Params
            data: list -> [3, "something", 55,5, "another_something"]
        <- Return
            list of a dict -> [{1:3, 2:"something", 3:55.5, 4:"another_something"}]
        """
        return [{index: i for index, i in enumerate(data)}]

class HorizontalTable(Table):

    def __init__(self,
                 min_width: int = 300,
                 min_height: int = 200,
                 table_number: int = 0,
                 object_name: str = None,
                 selection_mode: object = QTableWidget.SingleSelection,
                 editable:bool=False,
                 edit_callback: callable = None,
                 double_click_callback: callable = None,
                 grid_positions: tuple = None) -> None:
        super().__init__(min_width=min_width,
                         min_height=min_height,
                         selection_mode=selection_mode,
                         editable=editable,
                         double_click_callback=double_click_callback)
        self.setObjectName(object_name)
        self.table_number = table_number
        self.grid_positions = grid_positions
        if editable:
            self.set_callback(edit_callback)

    def set_callback(self, callback: callable) -> None:
        """
        Set callback for cellChange
        """
        if callback:
            self.cellChanged.connect(
                lambda x: callback(x, self.table_number))

    def setup_view(self,
                   h_headers: list = None,
                   row_count: int = 0,
                   column_count: int = 0,
                   has_width: list = None) -> None:
        """
        Setup table info such as number of rows
        and columns and cells view type.
        """
        self.setColumnCount(column_count)
        self.setRowCount(row_count)
        self.setHorizontalHeaderLabels(h_headers)
        self.H_HEADER = tuple(h_headers)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        if not has_width:
            self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().hide()

    def insert_row(self, 
                   value: list,
                   row: int = 0) -> None:
        """
        insert the given data row by row, it will clear
        previous inserted data on new insert calls
        -> Params:
                data
                row: row number default is 0
        """
        c_count = self.columnCount()
        for value, column in zip(value, range(c_count)):
            item = QTableWidgetItem(str(value))
            self.setItem(row, column, item)

    def insert_data(self,
                    headers: list,
                    data: list,
                    width: Union[list, int] = None) -> None:
        """
        Insert data into the table.
        ----------------------------------------------
        -> Params
            data: list of dicts
            width: list or int
        """
        self.clear_value()
        self.horizontalHeader().show()
        self.setup_view(h_headers=headers,
                        row_count=len(data),
                        column_count=len(headers),
                        has_width=width)
        for row_index, document in enumerate(data):
            self.setRowHeight(row_index, 75)

            value = list(document.values())
            self.insert_row(data=value,
                            width=width,
                            row=row_index)

    def insert_new_row(self, data: tuple) -> None:
        """
        Insert new row to the end of the rows.

        @args
            data:list
        """
        self.setRowCount(self.rowCount() + 1)
        last_row = self.rowCount() - 1
        for col in range(self.columnCount()):
            self.setItem(last_row, col, QTableWidgetItem(data[col]))

    def get_row(self, row: int, validator: bool = False) -> tuple:
        """
        return all the column of the given row as tuple
        ----------------------------------------------
        -> Params:
                row: row number
        """

        # total number of columns for iteration
        try:
            total_column = self.columnCount()
            row = [
                self._item_getter(row, column, validator)
                for column in range(0, total_column)
            ]
            return tuple(row)
        except AttributeError as error:
            max_row = self.rowCount()
            raise RowNotExists(
                f"given row number is invalid, can't be higher than {max_row}"
            ) from error

    def row_as_dict(self, row: int, validator: bool = False) -> dict:
        """
        Return value of the given row as dict by mapping
        the row value with the horizontal header
        -----------------------------------------------
        -> Params:
                row: row number
        """
        row = self.get_row(row, validator)
        value = zip(self.H_HEADER, row)
        return dict(value)

    def get_values(self, validator: bool = False) -> list:
        """
        Return value of the all the rows
        """
        total_rows = self.rowCount()
        if total_rows:
            return [
                self.row_as_dict(row, validator) for row in range(0, total_rows)
            ]

    def get_selected_row(self) -> dict:
        """
        Return selected row.
        """
        row = self.currentRow()
        return {**self.row_as_dict(row), "index": row}

    def get_selected_items(self) -> iter:
        """
        Return all selected cells.
        """
        for cell in self.selectedItems():
            yield cell.text()

    def get_selected_rows(self) -> iter:
        """
        Return selected rows when selection
        mode is multiple.
        -----------------------------------
        <- Return
            Generator
        """
        columns_count = self.columnCount()
        items = tuple(self.get_selected_items())
        for index, _ in enumerate(items):
            if index % columns_count == 0:
                yield dict(zip(self.H_HEADER, items[index:index+columns_count]))

    def clear_value(self) -> None:
        """
        Clear the table
        """
        self.horizontalHeader().hide()
        self.clear()

class CheckBox(QCheckBox):
    """
    Custom QtCheckbox widget
    """

    def __init__(self,
                 label: str,
                 callback_func: object = void_function,
                 icon_path: str = None,
                 icon_size: tuple = (15, 15),
                 icon_object: QIcon = None,
                 icon_size_object: QSize = None,
                 is_checked: bool = False,
                 object_name: str = None,
                 grid_positions: tuple = None,
                 **kwargs) -> None:
        super().__init__(label, **kwargs)
        self.setChecked(is_checked)
        self.stateChanged.connect(callback_func)
        self.stateChanged.connect(self.on_valid)
        # self.setCheckState(Qt.Checked)
        self.setObjectName(object_name)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        if icon_object:
            self.setIcon(icon_object)
            self.setIconSize(icon_size_object)
        else:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(*icon_size))
        self.grid_positions = grid_positions

    def get_value(self) -> bool:
        """
        return state of the check box
        """
        return self.isChecked()

    def change_state(self, state: int = 2) -> None:
        """
        Change state of the checkbox
        -> Params:
               states: 0 -> unchecked
                       1 -> partially checked
                       2 -> checked
        """
        self.setCheckState(state)
        self.setObjectName("valid")

    def on_valid(self) -> None:
        """
        change the css object name on when is unchecked
        """
        self.setObjectName("valid")

    def on_invalid(self) -> None:
        """
        change the css object name on when is unchecked
        """
        self.setObjectName("invalid")

class TextAnimation(Frame):
    """
    Contains widgets, animations and methods
    to show LUMENWERX in an animation way.
    """
    START_VALUE = 0.1
    END_VALUE = 1

    def __init__(self,
                 parent: object,
                 text: str,
                 frame_size: tuple = (260, 40),
                 speed: int = 50) -> None:
        super().__init__(parent=parent, layout=Horizontal)
        self.setHidden(True)
        self.setObjectName("text-animation")
        self.setFixedSize(*frame_size)
        self.text = text
        self.is_reverse = False
        self.charracter_index = -1
        self.duration = speed
        self.create_charracter_animation(text=text)
        self.is_running = False

    def get_next_charracter_index(self) -> None:
        """
        Increament a counter until it be equal to
        the length of the text. It helps animation
        to animate each charracter of the text.
        """
        self.charracter_index += 1
        if self.charracter_index == len(self.text):
            self.charracter_index = 0
            self.reverse_animation()
        return self.charracter_index

    def start(self) -> None:
        """
        Start the animations.
        """
        if self.is_running:
            return
        self.is_running = True
        self.set_animation_properties(self.START_VALUE, self.END_VALUE)
        self.setHidden(False)
        self.set_animation_finish_callback()

    def stop(self) -> None:
        """
        Stop the animations
        """
        if not self.is_running:
            return
        self.is_running = False
        self.setHidden(True)
        self.animation.stop()
        self.charracter_index = -1
        self.is_reverse = False
        for index, _ in enumerate(self.text, start=0):
            effect = getattr(self, f"effect{index}")
            effect.setOpacity(self.START_VALUE)

    def create_charracter_animation(self, text: str) -> None:
        """
        For each charracter in LUMENWERX create a label,
        effect and animation, so we can make them blink
        separately.
        """
        for index, char in enumerate(text, start=0):
            label = Label(char, object_name="loading-animation")
            effect = QGraphicsOpacityEffect(self, opacity=self.START_VALUE)
            label.setGraphicsEffect(effect)
            setattr(self, f"label{index}", label)
            setattr(self, f"effect{index}", effect)
        

    def set_animation_finish_callback(self) -> None:
        """
        Callback method whenever the animation finishes
        its job. It will switch its target(label effect)
        and start again with animating new target.
        """
        effect_index = self.get_next_charracter_index()
        self.animation.setTargetObject(getattr(self, f"effect{effect_index}"))
        self.animation.start()

    def reverse_animation(self) -> None:
        """
        This method calls when the last charracter
        animation is finished. It change the animations
        properties.
        """
        if self.is_reverse:
            self.set_animation_properties(start_value=self.START_VALUE,
                                          end_value=self.END_VALUE)
            self.is_reverse = False
            return
        self.set_animation_properties(start_value=self.END_VALUE,
                                      end_value=self.START_VALUE)
        self.is_reverse = True

    def set_animation_properties(self,
                                 start_value: float,
                                 end_value: float) -> None:
        """
        Set start value and end value for the animation.
        """
        self.animation = QPropertyAnimation(parent=self,
                                            targetObject=self.effect0,
                                            propertyName=b'opacity',
                                            startValue=self.START_VALUE,
                                            endValue=self.END_VALUE,
                                            duration=self.duration,
                                            loopCount=1)
        self.animation.finished.connect(self.set_animation_finish_callback)
        self.animation.setStartValue(start_value)
        self.animation.setEndValue(end_value)

