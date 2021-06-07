import os
import json
from http.server import HTTPServer,  BaseHTTPRequestHandler
import numpy as np
import config
config.DEVICE = 'pi_apa102'
config.LED_PIN_MOSI = 13
config.LED_PIN_SCLK = 19
config.BRIGHTNESS = 100
config.LED_ORDER = 'rbg'
config.SOFTWARE_GAMMA_CORRECTION = True

import led

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        """ Test only """
        config.DEVICE = 'pi_apa102'
        """ Test end """
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        """Get Pixels from JSON Post Body"""
        pixels_list =  json.loads(post_data.decode('utf-8'))
        led.pixels = np.asarray(pixels_list)
        """Test only remove"""
        print(led.pixels)
        """ Test end """
        led.update();
        self._set_response()

def run(server_class=HTTPServer, handler_class=S, port=8080):
    led.update()
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

run()
