import requests
import json

class NewRelicAccount():
    """ Interface to New Relic REST API """

    MAX_PAGES = 2
    MAX_RETRIES = 3

    def __init__(self, rest_api_key):
        self.rest_api_key = rest_api_key

    def get(self, endpoint, retry=MAX_RETRIES):
        headers = {'X-API-Key': self.rest_api_key}
        success = False
        result = {}
        count = 0
        while not success and count < retry:
            r = requests.get(self.endpoints['endpoint']['url'], headers=headers)
            count += 1
            success = (r.status_code == requests.codes.ok)

        if success:
            return r.json()[self.endpoints[endpoint]['collection']], True
        else:
            return [], False

    def getApplications(self, max_pages=MAX_PAGES, retry=MAX_RETRIES):
        applications, ok = [], True
        headers = {'X-API-Key': self.rest_api_key}
        params = {'page': 1}
        is_last_page = False
        while not is_last_page and params['page'] <= max_pages:
            is_successful = False
            count = 0
            while ok and not is_successful and count < retry:
                r = requests.get(
                    'https://api.newrelic.com/v2/applications.json',
                    headers=headers, params=params
                )
                count += 1
                is_successful = (r.status_code == requests.codes.ok)
            if is_successful:
                r_json = r.json()['applications']
                applications += r_json
            else:
                r_json = []
                ok = False
            params['page'] += 1
            is_last_page = (len(r_json) == 0)
        return applications, ok

    def getApplicationInstances(self, application_id, max_pages=MAX_PAGES, retry=MAX_RETRIES):
        applications, ok = [], True
        headers = {'X-API-Key': self.rest_api_key}
        params = {'page': 1}
        is_last_page = False
        while not is_last_page and params['page'] <= max_pages:
            is_successful = False
            count = 0
            while ok and not is_successful and count < retry:
                r = requests.get(
                    f'https://api.newrelic.com/v2/applications/{application_id}/instances.json',
                    headers=headers, params=params
                )
                count += 1
                is_successful = (r.status_code == requests.codes.ok)
            if is_successful:
                r_json = r.json()['application_instances']
                applications += r_json
            else:
                r_json = []
                ok = False
            params['page'] += 1
            is_last_page = (len(r_json) == 0)
        return applications, ok

    def getApplicationDeployments(self, application_id, max_pages=MAX_PAGES, retry=MAX_RETRIES):
        applications, ok = [], True
        headers = {'X-API-Key': self.rest_api_key}
        params = {'page': 1}
        is_last_page = False
        while not is_last_page and params['page'] <= max_pages:
            is_successful = False
            count = 0
            while ok and not is_successful and count < retry:
                r = requests.get(
                    f'https://api.newrelic.com/v2/applications/{application_id}/deployments.json',
                    headers=headers, params=params
                )
                count += 1
                is_successful = (r.status_code == requests.codes.ok)
            if is_successful:
                r_json = r.json()['deployments']
                applications += r_json
            else:
                r_json = []
                ok = False
            params['page'] += 1
            is_last_page = (len(r_json) == 0)
        return applications, ok

    def getMobileApplications(self, retry=MAX_RETRIES):
        applications, ok = [], True
        headers = {'X-API-Key': self.rest_api_key}
        is_successful = False
        count = 0
        while ok and not is_successful and count < retry:
            r = requests.get(
                'https://api.newrelic.com/v2/mobile_applications.json',
                headers=headers
            )
            count += 1
            is_successful = (r.status_code == requests.codes.ok)
        if is_successful:
            r_json = r.json()['applications']
            applications += r_json
        else:
            r_json = []
            ok = False
        return applications, ok

    def getBrowserApplications(self, retry=MAX_RETRIES):
        applications, ok = [], True
        headers = {'X-API-Key': self.rest_api_key}
        is_successful = False
        count = 0
        while ok and not is_successful and count < retry:
            r = requests.get(
                'https://api.newrelic.com/v2/browser_applications.json',
                headers=headers
            )
            count += 1
            is_successful = (r.status_code == requests.codes.ok)
        if is_successful:
            r_json = r.json()['browser_applications']
            applications += r_json
        else:
            r_json = []
            ok = False
        return applications, ok

    def getKeyTransactions(self, retry=MAX_RETRIES):
        applications, ok = [], True
        headers = {'X-API-Key': self.rest_api_key}
        is_successful = False
        count = 0
        while ok and not is_successful and count < retry:
            r = requests.get(
                'https://api.newrelic.com/v2/key_transactions.json',
                headers=headers
            )
            count += 1
            is_successful = (r.status_code == requests.codes.ok)
        if is_successful:
            r_json = r.json()['key_transactions']
            applications += r_json
        else:
            r_json = []
            ok = False
        return applications, ok

    def getServers(self, max_pages=MAX_PAGES, retry=MAX_RETRIES):
        applications, ok = [], True
        headers = {'X-API-Key': self.rest_api_key}
        params = {'page': 1}
        is_last_page = False
        while not is_last_page and params['page'] <= max_pages:
            is_successful = False
            count = 0
            while ok and not is_successful and count < retry:
                r = requests.get(
                    'https://api.newrelic.com/v2/servers.json',
                    headers=headers, params=params
                )
                count += 1
                is_successful = (r.status_code == requests.codes.ok)
            if is_successful:
                r_json = r.json()['servers']
                applications += r_json
            else:
                r_json = []
                ok = False
            params['page'] += 1
            is_last_page = (len(r_json) == 0)
        return applications, ok

    def getUsers(self, max_pages=MAX_PAGES, retry=MAX_RETRIES):
        applications, ok = [], True
        headers = {'X-API-Key': self.rest_api_key}
        params = {'page': 1}
        is_last_page = False
        while not is_last_page and params['page'] <= max_pages:
            is_successful = False
            count = 0
            while ok and not is_successful and count < retry:
                r = requests.get(
                    'https://api.newrelic.com/v2/users.json',
                    headers=headers, params=params
                )
                count += 1
                is_successful = (r.status_code == requests.codes.ok)
            if is_successful:
                r_json = r.json()['users']
                applications += r_json
            else:
                r_json = []
                ok = False
            params['page'] += 1
            is_last_page = (len(r_json) == 0)
        return applications, ok

    def getAlertsEvents(self, retry=MAX_RETRIES):
        applications, ok = [], True
        headers = {'X-API-Key': self.rest_api_key}
        is_successful = False
        count = 0
        while ok and not is_successful and count < retry:
            r = requests.get(
                'https://api.newrelic.com/v2/alerts_events.json',
                headers=headers
            )
            count += 1
            is_successful = (r.status_code == requests.codes.ok)
        if is_successful:
            r_json = r.json()['recent_events']
            applications += r_json
        else:
            r_json = []
            ok = False
        return applications, ok

    def getAlertsPolicies(self, max_pages=MAX_PAGES, retry=MAX_RETRIES):
        applications, ok = [], True
        headers = {'X-API-Key': self.rest_api_key}
        params = {'page': 1}
        is_last_page = False
        while not is_last_page and params['page'] <= max_pages:
            is_successful = False
            count = 0
            while ok and not is_successful and count < retry:
                r = requests.get(
                    'https://api.newrelic.com/v2/alerts_policies.json',
                    headers=headers, params=params
                )
                count += 1
                is_successful = (r.status_code == requests.codes.ok)
            if is_successful:
                r_json = r.json()['policies']
                applications += r_json
            else:
                r_json = []
                ok = False
            params['page'] += 1
            is_last_page = (len(r_json) == 0)
        return applications, ok

    def getAlertsConditions(self, policy_id, max_pages=MAX_PAGES, retry=MAX_RETRIES):
        applications, ok = [], True
        headers = {'X-API-Key': self.rest_api_key}
        params = {'page': 1, 'policy_id':   policy_id}
        is_last_page = False
        while not is_last_page and params['page'] <= max_pages:
            is_successful = False
            count = 0
            while ok and not is_successful and count < retry:
                r = requests.get(
                    'https://api.newrelic.com/v2/alerts_conditions.json',
                    headers=headers, params=params
                )
                count += 1
                is_successful = (r.status_code == requests.codes.ok)
            if is_successful:
                r_json = r.json()['conditions']
                applications += r_json
            else:
                r_json = []
                ok = False
            params['page'] += 1
            is_last_page = (len(r_json) == 0)
        return applications, ok

    def getAlertsPluginsConditions(self, policy_id, max_pages=MAX_PAGES, retry=MAX_RETRIES):
        applications, ok = [], True
        headers = {'X-API-Key': self.rest_api_key}
        params = {'page': 1, 'policy_id':   policy_id}
        is_last_page = False
        while not is_last_page and params['page'] <= max_pages:
            is_successful = False
            count = 0
            while ok and not is_successful and count < retry:
                r = requests.get(
                    'https://api.newrelic.com/v2/alerts_plugins_conditions.json',
                    headers=headers, params=params
                )
                count += 1
                is_successful = (r.status_code == requests.codes.ok)
            if is_successful:
                r_json = r.json()['plugins_conditions']
                applications += r_json
            else:
                r_json = []
                ok = False
            params['page'] += 1
            is_last_page = (len(r_json) == 0)
        return applications, ok

    def getAlertsExternalServiceConditions(self, policy_id, max_pages=MAX_PAGES, retry=MAX_RETRIES):
        applications, ok = [], True
        headers = {'X-API-Key': self.rest_api_key}
        params = {'page': 1, 'policy_id':   policy_id}
        is_last_page = False
        while not is_last_page and params['page'] <= max_pages:
            is_successful = False
            count = 0
            while ok and not is_successful and count < retry:
                r = requests.get(
                    'https://api.newrelic.com/v2/alerts_external_service_conditions.json',
                    headers=headers, params=params
                )
                count += 1
                is_successful = (r.status_code == requests.codes.ok)
            if is_successful:
                r_json = r.json()['external_service_conditions']
                applications += r_json
            else:
                r_json = []
                ok = False
            params['page'] += 1
            is_last_page = (len(r_json) == 0)
        return applications, ok

    def getAlertsSyntheticsConditions(self, policy_id, max_pages=MAX_PAGES, retry=MAX_RETRIES):
        applications, ok = [], True
        headers = {'X-API-Key': self.rest_api_key}
        params = {'page': 1, 'policy_id':   policy_id}
        is_last_page = False
        while not is_last_page and params['page'] <= max_pages:
            is_successful = False
            count = 0
            while ok and not is_successful and count < retry:
                r = requests.get(
                    'https://api.newrelic.com/v2/alerts_synthetics_conditions.json',
                    headers=headers, params=params
                )
                count += 1
                is_successful = (r.status_code == requests.codes.ok)
            if is_successful:
                r_json = r.json()['synthetics_conditions']
                applications += r_json
            else:
                r_json = []
                ok = False
            params['page'] += 1
            is_last_page = (len(r_json) == 0)
        return applications, ok

    def getAlertsNrqlConditions(self, policy_id, max_pages=MAX_PAGES, retry=MAX_RETRIES):
        applications, ok = [], True
        headers = {'X-API-Key': self.rest_api_key}
        params = {'page': 1, 'policy_id':   policy_id}
        is_last_page = False
        while not is_last_page and params['page'] <= max_pages:
            is_successful = False
            count = 0
            while ok and not is_successful and count < retry:
                r = requests.get(
                    'https://api.newrelic.com/v2/alerts_nrql_conditions.json',
                    headers=headers, params=params
                )
                count += 1
                is_successful = (r.status_code == requests.codes.ok)
            if is_successful:
                r_json = r.json()['nrql_conditions']
                applications += r_json
            else:
                r_json = []
                ok = False
            params['page'] += 1
            is_last_page = (len(r_json) == 0)
        return applications, ok

    def getAlertsChannels(self, max_pages=MAX_PAGES, retry=MAX_RETRIES):
        applications, ok = [], True
        headers = {'X-API-Key': self.rest_api_key}
        params = {'page': 1}
        is_last_page = False
        while not is_last_page and params['page'] <= max_pages:
            is_successful = False
            count = 0
            while ok and not is_successful and count < retry:
                r = requests.get(
                    'https://api.newrelic.com/v2/alerts_channels.json',
                    headers=headers, params=params
                )
                count += 1
                is_successful = (r.status_code == requests.codes.ok)
            if is_successful:
                r_json = r.json()['channels']
                applications += r_json
            else:
                r_json = []
                ok = False
            params['page'] += 1
            is_last_page = (len(r_json) == 0)
        return applications, ok

    def getAlertsViolations(self, max_pages=MAX_PAGES, retry=MAX_RETRIES):
        applications, ok = [], True
        headers = {'X-API-Key': self.rest_api_key}
        params = {'page': 1}
        is_last_page = False
        while not is_last_page and params['page'] <= max_pages:
            is_successful = False
            count = 0
            while ok and not is_successful and count < retry:
                r = requests.get(
                    'https://api.newrelic.com/v2/alerts_violations.json',
                    headers=headers, params=params
                )
                count += 1
                is_successful = (r.status_code == requests.codes.ok)
            if is_successful:
                r_json = r.json()['violations']
                applications += r_json
            else:
                r_json = []
                ok = False
            params['page'] += 1
            is_last_page = (len(r_json) == 0)
        return applications, ok

    def getAlertsIncidents(self, max_pages=MAX_PAGES, retry=MAX_RETRIES):
        applications, ok = [], True
        headers = {'X-API-Key': self.rest_api_key}
        params = {'page': 1}
        is_last_page = False
        while not is_last_page and params['page'] <= max_pages:
            is_successful = False
            count = 0
            while ok and not is_successful and count < retry:
                r = requests.get(
                    'https://api.newrelic.com/v2/alerts_incidents.json',
                    headers=headers, params=params
                )
                count += 1
                is_successful = (r.status_code == requests.codes.ok)
            if is_successful:
                r_json = r.json()['incidents']
                applications += r_json
            else:
                r_json = []
                ok = False
            params['page'] += 1
            is_last_page = (len(r_json) == 0)
        return applications, ok

    def getAlertsEntityConditions(self, entity_id, entity_type, retry=MAX_RETRIES):
        applications, ok = [], True
        headers = {'X-API-Key': self.rest_api_key}
        params = {'entity_type': entity_type}
        is_successful = False
        count = 0
        while ok and not is_successful and count < retry:
            r = requests.get(
                f'https://api.newrelic.com/v2/alerts_entity_conditions/{entity_id}.json',
                headers=headers, params=params
            )
            count += 1
            is_successful = (r.status_code == requests.codes.ok)
        if is_successful:
            r_json = r.json()['conditions']
            applications += r_json
        else:
            r_json = []
            ok = False
        return applications, ok

    def getPlugins(self, max_pages=MAX_PAGES, retry=MAX_RETRIES):
        applications, ok = [], True
        headers = {'X-API-Key': self.rest_api_key}
        params = {'page': 1}
        is_last_page = False
        while not is_last_page and params['page'] <= max_pages:
            is_successful = False
            count = 0
            while ok and not is_successful and count < retry:
                r = requests.get(
                    'https://api.newrelic.com/v2/plugins.json',
                    headers=headers, params=params
                )
                count += 1
                is_successful = (r.status_code == requests.codes.ok)
            if is_successful:
                r_json = r.json()['plugins']
                applications += r_json
            else:
                r_json = []
                ok = False
            params['page'] += 1
            is_last_page = (len(r_json) == 0)
        return applications, ok

    def getComponents(self, max_pages=MAX_PAGES, retry=MAX_RETRIES):
        applications, ok = [], True
        headers = {'X-API-Key': self.rest_api_key}
        params = {'page': 1}
        is_last_page = False
        while not is_last_page and params['page'] <= max_pages:
            is_successful = False
            count = 0
            while ok and not is_successful and count < retry:
                r = requests.get(
                    'https://api.newrelic.com/v2/components.json',
                    headers=headers, params=params
                )
                count += 1
                is_successful = (r.status_code == requests.codes.ok)
            if is_successful:
                r_json = r.json()['components']
                applications += r_json
            else:
                r_json = []
                ok = False
            params['page'] += 1
            is_last_page = (len(r_json) == 0)
        return applications, ok

    def getLabels(self, max_pages=MAX_PAGES, retry=MAX_RETRIES):
        applications, ok = [], True
        headers = {'X-API-Key': self.rest_api_key}
        params = {'page': 1}
        is_last_page = False
        while not is_last_page and params['page'] <= max_pages:
            is_successful = False
            count = 0
            while ok and not is_successful and count < retry:
                r = requests.get(
                    'https://api.newrelic.com/v2/labels.json',
                    headers=headers, params=params
                )
                count += 1
                is_successful = (r.status_code == requests.codes.ok)
            if is_successful:
                r_json = r.json()['labels']
                applications += r_json
            else:
                r_json = []
                ok = False
            params['page'] += 1
            is_last_page = (len(r_json) == 0)
        return applications, ok
