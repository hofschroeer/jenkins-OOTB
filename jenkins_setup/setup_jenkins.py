#!python

import jenkins
import docker
import pprint
import sys

from jenkins_plugins_list import plugins

pp = pprint.PrettyPrinter(indent=3)

# basic params
jenkins_server_url = 'http://localhost:8080'
jenkins_init_user = 'admin'
jenkins_master_name = 'jenkins_master'
jenkins_secret_path = '/var/jenkins_home/secrets/initialAdminPassword'

# get jenkins_master docker container to work with
client = docker.from_env()
jenkins_master = client.containers.get(jenkins_master_name)

# get initial adminpassword from container
jenkins_init_pw = jenkins_master.exec_run('cat %s' % jenkins_secret_path).strip('\n')

# retrieve server instance
jenkins_server = jenkins.Jenkins(jenkins_server_url,
    username=jenkins_init_user,
    password=jenkins_init_pw)

# print jenkins server info
#pp.pprint(jenkins_server.get_info())

# install plugins
restart_needed = False
print 'Installing plugins starting: ' + str(plugins)
for p in plugins:
	restart_needed = jenkins_server.install_plugin(p)
print 'Plugins requested. Wait for install to complete.'
