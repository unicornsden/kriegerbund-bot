from github import Github
from github import GithubObject
from . import messages
from .messages import MessageCode
from . import data


def dev_help(message):
    messages.send_message(message, 'dev-help')


def dev_issue(message, split, label):
    content = message.content.split(split, 1)[1].strip()

    description = ''

    if content[0] == '\"':
        splits = content[1:].split('\"', 1)
    else:
        splits = content.split(' ', 1)

    name = splits[0]
    if len(splits) > 1:
        description = splits[1]

    description = '[Issue created by {user}]\n'.format(user=message.author.name) + description
    make_github_issue(name, description, [label, 'status: pending'])
    messages.send_message(message, 'dev-issue-created')


def cmd_dev(message, args):
    if len(args) == 0:
        return MessageCode.UNKNOWN_ARGS
    if args[0] == 'help':
        return dev_help(message)
    if len(args) < 2:
        return MessageCode.UNKNOWN_ARGS
    if args[0] == 'request':
        return dev_issue(message, args[0], 'type: enhancement')
    if args[0] == 'bugreport':
        return dev_issue(message, args[0], 'type: bug')
    return MessageCode.UNKNOWN_ARGS


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
