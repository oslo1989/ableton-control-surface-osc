import sys
import shutil
import os
user_path = os.path.expanduser("~")
site_path = sys.path[-1] # assume that the last path is the site path of the virtual environment
for l in ["fastosc"]:
    shutil.copytree(f"{site_path}/{l}", f"{user_path}/Music/Ableton/User Library/Remote Scripts/{l}")