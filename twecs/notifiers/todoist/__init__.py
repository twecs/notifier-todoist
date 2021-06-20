import logging
import uuid

import requests

logger = logging.getLogger(
    __name__,
)


def request_response_hook(
        response,
        *args,
        **kwargs,
    ):
    logger.debug(
        'response: %s',
        response.text,
    )


def execute(
        parameters,
        transfer,
    ):
    task_placement = {
    }

    api_token = parameters['api_token']

    try:
        parent_id = parameters['parent_id']
    except KeyError:
        pass
    else:
        task_placement['parent_id'] = parent_id

    try:
        project_id = parameters['project_id']
    except KeyError:
        pass
    else:
        task_placement['project_id'] = project_id

    try:
        section_id = parameters['section_id']
    except KeyError:
        pass
    else:
        task_placement['section_id'] = section_id

    reference = transfer['reference']
    source_amount_via_transfer = transfer['source_amount_via_transfer']
    source_currency = transfer['source_currency']
    wise_transfer_id = transfer['wise_transfer_id']

    session = requests.Session(
    )

    session.hooks['response'].append(
        request_response_hook,
    )

    session.headers['Authorization'] = f'Bearer {api_token}'

    request_id = uuid.uuid4(
    )
    request_id_str = str(
        request_id,
    )

    response = session.post(
        'https://api.todoist.com/rest/v1/tasks',
        headers={
            'Content-Type': 'application/json',
            'X-Request-Id': request_id_str,
        },
        json={
            'content': f'Fund Wise transfer `{wise_transfer_id}` for {reference}',
            'due_lang': 'en',
            'due_string': 'today',
            'priority': 2,
            **task_placement,
        },
    )

    response_data = response.json(
    )

    task_id = response_data['id']

    request_id = uuid.uuid4(
    )
    request_id_str = str(
        request_id,
    )

    reponse = session.post(
        'https://api.todoist.com/rest/v1/comments',
        headers={
            'Content-Type': 'application/json',
            'X-Request-Id': request_id_str,
        },
        json={
            'content': f'Cost in source currency when funding via bank transfer: {source_amount_via_transfer} {source_currency}.',
            'task_id': task_id,
        },
    )
