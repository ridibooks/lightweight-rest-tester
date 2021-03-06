docker-compose -f ./test/json-server/docker-compose.test.yml down
docker-compose -f ./test/json-server/docker-compose.test.yml up --build -d

echo "Waiting until container becomes healthy..."

retries=0
while ! docker ps | grep json-server | grep healthy | grep -v unhealthy; do
    sleep 1

    if [ "$retries" -gt 10 ]
    then
        break
    fi

    retries=$(($retries+1))
done

if [ "$retries" -gt 10 ]
then
    echo "Fail to load json-server."
else
    echo "json-server is ready."
    tox
fi
