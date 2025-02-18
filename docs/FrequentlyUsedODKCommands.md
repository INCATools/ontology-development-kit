# Frequently used ODK commands

## Updates the Makefile to the latest ODK

```
sh run.sh update_repo 
```

## Recreates and deploys the automated documentation

```
sh run.sh make update_docs
```

## Preparing a new release

```
sh run.sh make prepare_release
```

## Refreshing a single import

```
sh run.sh make refresh-%
```

Example:

```
sh run.sh make refresh-chebi
```

## Refresh all imports

```
sh run.sh make refresh-imports 
```

## Refresh all imports excluding large ones

```
sh run.sh make refresh-imports-excluding-large
```

## Run all the QC checks

```
sh run.sh make test
```

## Print the version of the currently installed ODK

```
sh run.sh make odkversion
```

## Checks the OWL2 DL profile validity

(of a specific file)

```
sh run.sh make validate_profile_% 
```
Example:

```
sh run.sh make validate_profile_hp-edit.owl
```
