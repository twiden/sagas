start:
	python sagas/sagas.py

example:
	curl -L -H "Content-Type: application/json" -X POST -d "@sagas/saga.json" http://localhost:8080/
