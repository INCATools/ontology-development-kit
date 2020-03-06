**NOTE** This documentation is incomplete, for now you may be better consulting the [http://wiki.geneontology.org/index.php/Protege_setup_for_GO_Eds](GO Editor Docs]

# Configuration

## Configuring New Entities Metadata

1. In the Protege menu, select Preferences.

2. Click on: Annotate new entities with creator (user) 

3. Creator property: Add [http://www.geneontology.org/formats/oboInOwl#created_by](http://geneontology.org/formats/oboInOwl#created_by)

4. Creator value: Use user name
      
5. Check: Annotate new entities with creation date and time.

6. Date property: Add [http://www.geneontology.org/formats/oboInOwl#creation_date](http://geneontology.org/formats/oboInOwl#creation_date)

7. Check: ISO-8601


## Configuring User details

Select 'User name', and use the supplied user name; that is, your GOC identity.

#### Identifying the user for commits 

Git needs to know who is committing changes to the repository, so the first time you commit, you may see the following message: 

	   Committer: Kimberly Van Auken <vanauken@kimberlukensmbp.dhcp.lbnl.us>
         Your name and email address were configured automatically based on your username and hostname. Please check that they are accurate.
 
You can suppress this message by setting your name and email explicitly:

1. Type ```git config --global user.name "Your Name"```

2. Type ```git config --global user.email you@example.com```. 

3. You can then fix the identity used for this commit by typing: ```git commit --amend --reset-author```.
