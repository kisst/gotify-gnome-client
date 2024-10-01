#!/usr/bin/env python3
"""
simple gotify to gnome toast application
"""
import click
import sys
import os
import configparser
import asyncio
from gotify import AsyncGotify
from gi import require_version

require_version("Notify", "0.7")
from gi.repository import Notify


def load_config():
    """Load configuration from file"""
    config_file = os.path.join(os.path.expanduser("~"), ".config", "gotify.ini")

    # Check if file exists
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file '{config_file}' not found")

    # Check if file is valid
    try:
        config = configparser.ConfigParser()
        config.read(config_file)
        if not config.defaults():
            raise ValueError(f"Config file '{config_file}' is empty or invalid")
    except configparser.Error as e:
        raise ValueError(f"Failed to parse config file '{config_file}': {e}")

    return config, config_file


def init_notification(app_name):
    """Initialize notification system"""
    try:
        Notify.init(app_name)
    except Exception as e:
        print(f"Error: Failed to initialize notification system - {e}")
        sys.exit(1)


async def push_messages(config):
    """Fetch messages from Gotify and send to gnome"""
    try:
        async_gotify = AsyncGotify(
            base_url=config["DEFAULT"]["SERVER_URL"],
            client_token=config["DEFAULT"]["API_KEY"],
        )
        async for msg in async_gotify.stream():
            message = str(msg["title"]) + ' says "' + msg["message"] + '"'
            Notify.Notification.new(message).show()
    except Exception as e:
        print(f"Error: Failed to fetch messages from Gotify - {e}")
        sys.exit(1)


def generate_config():
    """Generate configuration file from user input"""
    config_file = os.path.join(os.path.expanduser("~"), ".config", "gotify.ini")
    config = configparser.ConfigParser()
    config["DEFAULT"] = {}

    server_url = input("Enter Gotify server URL: ")
    api_key = input("Enter Gotify API key: ")

    config["DEFAULT"]["SERVER_URL"] = server_url
    config["DEFAULT"]["API_KEY"] = api_key

    try:
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, "w") as f:
            config.write(f)
        print(f"Configuration file generated at {config_file}")
    except Exception as e:
        print(f"Error: Failed to write configuration file - {e}")
        sys.exit(1)


def validate_config(config):
    """Validate configuration file"""
    required_keys = ["SERVER_URL", "API_KEY"]
    for key in required_keys:
        if not config.has_option("DEFAULT", key):
            return False
    return True


def install_autostart():
    """Install autostart hook"""
    try:
        # Inline autostart config definition
        autostart_definition = """[Desktop Entry]
Name=Gotify GNOME relay
Comment=Relay Gotify messages to GNOME notifications
Type=Application
Exec=<runtime> <script_location> run
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true"""
        # replace the template with the actual script location, and python executable
        autostart_definition = autostart_definition.replace(
            "<script_location>", os.path.abspath(__file__)
        )
        autostart_definition = autostart_definition.replace("<runtime>", sys.executable)

        # Create the autostart user directory if it doesn't exist
        autostart_user_dir = os.path.join(
            os.path.expanduser("~"), ".config", "autostart"
        )
        os.makedirs(autostart_user_dir, exist_ok=True)

        # Write out the autostart config file
        autostart_config_file = os.path.join(autostart_user_dir, "gotify_gnome.desktop")
        with open(autostart_config_file, "w") as f:
            f.write(autostart_definition)
    except Exception as e:
        print(f"Error: Failed to install autostart config - {e}")
        sys.exit(1)


@click.group()
def cli():
    pass


@cli.command()
def init():
    """
    Initialize the configuration file
    and setup an autostarting config
    """
    try:
        config, config_file = load_config()
        click.echo(f"Configuration file found at {config_file}")
        if not validate_config(config):
            print(config)
            raise ValueError("Invalid configuration file")
    except (FileNotFoundError, ValueError):
        generate_config()
        click.echo("Configuration file generated successfully!")
    install_autostart()
    click.echo("User autostart config installed successfully!")


@cli.command()
def run():
    """Run the Gotify to Gnome notification service"""
    config, config_file = load_config()

    if not os.path.exists(config_file):
        print(
            "Config file not found. Please run `gotify init` to generate the configuration file."
        )
        sys.exit(1)

    if not validate_config(config):
        print(
            "Invalid configuration file. Please run `gotify init` to generate a new configuration file."
        )
        sys.exit(1)

    init_notification("Gotify")

    try:
        asyncio.run(push_messages(config))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli()
