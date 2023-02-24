# AAF_Collider
A media copying python script which takes an AAF of a Media Composer sequence as input, and copies all source MXF files referenced in it to a folder

## Usage:

```% AAF_Collider_v4.py MySequence.aaf```

## Expected Outcome:
This script uses the [pyaaf2 module](https://github.com/markreidvfx/pyaaf2) to parse an AAF files and collect the paths of all source MXF files referenced in a sequence, and then it copies those files into a folder on the desktop named for the sequence. It will also make a list of any missing media and write that to a text file in that same folder.

It has been tested in a collaborative environment, with AAF files exported using the "Link to (Don't Export) Media" setting. When source media are located on a Nexis or other network filesystem, the references to those locations in the AAF all start with file://nexispro/ or file://IP_Address/. In order to make the source locations function for copying from the Unix shell, the script replaces the URL portion of the path with "/Volumes/". This works on macOS, but other logic may be required for other computing platforms. 

## Prerequisites:
Depending on your version of macOS (or other OS), you may or may not have Python3 installed. On macOS this can be rectified by installing the "Homebrew" package system using the instructions at [homebrew.sh](http://homebrew.sh), and then running "brew install python". 

The script does depend on a couple of python modules (urllib3 and pyaaf2) that are not included in a standard Python distribution. If it finds that they are not installed on your system it will attempt to install them itself. If that fails, will provide some information on how to install them.

It is possible that you'll need the invoke the script in a slightly different fashion than the example provided above. The invocation may look more like:

```% python3 /path/to/AAF_Collider_v4.py /path/to/MySequence.aaf```

or

```% /usr/local/bin/python3 /path/to/AAF_Collider_v4.py /path/to/MySequence.aaf```

or

```% /opt/local/bin/python3 /path/to/AAF_Collider_v4.py /path/to/MySequence.aaf```

## Why the name?
This script _sucks_ the source media references out of an AAF, and the Large Hadron Collider is the world's largest *vacuum*. So… yeah it's a stretch but I didn't want to name it "My copy of Automatic Duck Media Copy no longer runs so I threw this together to fill a need".
