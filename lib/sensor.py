import board
from time import sleep
from adafruit_dht import DHT22, DHT11
from lib.eventhook import EventHook
from threading import Timer

"""
    The purpose of this class is to map the idea of a sensor to the pinouts on
    the raspberrypi. It provides methods to control get the temperature/humidity
    and also provides an event hook to notify you of the state change.
"""
class Sensor(object):
    def __init__(self, config):
        # Config
        pin = getattr(board, "D{pin}".format(pin=config['pin']))
        self.sensor = DHT22(pin) if config.get('dht22') else DHT11(pin)
        self.id = config['id']
        self.interval = int(config['interval']) * 60
        self._timer = None
        self.onInterval = EventHook()

    # Release timer resources
    def __del__(self):
        self.stop()
    # State is a read only property that actually gets its value from the pin
    @property
    def temperature(self):
        # Read the mode from the config. Then compare the mode to the current state. IE. If the circuit is normally closed and the state is 1 then the circuit is closed.
        # and vice versa for normally open
        count = 0
        while count < 5:
            try:
                # Print the values to the serial port
                temperature_c = self.sensor.temperature
                if temperature_c:
                    temperature_f = temperature_c * (9 / 5) + 32
                    humidity = self.sensor.humidity
                    return { 'temperature_f': temperature_f, 'temperature_c': temperature_c, 'humidity': humidity }
            except RuntimeError as error:
                pass
                # Errors happen fairly often, DHT's are hard to read, just keep going
                # print(error.args[0])

            sleep(0.5)
            count += 1
        return { 'fahrenheit': -1, 'celsius': -1, 'humidity': -1 }

    def start(self):
        if not self._timer:
            self._run()

    def stop(self):
        if self._timer:
            self._timer.cancel()
            self._timer = None

    def _run(self):
        # self._timer = None
        self._timer = Timer(self.interval, self._run)
        self._timer.start()
        self.onInterval.fire(self.temperature)
