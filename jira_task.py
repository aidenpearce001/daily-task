from jira import JIRA
from github import Github
import os

def get_all_assigned_issues():
    # Jira setup
    jira = JIRA(
        server='https://jira.yitec.group/',
        basic_auth=("nam.tran", "123@123a")
    )

    # GitHub setup
    g = Github("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")

    repo = g.get_repo('aidenpearce001/daily-task')

    jql = 'assignee = currentUser() AND status="To Do"'
    issues = jira.search_issues(jql)
    # print(issues)

    for issue in issues:
        found = False

        # Check if the issue is already created in Github
        for git_issue in repo.get_issues(state='open'):
            if git_issue.title == issue.fields.summary:
                found = True
                break

        if not found:
            # Create a new issue if not found in Github
            repo.create_issue(
                title=f"[{issue.key}] {issue.fields.summary}",
                body=str(issue.fields.description)
            )

if __name__ == "__main__":
    get_all_assigned_issues()