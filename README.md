# omlx

A lightweight CLI tool for managing your macOS applications list. Keep track of installed apps and sync them across machines.

> Fork of [jundot/omlx](https://github.com/jundot/omlx)

## Features

- Track installed applications
- Add and remove apps from your managed list
- Open apps directly from the CLI
- Simple JSON-based configuration
- Homebrew formula for easy installation

## Installation

### Via Homebrew

```bash
brew tap your-username/omlx
brew install omlx
```

### Manual

```bash
git clone https://github.com/your-username/omlx.git
cd omlx
pip install -r requirements.txt
```

## Usage

```bash
# List all tracked apps
omlx list

# Add an app to your list
omlx add "Visual Studio Code"

# Remove an app from your list
omlx remove "Visual Studio Code"

# Open a tracked app
omlx open "Visual Studio Code"

# Show help
omlx --help
```

## Configuration

Configuration is stored at `~/.config/omlx/config.json`.

```json
{
  "apps": [
    "Visual Studio Code",
    "iTerm",
    "Slack"
  ]
}
```

## Development

### Requirements

- Python 3.8+

### Running Tests

```bash
python -m pytest tests/
```

### Running Locally

```bash
python omlx.py --help
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feat/my-feature`)
3. Commit your changes (`git commit -m 'feat: add my feature'`)
4. Push to the branch (`git push origin feat/my-feature`)
5. Open a Pull Request

Please check the [issue tracker](../../issues) before submitting a new issue.

## License

GPL-3.0 — see [LICENSE](LICENSE) for details.
