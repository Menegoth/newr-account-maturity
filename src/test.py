class Account():

    def fetchApplications(self):
        print("FETCH: applications")
        self._applications = [
            {
                'appId': 1,
                'appName': "App 1"
            },
            {
                'appId': 2,
                'appName': "App 2"
            }
        ]

    def fetchApplicationInstances(self):
        print("FETCH: applicationInstances")
        for application in self.applications:
            instances = [
                {
                    'instanceId': 1,
                    'instanceName': "Instance 1"
                },
                {
                    'instanceId': 2,
                    'instanceName': "Instance 2"
                    }
            ]
            self._applicationInstances.append(
                {
                    'appId': application['appId'],
                    'instances': instances
                }
            )

    def applications():
        doc = "The applications list."
        def fget(self):
            if not "applications" in self.__cached:
                self.fetchApplications()
                self.__cached.append("applications")
            return self._applications
        def fdel(self):
            if "applications" in self.__cached:
                self.__cached.remove("applications")
                self._applications = []
        return locals()
    applications = property(**applications())

    def applicationInstances():
        doc = "The applicationInstances list."
        def fget(self):
            if not "applicationInstances" in self.__cached:
                self.fetchApplicationInstances()
                self.__cached.append("applicationInstances")
            return self._applicationInstances
        return locals()
    applicationInstances = property(**applicationInstances())
    def __init__(self):
        self.__cached = []
        self._applications = []
        self._applicationInstances = []

A = Account()

print(A.applicationInstances)
print(A.applications)
del A.applications
print(A.applications)
