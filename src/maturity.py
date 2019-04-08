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
    applications, _ = account.applications
    counts = {}
    counters = [
        'dotnet', 'go', 'java', 'nodejs', 'php', 'python', 'ruby',
        'browser_enabled', 'default_apdex_target', 'reporting',
        'host', 'instance', 'concurrent_instance', 'total']
    for counter in counters:
        counts[counter] = 0
    for application in applications:
        counts['total'] += 1
        counts[application['data']['language']] += 1
        if application['data']['reporting']:
            summary = application['data']['application_summary']
            counts['reporting'] += 1
            counts['host'] += summary['host_count']
            counts['instance'] += summary.get('instance_count', 0)
            counts['concurrent_instance'] += \
                summary.get('concurrent_instance_count', 0)
            if summary['apdex_target'] == 0.5:
                counts['default_apdex_target'] += 1
        if application['data']['settings']['enable_real_user_monitoring']:
            counts['browser_enabled'] += 1
    return counts

def main():
    start_time = time.time()
    counts = get_counts()
    elapsed_time = time.time() - start_time
    print(json.dumps(counts, indent=4))
    print(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))

if __name__ == '__main__':
    main()
