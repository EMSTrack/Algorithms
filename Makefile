none: 
	echo "\nThis Makefile installs Python 3.7 and required Python libraries. \n\
	Either run 'make docker' or 'make local'". 

install-docker: 
	docker-compose up 
	docker cp ../data-cruz-roja-clean 
# 	docker run 

install-mac:
	brew install python3  
	python3.7 -m pip install -r requirements.txt
	echo "Test run simple simulation. "
	python3.7 run-simulation configurations/example.yaml

install-ubuntu:
	apt-get install python3
	python3.7 -m pip install -r requirements.txt
	echo "Test run simple simulation. "
	python3.7 run-simulation configurations/example.yaml