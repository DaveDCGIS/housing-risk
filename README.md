# housing-risk
Georgetown Data Science DC Low Income Housing “Risk Of Loss” Group Project

# Team Workflow Conventions (to be discussed at team meeting)
* Never commit to the Master branch (only use pull requests on Github)
* Always make a new branch for your work
* Never work on someone else's branch - instead, make a branch off of their branch, which they can merge in.
* Push your branches to Github often
* There are two 'team' branches:
  * Dev is a staging area for anything that mostly works, but might not be complete yet. This is where we can bring together work from multiple people. 
  * Master is the branch for clean, fully working code. When `dev` has been tested and is working properly, use a pull request to merge into `master`.
* Always resolve potential merge conflicts before creating a pull request:
  * Pull down the 'dev' branch. If there are no changes, you are good to go. If there are changes -
  * Option 1 (intermediate): first, merge the current `dev` branch *into* your branch. Check out your branch (`git checkout my-branch-name`), then do `git merge dev`. Resolve any merge conflicts, then create pull request on github to merge your branch into dev.
  * Option 2 (advanced): Instead of merging dev changes in, rebase your branch onto dev, squash your commits into one (or just a couple) commits, then issue pull request. This is cleaner, but harder to fix if you don't do it correctly. 


# Getting Set Up
First, clone the repository to wherever you want to save it on your local computer.

This project currently assumes you are using Anaconda for virtual environments. environment.yml contains the info needed to duplicate the environment.

* Navigate to the local repository folder in your command prompt
* `conda env create -f environment.yml` on the command line to create the new environment. 
* Wait while it installs packages
* type `conda info --envs` to see a list of all your environments - there should be a new one called housing-risk. Anaconda by default stores all environments in one location on your computer, so instead of saving it in the project folder it will be saved elsewhere, so it is named after the project (instead of the generic env name).
* `activate housing-risk` (windows) or `source activate housing-risk` (mac) to start your virtual environment
* Check install went ok:
  * `conda list` to see installed packages - you should have just a few, including pandas, numpy, etc.
  * `python --version` - should return 3.5.2

*Important notes:*
* Any time you are running the project, activate the environment first
* Any time you add a new package to the code(`import mypackage`), you'll need to install it in the environment and then re-export the environment.yml file. Use `conda env export > environment.yml`
* Any time you see that the environment.yml has been updated in git, you'll need to remove and rebuild the environment (or, manually install the new packages). Use `conda remove --name housing-risk` --all` and then `conda env create -f environment.yml` to rebuild. 


# Project layout
* */tests* - example unit tests are set up in the /tests folder. Should add tests often.
* */logging* - basic logging is set up. 
* */data* - we will store all our data sources here. Because our data is too big to store in Github, the contents of this folder are ignored by Git. Instead, we will use the AWS command line interface to sync this folder between each of our computers. Ashish is writing a tutorial. 
* */ingestion* - all code related to ingestion. Gets our data out of messy CSV and other formats and into a PostgreSQL database. Can be re-run whenever we get new data sources. 
* */prediction* - code for post-ingestion phase. Assumes that there is clean, verified data in a well structured PostgreSQL database. 
* *environment.yml* - for setting up the Anaconda virtual environment.
* *LICENSE* - basic MIT license, says anyone can copy and use the code for any reason, but they can't sue us.
* *README.md* - this file, summarizing project info and how to set up the project.
