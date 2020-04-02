import os
import time
from datetime import datetime
import paho.mqtt.client as paho
import miio


## Logging to con
def log(level, msg):
    if ( level <= loglevel ):
        now = datetime.now()
        print(now.strftime("%Y-%m-%dT%H:%M:%S") + " " + str(level) + " " + msg)


## Receive the airpurifiers status and write it to mqtt
def updateMqttStateTopic():
    log(3, "Starting update of state-topic.")
    apStatus = ap.status()
    now = datetime.now()
    mqttClient.publish(mqtt_stateTopic + "TIMESTAMP", now.strftime("%Y-%m-%dT%H:%M:%S"))
    mqttClient.publish(mqtt_stateTopic + "airQualityIndex", apStatus.aqi)
    mqttClient.publish(mqtt_stateTopic + "airQualityIndexAvg", apStatus.average_aqi)
    mqttClient.publish(mqtt_stateTopic + "airTemperatureC", apStatus.temperature)
    mqttClient.publish(mqtt_stateTopic + "airRelHumidityPercent", apStatus.humidity)
    mqttClient.publish(mqtt_stateTopic + "fanMotorSpeed", apStatus.motor_speed)
    mqttClient.publish(mqtt_stateTopic + "fanLevel", apStatus.fan_level)
    mqttClient.publish(mqtt_stateTopic + "fanFavoriteSetLevel", apStatus.favorite_level)
    mqttClient.publish(mqtt_stateTopic + "filterUsedHours", apStatus.filter_hours_used)
    mqttClient.publish(mqtt_stateTopic + "filterRemainingPercent", apStatus.filter_life_remaining)
    mqttClient.publish(mqtt_stateTopic + "filterRfidProductId", apStatus.filter_rfid_product_id)
    mqttClient.publish(mqtt_stateTopic + "filterRfidTag", apStatus.filter_rfid_tag)
    mqttClient.publish(mqtt_stateTopic + "filterType", apStatus.filter_type.name)
    mqttClient.publish(mqtt_stateTopic + "deviceBuzzerEnabled", apStatus.buzzer)
    mqttClient.publish(mqtt_stateTopic + "deviceLedBrightnes", apStatus.led_brightness.name)
    mqttClient.publish(mqtt_stateTopic + "deviceChildLockActive", apStatus.child_lock)
    mqttClient.publish(mqtt_stateTopic + "devicePowerOn", apStatus.is_on)
    mqttClient.publish(mqtt_stateTopic + "devicePower", apStatus.power)
    mqttClient.publish(mqtt_stateTopic + "deviceMode", apStatus.mode.name)
    mqttClient.publish(mqtt_stateTopic + "statPurifiedVolumeM3", apStatus.purify_volume)
    mqttClient.publish(mqtt_stateTopic + "statTimeActive", apStatus.use_time)
    # mqttClient.publish(mqtt_stateTopic + "deviceBuzzerSetVolume", apStatus.buzzer_volume)
    # mqttClient.publish(mqtt_stateTopic + "deviceLedEnabled", apStatus.led)
    log(3, "Update of state-topic finished.")


## MQTT broker disconnected
def on_mqttDisconnect(client, userdata, rc):
    log(1, "MQTT broker disconnected")


## MQTT broker connected
def on_mqttConnect(client, userdata, flags, rc):
    log(1, "MQTT broker connected")

## Log unknown MQTT Message Data Values
def msgDataUnknown():
    log(2, "The data inside the MQTT topic is invalid")

## MQTT Subscription Loop Callback Function
def on_mqttMessage(client, userdata, message):
    mqttMsgData  = message.payload.decode("utf-8")
    mqttMsgTopic = message.topic
    log(2, "RECEIVED: " + mqttMsgTopic + ":" + mqttMsgData)
    if ( mqttMsgTopic == mqtt_cmdTopic+"devicePower" ):
        if (mqttMsgData == "on"):
            log(2, "ACTION: Power on")
            ap.on()
        elif (mqttMsgData == "off"):
            log(2, "ACTION: Power off")
            ap.off()
        else:
            msgDataUnknown()
    elif ( mqttMsgTopic == mqtt_cmdTopic+"fanLevel" ):
        if ( mqttMsgData == "1" ):
            log(2, "ACTION: Set fanLevel 1")
            ap.set_fan_level(1)
        elif ( mqttMsgData == "2" ):
            log(2, "ACTION: Set fanLevel 2")
            ap.set_fan_level(2)
        elif ( mqttMsgData == "3" ):
            log(2, "ACTION: Set fanLevel 3")
            ap.set_fan_level(3)
        else:
            msgDataUnknown()
    elif ( mqttMsgTopic == mqtt_cmdTopic+"deviceMode" ):
        if ( mqttMsgData == "Auto" ):
            log(2, "ACTION: Set deviceMode Auto")
            ap.set_mode(miio.airpurifier_miot.OperationMode.Auto)
        elif ( mqttMsgData == "Fan" ):
            log(2, "ACTION: Set deviceMode Fan")
            ap.set_mode(miio.airpurifier_miot.OperationMode.Fan)
        elif ( mqttMsgData == "Favorite" ):
            log(2, "ACTION: Set deviceMode Favorite")
            ap.set_mode(miio.airpurifier_miot.OperationMode.Favorite)
        elif ( mqttMsgData == "Silent" ):
            log(2, "ACTION: Set deviceMode Silent")
            ap.set_mode(miio.airpurifier_miot.OperationMode.Silent)
        else:
            msgDataUnknown()
    else:
        log(2, "The MQTT topic is invalid")

    ## Force update of STATE after switching things
    time.sleep(5)
    updateMqttStateTopic()



## --------------------------------------------------------------------------------------------------



## Get confiuration
configfile = os.getenv('airpurifierConfigFile', 'airpurifier.conf')
exec(open(configfile).read())


log(1, "---------------- Starting Air Purifier Bridge ----------------")
log(1, "Loaded confguration file: " + configfile)


## The airpurifier object
ap = miio.airpurifier_miot.AirPurifierMiot(ip=miot_ip, token=miot_token)


## The MQTT Client object
mqttClient = paho.Client("airPurifierBridge")
log(1, "Connecting to MQTT broker " + mqtt_ip)
mqttClient.connect(mqtt_ip)
time.sleep(5)


## Subscribe to mqtt command topics and start the loop
mqtt_cmdTopic = mqtt_topic + "/CMD/"
mqttClient.subscribe(mqtt_cmdTopic+"#")
mqttClient.on_message = on_mqttMessage
mqttClient.on_connect = on_mqttConnect
mqttClient.on_disconnect = on_mqttDisconnect
log(1, "Starting the subscription loop on " + mqtt_cmdTopic)
mqttClient.loop_start()


## State Update Loop
mqtt_stateTopic = mqtt_topic + "/STATE/"
log(1, "Starting the state update loop on " + mqtt_stateTopic)
while True:
    updateMqttStateTopic()
    time.sleep(update_interval)
