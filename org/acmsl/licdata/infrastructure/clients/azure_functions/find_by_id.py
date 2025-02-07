"""
org/acmsl/licdata/infrastructure/clients/azure_functions/find_by_id.py

This file provides an Azure Functions handler to update existing clients.

Copyright (C) 2023-today ACM S.L. Licdata

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


@bp.function_name(name="FindClientById")
@bp.route(route="clients/{id}", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
async def find_client_by_id(
    req: func.HttpRequest, context: func.Context
) -> func.HttpResponse:
    """
    Azure Function to retrieve a client by its id.
    :param req: The Azure Function HTTP request.
    :type req: azure.functions.HttpRequest
    :param context: The Azure Function context.
    :type context: azure.functions.Context
    :return: The response.
    :rtype: azure.functions.HttpResponse
    """
    from pythoneda.shared.infrastructure.azure.functions import get_pythoneda_app
    from pythoneda.shared.infrastructure.http import HttpMethod
    from org.acmsl.licdata.events.clients import (
        FindClientByIdRequested,
    )
    from org.acmsl.licdata.events.infrastructure.http.clients import (
        HttpClientResponseFactory,
        HttpFindClientByIdRequested,
    )

    event = HttpFindClientByIdRequested(
        httpMethod=HttpMethod.GET,
        queryStringParameters=req.params,
        headers=req.headers,
        pathParameters=req.route_params,
        body={},
    ).to_event()

    app = get_pythoneda_app()

    resulting_event = None
    resulting_events = await app.accept(event)

    if len(resulting_events) > 0:
        resulting_event = resulting_events[0]

    outcome = HttpClientResponseFactory.instance().from_find_client_by_id_requested(
        resulting_event, event
    )

    return func.HttpResponse(
        outcome.body,
        status_code=outcome.status_code,
        mimetype=outcome.mime_type,
        headers=outcome.headers,
        charset=outcome.charset,
    )


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
