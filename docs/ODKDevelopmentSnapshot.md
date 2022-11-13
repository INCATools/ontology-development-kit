# Using the ODK Development Snapshot

ODK is constantly being updated, but we release new versions only once every 3-4 months. 
For people with a nack to beta-testing and experimental features, or those which need to use the latest versions of the bundled tools,
we provide a "development" snapshot of the ODK which is updated roughly once per week:

Look for `dev` tag in https://hub.docker.com/r/obolibrary/odkfull/tags

You can install the development snapshot like this:

```
docker pull obolibrary/odkfull:dev
```

**Important:**

1. The `dev` snapshot of ODK _is unstable_, and therefore will have bugs. _You use it at your own risk_!
2. You cannot rely on any of the features in the development snapshot to make it into production (at least not with more than 85% confidence).

## How to install and use development snapshot in ODK Ontology Repo

If you want to use the development snapshot with your `run.sh` docker wrapper, you will have to make sure that have enabled it correctly. 

1. `docker pull obolibrary/odkfull:dev` As mentioned above, this command installs the development snapshot
1. `docker pull obolibrary/odkfull`
1. Make sure your repo is up to date with the latest official release version (at least 1.3.1)
1. If currently using 1.3.1: `IMAGE=odkfull:dev sh run.sh make update_repo`, else `ODK_TAG=dev sh run.sh make update_repo`
1. `ODK_TAG=dev sh run.sh make update_repo` (again, if you ran it above)

You have now set your repo up to run via the development snapshot. At the top of the file, in the comments, your automatically-generated src/ontology/Makefile should now reference the development snapshot you have installed rather than the stable production release.

**Finally:**

5. You can now run any command via the `run.sh` docker wrapper. Just make sure you use the appropriate prefix depending on your version of the ODK:
- If you are using ODK 1.3.1 run `IMAGE=obolibrary/odkfull:dev sh run.sh make update_repo` (or whatever other command you wanted to run).
- If you are using ODK 1.3.2 or later (or the `dev` image), run: `ODK_TAG=dev sh run.sh make update_repo` (or whatever other command you wanted to run).
