import os
import requests
import urllib

MAVEN_DIR = "MavenTestSources/"

def outputError(errorString, artifact, groupID, version):
	errorsFile.write(errorString + '. groupID: ' + groupID + ', artifact: ' + artifact + ', version: ' + version + os.linesep)
	print("Error with " + artifact + ": " + errorString)

errorsFile = open('errors.out', 'w')
sourcesFile = open('sourcelist.in', 'r')
if not os.path.exists(MAVEN_DIR):
    os.makedirs(MAVEN_DIR)

for line in sourcesFile.readlines():
        
        availableTypes = line.split(" - ")[1].split(",")
        artifact = line.split(" (")[0]
        groupID = line.split(" (")[1].split(") ")[0]
        version = line.split(") ")[1].split(" - ")[0]

        if not "-test-sources.jar" in availableTypes or "scala" in artifact:
                continue

        if not groupID or not version or not artifact:
                outputError("Version, groupID or artifact is empty.", artifact, groupID, version)

        groupID = groupID.replace(".", "/")
        mavenAPIQuery = "http://search.maven.org/remotecontent?filepath=" + groupID + "/" + artifact + "/" + version + "/" + artifact + "-" + version + "-test-sources.jar" # com/google/inject/guice/4.1.0/guice-4.1.0-sources.jar
        fileDownloadLocation= MAVEN_DIR + artifact + "-" + version + "-test-sources.jar"
        print(mavenAPIQuery)

        try:
                urllib.urlretrieve (mavenAPIQuery, fileDownloadLocation)
        except Exception as e:
                print("ERROR with artifact " + artifact + "-" + version)
                outputError("ERROR with artifact, " + str(e), artifact, groupID, version)
                continue

errorsFile.close()
sourcesFile.close()
