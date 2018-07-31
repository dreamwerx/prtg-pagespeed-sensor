# prtg-pagespeed-sensor
A python based custom sensor for PRTG to collect Google pagespeed insights scores.  It collects 2 channels of data.  
Desktop and mobile rankings.

Typically with PRTG you use either the HTTP or HTTP Advanced sensor to collect basic performance data and monitor uptime
on specific websites.  I've heard recently from some people in various positions (small website owner, product owner, CEO) - that 
they wanted to keep a close eye on the rating that Google gives there website, as it is taken into account in the rankings.

The main issue they had was that a number of parts of there websites are dynamic and controlled / configurable by various teams, 
who don't always pay attention to changes and what impact they might have (non-optimized images / non-scaled images / crazy javascript being
added in Google tag manager, etc.) - and it had happened multiple times that the website rating had dropped substantially and 
nobody knew about it.

So I whipped up this sensor - And now they have the sensor running on a 12 hour interval and an alarm alerting them when it drops below a specific number.

### Requirements

* [PRTG] 
* [Insights] - An API key activated for Google pagespeed insights

### Installation

I decided to not use any 3rd party packages or libraries since then you need to install pip and any dependencies.  
There are some libraries which might simplify things a bit, but it adds complexity to deploying.

Copy the google_pagespeed_insights.py script into: C:\Program Files (x86)\PRTG Network Monitor\Custom Sensors\python\

Once installed, add a custom python sensor - select the script name, and set these parameters (see screenshot in repo):
--apikey=XXXXXXXXXXXXXXX --url=https://www.example.com/

Adjust the params with your API key - and whichever URL you want to monitor. 
PRTG does pass some data over to the sensor, but depending on the device configuration it may be incorrect, so I avoided using it 
and went with the passed in parameters.

### License
The Unlicense

### Issues
Right after creating the sensor, be sure to adjust your scanning interval!  I have been adding these under the website device,
which typically has a PING, and HTTP Advanced sensor set to a 1 minute interval, this should be set to a much higher interval,
otherwise you'll probably get banned by Google / use up your API limit.

If you run into any issues, please raise an issue on GitHub.

[//]: #

   [PRTG]: <https://www.paessler.com/prtg>
   [Insights]: <https://developers.google.com/speed/pagespeed/insights/>
