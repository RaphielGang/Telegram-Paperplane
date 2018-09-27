if not __name__.endswith("sample_config"):
    import sys
    print("The README is there to be read. Extend this sample config to a config file, don't just rename and change "
          "values here. Doing that WILL backfire on you.\nBot quitting.", file=sys.stderr)
    quit(1)
API_ID="YOUR API ID"
API_HASH="YOUR API HASH"
LOGGER_GROUP="CHAT ID (-ve) OF THE LOG GROUP"
LOGGER=True    #Incase you want to turn off logging, put this to false
CONSOLE_LOGGER_VERBOSE=False
TRT_ENABLE=False
TTS_ENABLE=False
TRT_API_USERNAME="Insert API Username"    #For Using IBM Translator API
TTS_API_USERNAME="Insert API Username"    #For IBM Voice API
TRT_API_PASSWORD="Insert API Password"
TTS_API_PASSWORD="Insert API Password"
