jag config lru -j -k service.fault.bearers.critical -V '[]'
jag config lru -j -k service.fault.bearers.abnormal -V '[]'
jag config lru -j -k service.fault.bearers.event -V '[]'
jag config lru -j -k service.fault.bearers.health -V '[]'
jag profile save
jag sys save
echo "Rebooting..."
reboot
