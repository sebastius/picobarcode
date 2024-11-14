from machine import UART, Pin
import network
import time
from umqtt.simple import MQTTClient

# Configure your WiFi and MQTT details
WIFI_SSID = "ssid"
WIFI_PASSWORD = "password"
MQTT_BROKER = "broker"
MQTT_TOPIC = "topic"

# Set up UART
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# Set up WiFi connection (ESP8266 module or compatible is required for Pico)
def connect_wifi():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        print("Connecting to WiFi...")
        time.sleep(1)
    print("Connected to WiFi:", wlan.ifconfig())

# Set up MQTT
def connect_mqtt():
    client = MQTTClient("barcode_scanner", MQTT_BROKER)
    client.connect()
    print("Connected to MQTT Broker")
    return client

# Main loop to read from UART and publish to MQTT
def main():
    connect_wifi()
    client = connect_mqtt()

    while True:
        if uart.any():
            barcode_data = uart.read().decode('utf-8').strip()
            print("Received barcode:", barcode_data)
            client.connect()
            client.publish(MQTT_TOPIC, barcode_data)
            client.disconnect()
            print(f"Published barcode data '{barcode_data}' to MQTT topic '{MQTT_TOPIC}'")
            time.sleep(1)  # Small delay to avoid multiple rapid scans

try:
    main()
except KeyboardInterrupt:
    print("Stopped by user")

