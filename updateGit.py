# Author: William Aldrich
# Github: https://github.com/w-aldrich
# Created: 05-23-18
# Updated: 06-08-18

# Helpful sites / sites that code is from
# https://github.com/gitpython-developers/GitPython/issues/292
# http://gitpython.readthedocs.io/en/stable/tutorial.html
# https://stackoverflow.com/questions/11968976/list-files-in-only-the-current-directory?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa


# import progressbar, time # uncomment if using ProgressBar
import os
from git import Repo
from git import remote


# Uses gitpython must download
# Uses progressbar2 must download

# Navigate to the folder that has your git repos inside of it
# Mine is in my home directory so this is where everything takes place

'''
Setup of program
Finds the home directory and all of the directories immediately inside that directory
calls goThroughFolders() to do the heavy work
Prints out whether or not all git repos are up to date or not after this program
if not, will print out all repos that need to be updated
'''
def main():
    # get home directory
    home = os.environ['HOME']
    # navigate to home directory
    homeDir = os.chdir(home)

    # Get folders in current directory
    # This should be able to find all git repos even if you add a new one
    folders = [f for f in os.listdir('.') if not os.path.isfile(f)]

    '''
    Add this back in if you want to work with a progress bar
    Slower with one, but prettier
    As of right now must take everything out of functions for it to work
    '''
    # widgets = ["Complete: ", progressbar.Percentage(), progressbar.Bar()]
    # fileLen = len(folders)
    # bar = progressbar.ProgressBar(widgets=widgets, max_value=fileLen).start()

    # Get whether or not everything is up to date as well as the folders that are not up to date
    retVals = goThroughFolders(home, folders)

    # flag for everything up to date
    complete = retVals[0]
    # list of incomplete folders
    incompleteFolders = retVals[1]

    '''
    This will complete the progress bar, add this back in if you want it
    '''
    # This will say that the progress bar is finished 100%
    # bar.finish()

    # final print message stating everything is updated or up to date
    if complete:
        print ("\nAll git accounts have been updated or are up to date\n")
    else:
        print ("\nThe following folders are not up to date:")
        for incomplete in incompleteFolders:
            print ("\t" + incomplete)

'''
This will loop through all of the folders for a given directory
skips directories that begin with a .
'''
def goThroughFolders(home, folders):
    # flag if skipping repos
    completeFlag = True
    # list of skipped repos
    incompleteFolders = []


    for pos, folder in enumerate(folders):
        # ignore . directories
        # Change this if your git repos have '.' inside of them or start with '.'
        if '.' in folder:
            continue

        # change directory to inside the file
        insideFile = os.chdir(home + "/" + str(folder))
        # get the files inside the directory
        files = [y for y in os.listdir('.') if os.path.isfile(y)]

        # go through all of the files in the folder
        retVals = goThroughFiles(files, insideFile, folder, completeFlag, incompleteFolders)

        # get the complete flag and list of incomplete folders
        completeFlag = retVals[0]
        incompleteFolders = retVals[1]

    '''
    If adding the progress bar back in, uncomment this section
    This should update the progress bar for you
    '''
    # # sleep to watch progress bar actually do something
    # # if you want it to run faster, get rid of this sleep or the progress bar
    # time.sleep(0.1)
    #
    # #update the progress bar
    # bar.update(pos + 1)

    return(completeFlag, incompleteFolders)

'''
This will loop through all of the files for a given folder
Checks for .git to know if it is a repo or not
!!!
MUST HAVE .git file (.gitignore) to actually identify it as a github repo
!!!
Finds all of the untracked or changed files
'''
def goThroughFiles(files, insideFile, folder, completeFlag, incompleteFolders):
        # loop through the files
        for file in files:
            # if the files have a .git file they are a repository
            if ".git" in file:
                repo = Repo(insideFile)
                # check if anything is untracked or changed
                untracked = repo.untracked_files
                changedFiles = [repo.index.diff(None)]

                # if there are untracked or changed files
                if len(untracked) >= 1 or "<" in str(changedFiles[0]):
                    retVals = commitSteps(folder, untracked, changedFiles, repo, completeFlag, incompleteFolders)
                    completeFlag = retVals[0]
                    incompleteFolders = retVals[1]
        return (completeFlag, incompleteFolders)

'''
Used when have untracked or changed files to commit
Will print out the untracked or changed files
Gives option to add personal message, automated message, or skip committing anything
Will add all files to commit
'''
def commitSteps(folder, untracked, changedFiles, repo, completeFlag, incompleteFolders):
    print ("\n" + folder + " has untracked or changed files that will be committed.")

    if len(untracked) >= 1:
        print("Untracked Files:")
        for un in untracked:
            print ("\t" + un)
    if "<" in str(changedFiles[0]):
        print("Changed Files:")
        for ch in repo.index.diff(None):
            print ("\t" + ch.a_path)

    messageHelpFlag = True
    enterMessage = ""
    while(messageHelpFlag):
        # ask user if they want to add a commit message for the folder
        enterMessage = input("Would you like to add a custom commit message for: " + folder + "? \n")

        if ("y" in enterMessage or "sk" in enterMessage or "n" in enterMessage):
            messageHelpFlag = False
        else:
            print("\nEnter 'y' to add a custom commit message for: " + folder)
            print("Enter 'n' to have an automated message for your commit message for: " + folder)
            print("Enter 'sk' to skip committing for: " + folder + "\n")

    if("sk" in enterMessage or "SK" in enterMessage):
        completeFlag = False
        incompleteFolders.append(folder)
        print("Skipping commits for: " + folder + " \n")
        return (completeFlag, incompleteFolders)

    # add everything
    repo.git.add(A=True)
    index = repo.index

    commitMessage = ""

    # pull = input("Would you like to pull: " + folder + " before you commit? (yes(y)/no(n)) ")

    # if("y" in enterMessage or "Y" in enterMessage):
    pullReq = repo.remotes.origin
    pullReq.pull()
    print("\n" + folder + ": was pulled before commit\n")
    # enter a commit message if the user entered y
    # If they didnt, it will give an automatic message
    if("y" in enterMessage or "Y" in enterMessage):
        commitMessage = input("Enter your commit message: ")
    else:
        commitMessage = ("Automatic Update via updateGit.py")

    # Commit all of the untracked or changed files
    index.commit(commitMessage)

    # Push
    repo.git.push('origin')
    print (folder + " Updated.\n")
    return (completeFlag, incompleteFolders)




'''
Start of the program!

Need to add:
fix progressbar if want to use
add checkout option
add rm option

FIX:
stderr: 'fatal: unable to access 'https://github.com/w-aldrich/PersonalPythonScripts.git/': Could not resolve host: github.com'
// unable to access internet error system check
'''
main()
