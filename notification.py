from exponent_server_sdk import DeviceNotRegisteredError
from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage
from exponent_server_sdk import PushResponseError
from exponent_server_sdk import PushServerError
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError


def send_push_message(db, username, message, extra=None):
	users = db['user']
	user = users.find_one(
		{
		"username" : username
		})
	if 'device_token' in user:
		response = PushClient().publish(
				PushMessage(to=user['device_token'],
					body = message,
					data = extra)
				)
		try:
			# We got a response back, but we don't know whether it's an error yet
			# This call raises errors so we can handle them with normal exception
			# flows.
			response.validate_response()
		except DeviceNotRegisteredError:
			# Mark the push token as inactive
			print("device is not registered")
		except PushResponseError as exc:
			print("there is some push notification error")
				
	else:
		print("Cannot send the push notification to {}".format(username))
	return "Hello"
