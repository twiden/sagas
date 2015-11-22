start:
	python sagas/sagas.py

example:
	curl -L -H "Content-Type: application/json" -X POST -d "@data/saga.json" http://localhost:8080/

test:
	py.test tests/
