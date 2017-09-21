import zipfile
import os


MAVEN_DIR = "Maven Test Sources/"

for rootdir,dirs,files in os.walk(MAVEN_DIR):
    for filename in files:
        if filename.endswith(".jar"):
            fullPath = os.path.join(rootdir,filename)
            outputDir = os.path.join(rootdir,filename[:-4])
            print(outputDir)
            if not os.path.exists(outputDir):
                os.makedirs(outputDir)
            else:
                continue
            zip_ref = zipfile.ZipFile(fullPath, 'r')
            zip_ref.extractall(outputDir)
            zip_ref.close()
