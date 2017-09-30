import zipfile
import os
import shutil
import subprocess
import requests
import urllib
from git import Repo

DESCRIPTORS_DIR = "Descriptors/"
RESULTS_DIR = "Results/"

def outputError(errorString, artifact):
    errorsFile.write(errorString + '. Artifact: ' + artifact + os.linesep)
    print("Error with " + artifact + ": " + errorString)

errorsFile = open('errors.out', 'w')

for rootdir,dirs,files in os.walk(DESCRIPTORS_DIR):
    for filename in files:
        if not filename.endswith(".desc"):
            continue

        fullPath = os.path.join(rootdir, filename)
        descFile = open(fullPath, 'r')
        artifact = filename[:-5]

        try:
            type = ""
            git_url = ""
            versions = []
            lang = ""
            for line in descFile.readlines():
                if line.startswith("versions: "):
                    versions = line.replace("versions: ", "").split(",")
                elif line.startswith("git_url: "):
                    git_url = line.replace("git_url: ", "").strip()
                elif line.startswith("type: "):
                    type = line.replace("type: ", "").strip()
                elif line.startswith("lang: "):
                    lang = line.replace("lang: ", "").strip()

            if lang and lang == "scala":
                print(artifact + " uses scala, skipping")
                continue

            repo_dir = RESULTS_DIR + artifact

            print("Processing artifact ", artifact, " of repo type ", type)

            if type == "github":
                if not os.path.exists(repo_dir):
                    print("Cloning " + git_url + " to " + repo_dir)
                    repo = Repo.clone_from(git_url, repo_dir)
                else:
                    repo = Repo(repo_dir)
                git = repo.git
                for version in versions:
                    git.checkout(version, force=True)
                    print("Successfully checked out version " + version + " of artifact " + artifact)
            else:
                print(artifact + " has unknown type, skipping")

        except Exception as e:
            outputError(str(e), artifact)
            continue

        '''
        print("Running mvn test for " + artifact + "-" + version)
        os.chdir(outputDir)
        proc = subprocess.Popen(["mvn test"], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        if out is None:
            print("ERROR: no output for " + artifact + "-" + version)
        outputFile = open('mvntest.out', 'w')
        outputFile.write(out.decode("utf-8"))
        outputFile.close()
        if not err is None:
            errorFile = open('mvntest.err', 'w')
            errorFile.write(err.decode("utf-8"))
            errorFile.close()
        os.system("rm -r src/ target/")
        os.chdir("../../")
        
        os.system("mkdir \"" + outputDir + "\"/src")
        '''

        print("Finished Processing " + artifact)