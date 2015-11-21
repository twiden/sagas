start:
	python sagas/sagas.py

example:
	curl -H "Content-Type: application/json" -X POST -d "@sagas/saga.json" http://localhost:8080/add

test: start example
