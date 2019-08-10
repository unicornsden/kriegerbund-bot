from github import Github
from github import GithubObject
from . import data

# Authentication for user filing issue (must have read/write access to
# repository to add issue to)



def label_exists(repo, label):
    labels = repo.get_labels()
    for l in labels:
        if label == l.name:
            return True
    return False


def make_github_issue(title, body, labels=None):
    token = open(data.DATAPATH + 'tokens/' + 'github-token', 'r').read().strip()
    g = Github(token)
    for repo in g.get_user().get_repos():
        print(repo.name)
    repo = g.get_repo('%s/%s' % (data.REPO_OWNER, data.REPO_NAME))

    label_list = list()

    if isinstance(labels, str):
        if label_exists(repo, labels):
            label_list.append(repo.get_label(labels))
    elif labels is not None:
        for l in labels:
            if label_exists(repo, l):
                label_list.append(repo.get_label(l))

    if body is None:
        body = GithubObject.NotSet

    if len(label_list) == 0:
        label_list = GithubObject.NotSet

    repo.create_issue(title, body=body, labels=label_list)
    return
