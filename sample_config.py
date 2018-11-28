if not __name__.endswith("config"):
    import sys
    print("Plox rename and remove this.", file=sys.stderr)
    quit(1)
API_KEY="YOUR API KEY"    #get from my.telegram.org
API_HASH="YOUR API HASH"  #get from my.telegram.org
SCREEN_SHOT_LAYER_ACCESS_KEY="get from screenshot layer website google it "           #For using .screencapture commad...please refer readme for getting the key
OPEN_WEATHER_MAP_APPID="get it from openweather site"        #FOR USING .weather Command
LOGGER_GROUP=(CHAT ID OF THE LOG GROUP (APPLY A HYPEN aka NEGATIVE SIGN BEFORE THE ID)) {This is an integer. Plox dont use strings}
LOGGER=True    #Incase you want to turn off logging, put this to false
CONSOLE_LOGGER_VERBOSE=False
PM_AUTO_BAN=False
