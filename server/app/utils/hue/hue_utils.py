from phue import Bridge
from app.utils.hue.converters import ColorHelper, Converter
import os
import colorsys
import logging
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)

CONFIG_FILE = os.path.join(os.getcwd(), '.python_hue')


def get_api():
    bridge_ip = os.getenv('BRIDGE_ADDRESS')
    logger.debug('Bridge IP: {}'.format(bridge_ip))

    b = Bridge(ip=bridge_ip, config_file_path=CONFIG_FILE)
    b.connect()

    b.get_api()
    return b


def map_light(light):
    converter = Converter()
    x, y = (light.xy) if light.type != 'Dimmable light' else (-1, -1)
    supports_colour = light.type != 'Dimmable light'

    return {
        'id': light.light_id,
        'name': light.name,
        'colourTemp': light.colortemp if supports_colour else 0,
        'colourMode': light.colormode if supports_colour else 0,
        'saturation': light.saturation if supports_colour else 0,
        'on': light.on,
        'brightness': light.brightness if supports_colour else 0,
        'rgbColour': '#{}'.format(
            converter.xy_to_hex(x, y, light.saturation)
            if supports_colour
            else 'FFFFFF'
        ),
        'supportsColour': supports_colour
    }


def get_lights():
    b = get_api()
    lights = list(map(map_light, b.lights))

    return lights  # {x.light_id: x.name for x in b.lights}


def set_brightness(light_id, brightness):
    b = get_api()
    b.set_light(light_id, 'bri', brightness)


def set_colour(light_id, colour):
    helper = ColorHelper()
    rgb = helper.hex_to_rgb(colour)

    h, s, v = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])

    b = get_api()
    b.set_light(light_id, 'hue', int(round(h * 65535)))
    b.set_light(light_id, 'sat', int(round(s * 255)))
    b.set_light(light_id, 'bri', int(round(v)))

