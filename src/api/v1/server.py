import falcon
import json
from falcon_auth import BasicAuthBackend

from settings import (ID, NODENAME, DOMAIN)
from release_info import VERSION

from models.followers import FollowerRelation
from models.user import User

from utils.username import extract_user
from utils.webfinger import Webfinger

class serverInfo:

    auth = {'auth_disabled': True}

    def on_get(self, req, rest):
        nUsers = User.select().count()

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({"users": nUsers})

class wellknownNodeinfo:

    auth = {'auth_disabled': True}

    def on_get(self,req, resp):
        links=[
            {
                "rel": "http://nodeinfo.diaspora.software/ns/schema/2.0",
                "href": "{}/nodeinfo".format(ID),
            }
        ]
        resp.body = json.dumps(links)
        resp.status = falcon.HTTP_200

class nodeinfo:

    auth = {'auth_disabled':True}

    def on_get(self, req, resp):

        resp.append_header("Content-Type","application/json; profile=http://nodeinfo.diaspora.software/ns/schema/2.0#")

        {
            "version": "2.0",
            "software": {
                "name": "zinat",
                "version": "zinat {}".format(VERSION),
            },
            "protocols": ["activitypub"],
            "services": {"inbound": [], "outbound": []},
            "openRegistrations": False,
            "usage": {
                "users": {
                    "total": User.select().count()
                },
                "localPosts": Status.select().count()
            },
            "metadata": {
                "sourceCode": "https://github.com/yabirgb/zinat",
                "nodeName": NODENAME,
            },
        }

class wellknownWebfinger:

    auth = {'auth_disabled': True}

    def on_get(self, req, resp):

        # For now I will assume that webfinger only asks for the actor, so resources
        # is just one element.
        
        if not 'resource' in req.params.keys():
            raise falcon.HTTPBadRequest(description="No resource was provided along the request.")
        
        resources = req.params['resource']


        username, domain = extract_user(resources)

        if username == None and domain == None:
            raise falcon.HTTPBadRequest(description="Unable to decode resource.")

        if domain == DOMAIN:
            user = User.get_or_none(username=username)

            if user:
                response = Webfinger(user).generate()
                resp.body = json.dumps(response)
                resp.status = falcon.HTTP_200
            else:
                raise falcon.HTTPNotFound(description="User was not found.")
        else:
            raise falcon.HTTPBadRequest(description="Resouce domain doesn't match local domain.")