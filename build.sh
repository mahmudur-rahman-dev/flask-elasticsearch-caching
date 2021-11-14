sudo docker build -t query-service . &&
sudo docker save query-service > ../query-service.tar &&
cd .. &&
scp query-service.tar penta@202.181.14.19:/home/penta/new_query_service
