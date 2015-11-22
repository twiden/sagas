import cherrypy
import requests
import operator


def modify(saga, what):
    value = saga['value']
    pointer = saga['pointer']
    operation = saga['story'][pointer]
    saga['pointer'] += 1
    saga['value'] = what(float(value), float(operation['operand']))
    return saga


def next(saga):
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    next_handler = saga['story'][saga['pointer']]['chapter']
    return requests.post(next_handler, json=saga, headers=headers)


def result(resp):
    if resp.status_code == 200:
        return resp.json()
    else:
        return {'errors': [{'url': resp.url, 'status_code': resp.status_code}]}


def apply(operator):
    return result(next(modify(cherrypy.request.json, operator)))


class Math(object):

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.expose
    def add(self):
        return apply(operator.add)

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.expose
    def subtract(self):
        return apply(operator.sub)

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.expose
    def multiply(self, ):
        return apply(operator.mul)

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.expose
    def divide(self):
        return apply(operator.div)

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.expose
    def stop(self):
        return {'result': cherrypy.request.json['value'], 'errors': []}

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.expose
    def index(self):
        return result(next(cherrypy.request.json))


if __name__ == "__main__":
    cherrypy.config.update({'server.socket_port': 8080, 'server.socket_host': '0.0.0.0'})
    cherrypy.tree.mount(Math(), "/")
    cherrypy.engine.start()
    cherrypy.engine.block()
