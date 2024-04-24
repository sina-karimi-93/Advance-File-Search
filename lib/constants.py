
from os import getcwd

CWD = getcwd()

DATE_FORMAT = "%d-%m-%Y"
TABLE_HEADERS = ["Title", "Price", "Quantity",
                "Overall Price", "Categoty",
                "Date"]

CSS_COLORS_FILE_PATH = f"{CWD}/lib/css/colors.css"
CSS_FILE_PATH = f"{CWD}/lib/css/style.css"

# ====================================== Patterns ======================================
LENGTH_VALIDATION_PATTERN = "[a-zA-Z\\d\\s.]+"
DRIVER_VALIDATION_PATTERN = "[a-zA-Z\\d\\s()-]+"
LINE_TYPE_VALIDATION_PATTERN = "[a-zA-Z\\d-()]+"

# ====================================== Widgets Validators ======================================
ONLY_STRING_SPACE_PATTERN = "[a-zA-Z\\s\\d,]+"

