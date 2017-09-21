import zipfile
import os
import shutil


MAVEN_TEST_DIR = "Maven Test Sources/"
MAVEN_SOURCE_DIR = "../mvn-data/"


for rootdir,dirs,files in os.walk(MAVEN_TEST_DIR):
    for filename in files:
        if filename.endswith(".jar"):
            fullPath = os.path.join(rootdir,filename)
            outputDir = os.path.join(rootdir,filename[:-4])
            # print(outputDir)
            if not os.path.exists(outputDir):
                os.makedirs(outputDir)
                zip_ref = zipfile.ZipFile(fullPath, 'r')
                zip_ref.extractall(outputDir)
                zip_ref.close()
            # move the sources into the correct directory structure
            os.system("pwd")

            
