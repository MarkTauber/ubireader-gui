import shutil

from .constants import ACCENT, ACCENT2, GREEN


def check_ubireader() -> bool:
    return shutil.which("ubireader_extract_images") is not None or shutil.which("ubireader_display_info") is not None

def ubi_commands() -> dict:
    return {

        "extract_files": {
            "cmd": "ubireader_extract_files",
            "label": "Extract files",
            "icon": "📂",
            "desc": "Extract filesystem contents",
            "color": GREEN,
            "args": [

                # Output
                {
                    "name": "--output", 
                    "flag": "-o", 
                    "label": "Output directory", 
                    "type": "dir", 
                    "required": False
                },

                # Offset START
                {
                    "name": "--start-offset", 
                    "flag": "--start-offset", 
                    "label": "Start offset (bytes)", 
                    "type": "int", 
                    "required": False
                },

                # Offset END
                {
                    "name": "--end-offset", 
                    "flag": "--end-offset", 
                    "label": "End offset (bytes)", 
                    "type": "int", 
                    "required": False
                },

                # LOG
                {
                    "name": "--log", 
                    "flag": "--log", 
                    "label": "Log file", 
                    "type": "file_save", 
                    "required": False
                },

                # I wanna be smart so I really want to know what's going on (I will not read all the verbose output)
                {
                    "name": "--verbose", 
                    "flag": "--verbose", 
                    "label": "Verbose output", 
                    "type": "bool", 
                    "required": False
                },

            ],
        },


        "extract_images": {
            "cmd": "ubireader_extract_images",
            "label": "Extract images",
            "icon": "💾",
            "desc": "Extract individual volumes",
            "color": ACCENT,
            "args": [
                
                # Output
                {
                    "name": "--output", 
                    "flag": "-o", 
                    "label": "Output directory", 
                    "type": "dir", 
                    "required": False
                },
                
                # Offset START
                {
                    "name": "--start-offset", 
                    "flag": "--start-offset", 
                    "label": "Start offset (bytes)", 
                    "type": "int", 
                    "required": False
                },

                # Offset END
                {
                    "name": "--end-offset", 
                    "flag": "--end-offset", 
                    "label": "End offset (bytes)", 
                    "type": "int", 
                    "required": False
                },

                # Smartie
                {
                    "name": "--verbose", 
                    "flag": "--verbose", 
                    "label": "Verbose output", 
                    "type": "bool", 
                    "required": False
                },

            ],
        },


        "display_info": {
            "cmd": "ubireader_display_info",
            "label": "Display info",
            "icon": "📊",
            "desc": "Show image structure metadata",
            "color": "#E07EFF",
            "args": [
                
                # Offset START
                {
                    "name": "--start-offset", 
                    "flag": "--start-offset", 
                    "label": "Start offset (bytes)", 
                    "type": "int", 
                    "required": False
                },

                # Offset END
                {
                    "name": "--end-offset", 
                    "flag": "--end-offset", 
                    "label": "End offset (bytes)", 
                    "type": "int", 
                    "required": False
                },

                # smartie
                {
                    "name": "--verbose", 
                    "flag": "--verbose", 
                    "label": "Verbose output", 
                    "type": "bool", 
                    "required": False
                },

            ],
        },

        "list_files": {
            "cmd": "ubireader_list_files",
            "label": "List files",
            "icon": "📋",
            "desc": "List files without extraction",
            "color": ACCENT2,
            "args": [

                # Offset START
                {
                    "name": "--start-offset", 
                    "flag": "--start-offset", 
                    "label": "Start offset (bytes)", 
                    "type": "int", 
                    "required": False
                },

                # Offset END
                {
                    "name": "--end-offset", 
                    "flag": "--end-offset", 
                    "label": "End offset (bytes)", 
                    "type": "int", 
                    "required": False
                },

                # Verbose
                {
                    "name": "--verbose", 
                    "flag": "--verbose", 
                    "label": "Verbose output", 
                    "type": "bool", 
                    "required": False
                },
            ],
        },
    }
