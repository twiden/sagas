import cherrypy
import requests
import operator


def update_value(saga, what):
    value = saga['value']
    pointer = saga['pointer']
    operation = saga['story'][pointer]
    saga['pointer'] += 1
    saga['value'] = what(float(value), float(operation['operand']))
    return saga


def pass_on(saga):
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    next = saga['story'][saga['pointer']]['chapter']
    return requests.post(next, json=saga, headers=headers).json()


def read_on(operator):
    return pass_on(update_value(cherrypy.request.json, operator))


class Math(object):

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.expose
    def add(self):
        return read_on(operator.add)

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.expose
    def subtract(self):
        return read_on(operator.sub)

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.expose
    def multiply(self, ):
        return read_on(operator.mul)

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.expose
    def divide(self):
        return read_on(operator.div)

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.expose
    def stop(self):
        return {'result': cherrypy.request.json['value']}


def run():
    cherrypy.config.update({'server.socket_port': 8080, 'server.socket_host': '0.0.0.0'})
    cherrypy.tree.mount(Math(), "/")
    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == "__main__":
    run()
