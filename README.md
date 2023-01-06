# pingTester
This script does a ping test on devices in the network and sends an email and Slack msg if one or more results get failed. It needs to run via Crontab or Task scheduler.

``python3 pingTester.py -u <email_username> -p <email_password> -s <email_server> -o <email_port> -f <email_from>``
