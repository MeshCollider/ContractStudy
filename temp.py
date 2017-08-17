import os
import requests
import json
import xml.etree.ElementTree as ET

MAVEN_DIR = "../mvn-data/"

def outputError(errorString, artifact, groupID, version, filename):
	errorsFile.write(errorString + '. groupID: ' + groupID + ', artifact: ' + artifact + ', version: ' + version + ' in file ' + filename + os.linesep)
	print("Error with " + artifact + ": " + errorString)

errorsFile = open('errors.out', 'w')
successFile = open('sources2.out', 'a')

successFiles = []
oldErrorsFile = open('sources.out', 'r')
for line in oldErrorsFile:
	try:
		tempSplit = line.split(" (")
		artifact = tempSplit[0].strip()
		tempSplit = tempSplit[1].split(") ")
		groupID = tempSplit[0].strip()
		tempSplit = tempSplit[1].split(" ")
		version = tempSplit[0].strip()
		successFiles.append((artifact, version))
	except:
		continue

for rootdir,dirs,files in os.walk(MAVEN_DIR):
	for filename in files:
		try:
			if filename.endswith(".pom"):
				useParentVersion = False
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
					elif "version" in child.tag and not useParentVersion and not "parent.version" in child.text:
						version = child.text.strip()
					elif "parent" in child.tag:
						for child2 in child:
							if  "groupId" in child2.tag and not groupID:
								groupID = child2.text.strip()
							elif "artifactId" in child2.tag and not artifact:
								artifact = child2.text.strip()
							elif "version" in child2.tag and (not version or "parent.version" in version):
								version = child2.text.strip()
								if "parent.version" in version:
									useParentVersion = True
				if (artifact, version) in successFiles:
					continue
				mavenAPIQuery = "https://search.maven.org/solrsearch/select?q=g:\"" + groupID + "\"+AND+a:\"" + artifact + "\"+AND+v:\"" + version + "\""
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

errorsFile.close()
successFile.close()
