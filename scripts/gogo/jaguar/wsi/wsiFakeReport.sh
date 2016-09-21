#!/bin/bash

denter wsi-taps curl -H "Content-Type: application/json" -X POST -d '{"taps": "- TRP 212135  39.9267 -105.1149 018 018.0 312    786 0.00454  000.00  180.00 2.135  1.882  0.017 -0.017  10 02 00 00 298 4    738", "serial": "123456"}' https:/<AWS IP>//wsi/v1/taps