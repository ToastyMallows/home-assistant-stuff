# Fill in these parameters in the script before running:
#
# <hassioIP> - The static IP address of your Home Assistant (or homeassistant.local)
# <entityOne>, <entityTwo> - The entity names you'd like to switch on/off
# <token> - Your user account's "long lived access token"

from requests import get, post
import argparse
import traceback

parser = argparse.ArgumentParser(description="Turn on/off lights")
parser.add_argument("--on", dest="on_flag", action="store_true")
parser.add_argument("--off", dest="off_flag", action="store_true")
args = parser.parse_args()
on_flag = args.on_flag
off_flag = args.off_flag

if not on_flag and not off_flag:
	print("--on or --off are required.  Use at least one.")
	exit(1)

if on_flag and off_flag:
	print("--on and --off are exclusive.  Use one or the other.")
	exit(1)

healthUrl = "http://<hassioIP>:8123/api/"
lightOnUrl = "http://<hassioIP>:8123/api/services/light/turn_on"
lightOffUrl = "http://<hassioIP>:8123/api/services/light/turn_off"
lightsJSON = '{ "entity_id": ["<entityOne>", "<entityTwo>"]}'
headers = {
	"Authorization": "Bearer <token>",
	"content-type": "application/json",
}

try:
	healthResponse = get(healthUrl, headers=headers)

	if healthResponse.status_code != 200:
		print("cannot communicate with API: " + healthResponse.text)
		exit(1)

	lightUrl = None

	if on_flag:
		lightUrl = lightOnUrl
	else:
		lightUrl = lightOffUrl

	lightResponse = post(lightUrl, lightsJSON, headers=headers)

	if lightResponse.status_code != 200:
		print("error toggling lights: " + lightResponse.text)
		exit(1)
except:
	print("Unexpected error: ", traceback.format_exc())
	exit(1)

exit(0)