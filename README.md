# gotify-gnome-client

Simple Gotify client for Gnome desktop, to get Gotify messages pop up in your Gnome Desktop

![Screenshot from 2024-10-01 16-37-57](https://github.com/user-attachments/assets/0b842a80-5852-4835-9c5e-a02b64068896)

## Usage

```
$ ./gotify_gnome_desktop.py
Usage: gotify_gnome_desktop.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  init  Initialize the configuration file and setup an autostarting config
  run   Run the Gotify to Gnome notification service
```

## Configuration

It should be self generated as part of `init`, for an example see [config.ini](config.ini)


## The inner workings

The script is build with python3, click, gi, autostart, and packaged via pyinstaller


## Recommended setup

As there are dependencies the best option is to fetch the pre-built binary version, ( see build steps defined in github actions )
Second best option is to use virtal envirments.
```
sudo apt-get install python3-venv
python3 -m venv .venv
source .venv/bin/activate
pip install click
pip install gotify
pip install websockets
```
for the next libary we need few system packages again
```
sudo apt-get install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0
pip install pycairo
pip install PyGObject
```

and only after this run the init by ( still in the activated venv)

```
gotify_gnome_desktop.py init
```

Fill out your gotify url and API key values

Log out, and log in, it should be running in the background already.


## License

This project is licensed under the MIT License, see the [LICENSE](LICENSE)

## Contributing

Contributions are welcome! Please submit a pull request with your changes.
