# Google Pagespeed Insights Sensor (v5)
# Author: colbey@dreamwerx.net
# Description: PRTG script that tests your webpage against the Pagespeed Insights API (v5)
# https://developers.google.com/speed/docs/insights/v5/get-started

import urllib.request
import sys

from paepy.ChannelDefinition import CustomSensorResult

class PageSpeedSensor(object):
	apiFormat = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?locale=en&url={0}&key={1}&strategy={2}'
	apiKey = ''
	testUrl = ''

	def sendError(self, message):
		result = CustomSensorResult()
		result.add_error('Error occurred: ' + message)
		print(result.get_json_result())
		exit(1)

	def getApiUrl(self, strategy):
		return self.apiFormat.format(self.getTestUrl(), self.getApiKey(), strategy)

	def validateCliParams(self):
		import json
		import getopt

		try:
			prtgData = json.loads(sys.argv[1])
		except json.JSONDecodeError as err:
			self.sendError('Error decoding params')

		params = str.split(prtgData['params'])
		try:
			opts, args = getopt.getopt(params, 'x', ['apikey=', 'url='])
		except getopt.GetoptError as err:
			self.sendError('Incorrect arguement syntax')

		for opt, arg in opts:
			if opt == '--apikey':
				self.apiKey = str(arg)
			elif opt == '--url':
				self.testUrl = str(arg).replace('\\/', '/')

		if self.apiKey == '':
			self.sendError('API key not specified!')

		if self.testUrl == '':
			self.sendError('Test url not defined')

	def getApiKey(self):
		return self.apiKey;

	def getTestUrl(self):
		return self.testUrl

	def run(self):
		self.validateCliParams()

		mobileScore = self.getScore(self.getApiUrl('mobile'))
		desktopScore = self.getScore(self.getApiUrl('desktop'))

		sensor = CustomSensorResult(0)
		sensor.add_channel(channel_name="Mobile Score",unit="Percent",value=mobileScore)
		sensor.add_channel(channel_name="Desktop Score",unit="Percent",value=desktopScore)

		# Send results
		print(sensor.get_json_result())

	def getScore(self, apiUrl):
		import json
		req = urllib.request.Request(apiUrl)
		try:
			response = urllib.request.urlopen(req).read().decode('utf8')
		except urllib.error.HTTPError as e:
			self.sendError('Communicating with API (check your key and url): ' + e.msg)
		except Exception as e2:
			self.sendError('Communicating with API (check your key and url): ' + e2.msg)

		jsonResult = json.loads(response)
		return jsonResult['lighthouseResult']['categories']['performance']['score'] * 100


# Main run
sensor = PageSpeedSensor()
sensor.run()
