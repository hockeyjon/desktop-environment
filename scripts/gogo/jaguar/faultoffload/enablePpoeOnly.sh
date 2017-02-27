#!/usr/bin/env bash

jag config lru -j -k service.fault.bearers.critical -V '["bear-pppoe"]'
jag config lru -j -k service.fault.bearers.abnormal -V '["bear-pppoe"]'
jag config lru -j -k service.fault.bearers.event -V '["bear-pppoe"]'
jag config lru -j -k service.fault.bearers.health -V '["bear-pppoe"]'
echo "jag config lru -j -k service.fault.bearers.critical -V '[bear-pppoe]'"
echo "jag config lru -j -k service.fault.bearers.abnormal -V '[bear-pppoe]'"
echo "jag config lru -j -k service.fault.bearers.event -V '[bear-pppoe]'"
echo "jag config lru -j -k service.fault.bearers.health -V '[bear-pppoe]'"
echo "Saving profile ..."
jag profile save
jag sys save
echo "Rebooting ..."
reboot