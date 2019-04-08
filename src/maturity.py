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
        'dotnet', 'go', 'java', 'nodejs', 'php', 'python', 'ruby',
        'browser_enabled', 'default_apdex_target', 'apm_reporting',
        'hosts', 'instances', 'concurrent_instances', 'apm_applications',
        'mobile_applications', 'mobile_reporting', 'browser_applications' ]
    for counter in counters:
        counts[counter] = 0

    applications, _ = account.applications
    for application in applications:
        counts['apm_applications'] += 1
        if application['data']['reporting']:
            counts['apm_reporting'] += 1
            counts[application['data']['language']] += 1
            summary = application['data']['application_summary']
            counts['hosts'] += summary['host_count']
            counts['instances'] += summary.get('instance_count', 0)
            counts['concurrent_instances'] += \
                summary.get('concurrent_instance_count', 0)
            if summary['apdex_target'] == 0.5:
                counts['default_apdex_target'] += 1
        if application['data']['settings']['enable_real_user_monitoring']:
            counts['browser_enabled'] += 1
    del applications

    mobile_applications, _ = account.mobile_applications
    for mobile_application in mobile_applications:
        counts['mobile_applications'] += 1
        if application['data']['reporting']:
            counts['mobile_reporting'] += 1
            #if application['data']['crash_summary']['supports_crash_data']:
            #    counts['mobile_crash_enabled'] += 1

    browser_applications, _ = account.browser_applications
    for browser_application in browser_applications:
        counts['browser_applications'] += 1

    return counts

def main():
    start_time = time.time()
    counts = get_counts()
    elapsed_time = time.time() - start_time
    print(json.dumps(counts, sort_keys=True, indent=4))
    print(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))

if __name__ == '__main__':
    main()
