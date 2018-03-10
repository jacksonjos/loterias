# Lottery
This repository contains a project to extract from a Brazilian lottery game called Lotofácil[1] and to check if some lottery ticket played won some game.

As I already have created the Scrapy project and wrote the code this documentation doesn't tell how to create a Scrapy project. If you want to learn it check Scrapy framework website[3].

The data's about winning ticket and its format can be seen at `data/lotofacil/ganhos.json`.

This project uses Python3.6 and Scrapy.

*PS*: This project wasn't developed for production. This is the reason this documentation doesn't have information about version of softwares, libraries and Python modules. For more information you can check at projects Dockerfile.


# Building and running this project
    1. Modify Scrapy project owner typing:
    $ sudo chown -R jackson:jackson data/lotofacil/

    2. To build this project at main repository directory type:
    $ docker build -t lotofacil_i .

    3. To run start the projects container and do a a directory binding to store code and modify it while running the container and go to inside it type:
    $ docker run --name lotofacil_c --mount type=bind,source="$(pwd)"/data,target=/data -i -t lotofacil_i /bin/sh

    4. To run this project, i.e., run Scrapy to crawl games data and check if some ticket won the games data crawled, *when inside the container*, type:
    $ cd /data/
    $ scrapy crawl -a "first_game=number_of_first_game" -a "last_game=number_of_last_game" lotofacil


# Stop the container and starting it again
    1. To stop this container type:
    $ docker stop lotofacil_c

    2. To start this container type:
    $ docker start lotofacil_c

    3. To enter the container type:
    $ docker exec -ti lotofacil_c /bin/sh


# To remove the Docker container and Docker image
    1. To remove the container type:
    $ docker rm lotofacil_c

    1. To remove the image type:
    $ docker rmi lotofacil_i


<!-- # scrapy startproject lotofacil -->
<!-- # remover all containers: docker rm $(docker ps -a -q) -->
<!-- # docker system prune -->


# References
[1] http://loterias.caixa.gov.br/wps/portal/loterias/landing/lotofacil/  
[2] Projects Docker file is inspired by: https://hub.docker.com/r/aciobanu/scrapy/~/dockerfile/  
[3] https://scrapy.org/  
