# vim: set fileencoding=utf-8
"""
org/acmsl/licdata/infrastructure/azure/clients/list.py

This file defines the List-Clients script for Azure.

Copyright (C) 2024-today acm-sl's licdata

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
import azure.functions as func


bp = func.Blueprint()

from pythoneda.shared.infrastructure.azure.functions import get_pythoneda_app


@bp.function_name(name="ListClients")
@bp.route(route="clients", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
async def list_clients(
    req: func.HttpRequest, context: func.Context
) -> func.HttpResponse:
    """
    Azure Function to list existing clients.
    :param req: The Azure Function HTTP request.
    :type req: azure.functions.HttpRequest
    :param context: The Azure Function context.
    :type context: azure.functions.Context
    :return: The response.
    :rtype: azure.functions.HttpResponse
    """

    from pythoneda.shared import Ports
    from org.acmsl.licdata import ClientRepo
    import org.acmsl.licdata.infrastructure.rest as rest

    client_repo = Ports.instance().resolve_first(ClientRepo)
    ClientRepo.logger().info("Listing clients.")

    event = {
        "httpMethod": "GET",
        "queryStringParameters": req.params,
        "headers": req.headers,
        "body": {},
    }

    resp = rest.list(event, context, Ports.instance().resolve_first(ClientRepo))

    return func.HttpResponse(resp["body"], status_code=resp["statusCode"])


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
