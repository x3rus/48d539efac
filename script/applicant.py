#!/usr/bin/python
#
# Author: Thomas Boutry <thomas.boutry@x3rus.com>
##################################################

import requests


class applicant():
    """application to interact with sample-app"""
    def __init__(self, baseurl, version):
        """Init applicant"""
        self.baseurl = baseurl
        self.version = version

    def getAppUrl(self):
        """Return full url"""
        return self.baseurl + "/" + self.version

    def getClientList(self):
        response = requests.get(self.getAppUrl() + "/client")
        return response.content

    def getOneClient(self, c_id):
        response = requests.get(self.getAppUrl() + "/client/" + c_id)
        return response.content

    def addClient(self, c_id, c_name, c_url):
        """ add a client to the app """
        # create json structure
        client_json = {
            "id": c_id,
            "name": c_name,
            "url": c_url
        }
        r = requests.post(self.getAppUrl() + "/client", json=client_json)
        print(r)

    def delClient(self, c_id):
        r = requests.delete(self.getAppUrl() + "/client/" + c_id)
        print(r)

    def updateClient(self, c_id, c_name=None, c_url=None, c_reachable=None, c_status=None):
        client_json = {
            "id": c_id,
            "name": c_name,
            "url": c_url,
            "reachable": "",
            "status": ""
        }
        r = requests.put(self.getAppUrl() + "/client/", json=client_json)
        print(r)


if __name__ == "__main__":
    app = applicant("https://interview-48d539efac.interview.vme.dev/api", "v1")
    print(app.getClientList())

    app.addClient("1234", "ze_client", "http://goototogle.com")
    print(app.getClientList())

    print(app.getOneClient("1234"))

    app.addClient("9876", "ze_second_client", "http://google.com")
    print(app.getClientList())

    print(app.getOneClient("9876"))

    app.delClient("1234")
    print(app.getClientList())

    app.delClient("9876")
    print(app.getClientList())
