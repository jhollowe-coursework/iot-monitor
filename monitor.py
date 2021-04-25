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


def doMetrics():
  if cfg.get("metrics") is None:
    print("No metrics to publish, exiting")
    # send a SIGINT signal so the connection is gracefully closed
    os.kill(os.getpid(), signal.SIGINT)
    return


  while(True):
    # shell metrics
    if cfg.get("metrics").get("shell") is not None:
      for metricName in cfg.get("metrics").get("shell").keys():
        outputFd = os.popen(cfg.get("metrics").get("shell").get(metricName, "echo No command specified"))
        client.publish(topic="hosts/"+cfg.get("clientId")+"/"+metricName, payload=outputFd.read(), qos=mqtt.QoS.AT_LEAST_ONCE)

    # python metrics
    if cfg.get("metrics").get("python") is not None:
      for metricName in cfg.get("metrics").get("python").keys():
        client.publish(topic="hosts/"+cfg.get("clientId")+"/"+metricName, payload=str(eval(cfg.get("metrics").get("python").get(metricName, ""))), qos=mqtt.QoS.AT_LEAST_ONCE)

    print("sent {} shell and {} python metrics".format(len(cfg.get("metrics").get("shell") or []),len(cfg.get("metrics").get("python") or [])))
    time.sleep(float(cfg.get("delay") or 1))


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

  # Spin up resources
  event_loop_group = io.EventLoopGroup(1)
  host_resolver = io.DefaultHostResolver(event_loop_group)
  client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

  # create MQTT client
  client = mqtt_connection_builder.mtls_from_path(
            endpoint=cfg.get("endpoint"),
            cert_filepath=cfg.get("certFile")  or "certs/aws-iot.crt",
            pri_key_filepath=cfg.get("keyFile") or "certs/aws-iot.key",
            client_bootstrap=client_bootstrap,
            client_id=cfg.get("clientId"),
            clean_session=False,
            keep_alive_secs=60)

  print("Connecting with client ID '{}'...".format(cfg.get("clientId")))

  connect_future = client.connect()

  # Future.result() waits until a result is available
  connect_future.result()
  print("Connected!")
  print("Press Ctrl+C to exit")

  # publish existence
  client.publish(topic="activity/hosts/add", payload=cfg.get("clientId"), qos=mqtt.QoS.AT_LEAST_ONCE)

  # continually gather and send metrics until Ctrl+C is pressed
  doMetrics()



if __name__ == '__main__':
  signal.signal(signal.SIGINT, sigint_handler)
  main()
