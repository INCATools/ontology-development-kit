**NOTE** This documentation is incomplete, for now you may be better consulting the [http://wiki.geneontology.org/index.php/Installing_and_Using_git](GO Editor Docs]

# Installing and Using git

## Installing git

1. In order to locally edit the ontology and push changes back to the GitHub repository, you will need to have git installed on your machine.

2. To check if you already have git installed, or to see what version of git you have, type either of these commands in your terminal: 
```which git``` or ```git --version```.
 
3. To install git, follow  instructions here: [https://git-scm.com/](https://git-scm.com/)
  
 __Note for MacOSX users:__ it is advised to install Xcode tools.


## Cloning the go-ontology repository from GitHub

1. Create a directory called ```repos``` on your local machine using this command: ```mkdir repos```.

2. Then paste this command into your terminal: ```git clone https://github.com/geneontology/go-ontology.git```.
       
    Example result:

       Cloning into 'go-ontology'...
       remote: Counting objects: 2541, done.
       remote: Compressing objects: 100% (100/100), done.
       remote: Total 2541 (delta 52), reused 0 (delta 0), pack-reused 2440
       Receiving objects: 100% (2541/2541), 21.19 MiB | 5.22 MiB/s, done.
       Resolving deltas: 100% (1532/1532), done.


## Editing the .profile (or .bashrc) file to indicate the branch you are working on

It can be very helpful to know what branch you are working in on your terminal window. You can set this up to display by adding the following information to your .profile file (found by typing ls -a):

       export GO_REPO=~/repos/MY-ONTOLOGY
       . $GO_REPO/src/util/git-completion.bash
       parse_git_branch() {
           git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
       }
       PS1="\w\$(parse_git_branch) $ "
       export PATH=$PATH:$HOME/bin/
 
 Note the last line is not relevant to git, but we do this now for later on when we want to run tools like robot.



