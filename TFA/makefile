up:
	docker build . -t tfa
	docker run -d -p 3081:3081 --name tfa-container --network=host tfa

down:
	docker stop tfa-container
	docker rm tfa-container
	docker rmi tfa
