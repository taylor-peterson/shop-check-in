import smtplib
import os
import shop_user
from shop_user_database import PATH_LOGIN_INFO

EMAIL_TEMPLATE = """From: From Person <%s>
To: To Person <%s>
MIME-Version: 1.0
Content-type: text/html
Subject: %s

%s
"""

EMAIL_BODY_TEMPLATE = """Dear %s,<br /><br />
<p>We have received indication that you did not check out
with the proctor last time you left the shop. It is important
to check out properly so that the proctor knows who in in the
shop at all times.</p>
<br />
<br />
Best Wishes,
<br />
Shop Management"""

EMAIL_SUBJECT = "ID Removed from shop without checkout"


class Mailer(object):

    def __init__(self):
        login_info = self._get_login_info()
        self._username = login_info["GOOGLE_USERNAME"]
        self._password = login_info["GOOGLE_PASSWORD"]

    @staticmethod
    def _get_login_info():
        Mailer._correct_current_working_directory()
        with open(PATH_LOGIN_INFO, "r") as login_info:
            return dict([line.split() for line in login_info])

    def _send_id_card_email_s(self, user_s):
        for user in user_s:
            self._send_id_card_email(user)

    def _send_id_card_email(self, user):
        print "Sending mail to %s at %s" % (user.name, user.email)
        message = self._make_id_card_email(user)
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        try:
            server.login(self._username, self._password)
        except:
            print "Could not login to the python server!"
        else:
            try:
                server.sendmail(self._username, user.email, message)
                server.quit()
            except:
                print "Could not send mmail to the the address %s" % user.email

    def _make_id_card_email(self, user):
        body =  EMAIL_BODY_TEMPLATE % (user.name)
        return self._populated_template(self._username,
                                        user.email,
                                        EMAIL_SUBJECT,
                                        body)

    @staticmethod
    def _correct_current_working_directory():
        absolute_path = os.path.abspath(__file__)
        directory_name = os.path.dirname(absolute_path)
        os.chdir(directory_name)

    @staticmethod
    def _populated_template(from_address, to_address, subject, body):
        return EMAIL_TEMPLATE % (from_address, to_address, subject, body)

