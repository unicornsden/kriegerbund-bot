from github import Github
from github import GithubObject
from . import messages
from . import data


def dev_issue(message, split, label):
    """
    create a new issue
    :param message: MessageWrapper for formatting & data
    :param split: where to split the message content to get the issue content
    :param label: the label to apply, TODO: SUPPORT MORE THAN ONE
    :return: messages.send_message() result
    """
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
    return messages.send_message(message, 'dev-issue-created')


def cmd_dev(message, args):
    """
    cmd switch for dev
    :param message: MessageWrapper for formatting & data
    :param args: list of arguments after the command
    :return: MessageCode result of dev actions
    """
    if len(args) == 0:
        return messages.MessageCode.UNKNOWN_ARGS
    if args[0] == 'help':
        return messages.send_message(message, 'dev-help')
    if len(args) < 2:
        return messages.MessageCode.UNKNOWN_ARGS
    if args[0] == 'request':
        return dev_issue(message, args[0], 'type: enhancement')
    if args[0] == 'bugreport':
        return dev_issue(message, args[0], 'type: bug')
    return messages.MessageCode.UNKNOWN_ARGS


def label_exists(repo, label):
    """
    checks if a label exists in a repository's issue system
    :param repo: github.Repository - must be authenticated
    :param label: the label name to check
    :return: True if the label exists, False otherwise
    """
    labels = repo.get_labels()
    for l in labels:
        if label == l.name:
            return True
    return False


def make_github_issue(title, body, labels=None):
    """
    create a github issue in github.com/data.REPO_OWNER/data.REPO_NAME / TODO: MAKE REPO OWNER AND NAME ARGS
    :param title: Issue title
    :param body: Issue description
    :param labels: Issue labels
    :return: Nothing / TODO: RETURN FAILURE / SUCCESS
    """
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
