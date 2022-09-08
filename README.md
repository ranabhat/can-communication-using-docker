### Instructions for Creating a Container for CAN Communication

1. Build the docker image `can-docker-test:latest`
2. Now that we have our customized container image for CAN in our target system, we can execute it `docker run -it --rm --name=can-test --net=host --cap-add="NET_ADMIN" -v /dev:/dev -v /tmp:/tmp -v /run/udev/:/run/udev/ can-docker-test`

The main secret behind the setup and usage of CAN on containers  is the usage of the following flags when running your container:

    --net=host : This will make Docker to uses the host's network stack for the container.
    --cap-add=NET_ADMIN : For interacting with the network stack, this allow to modify the network interfaces.

Once within the container console, you'll have to configure the CAN Network. This process is much similar to the setup of CAN on Linux.

We'll set only one CAN interface. But depending on your CoM, you may have more CAN interfaces available.

1. Configure the CAN0 interface with a bitrate of 125000 bps: `ip link set can0 type can bitrate 125000`
2. If everything went fine (no complaints!), bring that interface up: `ip link set can0 up`
3. To be sure that the interface is now set and ready, check it by using the following command: `ip link show`


### Simple testing with can-utils
1. Use the cansend <interface> <message> to send CAN messages on a given interface. Like for example:
`cansend can0 115#010000000000`
2. Listen the can messages:  `candump can0`


### Docker Compose File 

Build the docker image first

### Reference

1. [Toradex Can Container Develoment Documentation](https://developer.toradex.com/torizon/how-to/peripheral-access/how-to-use-can-on-torizoncore/)
2. [Github docker-compose] (https://github.com/toradex/torizon-samples/blob/bullseye/debian-container/demonstration/docker-compose.arm64.yml)

