How to run the container:

docker pull mysql
docker run --rm --network host --name snekdb --mount type=bind,src=/home/rasmus/TDDE41/deploy/mysql-docker/my.cnf,dst=/etc/my.cnf -e MYSQL_ROOT_PASSWORD=snekboys -d mysql:latest

Or just run the start_mysql_container.sh script



