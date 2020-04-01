# POC: Xiaomi Airpurifier 3H MQTT Bridge
This is a proof-of-concept, lacking a lot of errorhandling.

The Xiaomi Airpurifier 3H uses the (new) miot api.
This script bridges the air pufifier to the following state and control topics in mqtt.

These topics are reported from the device:

| STATE Topic                         | Values to expect             | Meaning                                                                    |
|-------------------------------------|------------------------------|----------------------------------------------------------------------------|
| $device/STATE/TIMESTAMP             | 2020-03-29T15:44             | Timestamp of the last state update                                         |
| $device/STATE/airQualityIndex       | 0-999                        | AQI current value (ppm2.5?)                                                |
| $device/STATE/airQualityIndexAvg    | 0-999                        | AQI as displayed on the frontpanel (?)                                     |
| $device/STATEairTemperatureC        | FLOAT                        | Current temperature in °C                                                  |
| $device/STATE/airRelHumidityPercent | 0-100                        | Relative humidity in %                                                     |
| $device/STATE/fanMotorSpeed         | INT                          | Current motorspeed in rpm                                                  |
| $device/STATE/fanLevel              | 1-3                          | Fanlevel preset as selected by the button (1,2,3 waves)                    |
| $device/STATE/fanFavoriteSetLevel   | 1-14                         | Fanlevel preset for heart-mode (fanLevels 1-3 are positions in this range) |
| $device/STATE/filterUsedHours       | INT                          | Filter-usage-time in hours                                                 |
| $device/STATE/filterRemainingPercent| 0-100                        | Remaining filter-live in %                                                 |
| $device/STATE/filterRfidProductId   | 0:0:31:31                    | Filter product-id                                                          |
| $device/STATE/filterType            | Regular, ...                 | Common name for the filtertype                                             |
| $device/STATE/filterRfidTag         | 80:66:58:da:7f:55:4          | The filters unique ID                                                      |
| $device/STATE/deviceBuzzerEnabled   | True/False                   | Can the buzzer buzz?                                                       |
| $device/STATE/deviceLedBrightnes    | Bright, Dim, Off             | Brightness...                                                              |
| $device/STATE/deviceChildLockActive | True/False                   | Is the childlock active?                                                   |
| $device/STATE/devicePowerOn         | True/False                   | Is the device powered on?                                                  |
| $device/STATE/devicePower           | on/off                       | Power...                                                                   |
| $device/STATE/deviceMode            | Auto, Silent, Favorite, Fan  | Mode as selcted by the front-button. (3 fanmodes indicated by fanLevel)    |
| $device/STATE/statPurifiedVolumeM3  | INT                          | Purified volume of air                                                     |
| $device/STATE/statTimeActive        | INT                          | Seconds active                                                             |



These topics can control the device:

| CMD Topic            | Values expected  | Meaning                       |
|----------------------|------------------|-------------------------------|
| $device/CMD/power    | on/off           | Turn the device on or off     |




## Prerequisits
- Python 3
- PAHO MQTT-Client module
- python-miio > 5.0.1 (available from PIP) 
- The devices security token

## Usage
- Copy airpurifier.conf.sample to airpurifier.conf
- Adjust the values in airpurifier.conf
- Run miotAirpurifierBridge.py

Set the environment `airpurifierConfigFile` to use a different configfile.

### systemd
The systemd folder conatins a systemd service that can be customized and dropped
into `/etc/systemd/system`. It assumes the `miotAirpurifierBridge.py` script is
located in `/opt/miotAirpurifierBridge/`
