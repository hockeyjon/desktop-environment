#!/usr/bin/env bash

jag config lru -j -k service.fault.bearers.critical -V '["bear-router"]'
jag config lru -j -k service.fault.bearers.abnormal -V '["bear-router"]'
jag config lru -j -k service.fault.bearers.event -V '["bear-router"]'
jag config lru -j -k service.fault.bearers.health -V '["bear-router"]'
echo "jag config lru -j -k service.fault.bearers.critical -V '[bear-router]'"
echo "jag config lru -j -k service.fault.bearers.abnormal -V '[bear-router]'"
echo "jag config lru -j -k service.fault.bearers.event -V '[bear-router]'"
echo "jag config lru -j -k service.fault.bearers.health -V '[bear-router]'"
echo "Saving profile ..."
jag profile save
jag sys save
echo "Rebooting ..."
reboot