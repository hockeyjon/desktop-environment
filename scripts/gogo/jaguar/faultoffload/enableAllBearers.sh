#!/usr/bin/env bash

jag config lru -j -k service.fault.bearers.critical -V '["bear-tm","bear-4g","bear-gogo","bear-pppoe","bear-router","bear-ka"]'
jag config lru -j -k service.fault.bearers.abnormal -V '["bear-tm","bear-4g","bear-gogo","bear-pppoe","bear-router","bear-ka"]'
jag config lru -j -k service.fault.bearers.event -V '["bear-tm","bear-4g","bear-gogo","bear-pppoe","bear-router","bear-ka"]'
jag config lru -j -k service.fault.bearers.health -V '["bear-tm","bear-4g","bear-gogo","bear-pppoe","bear-router","bear-ka"]'
jag profile save
jag sys save
echo "Rebooting..."
reboot
