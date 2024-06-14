up:
	docker build . -t users
	docker run -d -p 3080:3080 --name users-container --network=host users

down:
	docker stop users-container
	docker rm users-container
	docker rmi users
