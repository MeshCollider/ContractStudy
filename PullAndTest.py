import zipfile
import os
import shutil
import subprocess
import requests
import urllib
from git import Repo
import time
import sys
import collections

DESCRIPTORS_DIR = "Descriptors/"
RESULTS_DIR = "Results/"

# Get the names of specific projects to run as command line parameters
if len(sys.argv) > 1:
    SPECIFIC_PROJECTS = sys.argv[1:]

# Helper function to print error and write it to an errors file
def outputError(errorString, artifact):
    errorsFile.write(errorString + '. Artifact: ' + artifact + os.linesep)
    print("Error with " + artifact + ": " + errorString)

errorsFile = open('errors.out', 'w')

# Iterate over the contents of the descriptors directory
for rootdir,dirs,files in os.walk(DESCRIPTORS_DIR):
    for filename in files:
        
        # Skip non-descriptor files
        if not filename.endswith(".desc"):
            continue

        fullPath = os.path.join(rootdir, filename)

        # Open the descriptor file and grab the artifact name
        descFile = open(fullPath, 'r')
        artifact = filename[:-5]

        # If we specified only certain projects, check if this is one of them
        if SPECIFIC_PROJECTS and artifact not in SPECIFIC_PROJECTS:
            continue

        try:
            descriptor = collections.defaultdict(str)

            for line in descFile.readlines():

                # Skip comments in descriptor file
                if line.startswith("#"):
                    continue

                # Default values:
                descriptor["testdir"] = "src/tests"
                descriptor["run_command"] = "mvn test"
                
                # Split line into name and value
                # Currently these include 'versions', 'git_url', 'type', 'lang', 'prefix', 'separator', 'testdir', 'run_command', and 'subdir'
                entryName, entryVal = line.split(": ")
                descriptor[entryName.strip()] = entryVal.strip()

                descriptor["versions"] = descriptor["versions"].split(",")

            # Skip scala projects for now
            if descriptor["lang"] == "scala":
                print(artifact + " uses scala, skipping")
                continue

            # Create a new directory to hold data from this repo
            repo_dir = RESULTS_DIR + artifact
            repo_tests_dir = RESULTS_DIR + artifact + "-processed"
            if not os.path.exists(repo_tests_dir):
                os.makedirs(repo_tests_dir)

            print("Processing artifact ", artifact, " of repo type ", descriptor["type"])

            # If this is a github project, clone it using git
            if descriptor["type"] == "github":

                # Check if the repo already exists before cloning
                if not os.path.exists(repo_dir):
                    print("Cloning " + descriptor["git_url"] + " to " + repo_dir)
                    repo = Repo.clone_from(descriptor["git_url"], repo_dir)
                else:
                    repo = Repo(repo_dir)
                git = repo.git

                # Iterate over the list of versions
                for version in descriptor["versions"]:
                    try:

                        # If this project is actually in a subdirectory of the repository, use that
                        repo_dir_temp = repo_dir
                        if descriptor["subdir"]:
                            repo_dir_temp += "/" + descriptor["subdir"]

                        # Split the version number into its components (the patch may include a suffix e.g. rc1 or -something)
                        versionParts = version.split(".")
                        # Create the string for the tag of this version on git by combining with the prefix and separators
                        versionString = descriptor["prefix"] + versionParts[0] + descriptor["separator"] + versionParts[1]
                        # Some cases we only have a major and minor version number with no patch, so we must check this
                        if len(versionParts) > 2:
                             versionString += descriptor["separator"] + versionParts[2]

                        # Check out the tag
                        git.checkout(versionString, force=True)

                        # Copy the test directory into the processed directory for cross version testing later
                        shutil.copytree(os.path.join(repo_dir_temp, descriptor["testdir"]), os.path.join(repo_tests_dir, version))
                        print("Successfully checked out version " + version + " of artifact " + artifact + ". Running tests...")

                        # cd into the repo directory
                        os.chdir(repo_dir_temp)
                        print ("Running command:", descriptor["run_command"], "in directory", os.getcwd())

                        # Run the run_command and capture the output
                        proc = subprocess.Popen([descriptor["run_command"]], stdout=subprocess.PIPE, shell=True)
                        (out, err) = proc.communicate()

                        # Move back up into the root project folder, including additional ../ for any
                        numDirsUp = 3 if descriptor["subdir"] else 2
                        os.chdir("../" * numDirsUp)
                        
                        if out is None:
                            print("ERROR: no output for " + artifact + "-" + version)

                        # Write the output to a version file for this project
                        outputFile = open(repo_tests_dir + "/" + version + '.out', 'w')
                        outputFile.write(out.decode("utf-8"))
                        outputFile.close()

                        # If we also have errors, write these to an errors file
                        if not err is None:
                            errorFile = open(repo_tests_dir + "/" + version + '.err', 'w')
                            errorFile.write(err.decode("utf-8"))
                            errorFile.close()

                    except Exception as e:
                        outputError("Error checking out version " + version + ": " + str(e), artifact)
                        continue
                    
            # So far only github is implemented, others like svn/soureforge may need to be added
            else:
                print(artifact + " has unknown type, skipping")

        except Exception as e:
            outputError(str(e), artifact)
            continue

        print("Finished Processing " + artifact)
