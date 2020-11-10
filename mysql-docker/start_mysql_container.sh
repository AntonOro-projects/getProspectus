docker pull mysql
docker run --rm --network host --name prospectusMySQL -v $(pwd)/data:/var/lib/mysql --mount type=bind,src=$(pwd)/my.cnf,dst=/etc/my.cnf -e MYSQL_ROOT_PASSWORD=getprospectus -d mysql:latest

