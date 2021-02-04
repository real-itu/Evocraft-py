import docker

def remove_image(client, container_name):
    try:
        client.images.remove(container_name)
    except Exception as e:
        print(
            "Can't remove image (this could be expected) with error {}".format(e)
        )

if __name__ == "__main__":
    client = docker.from_env()
    remove_image(client, "evocraft-server:latest")
