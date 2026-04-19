#!/usr/bin/env python3
"""omlx - A command-line tool for managing and launching applications.

Fork of jundot/omlx with additional features and improvements.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

__version__ = "0.1.0"
__author__ = "omlx contributors"

DEFAULT_CONFIG_PATH = Path.home() / ".config" / "omlx" / "config.json"


def load_config(config_path: Path = DEFAULT_CONFIG_PATH) -> dict:
    """Load configuration from JSON file.

    Args:
        config_path: Path to the configuration file.

    Returns:
        Dictionary containing configuration values.
    """
    if not config_path.exists():
        return {}
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config: dict, config_path: Path = DEFAULT_CONFIG_PATH) -> None:
    """Save configuration to JSON file.

    Args:
        config: Dictionary of configuration values to save.
        config_path: Path to the configuration file.
    """
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def list_apps(config: dict) -> None:
    """List all registered applications."""
    apps = config.get("apps", {})
    if not apps:
        print("No applications registered.")
        return
    print(f"{'Name':<20} {'Command':<40} {'Description'}")
    print("-" * 80)
    for name, info in sorted(apps.items()):
        cmd = info.get("command", "")
        desc = info.get("description", "")
        print(f"{name:<20} {cmd:<40} {desc}")


def add_app(config: dict, name: str, command: str, description: str = "") -> None:
    """Register a new application."""
    if "apps" not in config:
        config["apps"] = {}
    config["apps"][name] = {"command": command, "description": description}
    save_config(config)
    print(f"Registered '{name}' -> {command}")


def remove_app(config: dict, name: str) -> None:
    """Remove a registered application."""
    apps = config.get("apps", {})
    if name not in apps:
        print(f"Application '{name}' not found.", file=sys.stderr)
        sys.exit(1)
    del config["apps"][name]
    save_config(config)
    print(f"Removed '{name}'.")


def launch_app(config: dict, name: str, extra_args: list) -> None:
    """Launch a registered application."""
    apps = config.get("apps", {})
    if name not in apps:
        print(f"Application '{name}' not found.", file=sys.stderr)
        sys.exit(1)
    command = apps[name]["command"]
    full_cmd = command.split() + extra_args
    subprocess.run(full_cmd, check=False)


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="omlx",
        description="omlx - Manage and launch your applications from the command line.",
    )
    parser.add_argument("--version", action="version", version=f"omlx {__version__}")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH, help="Path to config file")

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list", help="List registered applications")

    add_parser = subparsers.add_parser("add", help="Register an application")
    add_parser.add_argument("name", help="Application name")
    add_parser.add_argument("cmd", help="Command to execute")
    add_parser.add_argument("--description", "-d", default="", help="Short description")

    rm_parser = subparsers.add_parser("remove", help="Remove an application")
    rm_parser.add_argument("name", help="Application name")

    run_parser = subparsers.add_parser("run", help="Launch an application")
    run_parser.add_argument("name", help="Application name")
    run_parser.add_argument("args", nargs=argparse.REMAINDER, help="Extra arguments")

    return parser


def main() -> None:
    """Main entry point for omlx CLI."""
    parser = build_parser()
    args = parser.parse_args()

    config = load_config(args.config)

    if args.command == "list":
        list_apps(config)
    elif args.command == "add":
        add_app(config, args.name, args.cmd, args.description)
    elif args.command == "remove":
        remove_app(config, args.name)
    elif args.command == "run":
        launch_app(config, args.name, args.args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
