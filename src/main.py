import json

from newrelic_account_maturity import NewRelicAccountMaturity

"""
TODO:
1) load a config.json with all accounts REST keys and iterate it
2) create a facade for New Relic Query API
3) get agents version data from Insights
4) count any non major agents versions
"""

account_maturity = NewRelicAccountMaturity()
metrics = account_maturity.metrics
print(json.dumps(metrics, sort_keys=True, indent=4))
