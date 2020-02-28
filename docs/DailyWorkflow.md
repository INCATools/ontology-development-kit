**NOTE** This documentation is incomplete, for now you may be better consulting the [http://wiki.geneontology.org/index.php/Ontology_Editing_Guide](GO Editor Docs]

# Daily Workflow

## Updating the local copy of the ontology with 'git pull'

1. Navigate to the ontology directory of go-ontology:  ```cd repos/MY-ONTOLOGY/src/ontology```.

2. If the terminal window is not configured to display the branch name, type: ```git status```. You will see: 
    
       On branch [master] [or the name of the branch you are on]
       Your branch is up-to-date with 'origin/master'.

3. If you’re not in the master branch, type: ```git checkout master```.

4. From the master branch, type: ```git pull```. This will update your master branch, and all working branches, with the files that are most current on GitHub, bringing in and merging any changes that were made since you last pulled the repository using the command ```git pull```. You will see something like this:

```
~/repos/MY-ONTOLOGY(master) $ git pull
remote: Counting objects: 26, done.
remote: Compressing objects: 100% (26/26), done.
remote: Total 26 (delta 12), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (26/26), done.
From https://github.com/geneontology/go-ontology
   580c01d..7225e89  master 	-> origin/master
 * [new branch]  	issue#13029 -> origin/issue#13029
Updating 580c01d..7225e89
Fast-forward
 src/ontology/go-edit.obo | 39 ++++++++++++++++++++++++---------------
 1 file changed, 24 insertions(+), 15 deletions(-)
~/repos/MY-ONTOLOGY(master) $
```

## Creating a New Working Branch with 'git checkout'

1. When starting to work on a ticket, you should create a new branch of the repository to edit the ontology file.

2. **Make sure you are on the master branch before creating a new branch**. If the terminal window is not configured to display the branch name, type: ```git status``` to check which is the active branch. If necessary, go to master by typing ```git checkout master```.  

3. To create a new branch, type:  ```git checkout -b issue-NNNNN``` in the terminal window. For **naming branches**, we recommend using the string 'issue-' followed by the issue number. For instance, for this issue in the tracker: https://github.com/geneontology/go-ontology/issues/13390, you would create this branch: ```git checkout -b issue-13390```. Typing this command will automatically put you in the new branch. You will see this message in your terminal window: 

      ```
      ~/repos/MY-ONTOLOGY/src/ontology(master) $ git checkout -b issue-13390
      Switched to a new branch 'issue-13390'
      ~/repos/MY-ONTOLOGY/src/ontology(issue-13390) $
      ```


## Continuing work on an existing Working Branch 
1. If you are continuing to do work on an existing branch, in addition to updating master, go to your branch by typing ```git checkout [branch name]```. Note that you can view the existing local branches by typing ```git branch -l```.

2. **OPTIONAL**: To update the working branch with respect to the current version of the ontology, type ```git pull origin master ```.
This step is optional because it is not necessary to work on the current version of the ontology; all changes will be synchronized when git merge is performed.

## Loading, navigating and saving the Ontology in Protégé 

1. Before launching Protégé, make sure you are in the correct branch. To check the active branch, type ```git status```.  

2. Click on the 'File' pulldown. Open the file: go-edit.obo. The first time, you will have to navigate to ```repos/MY-ONTOLOGY/src/ontology```. Once you have worked on the file, it will show up in the menu under 'Open'/'Recent'.

3. Click on the 'Classes' tab.

4. Searching: Use the search box on the upper right to search for a term in the ontology. Wait for autocomplete to work in the pop-up window.

5. Viewing a term: Double-click on the term. This will reveal the term in the 'Class hierarchy' window after a few seconds.

6. Launching the reasoner: To see the term in the 'Class hierarchy' (inferred) window, you will need to run the 'ELK reasoner'. 'Reasoner' > select ELK 0.4.3, then click 'Start reasoner'. Close the various pop-up warnings about the ELK reasoner. You will now see the terms in the inferred hierarchy.

7. After modification of the ontology, synchronize the reasoner. Go to menu: 'Reasoner' > ' Synchronize reasoner'. 
   - **NOTE**: The only changes that the reasoner will detect are those impacting the ontology structure: changes in equivalence axioms, subclasses, merges, obsoletions, new terms. 
   - **TIP**: When adding new relations/axioms, 'Synchronize' the reasoner. When deleting relations/axioms, it is more reliable to 'Stop' and 'Start' the reasoner again. 

8. Use File > Save to save your changes. 

<a name="commmit"></a>
## Committing, pushing and merging your changes to the repository
 
1. **Review**: Changes made to the ontology can be viewed by typing ```git diff``` in the terminal window. If there are changes that have already been committed, the changes in the active branch relative to master can be viewed by typing  ```git diff master```. 

2. **Commit**: Changes can be committed by typing: ```git commit -m ‘Meaningful message Fixes #ticketnumber’ go-edit.obo```. 

      For example: 
      
          git commit -m ‘hepatic stellate cell migration and contraction and regulation terms. Fixes #13390’ go-edit.obo 
	
	This will save the changes to the go-edit.obo file. The terminal window will show something like: 

        ~/repos/MY-ONTOLOGY/src/ontology(issue-13390) $ git commit -m 'Added hepatic stellate cell migration and contraction and regulation terms. Fixes #13390' go-edit.obo
        [issue-13390 dec9df0] Added hepatic stellate cell migration and contraction and regulation terms. Fixes #13390
        1 file changed, 79 insertions(+)
        ~/repos/MY-ONTOLOGY/src/ontology(issue-13390) $

   - **NOTE**: The word 'fixes' is a magic word in GitHub; when used in combination with the ticket number, it will automatically close the ticket. In the above example, when the file is merged in GitHub, it will close issue number 13390. Learn more on this [GitHub Help Documentation page about 'Closing issues via commit messages'](https://help.github.com/articles/closing-issues-via-commit-messages/).
   - 'Fixes' is case-insensitive. 
   - If you don't want to close the ticket, just refer to the ticket # without the word 'Fixes'. The commit will be associated with the correct ticket but the ticket will remain open. 
    - **NOTE**: It is also possible to type a longer message than allowed when using the '-m' argument; to do this, skip the -m, and a vi window (on mac) will open in which an unlimited description may be typed. 
   - **TIP**: Git needs to know who is committing changes to the repository, so the first time you commit, you may see the following message: 

	     Committer: Kimberly Van Auken <vanauken@kimberlukensmbp.dhcp.lbnl.us>
            Your name and email address were configured automatically based on your username and hostname. Please check that they are accurate.
   - See [Configuration instructions](http://ontology-development-kit.readthedocs.io/en/latest/index.html#configuration) to specify your name and email address. 

3. **Push**: To incorporate the changes into the remote repository, type: ```git push origin mynewbranch```. 

      Example: 
       
        git push origin issue-13390 
	
   - **TIP**: Once you have pushed your changes to the repository, they are available for everyone to see, so at this stage you can ask for feedback.    
   
4. **Pull** 
   1. In your browser, return to the [GO Ontology repository](https://github.com/geneontology/go-ontology) on GitHub.
   2. Navigate to the tab labeled as 'Code' ```geneontology/go-ontology/code```. You will see your commit listed at the top of the page in a light yellow box. If you don’t see it, click on the 'Branches' link to reveal it in the list, and click on it. 
   3. Click the green button 'Compare & pull request' on the right.
   4. You may now add comments and ask a colleague to review your pull request. If you want to have the ticket reviewed before closing it, you can select a reviewer for the ticket before you make the pull request by clicking on the 'Reviewers' list and entering a GitHub identifier (e.g. @superuser1). The reviewer will be notified when the pull request is submitted.  Since the Pull Request is also a GitHub issue, the reviewer’s comments will show up in the dialog tab of the pull request, similarly to any other issue filed on the tracker.
   5. The diff for your file is at the bottom of the page. Examine it as a sanity check. 
   6. Click on the green box 'Pull request' to generate a pull request.   
   7. Wait for the Travis checks to complete (this can take a few minutes). If the Travis checks failed, go back to your working copy and correct the reported errrors.   
   
5. **Merge** If the Travis checks are succesful and **if you are done working on that branch**, merge the pull request. Confirming the merge will close the ticket if you have used the word 'fixes' in your commit comment. 
 **NOTE**: Merge the branches only when the work is completed. If there is related work to be done as a follow up to the original request, create a new GitHub ticket and start the process from the beginning. 
 
6. **Delete** your branch on the repository using the button on the right of the successful merge message. 

7. You may also delete the working branch on your local copy. Note that this step is optional.  However, if you wish to delete branches on your local machine, in your terminal window: 
   1. Go back to the master branch by typing ```git checkout master```.     
   2. Update your local copy of the repository by typing  ```git pull origin master``` 
   3. Delete the branch by typing ```git branch -d workingbranchname```. 
      Example:   ```git branch -d issue-13390```

