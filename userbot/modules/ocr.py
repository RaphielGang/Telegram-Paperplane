from telethon import events
import os
import requests
import logging
from userbot import bot, OCR_SPACE_API_KEY
from userbot.events import register

TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./")

def ocr_space_file(filename, overlay=False, api_key=OCR_SPACE_API_KEY, language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.json()


def ocr_space_url(url, overlay=False, api_key=OCR_SPACE_API_KEY, language='eng'):
    """ OCR.space API request with remote file.
        Python3.5 - not tested on 2.7
    :param url: Image url.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'url': url,
               'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    return r.json()


def progress(current, total):
    logging.info("Downloaded {} of {}\nCompleted {}".format(
        current, total, (current / total) * 100))
 
@register(pattern=r"\.ocr (.*)", outgoing=True)
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Processing......")
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    lang_code = event.pattern_match.group(1)
    downloaded_file_name = await bot.download_media(
        await event.get_reply_message(),
        TEMP_DOWNLOAD_DIRECTORY,
        progress_callback=progress
    )
    test_file = ocr_space_file(filename=downloaded_file_name, language=lang_code)
    try:
        ParsedText = test_file["ParsedResults"][0]["ParsedText"]
        ProcessingTimeInMilliseconds = str(int(test_file["ProcessingTimeInMilliseconds"]) // 1000)
    except:
        await event.edit("Errors...")
    else:
        await event.edit("Read Document in {} seconds. \n{}".format(ProcessingTimeInMilliseconds, ParsedText))
    os.remove(downloaded_file_name)
