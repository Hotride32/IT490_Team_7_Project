import os
cmd = 'sudo service rabbitmq-server start'
os.system(cmd)
cmd = 'sudo service rabbitmq-server status'
os.system(cmd)
