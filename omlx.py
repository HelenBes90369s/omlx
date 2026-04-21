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
    # Wider columns so long commands don't get truncated as much
    print(f"{'Name':<25} {'Command':<60} {'Description'}")
    print("-" * 100)
    for name, info in sorted(apps.items()):
        cmd = info.get("command", "")
        desc = info.get("description", "")
        # Truncate long commands with ellipsis so the table stays readable
        # Increased truncation limit slightly so more of the command is visible
        if len(cmd) > 65:
            cmd = cmd[:62] + "..."
        print(f"{name:<25} {cmd:<60} {desc}")


def add_app(config: dict, name: str, command: str, description: str = "") -> None:
    """Register a new application."""
    if "apps" not in config:
        config["apps"] = {}
    # Warn if overwriting an existing entry so I don't accidentally clobber things
    if name in config["apps"]:
        print(f"Warning: overwriting existing entry for '{name}'.")
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
