# Bachelor thesis

Controlling a mechanical arm with 3 DoF (3D space) with [Microsoft Kinect](https://github.com/saleone/bachelor-kinect-client)

## How to start
1. Flash [Firmata](https://github.com/firmata/arduino) sketch on Arduino (needs to support servo motors).
2. Contruct the mechanical arm:
    * Base joint rotates in ground plane.
    * Other two joints make up a planar manipulator perpendicular to the ground plane
3. Install all the dependencies with `pipenv install`
4. Adjust link lengths in [server.py](./src/server.py)
5. Run the server application `pipenv run python src/server.py`
6. Send coordinates to the server (TCP server) in the following format: `XX;YY;ZZ`, where XX and YY define ground plane.

> There is simple client provided in [src/client.py](./src/client.py). Run it with `pipenv run python src/client.py`.

## Contributing
Everything is welcome, post a pull request. Try to create your own client and share it here.

## License
[MIT license](./LICENSE.md), unless specified otherwise. 
