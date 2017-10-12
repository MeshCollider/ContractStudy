import zipfile
import os
import shutil
import subprocess
import requests
import urllib
from git import Repo
import time

DESCRIPTORS_DIR = "Descriptors/"
RESULTS_DIR = "Results/"

SPECIFIC_PROJECT = "log4j-core"

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

        if SPECIFIC_PROJECT and artifact != SPECIFIC_PROJECT:
            continue

        try:
            type = ""
            git_url = ""
            versions = []
            lang = ""
            versionstyle = ""
            testdir = "src/tests"
            run_command = "mvn test"
            subdir = ""
            for line in descFile.readlines():
                if line.startswith("versions: "):
                    versions = line.replace("versions: ", "").split(",")
                elif line.startswith("git_url: "):
                    git_url = line.replace("git_url: ", "").strip()
                elif line.startswith("type: "):
                    type = line.replace("type: ", "").strip()
                elif line.startswith("lang: "):
                    lang = line.replace("lang: ", "").strip()
                elif line.startswith("versionstyle: "):
                    versionstyle = line.replace("versionstyle: ", "").strip()
                elif line.startswith("testdir: "):
                    testdir = line.replace("testdir: ", "").strip()
                elif line.startswith("run_command: "):
                    run_command = line.replace("run_command: ", "").strip()
                elif line.startswith("subdir: "):
                    subdir = line.replace("subdir: ", "").strip()

            if lang and lang == "scala":
                print(artifact + " uses scala, skipping")
                continue

            repo_dir = RESULTS_DIR + artifact
            repo_tests_dir = RESULTS_DIR + artifact + "-test-dirs"
            if not os.path.exists(repo_tests_dir):
                os.makedirs(repo_tests_dir)

            print("Processing artifact ", artifact, " of repo type ", type)

            if type == "github":
                if not os.path.exists(repo_dir):
                    print("Cloning " + git_url + " to " + repo_dir)
                    repo = Repo.clone_from(git_url, repo_dir)
                else:
                    repo = Repo(repo_dir)
                git = repo.git
                for version in versions:
                    try:
                        repo_dir_temp = repo_dir
                        if subdir != "":
                            repo_dir_temp += "/" + repodir
                            
                        versionParts = version.split(".")
                        versionString = versionstyle.replace("{MAJ}", versionParts[0]).replace("{MIN}", versionParts[1]).replace("{PATCH}", versionParts[2])
                        git.checkout(versionString, force=True)
                        shutil.copytree(repo_dir_temp + "/" + testdir, repo_tests_dir + "/" + version)
                        print("Successfully checked out version " + version + " of artifact " + artifact + ". Running tests...")
                         
                        os.chdir(repo_dir_temp)
                        print (run_command)
                        print(os.getcwd())
                        proc = subprocess.Popen([run_command], stdout=subprocess.PIPE, shell=True)
                        (out, err) = proc.communicate()
                        if out is None:
                            print("ERROR: no output for " + artifact + "-" + version)
                        outputFile = open(version + '.out', 'w')
                        outputFile.write(out.decode("utf-8"))
                        outputFile.close()
                        if not err is None:
                            errorFile = open(version + '.err', 'w')
                            errorFile.write(err.decode("utf-8"))
                            errorFile.close()
                        os.chdir("../../")
                        if subdir != "":
                            os.chdir("../") # go up one more level if needed
                        shutil.copyfile(repo_dir_temp + "/" + version + '.out', repo_tests_dir + "/" + version + '.out')
                        shutil.copyfile(repo_dir_temp + "/" + version + '.err', repo_tests_dir + "/" + version + '.err')

                    except Exception as e:
                        outputError("Error checking out version " + versionString + ": " + str(e), artifact)
                        continue
            else:
                print(artifact + " has unknown type, skipping")

        except Exception as e:
            outputError(str(e), artifact)
            continue

        print("Finished Processing " + artifact)
