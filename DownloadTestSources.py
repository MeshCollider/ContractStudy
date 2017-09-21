import os
import requests
import urllib

MAVEN_DIR = "Maven Test Sources/"

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

        '''
        String groupPath = version.getGroupId().replace('.', '/');
        try:
                if filename.endswith(".pom"):
			fullPath = os.path.join(rootdir,filename)
			tree = ET.parse(fullPath)
			root = tree.getroot()
			groupID = ""
			artifact = ""
			version = ""
			for child in root:
				if  "groupId" in child.tag:
					groupID = child.text.strip()
				elif "artifactId" in child.tag:
					artifact = child.text.strip()
				elif "version" in child.tag:
					version = child.text.strip()
				elif "parent" in child.tag:
					for child2 in child:
						if  "groupId" in child2.tag and not groupID:
							groupID = child2.text.strip()
						elif "artifactId" in child2.tag and not artifact:
							artifact = child2.text.strip()
						elif "version" in child2.tag and not version:
							version = child2.text.strip()
			
			response = requests.get(mavenAPIQuery)
			if not response.ok:
				response = requests.get(mavenAPIQuery)
			if response.ok:
				try:
					jsonData = json.loads(response.content.decode("utf-8"))
				except: 
					outputError("Error loading JSON data", artifact, groupID, version, filename)
					print("Error loading JSON data from " + filename)
					continue
				numFound = jsonData["response"]["numFound"]
				if numFound != 1:
					outputError("Num found not 1, instead " + str(numFound), artifact, groupID, version, filename)
				else:
					successFile.write(artifact + " (" + groupID + ") " + version + " - " + ",".join(jsonData["response"]["docs"][0]["ec"]) + '\n')
					print("Successfully retrieved " + artifact + ' ' + version)
			else:
				outputError("Response not ok", artifact, groupID, version, filename)
	except Exception as e:
		print("ERROR with file: " + filename + ", " +str(e))
		outputError("ERROR with file, " + str(e), artifact, groupID, version, filename)
		continue
        '''

errorsFile.close()
sourcesFile.close()
