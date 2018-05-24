# Author: William Aldrich
# Created: 5-23-18
# Updated: 5-24-18

# Helpful sites / sites that code is from
# https://github.com/gitpython-developers/GitPython/issues/292
# http://gitpython.readthedocs.io/en/stable/tutorial.html
# https://stackoverflow.com/questions/11968976/list-files-in-only-the-current-directory?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa


import os
from git import Repo

# Uses GitPython must download

# Navigate to the folder that has your git repos inside of it
# Mine is in my home directory so this is where everything takes place

# get home directory
home = os.environ['HOME']

# navigate to home directory
homeDir = os.chdir(home)


# Get folders in current directory
# This should be able to find all git repos even if you add a new one
folders = [f for f in os.listdir('.') if not os.path.isfile(f)]
for f in folders:
    # ignore . directories
    # Change this if your git repos have '.' inside of them
    if '.' in f:
        continue

    # change directory to inside the file
    insideFile = os.chdir(home + "/" + str(f))
    # get the files inside the directory
    files = [y for y in os.listdir('.') if os.path.isfile(y)]

    for x in files:
        # if the files have a .git file they are a repository
        if ".git" in x:
            repo = Repo(insideFile)
            # check if anything is untracked or changed
            untracked = repo.untracked_files
            changedFiles = [repo.index.diff(None)]

            # if there is something untracked...
            # add everything to be commited
            # commit message is "Automatic Backup via python scripts"
            if len(untracked) >= 1 or "<" in str(changedFiles[0]):
                print (f + " has untracked or changed files that will be commited.")
                # add everything
                repo.git.add(A=True)
                index = repo.index
                # commit
                index.commit("Automatic Backup via updateGit.py")
                # Push
                repo.git.push('origin')
                print (f + " Updated.")

print ("\nAll git accounts have been updated or are up to date\n")
