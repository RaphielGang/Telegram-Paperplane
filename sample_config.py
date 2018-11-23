if not __name__.endswith("config"):
    import sys
    print("Plox rename and remove this.", file=sys.stderr)
    quit(1)
API_ID="YOUR API ID"    #get from my.telegram.org
API_HASH="YOUR API HASH"  #get from my.telegram.org
SCREEN_SHOT_LAYER_ACCESS_KEY="get from screenshot layer website google it "           #For using .screencapture commad...please refer readme for getting the key
OPEN_WEATHER_MAP_APPID="get it from openweather site"        #FOR USING .weather Command
LOGGER_GROUP="CHAT ID OF THE LOG GROUP (APPLY A HYPEN aka NEGATIVE SIGN BEFORE THE ID)"
LOGGER=True    #Incase you want to turn off logging, put this to false
CONSOLE_LOGGER_VERBOSE=False
TRT_ENABLE=False
PM_AUTO_BAN=False
TTS_ENABLE=False
TRT_API_USERNAME="Insert API Username"    #For Using IBM Translator API
TTS_API_USERNAME="Insert API Username"    #For IBM Voice API
TRT_API_PASSWORD="Insert API Password"
TTS_API_PASSWORD="Insert API Password"
