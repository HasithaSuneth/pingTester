import os
import sys
import getopt
import platform
import email.message
import smtplib

hostList = {"Device 01": "192.168.8.100",
            "Device 02": "192.168.8.101"}
numOfTests = "1"
to_name = "Receiver_Name"
to_email = "Receiver_Email"
cc_email = ['CC_email_1', 'CC_email_2']


def connectionTest(numOfTests, hostList):
    found_list = []
    for key, value in hostList.items():
        pingResult = ping(numOfTests, value)
        if not pingResult:
            found_list.append((key, value))
    return found_list


def ping(numOfTests, host):
    res = False
    ping_param = "-n " if platform.system().lower() == "windows" else "-c "
    ttl = "TTL=" if platform.system().lower() == "windows" else "ttl="
    resultado = os.popen("ping " + ping_param +
                         numOfTests + " " + host).read()
    if ttl in resultado:
        res = True
    return res


def email_send(name, email_addr, username, password, server, port, emailfrom, msg, cc_email):
    try:
        email_content = msg
        email_server = server + ": " + port
        msg = email.message.Message()
        msg['Subject'] = 'Warning! unreachable device/s detected'
        msg['From'] = emailfrom
        msg['To'] = email_addr
        msg['Cc'] = ', '.join(cc_email)
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(email_content)
        smtp = smtplib.SMTP(email_server)
        smtp.starttls()
        smtp.login(username, password)
        smtp.send_message(msg)
        print("email sent to: {} - {}".format(name, email_addr))
    except:
        print("Failed to send the email. Please check the email server credentials.")


def msg_create(result, to_name):
    msg = """ <h3>Hi {},</h3>
            The following device/s are unreachable at the moment. Please take the necessary actions.<br><br>
            Device List:<br>""".format(to_name)
    msg = msg + "<ul>"
    for i in result:
        msg = msg + "<li><b>{} ({})</b></li>".format(i[0], i[1])
    msg = msg + "</ul>"
    msg = msg + "<br><hr><i>This is an auto-generated email by pingTester.</i><hr>"
    return msg


def user_arg(argv):
    arg_emailuser = ""
    arg_emailpass = ""
    arg_emailserv = ""
    arg_emailport = ""
    arg_emailfrom = ""
    arg_help = "{0} -u <emailuser> -p <emailpass> -s <emailserv> -o <emailport> -f <emailfrom>".format(
        argv[0])

    try:
        opts, args = getopt.getopt(argv[1:], "hu:p:s:o:f:", [
                                   "help", "emailuser=", "emailpass=", "emailserv=", "emailport=", "emailfrom="])
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)
            sys.exit(2)
        elif opt in ("-u", "--emailuser"):
            arg_emailuser = arg
        elif opt in ("-p", "--emailpass"):
            arg_emailpass = arg
        elif opt in ("-s", "--emailserv"):
            arg_emailserv = arg
        elif opt in ("-o", "--emailport"):
            arg_emailport = arg
        elif opt in ("-f", "--emailfrom"):
            arg_emailfrom = arg

    return arg_emailuser, arg_emailpass, arg_emailserv, arg_emailport, arg_emailfrom


def main(to_name, to_email, cc_email, numOfTests, hostList):
    if __name__ == "__main__":
        emailuser, emailpass, emailserv, emailport, emailfrom = user_arg(
            sys.argv)
    result = connectionTest(numOfTests, hostList)
    if result != []:
        msg = msg_create(result, to_name)
        email_send(to_name, to_email, emailuser, emailpass,
                   emailserv, emailport, emailfrom, msg, cc_email)


main(to_name, to_email, cc_email, numOfTests, hostList)
