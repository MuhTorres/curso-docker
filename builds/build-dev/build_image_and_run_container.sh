echo 'Nome da imagem: '
read image_name

echo 'Nome do container: '
read container_name

docker image build -t $image_name .

docker container run -it \
-v $(pwd):/app \
-p 88:8000 \
--name $container_name \
$image_name