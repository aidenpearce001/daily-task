from jira import JIRA
from github import Github
import os

def get_all_assigned_issues():
    # Jira setup
    jira = JIRA(
        server='https://jira.yitec.group/',
        basic_auth=(os.getenv('JIRA_USERNAME'),os.getenv('JIRA_PASSWD'))
    )

    # GitHub setup
    g = Github(os.getenv('GITHUB_TOKEN'))

    repo = g.get_repo('aidenpearce001/daily-task')

    jql = 'assignee = currentUser() AND status="To Do"'
    issues = jira.search_issues(jql)

    for issue in issues:
        issue_title = f"[{issue.key}] {issue.fields.summary}"
        found = False

        # Check if the issue is already created in Github
        for git_issue in repo.get_issues(state='open'):
            if git_issue.title == issue_title:
                found = True
                break

        if not found:
            # Create a new issue if not found in Github
            repo.create_issue(
                title=issue_title,
                body=str(issue.fields.description)
            )

if __name__ == "__main__":
    get_all_assigned_issues()