#!/usr/bin/python3

import sys
import os
import shutil
import subprocess
import re

# check to see if the user specified an AAF file
if len(sys.argv) < 2:
    script_name = os.path.basename(sys.argv[0])
    print(f"Error: No AAF file specified.\nUsage: {script_name} <AAF file>")
    sys.exit(1)

# there are two Python modules we use that aren't part of a normal Python distribution. urllib3 and pyaaf2. Let's check for them and install if necessary.
try:
    from urllib.parse import unquote
except ImportError:
    print("The 'urllib' module is not installed. Installing now...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "urllib3"])
        print("Installation of 'urllib' module successful!")
        from urllib.parse import unquote
    except subprocess.CalledProcessError:
        print("Error: Failed to install 'urllib' module using pip.")
        print("The 'urllib' module is not installed. Please run 'pip install urllib3' to install it.")
        sys.exit(1)

try:
    import aaf2
except ImportError:
    print("The 'aaf2' module is not installed. Installing now...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyaaf2"])
        print("Installation of 'aaf2' module successful!")
        import aaf2
    except subprocess.CalledProcessError:
        print("Error: Failed to install 'aaf2' module using pip.")
        print("The 'aaf2' module is not installed. Please run 'pip install pyaaf2' to install it.")
        print("\nMore information on the pyaaf2 module can be found at https://pyaaf.readthedocs.io/en/latest/quickstart.html")
        sys.exit(1)
    
# import aaf2
from aaf2.file import AAFFile
# from aaf2 import properties
# from aaf2.mobid import MobID

existing_files = []
missing_files = []

with aaf2.open(sys.argv[1], "r") as f:
    
    # uncomment next line to dump all AAF content for examination
    # print(f.dump().encode('utf-8'))

    # Let's get the sequence's name.
    main_compostion = next(f.content.toplevel())
    sequence_name = main_compostion.name
    
    #Avid Media Composer adds ".Exported.01" to the end of sequence names when doing an AAF export let's remove that unnecessary cruft.    
    sequence_name = re.sub(r".Exported.\d\d","",sequence_name)
    
    # Create the directory for copied files
    desktop_folder = os.path.expanduser(f"~/Desktop/copied_files/{sequence_name}")
    os.makedirs(desktop_folder, exist_ok=True)
    
    
    print(f"\nFinding and copying MXF sources for clips in sequence \"{sequence_name}\"")

    
    for mobby in f.content.sourcemobs():
        if hasattr(mobby.descriptor, 'locator') and not isinstance(mobby.descriptor, aaf2.essence.ImportDescriptor):
            for loc in mobby.descriptor.locator:
                file_location = unquote(loc['URLString'].value.encode('utf-8'))
                                
                # the returned file paths usually are of a form that starts with "file://nexispro/" or "file://10.0.1.199/", the name of the fileserver on which the files are located. For our purposes we need to replace this with "/Volumes/" so that it produces normal filesystem paths that can be used to copy files.
                
                file_location = re.sub(r"file://([^/]+)/", "/Volumes/", file_location)

                # check if the file exists
                if os.path.exists(file_location):
                    existing_files.append(file_location)
                else:
                    missing_files.append(file_location)

# copy the existing files to the Desktop folder
os.makedirs(desktop_folder, exist_ok=True)
for file_location in existing_files:
    file_name = os.path.basename(file_location)
    dest_file_path = os.path.join(desktop_folder, file_name)
    try:
        shutil.copy2(file_location, dest_file_path)
        print(f"Successfully copied {file_name} to \"{desktop_folder}\"")
    except Exception as e:
        print(f"Error copying {file_name}: {e}")

# print a summary of the copied files and make a list of any missing files
print(f"\nCopied {len(existing_files)} files to {desktop_folder}")
if len(missing_files) > 0:
    missing_file_list_path = os.path.join(desktop_folder, "missing_files.txt")
    with open(missing_file_list_path, "w") as f:
        f.write("\n".join(missing_files))
    print(f"\n{len(missing_files)} files were not found. A list of the missing files has been written to \"{missing_file_list_path}\".")
    # for file_location in missing_files:
    #     print(file_location)
else:
    print("\nAll files found and copied successfully!")
