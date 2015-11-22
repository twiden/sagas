import cherrypy
import requests
from sagas.sagas import Math


saga = {
    "story":
        [
            {
                "chapter": "http://127.0.0.1:8080/add/",
                "operand": 7
            },
            {
                "chapter": "http://127.0.0.1:8080/subtract/",
                "operand": 2
            },
            {
                "chapter": "http://127.0.0.1:8080/multiply/",
                "operand": 4
            },
            {
                "chapter": "http://127.0.0.1:8080/add/",
                "operand": 89
            },
            {
                "chapter": "http://127.0.0.1:8080/divide/",
                "operand": 12
            },
            {
                "chapter": "http://127.0.0.1:8080/subtract/",
                "operand": 7
            },
            {
                "chapter": "http://127.0.0.1:8080/add/",
                "operand": 72
            },
            {
                "chapter": "http://127.0.0.1:8080/divide/",
                "operand": 2
            },
            {
                "chapter": "http://127.0.0.1:8080/stop/"
            }
        ],
    "value": 9.3,
    "pointer": 0
}


def setup_module():
    cherrypy.tree.mount(Math(), "/")
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.engine.start()


def teardown_module():
    cherrypy.engine.stop()


def test_performing_a_series_of_operations_as_the_story_of_a_saga():
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    result = requests.post('http://127.0.0.1:8080/', json=saga, headers=headers).json()
    assert {'result': 38.59166666666667} == result
