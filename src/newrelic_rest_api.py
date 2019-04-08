import json
import os
import requests

class NewRelicRestAPI():
    """ Facade to New Relic REST API LIST endpoints """

    MAX_PAGES = 1000
    MAX_RETRIES = 5

    ENDPOINTS = {
    'applications': {
        'url': 'https://api.newrelic.com/v2/applications.json',
        'paginates': True,
        'set_name': 'applications'
    },
    'application_hosts': {
        'url': 'https://api.newrelic.com/v2/applications/{}/hosts.json',
        'paginates': True,
        'set_name': 'application_hosts'
    },
    'application_instances': {
        'url': 'https://api.newrelic.com/v2/applications/{}/instances.json',
        'paginates': True,
        'set_name': 'application_instances'
    },
    'application_deployments': {
        'url': 'https://api.newrelic.com/v2/applications/{}/deployments.json',
        'paginates': True,
        'set_name': 'application_deployments'
    },
    'mobile_applications': {
        'url': 'https://api.newrelic.com/v2/mobile_applications.json',
        'paginates': False,
        'set_name': 'applications'
    },
    'browser_applications': {
        'url': 'https://api.newrelic.com/v2/browser_applications.json',
        'paginates': False,
        'set_name': 'browser_applications'
    },
    'key_transactions': {
        'url': 'https://api.newrelic.com/v2/key_transactions.json',
        'paginates': True,
        'set_name': 'key_transactions'
    },
    'users': {
        'url': 'https://api.newrelic.com/v2/users.json',
        'paginates': True,
        'set_name': 'users'
    },
    'plugins': {
        'url': 'https://api.newrelic.com/v2/plugins.json',
        'paginates': True,
        'set_name': 'plugins'
    },
    'labels': {
        'url': 'https://api.newrelic.com/v2/labels.json',
        'paginates': True,
        'set_name': 'labels'
    },
    'alerts_events': {
        'url': 'https://api.newrelic.com/v2/alerts_events.json',
        'paginates': True,
        'set_name': 'recent_events'
    },
    'alerts_policies': {
        'url': 'https://api.newrelic.com/v2/alerts_policies.json',
        'paginates': True,
        'set_name': 'policies'
    },
    'alerts_channels': {
        'url': 'https://api.newrelic.com/v2/alerts_channels.json',
        'paginates': True,
        'set_name': 'channels'
    },
    'alerts_conditions': {
        'url': 'https://api.newrelic.com/v2/alerts_conditions.json',
        'paginates': True,
        'set_name': 'conditions'
    },
    'alerts_plugins_conditions': {
        'url': 'https://api.newrelic.com/v2/alerts_plugins_conditions.json',
        'paginates': True,
        'set_name': 'conditions'
    },
    'external_service_conditions': {
        'url': 'https://api.newrelic.com/v2/alerts_external_service_conditions.json',
        'paginates': True,
        'set_name': 'conditions'
    },
    'alerts_synthetics_conditions': {
        'url': 'https://api.newrelic.com/v2/alerts_synthetics_conditions.json',
        'paginates': True,
        'set_name': 'conditions'
    },
    'alerts_nrql_conditions': {
        'url': 'https://api.newrelic.com/v2/alerts_nrql_conditions.json',
        'paginates': True,
        'set_name': 'conditions'
    },
    'alerts_entity_conditions': {
        'url': 'https://api.newrelic.com/v2/alerts_entity_conditions/{}.json',
        'paginates': False,
        'set_name': 'conditions'
    }
    }

    def __init__(self, rest_api_key=''):
        if rest_api_key == '':
            rest_api_key = os.getenv('NEW_RELIC_REST_API_KEY', '')
        self.__headers = {'X-API-Key': rest_api_key}

    def __get_paging_set(
        endpoint, entity=None, params={}, headers={},
        max_retries=MAX_RETRIES, max_pages=MAX_PAGES
    ):
        """ returns a list of entities from paginating endpoints """

        result, ok = [], True
        set_name = NewRelicRestAPI.ENDPOINTS[endpoint]['set_name']
        url = NewRelicRestAPI.ENDPOINTS[endpoint]['url']
        if '{}' in url:
            if entity is None:
                ok = False
            else:
                url = url.format(entity)

        last_page = False
        params['page'] = 1
        while ok and not last_page and params['page'] <= max_pages:
            succeeded = False
            count_retries = 0
            while not succeeded and count_retries < max_retries:
                try:
                    count_retries += 1
                    response = requests.get(
                        url,
                        headers=headers,
                        params=params
                    )
                    succeeded = (response.status_code == requests.codes.ok)
                except:
                    succeeded = False
            if succeeded:
                response_json = response.json()[set_name]
                result += response_json
                last_page = (len(response_json) == 0)
            else:
                result, ok = [], False
            params['page'] += 1

        del params['page']
        return result, ok

    def __get_non_paging_set(
        endpoint, entity=None, params={}, headers={},
        max_retries=MAX_RETRIES
    ):
        """ returns a list of entities from non paginating endpoints """

        result, ok = [], True
        set_name = NewRelicRestAPI.ENDPOINTS[endpoint]['set_name']
        url = NewRelicRestAPI.ENDPOINTS[endpoint]['url']
        if '{}' in url:
            if entity is None:
                ok = False
            else:
                url = url.format(entity)

        if ok:
            count_retries = 0
            succeeded = False
            while not succeeded and count_retries < max_retries:
                try:
                    count_retries += 1
                    response = requests.get(
                        url,
                        headers=headers,
                        params=params
                    )
                    succeeded = (response.status_code == requests.codes.ok)
                except:
                    pass
            if succeeded:
                result = response.json()[set_name]
            else:
                ok = False

        return result, ok

    def get_set(
        self, endpoint, entity=None, params={},
        max_retries=MAX_RETRIES, max_pages=MAX_PAGES
    ):
        """
        returns a list of entities from an API endpoint
            endpoint: NewRelicRestAPI.ENDPOINTS
            entity: entity_id for endpoints requiring it on the url
            params: extra GET parameters
        """

        if not endpoint in NewRelicRestAPI.ENDPOINTS:
            result, ok = [], False
        elif NewRelicRestAPI.ENDPOINTS[endpoint]['paginates']:
            result, ok = NewRelicRestAPI.__get_paging_set(
                endpoint,
                entity=entity,
                params=params,
                headers=self.__headers,
                max_retries=max_retries,
                max_pages=max_pages
            )
        else:
            result, ok = NewRelicRestAPI.__get_non_paging_set(
                endpoint,
                entity=entity,
                params=params,
                headers=self.__headers,
                max_retries=max_retries
            )
        return result, ok

if __name__ == "__main__":
    api, ok = NewRelicRestAPI('API_KEY'), False

    result, ok = api.get_set('applications')
    if ok:
        print(json.dumps(result, sort_keys=True, indent=4))

    result, ok = api.get_set('application_instances', entity=233912431)
    if ok:
        print(json.dumps(result, sort_keys=True, indent=4))

    result, ok = api.get_set('mobile_applications')
    if ok:
        print(json.dumps(result, sort_keys=True, indent=4))
