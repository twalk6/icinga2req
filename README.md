# Requests based Icinga2 Integration Pack for Stackstorm

author: Todd Walk<br/>
email: toddwalk6@hotmail.com<br/>
verison: 2.1.1

Copyright 2017 Todd Walk

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

--------

This is a python requests based Icinga2 integration pack that was modified, tested, and now working with StackStorm 2.x+. 

Version 2.0: Major cleanup with this version, supporting a new, "generic", trigger format, collecting extra information including addresses & custom check attributes, and a configurable filtering system.

Version 2.1: Adds a configurable icinga2 queue setting. Hardens the code with reconnect support.

The filtering system works like this: For each block, the key is checked against everything in the payload. If there's a match made, then the type operation is done against the pattern. If it's a match, then that event is filtered out.
