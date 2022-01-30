#!/usr/bin/python
#
# Author: Thomas Boutry <thomas.boutry@x3rus.com>
##################################################

# Modules
# improvement : import only method we use ...

import csv
import requests
import logging
import json


class applicant():
    """application to interact with sample-app"""
    def __init__(self, baseurl, version, log_level=logging.INFO):
        """Init applicant"""
        self.baseurl = baseurl
        self.version = version
        logging.basicConfig(level=log_level)

    def getAppUrl(self):
        """Return structured url to reach app"""
        return self.baseurl + "/" + self.version

    def extractClientFromCsv(self, csv_file):
        """ extract list of client from a csv file

        return clients dictionnary
        """
        clients = []
        try:
            fd = open(csv_file)
            csv_content = csv.reader(fd)
            next(csv_content)
            for row in csv_content:
                clients.append(row)
        except Exception as e:
            print("An error occur, the script returned an empty array.")
            print('the exception occurred: {}'.format(e))
        else:
            fd.close()
        return clients

    def getClientList(self):
        """ return list of client in the app

        return http code, client list ( empty if http code is not 200)
        """
        response = requests.get(self.getAppUrl() + "/client")

        clients = []
        if response.status_code == 200:
            if len(response.content) > 0:
                http_string = response.content.decode('utf-8')
                clients = json.loads(http_string)
        else:
            logging.warning("Getting clients list return an issue http code : %d / messge %s", response.status_code,
                            response.content)

        return (response.status_code, clients)

    def getOneClient(self, c_id):
        """ retreive one client and return it in json format
        """
        response = requests.get(self.getAppUrl() + "/client/" + c_id)

        if response.status_code == 200:
            http_string = response.content.decode('utf-8')
            json_obj = json.loads(http_string)
            return response.status_code, json_obj

        if response.status_code == 404:
            return response.status_code, {}

        logging.error("Problem when contacting the app: %s", response.content)
        return response.status_code, {}

    def addClient(self, c_id, c_name, c_url):
        """ add a client to the app

        return http code, client information added OR None
        """
        # create json structure
        client_json = {
            "id": c_id,
            "name": c_name,
            "url": c_url
        }
        r = requests.post(self.getAppUrl() + "/client", json=client_json)

        if r.status_code == 200:
            return(r.status_code, client_json)
        if r.status_code == 409:
            logging.warning("client ID %s , already exist", c_id)
        else:
            logging.warning("Error adding client http code: %d / %s", r.status_code, r.content)

        return(r.status_code, None)

    def delClient(self, c_id):
        """ delete client
        return true or false
        """
        response = requests.delete(self.getAppUrl() + "/client/" + c_id)

        if response.status_code == 200:
            return True
        else:
            logging.error("Problem deleting client : %s, got error : %s", c_id, response.content)

        return False

    def updateClient(self, c_id, c_name="", c_url=""):
        """ Update client information """
        client_json = {
            "id": c_id,
            "name": c_name,
            "url": c_url,
        }
        # Need big improvement but it was to test / validate some behavior
        r = requests.put(self.getAppUrl() + "/client/", json=client_json)
        print(r)

    def isHealthy(self):
        """
        check if the app is healthy
        """
        response = requests.get(self.getAppUrl() + "/healthz")
        if response.status_code == 200:
            return True
        else:
            return False

    def compareClientInfo(self, c_id, c_name, c_url, mustBeRecheable=False):
        """ compare client information

        return true if information match, we can add criteria like must be recheable.
        """
        http_code, client_in_app = self.getOneClient(c_id)
        if http_code != 200:
            return False

        # compare
        if c_id == client_in_app['id'] and \
           c_name == client_in_app['name'] and \
           c_url == client_in_app['url']:
            if mustBeRecheable is False:
                return True
            else:
                return client_in_app['reachable']


if __name__ == "__main__":

    # Improvement add commande line argument because it's a script otherwise I will use env variables
    app_url = "https://interview-48d539efac.interview.vme.dev/api"
    cvs_file = 'clients.csv'

    # APPLICATION CONNECTION
    app = applicant(app_url, "v1", logging.WARNING)

    # check if the app is healthy before pushing content
    if app.isHealthy() is False:
        print("ERROR: the applicationg is not healthy , fix it before running the script")

    # DATA LOADING
    # Loading csv file with info
    clients_retreived = app.extractClientFromCsv(cvs_file)

    # push it to the application
    for client in clients_retreived:
        if len(client) != 3:
            print("ERROR: field number is not ok for this client entry")
            print(client)

        if app.addClient(client[0], client[1], client[2]) is None:
            print("ERROR: when I try to add client %s", client[0])

    # DATA VALIDATION
    # I reuse csv information loaded previously

    all_data_is_csv_is_in_the_app = True
    lst_of_client_in_error = []

    for client in clients_retreived:
        if app.compareClientInfo(client[0], client[1], client[2], True) is False:
            all_data_is_csv_is_in_the_app = False
            lst_of_client_in_error.append(client[0])

    if all_data_is_csv_is_in_the_app is False:
        print('ERROR: all client not in the app please check those : ')
        print(lst_of_client_in_error)

    # No Error so no message
