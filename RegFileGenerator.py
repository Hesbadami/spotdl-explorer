from textwrap import dedent
import os
from string import ascii_lowercase

class RegGenerator():
    def __init__(self):
        self.types = {
            "mp3": {'options': '', 'icon': 103, 'name': 'Download audio (MP3)'},
            "wav": {'options': '--output-format ogg', 'icon': 80, 'name': 'Download audio (OGG)'},
        }
        self.reg_common = "HKEY_CLASSES_ROOT\Directory\Background\shell\SpotDL"
        self.command_common = \
        """
        @="powershell.exe -Command
        \\"spotdl $(Get-Clipboard)
        """
        
        self.command_common = " ".join(self.command_common.split())
        self.command_common_end = '\\""'
        self.start = \
        """
        Windows Registry Editor Version 5.00
        ; Spotify downloader context menu
        ; by Hesbadami
        ; inspired by notthebee

        ; Deleting the previous version
        [-{reg_common}]


        [{reg_common}]
        "MUIVerb"="spotdl"
        "SubCommands"=""

        [{reg_common}\shell]

        """.format(reg_common = self.reg_common)
        self.start = dedent(self.start)

    def gen_all(self):
        types_string = ""
        count = 0
        for type, subtypes in self.types.items():
            reg_root_dir = "[{reg_common}\shell\{alpha_type}_{type}]".format(reg_common = self.reg_common, alpha_type = ascii_lowercase[count], type = type)

            at = "@"
            subcommands = ""
            reg_root_dir_command = reg_root_dir[:-1] + "\command]"
            command = self.command_common + " " + subtypes['options'] + self.command_common_end
            reg_name = '{}="{}"'.format(at, subtypes['name'])
            icon = '"Icon"="imageres.dll,{}"'.format(subtypes['icon'])

            result_string = ("\n").join([reg_root_dir, reg_name, subcommands, icon, reg_root_dir_command, command, ""]).replace("\n\n", "\n")
            types_string += "\n" + result_string
            count += 1
        result = self.start + types_string
        cwd = os.path.dirname(os.path.realpath(__file__))
        file = os.path.join(cwd, 'spotdl.reg')
        with open(file, "w+") as regfile:
            regfile.write(result.strip())
        


RegGenerator().gen_all()
