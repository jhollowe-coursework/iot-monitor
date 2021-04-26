# iot-monitor
A tool using AWS IoT Core's MQTT to gather and send metrics on the device

**NOTE:** This program runs arbitrary shell and python code contained in the `config.json` file. Do not run this program with unknown scripts in the config file. Do not use config files from other people (the default config file *should* be safe). For liability and warranty information, see [LICENSE](LICENSE).

## Getting Started

### Environment

#### Devcontainer (Recommended)
1. Install Docker ([Instructions](https://www.docker.com/get-started))
2. Install Visual Studio Code ([Instructions](https://code.visualstudio.com/download))
3. Install the ["Remote - Containers" extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
4. Clone this repository into a container ([Instructions](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers))

#### Manual Installation

1. Install Python 3 ([Instructions](https://realpython.com/installing-python/))
2. Install Pip for Python 3 ([Instructions](https://pip.pypa.io/en/stable/installing/))
3. clone this repo with `git clone https://github.com/jhollowe/iot-monitor.git`
4. Install dependencies with `pip3 install --user -r requirements.txt` (running in this repo's directory)

### Configuration

1. Copy the private key and certificate for your Thing into the certs directory
2. Edit the `config.json` file with the path to both files
3. Edit the `config.json` file with the endpoint for your thing (look in the "Interact" section of your Thing in the AWS console)
4. Edit the region if needed

### Execution

1. Run the monitor using `python monitor.py`
2. To use a configuration file other than `config.json`, use `python monitor.py <config file>`
