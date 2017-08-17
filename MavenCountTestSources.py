import os
import requests
import json
import xml.etree.ElementTree as ET

MAVEN_DIR = "../mvn-data/"

def outputError(errorString, artifact, groupID, version, filename):
	errorsFile.write(errorString + '. groupID: ' + groupID + ', artifact: ' + artifact + ', version: ' + version + ' in file ' + filename + os.linesep)
	print("Error with " + artifact + ": " + errorString)

errorsFile = open('errors.out', 'w')
successFile = open('sources.out', 'w')

for rootdir,dirs,files in os.walk(MAVEN_DIR):
	for filename in files:
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
					elif child.tag == "parent":
						for child2 in child:
							if  "groupId" in child2.tag and not groupID:
								groupID = child2.text.strip()
							elif "artifactId" in child2.tag and not artifact:
								artifact = child2.text.strip()
							elif "version" in child2.tag and not version:
								version = child2.text.strip()
				mavenAPIQuery = "https://search.maven.org/solrsearch/select?q=g:\"" + groupID + "\"+AND+a:\"" + artifact + "\"+AND+v:\"" + version + "\""
				response = requests.get(mavenAPIQuery)
				if not response.ok:
					response = requests.get(mavenAPIQuery)
				if response.ok:
					try:
						jsonData = json.loads(response.content.decode("utf-8"))
					except: 
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
			continue

errorsFile.close()
successFile.close()
