import json
import os
import requests
import logging

user_auth = (os.environ.get("LC_user", '*'), os.environ.get("LC_pass", '*'))

base_url = os.environ.get("LC_base_url", '*')
rapidView = os.environ.get("LC_rapidView", '*')


def get_all_issues():
    issues = []
    url_template = "{}/rest/agile/latest/board/{}/issue?startAt={}&maxResults={}"
    maxResults = 50
    jira_result = {
        "startAt": 0,
        "maxResults": maxResults,
        "total": 51,
        "issues": [True] * maxResults
    }
    while jira_result["startAt"] + len(
            jira_result["issues"]) < jira_result["total"]:
        url = url_template.format(base_url, rapidView, jira_result["startAt"],
                                  jira_result["maxResults"])
        res = requests.get(url, auth=user_auth)
        if res.status_code == 200:
            jira_result = res.json()
            issues += jira_result["issues"]
        else:
            logging.error("requests problem: {}".format(res.status_code))

    no_assignee = []
    for i in issues:
        if not i["fields"]["assignee"] and i["fields"]["sprint"]:
            no_assignee.append({
                "k": i["key"],
                "p": i["fields"]["priority"]["name"],
                "sp": i["fields"]["sprint"]["name"],
                "s": i["fields"]["summary"],
                "d": i["fields"]["description"],
            })
    return no_assignee
