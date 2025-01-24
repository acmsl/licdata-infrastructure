"""
org/acmsl/licdata/infrastructure/licenses/aws_lambda/isValid.py

This file provides an AWS Lambda handler to check if a license is valid.

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

from org.acmsl.licdata import IncidentRepo, LicenseRepo
import org.acmsl.licdata.infrastructure.mail
import org.acmsl.licdata.infrastructure.params
import org.acmsl.licdata.infrastructure.resp
from pythoneda.shared import Ports

import json
import os
import datetime


def handler(event, context):
    """
    AWS Lambda handler to check if a license is valid.
    :param event: The AWS Lambda event.
    :type event: event
    :param context: The AWS Lambda context.
    :type context: context
    :return: The response.
    :rtype: Dict
    """
    status = 410
    file = None

    (body, error) = params.loadBody(event)

    if error:
        status = 500
    else:
        email = params.retrieveEmail(body, event)
        product = params.retrieveProduct(body, event)
        productVersion = params.retrieveProductVersion(body, event)
        installationCode = params.retrieveInstallationCode(body, event)

        license = (
            Ports.instance()
            .resolve_first(LicenseRepo)
            .findByEmailProductAndInstallationCode(
                email, product, productVersion, installationCode
            )
        )

        if license:
            licenseId = license["id"]
            licenseData = json.dumps(license, indent=4, sort_keys=True, default=str)
            licenseEnd = license["licenseEnd"]
            if licenseEnd >= datetime.datetime.now():
                status = 200
                respBody = licenseData
                mail.send_email(
                    os.environ["MAIL_FROM"],
                    os.environ["MAIL_TO"],
                    f"License in use: {licenseId}",
                    f"""<html>
  <body>
    <h1>Valid license requested</h1>
    <ul>
      <li>license: {licenseId}</li>
      <li>email: {email}</li>
      <li>product: {product}</li>
      <li>version: {productVersion}</li>
      <li>installationCode: {installationCode}</li>
      <li>licenseData: <pre>{licenseData}</pre></li>
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
            else:
                print(f"License expired {licenseEnd}")
                status = 410
                incidentId = incidentrepo.insert(
                    licenseId, email, product, productVersion, installationCode
                )
                respBody = {
                    "error": "license expired",
                    "licenseId": licenseId,
                    "incident": incidentId,
                    "email": email,
                    "product": product,
                    "version": productVersion,
                    "installationCode": installationCode,
                }
                mail.send_email(
                    f"License expired: {licenseId}",
                    f"""<html>
                    <body>
                    <h1>License expired: {licenseId}</h1>
                    <ul>
                        <li>Incident: {incidentId}</li>
                        <li>license: {licenseId}</li>
                        <li>email: {email}</li>
                        <li>product: {product}</li>
                        <li>version: {productVersion}</li>
                        <li>installationCode: {installationCode}</li>
                        <li>licenseData: <pre>{licenseData}</pre></li>
                    </ul>
  </body>
</html>
""",
                    "html",
                )
        else:
            status = 404
            respBody = {
                "error": "unknown license",
                "email": email,
                "product": product,
                "productVersion": productVersion,
                "installationCode": installationCode,
            }
            mail.send_email(
                f"Unknown license: {email}",
                f"""<html>
  <body>
    <h1>Unknown license requested by {email}</h1>
    <ul>
      <li>email: {email}</li>
      <li>product: {product}</li>
      <li>version: {productVersion}</li>
      <li>installationCode: {installationCode}</li>
    </ul>
  </body>
</html>
""",
                "html",
            )

    return resp.buildResponse(status, respBody, event, context)
