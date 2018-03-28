
"""https://developer.amazon.com/public/solutions/alexa/alexa-voice-service/reference/system"""

import uuid
import datetime


class Settings(object):
    __local__ = ['en-US', 'en-GB', 'en-IN', 'de-DE', 'ja-JP']

    def __init__(self, alexa):
        self.alexa = alexa
        self.last_inactive_report = datetime.datetime.utcnow()

    def SettingsUpdated(self, local):
        if local not in self.__local__:
            return
        event = {
            "header": {
                "namespace": "Settings",
                "name": "SettingsUpdated",
                "messageId": uuid.uuid4().hex
            },
            "payload": {
                "settings": [
                    {
                        "key": "locale",
                        "value": local
                    }
                ]
            }
        }

        def on_finished():
            self.alexa.state_listener.on_ready()

        self.alexa.send_event(event, listener=on_finished)
