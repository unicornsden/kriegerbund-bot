from github import Github
import subprocess
import docker
import time

class DeployControl:

    def __init__(self, owner, name):
        print('Setting up automatic repo build for {0}/{1}'.format(owner, name))
        self.owner = owner
        self.name = name
        with open('github-token', 'r') as t:
            token = t.read().strip()
        g = Github(token)
        repo_name = owner + '/' + name
        self.repo = g.get_repo(repo_name)
        self.docker_client = docker.from_env()
        self.branches = dict()
        self.branches['dev'] = self.repo.get_branch(branch='dev').commit.sha.strip()
        self.branches['master'] = self.repo.get_branch(branch='master').commit.sha.strip()

    def check(self, branch):
        container_list = self.docker_client.containers.list(filters={'name':self.name + '-' + branch})
        if len(container_list) == 0:
            return False
        container = container_list[0]
        version = container.labels['deploy.version'].strip()
        if version != self.branches[branch]:
            return False
        return True

    def safe_get(self, container_name):
        container_list = self.docker_client.containers.list(all=True,filters={'name':container_name})
        if len(container_list) == 0:
            return False
        return container_list[0]
        

    def restart(self, branch):
        image = self.name + '-' + branch
        print('Stopping old {0} ...'.format(image))
        container = self.safe_get(image)
        if container:
            container.stop()
            container.remove()
        print('Building {0} ...'.format(image))
        print(self.docker_client.images.build(path=('./' + image), tag=image, labels={'deploy.version':self.branches[branch]}))
        print('Running {0} ...'.format(image))
        print(self.docker_client.containers.run(image + ':latest', volumes={image: {'bind': '/storage', 'mode': 'rw'}},name=image, detach=True))

    def deploy_control(self):
        while True:
            time.sleep(10)
            container_failed = False
            print('Checking containers ...')
            for b, v in self.branches.items():
                self.branches[b] = self.repo.get_branch(branch=b).commit.sha.strip()
                if not self.check(b):
                    container_failed = True
                    self.restart(b)

controller = DeployControl('unicornsden', 'pixie')
controller.deploy_control()
