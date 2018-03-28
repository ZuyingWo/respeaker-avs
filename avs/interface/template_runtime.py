
"""https://developer.amazon.com/public/solutions/alexa/alexa-voice-service/reference/system"""

import uuid
import datetime
import RPi.GPIO as GPIO  # import RPi.GPIO module
import logging
import pygame
import numpy
from threading import Timer

__Raspex_Skill_Id__ = "amzn1.ask.skill.b0e52bae-2304-423f-8d97-1b16a511bd5d"
__PeeCo_Skill_Id__ = "amzn1.ask.skill.da41e7ab-3a36-43d1-92ea-27567cce7594"


class TemplateRuntime(object):
    __whitefilm_pin__ = 6  # gpio pin 6
    __grayfilm_pin__ = 26  # gpio pin 26
    __audio_files__ = []
    __env_sound__ = None
    __playing_env_sound__ = False

    __types__ = [
        'BodyTemplate1',    # 画像なしのWikipediaのエントリーやAlexaスキルにより提供されるシンプルなカード。
        'BodyTemplate2',    # 画像ありのWikipediaエントリー。
        'ListTemplate1',    # 買い物リスト、To Doリスト、カレンダーのエントリー。
        'WeatherTemplate',  # 天気。
    ]

    def __init__(self, alexa):
        self.alexa = alexa
        self.last_inactive_report = datetime.datetime.utcnow()
        pygame.mixer.init()

        GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD

        try:
            GPIO.setup(self.__whitefilm_pin__, GPIO.OUT)  # set a port/pin as an output
        except:
            pass
        finally:
            pass

        try:
            GPIO.setup(self.__grayfilm_pin__, GPIO.OUT)  # set a port/pin as an output
        except:
            pass
        finally:
            pass

        try:
            self.switchWhiteFilm(0)
            self.switchGrayFilm(0)
        except Exception as ex:
            pass
        finally:
            pass

        self.__getFiles__()

        return

    def __getFiles__(self):
        try:
            from os import listdir
            from os.path import isfile, join
            mypath = '/opt/wav/'

            self.__audio_files__ = [mypath + f for f in listdir(mypath) if isfile(join(mypath, f))]

        except Exception as ex:
            pass

        return
    # {
    #     "directive": {
    #         "header": {
    #             "namespace": "TemplateRuntime",
    #             "name": "RenderTemplate",
    #             "messageId": {{STRING}},
    #             "dialogRequestId": {{STRING}}
    #         },
    #         "payload": {
    #             "token": "",
    #             "type": "bodyTemplate2",
    #             "title": {
    #                 "mainTitle": "Who is Usain Bolt?",
    #                 "subTitle": "Wikipedia"
    #             },
    #             "skillIcon": null,
    #             "textField": "Usain St Leo Bolt, OJ, CD born 21 August 1986..."
    #         }
    #     }
    # }

    def RenderTemplate(self, directive):
        logging.info('RenderTemplate: {}'.format(directive))
        try:

            if directive['payload']['type'] != 'BodyTemplate1':
                return
            if not str(directive['payload']['title']['mainTitle']).startswith('RespexCmd'):
                return

            if str(directive['payload']['title']['mainTitle']).endswith('White'):
                self.switchWhiteFilm(0)
                self.switchGrayFilm(1)
            elif str(directive['payload']['title']['mainTitle']).endswith('Gray'):
                self.switchWhiteFilm(1)
                self.switchGrayFilm(0)
            elif str(directive['payload']['title']['mainTitle']).endswith('Clear'):
                self.switchWhiteFilm(1)
                self.switchGrayFilm(1)
            elif str(directive['payload']['title']['mainTitle']).endswith('AudioOn'):
                self.playAudio()
            elif str(directive['payload']['title']['mainTitle']).endswith('AudioOff'):
                self.stopAudio()
            else:
                pass
        except Exception as ex:
            logging.error("{}".format(ex))
        finally:
            pass

        return

    def switchWhiteFilm(self, on):
        GPIO.output(self.__whitefilm_pin__, on)

    def switchGrayFilm(self, on):
        GPIO.output(self.__grayfilm_pin__, on)

    def playAudio(self):

        if self.__playing_env_sound__ :
            return
        try:
            self.__env_sound__ = pygame.mixer.Sound(
                self.__audio_files__[
                    numpy.random.randint(0, len(self.__audio_files__))
                ]
            )
            self.__env_sound__.play()

            Timer(5, self.check_and_repeat, ()).start()
        except:
            pass
        finally:
            self.__playing_env_sound__ = True
        return

    def stopAudio(self):
        try:
            if pygame.mixer.get_busy():
                self.__env_sound__.stop()

            self.__playing_env_sound__ = False
        except:
            pass
        return

    def check_and_repeat(self):
        try:
            if self.__playing_env_sound__:
                if not pygame.mixer.get_busy():
                    self.__env_sound__ = pygame.mixer.Sound(
                        self.__audio_files__[
                            numpy.random.randint(0, len(self.__audio_files__))
                        ]
                    )
                    self.__env_sound__.play()
                    logging.info('Env Sound is going to be repeated.')

                Timer(5, self.check_and_repeat, ()).start()

        except Exception as es:
            pass
        finally:
            pass
        return
