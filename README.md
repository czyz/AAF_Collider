# AAF_Collider
A media copying python script which takes an AAF of a Media Composer sequence as input, and copies all source MXF files referenced in it to a folder

Usage:

```% AAF_Collider_v4.py MySequence.aaf```

This script uses the pyaaf2 module to parse an AAF files and collect the paths of all source MXF files referenced in a sequence, and then it copies those files into a folder on the desktop named for the sequence. It will also make a list of any missing media and write that to a text file in that same folder. 
