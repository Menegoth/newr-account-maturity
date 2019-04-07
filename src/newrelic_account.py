# a = [{'id':e, 'data':e} for e in a]
import os
import json

from newrelic_rest_api import NewRelicRestAPI

class NewRelicAccount():

    def __init__(self, rest_api_key=''):
        if rest_api_key == '':
            rest_api_key = os.getenv('NEW_RELIC_REST_API_KEY', '')
        self.__rest_api = NewRelicRestAPI(rest_api_key)
        self.__cache = []

    def __get_cache(self, set_name):
        L = list(filter(lambda set: set['set_name'] == set_name, self.__cache))
        if len(L) == 1:
            return L[0]['data'], True
        else:
            return [], False

    def applications():
        doc = "The applications dictionary."
        def fget(self):
            result, ok = self.__get_cache('applications')
            if not ok:
                result, ok = self.__rest_api.get_set('applications')
                if ok:
                    result = [{'id':item['id'], 'data':item} for item in result]
                    self.__cache.append({
                        'set_name': 'applications',
                        'data': result,
                    })
            return result, ok
        return locals()
    applications = property(**applications())

    def mobile_applications():
        doc = "The mobile applications dictionary."
        def fget(self):
            result, ok = self.__get_cache('mobile_applications')
            if not ok:
                result, ok = self.__rest_api.get_set('mobile_applications')
                if ok:
                    result = [{'id':item['id'], 'data':item} for item in result]
                    self.__cache.append({
                        'set_name': 'mobile_applications',
                        'data': result,
                    })
            return result, ok
        return locals()
    mobile_applications = property(**mobile_applications())

    def browser_applications():
        doc = "The browser applications dictionary."
        def fget(self):
            result, ok = self.__get_cache('browser_applications')
            if not ok:
                result, ok = self.__rest_api.get_set('browser_applications')
                if ok:
                    result = [{'id':item['id'], 'data':item} for item in result]
                    self.__cache.append({
                        'set_name': 'browser_applications',
                        'data': result,
                    })
            return result, ok
        return locals()
    browser_applications = property(**browser_applications())

if __name__ == "__main__":
    account = NewRelicAccount()

    result, ok = account.applications
    if ok:
        print(json.dumps(result, sort_keys=True, indent=4))

    result, ok = account.mobile_applications
    if ok:
        print(json.dumps(result, sort_keys=True, indent=4))

    result, ok = account.browser_applications
    if ok:
        print(json.dumps(result, sort_keys=True, indent=4))
