import json
import time

from newrelic_account import NewRelicAccount

"""
TODO:

0) create a proper class for this
1) load a config.json with all accounts/REST keys
2) create a facade for New Relic Query API
3) get agents version data from Insights
4) count any non major agents versions

"""

def get_counts():
    account = NewRelicAccount()

    counts = {}
    counters = [
        'apps_apm_dotnet', 'apps_apm_go', 'apps_apm_java', 'apps_apm_nodejs',
        'apps_apm_php', 'apps_apm_python', 'apps_apm_ruby',
        'apps_apm_browser_enabled', 'apps_apm_default_apdex',
        'apps_apm_reporting', 'apps_apm_hosts', 'apps_apm_instances',
        'apps_apm_concurrent_instances', 'apps_apm_total',
        'apps_mobile_total', 'apps_mobile_reporting', 'apps_browser_total',
        'users_total'
    ]
    for counter in counters:
        counts[counter] = 0

    users, _ = account.users
    for user in users:
        counts['users_total'] += 1
    del users

    apm_applications, _ = account.apm_applications
    for apm_application in apm_applications:
        counts['apps_apm_total'] += 1
        if apm_application['data']['reporting']:
            counts['apps_apm_reporting'] += 1
            counts['apps_apm_' + apm_application['data']['language']] += 1
            summary = apm_application['data']['application_summary']
            counts['apps_apm_hosts'] += summary['host_count']
            counts['apps_apm_instances'] += summary.get('instance_count', 0)
            counts['apps_apm_concurrent_instances'] += \
                summary.get('concurrent_instance_count', 0)
            if summary['apdex_target'] == 0.5:
                counts['apps_apm_default_apdex'] += 1
        if apm_application['data']['settings']['enable_real_user_monitoring']:
            counts['apps_apm_browser_enabled'] += 1
    del apm_applications

    mobile_applications, _ = account.mobile_applications
    for mobile_application in mobile_applications:
        counts['apps_mobile_total'] += 1
        if mobile_application['data']['reporting']:
            counts['apps_mobile_reporting'] += 1
            #if application['data']['crash_summary']['supports_crash_data']:
            #    counts['mobile_crash_enabled'] += 1
    del mobile_applications

    browser_applications, _ = account.browser_applications
    for browser_application in browser_applications:
        counts['apps_browser_total'] += 1
    del browser_applications

    return counts

def main():
    start_time = time.time()
    counts = get_counts()
    elapsed_time = time.time() - start_time
    print(json.dumps(counts, sort_keys=True, indent=4))
    print(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))

if __name__ == '__main__':
    main()
