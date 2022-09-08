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

## How to use development snapshot in ODK Ontology Repo

If you want to use the development snapshot with your `run.sh` docker wrapper, you will have to make sure that you use the development snapshot. 
Make sure your repo is up to date with the latest official release version by running `docker pull obolibrary/odkfull` and `sh run.sh make update_repo` _twice_.

Then: 

- If you are using ODK 1.3.1 run `IMAGE=obolibrary/odkfull:dev sh run.sh make update_repo` (or whatever other command you wanted to run).
- If you are using ODK 1.3.2 or later (or the `dev` image), run: `ODK_TAG=dev sh run.sh make update_repo` (or whatever other command you wanted to run).
