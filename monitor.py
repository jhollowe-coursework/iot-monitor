from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
from uuid import uuid4
import sys, os, time, signal, json
import threading
import psutil

client = None
cfg = {}

# cleanly exit when Ctrl+C is pressed
def sigint_handler(sig, frame):
  if client is not None:
    # send host disconnect
    client.publish(topic="activity/hosts/remove", payload=cfg.get("clientId"), qos=mqtt.QoS.AT_LEAST_ONCE)

    client.disconnect().result()
    print("Disconnected!")
  sys.exit(0)


def main():
  global cfg, client

  # get the config file from command line argument or default to "config.json"
  configPath = sys.argv[1] if len(sys.argv) >= 2 else "config.json"

  # read in the config
  try:
    with open(configPath, "r") as configFile:
        cfg = json.load(configFile)
  except:
    print(f'Unable to load config file "{configPath}"')
    sys.exit(1)

  if cfg.get("clientId") is None:
    cfg["clientId"] = "monitor-" + str(uuid4())

  if cfg.get("endpoint") is None:
    print("endpoint required")
    sys.exit(1)



if __name__ == '__main__':
  signal.signal(signal.SIGINT, sigint_handler)
  main()
