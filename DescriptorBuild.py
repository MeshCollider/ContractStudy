import zipfile
import os
import shutil
import subprocess


DESCRIPTOR_DIR = "Descriptors/"

sourcesFile = open('sourcelist.in', 'r')
artifacts = {}
for line in sourcesFile.readlines():
        artifact = line.split(" (")[0]
        groupID = line.split(" (")[1].split(") ")[0]
        version = line.split(") ")[1].split(" - ")[0]

        if artifact in artifacts:
                artifacts[artifact].append(version)
        else:
                artifacts[artifact] = [version]

        

for artifact,versions in artifacts.items():
        fileName = DESCRIPTOR_DIR + artifact + ".desc"
        sourcesFile = open(fileName, 'w')
        sourcesFile.write("versions: " + ','.join(versions) + "\n")
        sourcesFile.write("git_url: " + "-" + "\n")
        sourcesFile.write("run_command: " + "`mvn test`" + "\n")
