"""
org/acmsl/licdata/infrastructure/licenses/aws_lambda/post.py

This file provides an AWS Lambda handler to create a license as well as associated entities.

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

from org.acmsl.licdata.domain import ClientRepo, LicenseRepo, PcRepo
import org.acmsl.licdata.infrastructure.params
import org.acmsl.licdata.infrastructure.mail
import org.acmsl.licdata.infrastructure.resp
from pythoneda.shared import Ports

import base64
import json
from github import Github
import os


def handler(event, context):
    """
    AWS Lambda handler to create a new license as well as associated entities.
    :param event: The AWS Lambda event.
    :type event: event
    :param context: The AWS Lambda context.
    :type context: context
    :return: The response.
    :rtype: Dict
    """
    headers = event.get("headers", {})
    host = headers.get("host", event.get("host", ""))

    status = 200
    file = None

    (body, error) = params.loadBody(event)
    if error:
        status = 500
        respBody = {"error": "Cannot parse body"}
    else:
        email = params.retrieveEmail(body, event)
        productName = params.retrieveProduct(body, event)
        productVersion = params.retrieveProductVersion(body, event)
        installationCode = params.retrieveInstallationCode(body, event)
        description = params.retrieveDescription(body, event)

        client = Ports.instance().resolve_first(ClientRepo).findByEmail(email)
        if client:
            clientId = client["id"]
        else:
            clientId = clientrepo.insert(email)
            print(f"Inserted new client {email} -> {clientId}")

            licenseRepo = Ports.instance().resolve_first(LicenseRepo)
            license = licenseRepo.findByClientIdAndInstallationCode(
                clientId, installationCode
            )
            if license:
                licenseId = license["id"]
                licenseData = json.dumps(license, indent=4, sort_keys=True, default=str)
                respBody = license
            else:
                licenseId = licenseRepo.insert(clientId, productName, productVersion)
                print(f"Inserted new license for client {clientId} -> {licenseId}")
                if licenseId:
                    status = 201
                    respBody = {
                        "id": licenseId,
                        "clientId": clientId,
                        "product": productName,
                        "version": productVersion,
                        "installationCode": installationCode,
                    }
                else:
                    status = 500
                    respBody = {
                        "error": "Error creating license",
                        "clientId": clientId,
                        "product": productName,
                        "version": productVersion,
                        "installationCode": installationCode,
                    }

    if licenseId:
        pcRepo = Ports.instance().resolve_first(PcRepo)
        pc = pcRepo.findByInstallationCode(installationCode)
        if pc:
            if not licenseId in pc["licenses"]:
                pcId = pc["id"]
                pcRepo.addLicense(pc["id"], licenseId)
                print(f"Added license {licenseId} to {pcId}")
            else:
                pcId = pcRepo.insert([licenseId], installationCode, description)
                print(f"Inserted new pc for license {licenseId} -> {pcId}")
        else:
            pcId = pcRepo.insert([licenseId], installationCode, description)
            print(f"Inserted new pc for license {licenseId} -> {pcId}")

        response["headers"].update({"Location": f"https://{host}/licenses/{licenseId}"})

        if status == 201:
            try:
                mail.send_email(
                    os.environ["MAIL_FROM"],
                    os.environ["MAIL_TO"],
                    f"New license: {licenseId}",
                    f"""<html>
<body>
    <h1>New license: {licenseId}</h1>
    <ul>
      <li>license: {licenseId}</li>
      <li>email: {email}</li>
      <li>product: {productName}</li>
      <li>version: {productVersion}</li>
      <li>installationCode: {installationCode}</li>
    </ul>
  </body>
</html>
""",
                    "html",
                    os.environ["AWS_SES_SMTP_HOST"],
                    os.environ["AWS_SES_SMTP_PORT"],
                    os.environ["AWS_SES_SMTP_USERNAME"],
                    os.environ["AWS_SES_SMTP_PASSWORD"],
                    os.environ["AWS_SES_SMTP_TIMEOUT"],
                    os.environ["MAIL_BCC"],
                )
            except:
                print(f"Error sending new-license email")

    return buildResponse(status, respBody, event, context)
