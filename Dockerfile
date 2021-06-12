# Build: docker build -t [build-name] .
# Run: docker run -it --rm -p 5001:5001 -p 25565:25565 [build-name]
# Connections to the server and API are now available on the host machine.

FROM openjdk:8

WORKDIR /work-it

COPY . .

RUN java -jar spongevanilla-1.12.2-7.3.0.jar
RUN head -n -1 eula.txt > temp.txt \
    && mv temp.txt eula.txt \
    && echo "eula=True" >> eula.txt

CMD java -jar spongevanilla-1.12.2-7.3.0.jar
