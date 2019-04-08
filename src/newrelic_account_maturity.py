import json
import time

from newrelic_account import NewRelicAccount

class NewRelicAccountMaturity():

    __WEEK_TIME = 60*60*24*7
    __MONTH_TIME = __WEEK_TIME * 4.5
    __METRIC_NAMES = [
        'apps_apm_dotnet',
        'apps_apm_go',
        'apps_apm_java',
        'apps_apm_nodejs',
        'apps_apm_php',
        'apps_apm_python',
        'apps_apm_ruby',
        'apps_apm_browser_enabled',
        'apps_apm_default_apdex',
        'apps_apm_reporting',
        'apps_apm_hosts',
        'apps_apm_instances',
        'apps_apm_concurrent_instances',
        'apps_apm_total',
        'apps_mobile_total',
        'apps_mobile_reporting',
        'apps_browser_total',
        'users_total',
        'alerts_policies_per_entity',
        'alerts_policies_per_policy',
        'alerts_policies_per_condition',
        'alerts_policies_week_old',
        'alerts_policies_month_old',
        'alerts_policies_total',
        'get_metadata_duration'
    ]

    def __init__(self):
        self.__account = NewRelicAccount()

    def reset_metrics(self):
        self._metrics = {}
        for metric_name in NewRelicAccountMaturity.__METRIC_NAMES:
            self._metrics[metric_name] = 0

    def get_users_metrics(self):
        users, _ = self.__account.users
        for user in users:
            self._metrics['users_total'] += 1

    def get_apm_metrics(self):
        apm_applications, _ = self.__account.apm_applications
        for apm_application in apm_applications:
            self._metrics['apps_apm_total'] += 1

            if apm_application['data']['reporting']:
                self._metrics['apps_apm_reporting'] += 1
                metric_name = 'apps_apm_' + apm_application['data']['language']
                self._metrics[metric_name] += 1

                summary = apm_application['data']['application_summary']
                self._metrics['apps_apm_hosts'] += summary['host_count']
                self._metrics['apps_apm_instances'] += \
                    summary.get('instance_count', 0)
                self._metrics['apps_apm_concurrent_instances'] += \
                    summary.get('concurrent_instance_count', 0)
                if summary['apdex_target'] == 0.5:
                    self._metrics['apps_apm_default_apdex'] += 1

            settings = apm_application['data']['settings']
            if settings['enable_real_user_monitoring']:
                self._metrics['apps_apm_browser_enabled'] += 1

    def get_mobile_metrics(self):
        mobile_applications, _ = self.__account.mobile_applications
        for mobile_application in mobile_applications:
            self._metrics['apps_mobile_total'] += 1
            if mobile_application['data']['reporting']:
                self._metrics['apps_mobile_reporting'] += 1

    def get_browser_metrics(self):
        browser_applications, _ = self.__account.browser_applications
        self._metrics['apps_browser_total'] = len(browser_applications)

    def get_alerts_policies_metrics(self, current_time):
        alerts_policies, _ = self.__account.alerts_policies
        for alerts_policy in alerts_policies:
            self._metrics['alerts_policies_total'] += 1

            incident_preference = alerts_policy['data']['incident_preference']
            if incident_preference == 'PER_POLICY':
                self._metrics['alerts_policies_per_policy'] += 1
            elif incident_preference == 'PER_CONDITION':
                self._metrics['alerts_policies_per_condition'] += 1
            elif incident_preference == 'PER_ENTITY':
                self._metrics['alerts_policies_per_entity'] += 1

            update_delta = current_time - alerts_policy['data']['updated_at']
            #if update_delta < NewRelicAccountMaturity.__WEEK_TIME:
            #    self._metrics['alerts_policies_week_old'] += 1
            #elif update_delta < NewRelicAccountMaturity.__MONTH_TIME:
            #    self._metrics['alerts_policies_month_old'] += 1

    def metrics():
        doc = "The metrics dictionary."
        def fget(self):
            start_time = time.time()
            self.reset_metrics()
            self.get_users_metrics()
            self.get_apm_metrics()
            self.get_browser_metrics()
            self.get_mobile_metrics()
            self.get_alerts_policies_metrics(start_time)
            elapsed_time = round(time.time() - start_time, 2)
            self._metrics['get_metadata_duration'] = elapsed_time
            return self._metrics
        return locals()
    metrics = property(**metrics())

if __name__ == '__main__':
    account_maturity = NewRelicAccountMaturity()
    metrics = account_maturity.metrics
    print(json.dumps(metrics, sort_keys=True, indent=4))
