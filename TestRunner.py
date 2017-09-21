import zipfile
import os
import shutil


MAVEN_TEST_DIR = "Maven Test Sources/"
MAVEN_SOURCE_DIR = "../mvn-data/"

sourcesFile = open('sourcelist.in', 'r')
for line in sourcesFile.readlines():
        
        availableTypes = line.split(" - ")[1].split(",")
        artifact = line.split(" (")[0]
        groupID = line.split(" (")[1].split(") ")[0]
        version = line.split(") ")[1].split(" - ")[0]

        if not "-test-sources.jar" in availableTypes or "scala" in artifact:
                continue

        fileName = MAVEN_TEST_DIR + artifact + "-" + version + "-test-sources.jar"
        outputDir = fileName[:-4]
        
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
            zip_ref = zipfile.ZipFile(fileName, 'r')
            zip_ref.extractall(outputDir)
            zip_ref.close()
                
        if not os.path.exists(outputDir + "/src"):
            # move the sources into the correct directory structure
            os.system("mkdir \"" + outputDir + "\"/src")
            os.system("mkdir \"" + outputDir + "\"/src/test")
            os.system("mv \"" + outputDir + "\"/* \"" + outputDir + "\"/src/test/")

        outputDirSrcMain = outputDir + "/src/main/"
        zipFilePath = MAVEN_SOURCE_DIR + artifact + "/" + artifact + "-" + version + ".zip"
        if not os.path.exists(outputDirSrcMain):
            os.makedirs(outputDirSrcMain)
            zip_ref = zipfile.ZipFile(zipFilePath, 'r')
            zip_ref.extractall(outputDirSrcMain)
            zip_ref.close()

        if not os.path.exists(outputDir + "/pom.xml"):
            pomFileLocation = MAVEN_SOURCE_DIR + artifact + "/" + artifact + "-" + version + ".pom"
            os.system("cp \"" + pomFileLocation + "\" \"" + outputDir + "\"/pom.xml")
            
                
