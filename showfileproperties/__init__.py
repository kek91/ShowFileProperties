from fman import DirectoryPaneCommand, load_json, show_alert
from os import stat, path, walk
import datetime

def calculate_size_subdirectories(rootdir = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in walk(rootdir):
        for f in filenames:
            fp = path.join(dirpath, f)
            total_size += path.getsize(fp)
    return total_size

def convert_bytes(n):
    for x in ['B', 'KB', 'MB', 'GB', 'TB']:
        if n < 1024.0:
            return "%3.1f %s" % (n, x)
        n /= 1024.0

class ShowFileProperties(DirectoryPaneCommand):
    def __call__(self):
        selected_files = self.pane.get_selected_files()
        files_num = 0
        files_size = 0
        folders_num = 0
        fsubfiles = 0
        output = "Properties\n\n"

        if len(selected_files) > 1:
            for n in selected_files:
                if path.isdir(n):
                    folders_num += 1
                    fsubfiles += calculate_size_subdirectories(n)
                else:
                    files_num += 1
                    files_size += stat(n).st_size
            if files_num >= 1:
                output += "Selected files:\t\t\t" + str(files_num) + "\n"
                output += "Combined filesize:\t\t" + str(convert_bytes(files_size)) + "\n\n"
            if folders_num >= 1:
                output += "Selected directories:\t\t" + str(folders_num) + "\n"
                output += "Combined size for directories::\t" + str(convert_bytes(fsubfiles)) + "\n\n"

        elif len(selected_files) == 1 or (len(selected_files) == 0 and self.get_chosen_files()):
            if len(selected_files) == 1:
                n = selected_files[0]
            elif len(selected_files) == 0 and self.get_chosen_files():
                n = self.get_chosen_files()[0]
            files_size += stat(n).st_size
            finfo = stat(n)
            flastmodified = datetime.date.fromtimestamp(finfo.st_mtime)
            flastaccessed = datetime.date.fromtimestamp(finfo.st_atime)
            fsize = finfo.st_size
            output += n + "\n\n"
            output += "Last viewed:\t\t\t" + str(flastaccessed) + "\n"
            output += "Last modified:\t\t\t" + str(flastmodified) + "\n\n"
            output += "Size:\t\t\t" + str(convert_bytes(fsize)) + "\n"
            if path.isdir(n):
                folders_num += 1
                fsubfiles = calculate_size_subdirectories(n)
                output += "Total size subdirectories and files:\t" + str(convert_bytes(fsubfiles)) + "\n"
            else:
                files_num += 1

        else:
            output += "No files or directories selected"

        show_alert(output)
