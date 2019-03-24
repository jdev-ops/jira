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
        url = url_template.format(
            base_url, rapidView,
            jira_result["startAt"] + len(jira_result["issues"]),
            jira_result["maxResults"])
        res = requests.get(url, auth=user_auth)
        if res.status_code == 200:
            jira_result = res.json()
            issues += jira_result["issues"]
        else:
            logging.error("requests problem: {}".format(res.status_code))

    no_assignee = {}
    index = 1
    for issue in issues:
        if not issue["fields"]["assignee"] and issue["fields"]["sprint"]:
            no_assignee[index] = {
                "k": issue["key"],
                "pn": issue["fields"]["priority"]["name"],
                "sn": issue["fields"]["sprint"]["name"],
                "s": issue["fields"]["summary"],
                "d": issue["fields"]["description"],
            }
            index += 1
    return no_assignee
