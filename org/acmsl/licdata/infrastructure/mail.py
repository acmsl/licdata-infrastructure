"""
org/acmsl/licdata/infrastructure/mail.py

This file provides some utilities for sending emails.

Copyright (C) 2023-today ACM S.L. Licdata-Infrastructure

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, Optional


def send_email(
    mailFrom: str,
    mailTo: str,
    subject: str,
    body: str,
    mimeType: str,
    smtpHost: str,
    smtpPort: str,
    smtpUsername: str,
    smtpPassword: str,
    smtpTimeout: str,
    bcc: Optional[str] = None,
) -> bool:
    """
    Sends an email.
    :param mailFrom: The source address.
    :type mailFrom: str
    :param mailTo: The destination address.
    :type mailTo: str
    :param subject: The subject of the email.
    :type subject: str
    :param body: The body of the email.
    :type body: str
    :param mimeType: The mime-type of the email.
    :type mimeType: str
    :param smtpHost: The SMTP host.
    :type smtpHost: str
    :param smtpPort: The SMTP port.
    :type smtpPort: str
    :param smtpUsername: The SMTP username.
    :type smtpUpsername: str
    :param smtpPassword: The password for the SMTP username.
    :type smtpPassword: str
    :param smtpTimeout: The timeout for SMTP connections.
    :type smtpTimeout: str
    :param bcc: The blind-copy address.
    :type bcc: str
    :return: True if the email is sent.
    :rtype: bool
    """
    try:
        rcpt = bcc.split(",") + [mailTo]
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["To"] = mailTo
        msg.attach(MIMEText(body, mimeType))
        try:
            server = smtplib.SMTP(smtpHost, smtpPort, smtpTimeout)
            server.ehlo()
            server.starttls()
            server.login(smtpUsername, smtpPassword)
            server.sendmail(mailFrom, rcpt, msg.as_string())
            server.quit()
            result = True
        except BaseException as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            result = False
        except:
            print("Unknown error")
            result = False

    except BaseException as err:
        print(type(err))
        print(err.args)
        print(err)
        result = False

    return result
