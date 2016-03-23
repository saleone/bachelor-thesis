# Bachelor thesis

Robot with three degrees of freedom controled with Kinect sensor and 3 stepper motors.

## Running the script
To make sure that the script can talk to arduino over serial connection we need to add user to the group which owns the serial port.
On Linux this is mostly the 'dialout' group but for some users/distros (like me/Arch linux) it's different.
So first, the easy way, you can try to call
```bash
sudo usermod -a -G dialout [your-username]
```
If you get error that the 'dialout' group does not exist try to run
```bash
stat -c "%G" [port]
```
This will return you the group that owns the specified port ('/dev/ttyACM0' is the port that my computer uses, like most distros). Change the port to match your computer and you will get the group name. After that run the following command (replace the group-name with whatever previous command returned)
```bash
sudo usermod -a -G [group-name] [your-username]
```
Restart your computer and you should be fine.

**OR**

You can just run
```bash
sudo chown [your-username] [port]
```
to get temporary access to the port without restarting, but this is not persistent you will have to do it every time you reconnect your board.


Besides that you need to upload FirmataPlus to your Arduino. Instructions can be found [here](https://github.com/MrYsLab/pymata-aio/wiki/Uploading-FirmataPlus-to-Arduino)


## Sources
* [socket - Low-level networking interface](https://docs.python.org/3/library/socket.html)
* [Socket Programming HOWTO](https://docs.python.org/3/howto/sockets.html) - Gordon McMillan
* [ZeroMQ - The Guide](http://zguide.zeromq.org/py:all)
* [Get idVendor and idProduct of your Arduino/USB devices](http://arduino-er.blogspot.ba/2015/04/get-idvendor-and-idproduct-of-you.html)
* [Python auto detect Arduino connected serial port](https://arduino-er.blogspot.ba/2015/04/python-auto-detect-arduino-connect.html)
* [Arduino - Firmata Library](https://arduino.cc/en/Reference/Firmata)
* [tino/pyFirmata](https://github.com/tino/pyFirmata)
* [MrYsLab/pymata-aio wiki](https://github.com/MrYsLab/pymata-aio/wiki)

## License
This thesis/project code is currently (I must ask permission from my college to confirm this, not sure yet) licensed under the MIT license, unless specified otherwise. Check the [LICENSE.md](./LICENSE.md) file for more info.
