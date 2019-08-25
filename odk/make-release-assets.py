#!/usr/bin/env python3

"""
Requires: https://github.com/PyGithub/PyGithub

Command line wrapper to make github assets

No download (dry-run mode), just list assets:

    make-release-assets.py -k -r ontodev/robot -v v1.1.0

Release files

    make-release-assets.py -k -r foo/bar --release v2018-10-26 FILE1 FILE2 ... FILEn

"""

from github import Github
import os
import click
import logging
logging.basicConfig(level=logging.INFO)

@click.command()
@click.option("-k", "--dry-run/--no-dry-run", default=False)
@click.option("-f", "--force/--no-force", default=False)
@click.option("-c", "--create/--no-create", default=False)
@click.option("-t", "--token")
@click.option("-o", "--org")
@click.option("-r", "--repo", default="mondo")
@click.option("-v", "--release", default="v2018-08-24")
@click.argument("paths", nargs=-1)
def make_assets(dry_run, force, create, token, org, repo, release, paths):
    if '/' in repo:
        [org,repo] = repo.split('/')
    if org == None:
        org = 'monarch-initiative'
    logging.info('org={} repo={} rel={}'.format(org, repo, release))
    if token == None:
        with open('.token') as f:
            logging.info("Reading token from file")
            token = f.read().rstrip().lstrip()
    G = Github(token)
    G_org = G.get_organization(org)
    G_repo = G_org.get_repo(repo)

    if create:
        message = ""
        if release == 'current':
            message = "Running current release. This will be re-created with each release"
        for r in G_repo.get_releases():
            if r.tag_name == release:
                if force:
                    logging.info("Release already exists - will delete and re-create")
                    r.delete_release()
                else:
                    logging.error("Release already exists!")
                logging.info("Creating release")
        G_repo.create_git_release(release, release, message, draft=False, prerelease=False)
    
    G_rel = G_repo.get_release(release)

    existing_assets = {}
    print('Existing assets:')
    for a in G_rel.get_assets():
        print('Asset: {} Size: {} Downloads: {}'.format(a.name, a.size, a.download_count))
        existing_assets[a.name] = a

    if (dry_run):
        print("DRY RUN")
    else:
        for path in paths:
            bn = os.path.basename(path)
            logging.info("Testing if {} in {}".format(bn, existing_assets))
            if bn in existing_assets.keys():
                a = existing_assets[bn]
                if force:
                    logging.info("{} already exists; will replace".format(path))
                    a.delete_asset()
                else:
                    logging.error("{} already exists".format(path))
                    # TODO: if asset already exists, skip; add a --force option to explicitly overwrite
                
            print('Uploading: {}'.format(path))
            a = G_rel.upload_asset(path=path)
            print('Uploaded: {} {} from {}'.format(a.name, a.size, path))

    
if __name__ == "__main__":
    make_assets()
