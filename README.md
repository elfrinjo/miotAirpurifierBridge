# POC: Xiaomi Airpurifier 3H MQTT Bridge
This is a proof-of-concept, lacking a lot of errorhandling.

The Xiaomi Airpurifier 3H uses the (new) miot api.
This script bridges the air pufifier to the following state and control topics in mqtt.

These topics are reported from the device:

| STATE Topic                                | Values to expect             | Meaning                                                                    |
|--------------------------------------------|------------------------------|----------------------------------------------------------------------------|
| `{mqtt_topic}/STATE/TIMESTAMP`             | 2020-03-29T15:44             | Timestamp of the last state update                                         |
| `{mqtt_topic}/STATE/airQualityIndex`       | 0-999                        | AQI current value from the frontpanel (PM2.5[µg/m³])                       |
| `{mqtt_topic}/STATE/airQualityIndexAvg`    | 0-999                        | Average AQI (Not yet seen elsewehere)                                      |
| `{mqtt_topic}/STATEairTemperatureC`        | NUM-1                        | Current temperature in °C                                                  |
| `{mqtt_topic}/STATE/airRelHumidityPercent` | 0-100                        | Relative humidity in %                                                     |
| `{mqtt_topic}/STATE/fanMotorSpeed`         | 0.0-2500.0                   | Current motorspeed in rpm                                                  |
| `{mqtt_topic}/STATE/fanLevel`              | 1-3                          | Fanlevel preset as selected by the button (1, 2, 3 waves)                  |
| `{mqtt_topic}/STATE/fanFavoriteSetLevel`   | 1-14                         | Fanlevel preset for heart-mode (fanLevels 1-3 are positions in this range) |
| `{mqtt_topic}/STATE/filterUsedHours`       | INT                          | Filter-usage-time in hours                                                 |
| `{mqtt_topic}/STATE/filterRemainingPercent`| 0-100                        | Remaining filter-live in %                                                 |
| `{mqtt_topic}/STATE/filterRfidProductId`   | 0:0:31:31                    | Filter product-id                                                          |
| `{mqtt_topic}/STATE/filterType`            | Regular, ...                 | Commonname for the filtertype                                              |
| `{mqtt_topic}/STATE/filterRfidTag`         | 80:66:58:da:7f:55:4          | The current filters unique ID                                              |
| `{mqtt_topic}/STATE/deviceBuzzerEnabled`   | True/False                   | Can the buzzer buzz?                                                       |
| `{mqtt_topic}/STATE/deviceLedBrightnes`    | Bright, Dim, Off             | Selected LED Brightness                                                    |
| `{mqtt_topic}/STATE/deviceChildLockActive` | True/False                   | Is the childlock active?                                                   |
| `{mqtt_topic}/STATE/devicePowerOn`         | True/False                   | Is the device powered on?                                                  |
| `{mqtt_topic}/STATE/devicePower`           | on/off                       | Power...                                                                   |
| `{mqtt_topic}/STATE/deviceMode`            | Auto, Silent, Favorite, Fan  | Mode as selcted by the front-button. (3 fanmodes indicated by fanLevel)    |
| `{mqtt_topic}/STATE/statPurifiedVolumeM3`  | INT                          | Purified volume of air                                                     |
| `{mqtt_topic}/STATE/statTimeActive`        | INT                          | Seconds active                                                             |



These topics can control the device:

| CMD Topic                   | Values expected  | Meaning                       |
|-----------------------------|------------------|-------------------------------|
| `{mqtt_topic}/CMD/power`    | on/off           | Turn the device on or off     |




## Prerequisits
* Python 3
    * paho-mqtt
    * python-miio >= 0.5.0.1 (available from pip / pyPI)
* The devices security token

## Usage
* Copy `airpurifier.conf.sample` to `airpurifier.conf`
* Adjust the values in `airpurifier.conf`
* Run `miotAirpurifierBridge.py`

Set the environment `airpurifierConfigFile` to use a different configfile.

### systemd
The systemd folder conatins a systemd service that can be customized and dropped
into `/etc/systemd/system`. It assumes the `miotAirpurifierBridge.py` script is
located in `/opt/miotAirpurifierBridge/`
