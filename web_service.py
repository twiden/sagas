import cherrypy
import json

saga = {
    'story': [
        {
            'chapter': 'url1',
            'operand': 'value1'
        },
        {
            'chapter': 'url2',
            'operand': 'value2'
        },
    ],
    'value': 'value'
    'pointer': 'operations index'
    'title': 'uuid'
}

def read_chapter(saga, what):
    job = json.loads(saga)
    value = job['value']
    pointer = job['pointer']
    operation = job['story'][pointer]
    next_pchapter = job['story'][pointer + 1]
    job['pointer'] += 1
    job['value'] = what(value, operation['value'])
    return next_processor, job

def pass_on(next_processor, job):
    pass

class Math(object):

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def add(self, saga):
        pass_on(read_chapter(saga, lambda x, y: x + y))
        return 1

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def subtract(self, saga):
        pass_on(read_chapter(saga, lambda x, y: x - y))
        return 1

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def multiply(self, saga):
        pass_on(read_chapter(saga, lambda x, y: x * y))
        return 1

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def divide(self, saga):
        pass_on(read_chapter(saga, lambda x, y: x / y))
        return 1

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def persist(self, saga):
        return 1


def run():
    cherrypy.config.update({'server.socket_port': 8080, 'server.socket_host': '0.0.0.0'})
    cherrypy.tree.mount(Math(), "/")
    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == "__main__":
    run()
