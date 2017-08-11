# Requests based Icinga2 Integration Pack for Stackstorm

author: Todd Walk / Verizon Wireless VCP<br/>
email: todd.walk@verizonwireless.com<br/>
verison: 2.0

Copyright 2017 Verizon Wireless VCP

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

NOTE: The older test/example remediation code in the actions and rules directories has been deleted because it was out of date and I didn't have the time to update it 

This is a python requests based Icinga2 integration pack that was modified, tested, and now working with StackStorm 2.x+. 

Major cleanup with this version, supporting a new, "generic", trigger format, collecting extra information including addresses & custom check attributes, and a configurable filtering system.

NOTE: The testing of this sensor is not to the level of a commercial product. There are code paths that I have not bothered to exercise. If you run into a bug, let me know and I'll try to find time to fix it.

For connecting / reconnecting to multiple icinga2 servers, you should examine using something like haproxy

The filtering system works like this: For each block, the key is checked against everything in the payload. If there's a match made, then the type operation is done against the pattern. If it's a match, then that event is filtered out
