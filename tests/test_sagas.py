import cherrypy
import requests
from sagas.sagas import Math

headers = lambda: {'Content-type': 'application/json', 'Accept': 'application/json'}
url = lambda x='': 'http://127.0.0.1:4711/{}/'.format(x)

def saga():
    return {
        "story":
            [
                {
                    "chapter": url('add'),
                    "operand": 7
                },
                {
                    "chapter": url('subtract'),
                    "operand": 2
                },
                {
                    "chapter": url('multiply'),
                    "operand": 4
                },
                {
                    "chapter": url('add'),
                    "operand": 89
                },
                {
                    "chapter": url('divide'),
                    "operand": 12
                },
                {
                    "chapter": url('subtract'),
                    "operand": 7
                },
                {
                    "chapter": url('add'),
                    "operand": 72
                },
                {
                    "chapter": url('divide'),
                    "operand": 2
                },
                {
                    "chapter": url('stop')
                }
            ],
        "value": 9.3,
        "pointer": 0
    }


def setup_module():
    cherrypy.tree.mount(Math(), "/")
    cherrypy.config.update({'server.socket_port': 4711})
    cherrypy.engine.start()


def teardown_module():
    cherrypy.engine.stop()


def test_performing_a_series_of_operations_as_the_story_of_a_saga():
    result = requests.post(url(), json=saga(), headers=headers()).json()
    expected = {'result': 38.59166666666667, 'errors': []}
    assert expected == result


def test_handling_malformed_saga():
    s = saga()
    s['story'][5]['operand'] = 'foobar'
    result = requests.post(url(), json=s, headers=headers()).json()
    expected = {'errors': [{'status_code': 500, 'url': 'http://127.0.0.1:4711/subtract/'}]}
    assert expected == result


def test_handling_malformed_url():
    s = saga()
    s['story'][5]['chapter'] = url('foobar')
    result = requests.post(url(), json=s, headers=headers()).json()
    expected = {'errors': [{'status_code': 404, 'url': 'http://127.0.0.1:4711/foobar/'}]}
    assert expected == result
