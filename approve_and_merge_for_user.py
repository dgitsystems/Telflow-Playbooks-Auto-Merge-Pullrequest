#!/usr/bin/env python
# -*- encoding: utf-8

import json
import os
import sys

import requests


def neutral_exit():
    # In the early versions of GitHub Actions, you could use exit code 78 to
    # mark a run as "neutral".
    #
    # This got removed in later versions because it's not ambiguous.
    # https://twitter.com/zeitgeistse/status/1163444737057132547
    #
    # (Can I say "I told you so"?)
    #
    sys.exit(0)


def get_session(github_token):
    sess = requests.Session()
    sess.headers = {
        "Accept": "; ".join([
            "application/vnd.github.v3+json",
            "application/vnd.github.antiope-preview+json",
        ]),
        "Authorization": f"token {github_token}",
        "User-Agent": f"GitHub Actions script in {__file__}"
    }

    def raise_for_status(resp, *args, **kwargs):
        try:
            resp.raise_for_status()
        except Exception:
            print(resp.text)
            sys.exit("Error: Invalid repo, token or network issue!")

    sess.hooks["response"].append(raise_for_status)
    return sess

def get_session_personal(github_token):
    sess = requests.Session()
    sess.headers = {
        "Accept": "; ".join([
            "application/vnd.github.v3+json",
            "application/vnd.github.antiope-preview+json",
        ]),
        "Authorization": f"token {github_token}",
        "User-Agent": f"GitHub Actions script in {__file__}"
    }

    def raise_for_status(resp, *args, **kwargs):
        try:
            resp.raise_for_status()
        except Exception:
            print(resp.text)
            sys.exit("Error: Invalid personal, token or network issue!")

    sess.hooks["response"].append(raise_for_status)
    return sess


if __name__ == '__main__':
    #Set env to variables 
    github_token = os.environ["INPUT_GITHUB_TOKEN"]
    github_repository = os.environ["GITHUB_REPOSITORY"]
    github_pr_author = os.environ["INPUT_GITHUB_PR_AUTHOR"]
    github_personal_token = os.environ["INPUT_GITHUB_PERSONAL_TOKEN"]

    #event path that contains webhook like informaton
    github_event_path = os.environ["GITHUB_EVENT_PATH"]

    #load event data
    event_data = json.load(open(github_event_path))

    check_run = event_data["check_run"]
    name = check_run["name"]

    sess = get_session(github_token)
    sess_personal = get_session_personal(github_personal_token)


    pull_request = check_run["pull_requests"][0]
    pr_number = pull_request["number"]
    pr_src = pull_request["head"]["ref"]
    pr_dst = pull_request["base"]["ref"]

    print(f"*** Checking pull request #{pr_number}: {pr_src} ~> {pr_dst}")
    pr_data = sess.get(pull_request["url"]).json()


    #lets check who created the PR 
    pr_user = pr_data["user"]["login"]
    print(f"*** This PR was opened by {pr_user}")
    if pr_user != github_pr_author:
        print("*** This PR was opened by somebody who isn't {github_pr_author} !")
        

        #add a review to the pull request saying it shouldnt exist
        review_url = pull_request["url"] + "/reviews"
        review_json = {"body": "Stable branches do not accept pull requests other then from jenkins.", "event": "COMMENT"}
        review_response = sess.post(review_url,json=review_json);

        if review_response.status_code == 200:
            print ('Review post made succesfully.')
        else:
            print ('Review post error')
            sys.exit(1)

        neutral_exit()

    #this needs to be done under the personal token not the repo one so it works
    print("*** This PR is ready to be merged.")
    merge_url = pull_request["url"] + "/merge"
    sess_personal.put(merge_url)
