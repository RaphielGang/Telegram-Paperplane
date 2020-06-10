import userbot.modules.libs.git_api as api

from userbot import CMD_HELP
from userbot.events import register


# do not async
def getData(url, index):
    if not api.getData(url):
        return "Invalid user/repo combo"
    recentRelease = api.getReleaseData(api.getData(url), index)
    if recentRelease is None:
        return "The specified release could not be found"
    author = api.getAuthor(recentRelease)
    authorUrl = api.getAuthorUrl(recentRelease)
    assets = api.getAssets(recentRelease)
    releaseName = api.getReleaseName(recentRelease)
    message = "<b>Author:</b> <a href='{}'>{}</a>\n".format(authorUrl, author)
    message += "<b>Release Name:</b> " + releaseName + "\n\n"
    for asset in assets:
        message += "<b>Asset:</b> \n"
        fileName = api.getReleaseFileName(asset)
        fileURL = api.getReleaseFileURL(asset)
        assetFile = "<a href='{}'>{}</a>".format(fileURL, fileName)
        sizeB = ((api.getSize(asset)) / 1024) / 1024
        size = "{0:.2f}".format(sizeB)
        downloadCount = api.getDownloadCount(asset)
        message += assetFile + "\n"
        message += "Size: " + size + " MB"
        message += "\nDownload Count: " + str(downloadCount) + "\n\n"
    return message


@register(pattern=".git(?: |$)(.*)", outgoing=True)
async def get_release(event):
    if not event.text[0].isalpha() and event.text[0] in ("."):
        commandArgs = event.text.split(" ")
        if len(commandArgs) != 2 or not "/" in commandArgs[1]:
            await event.edit("Invalid arguments! Make sure you are typing a valid combination of user/repo")
            return
        index = 0  # for now...
        url = commandArgs[1]
        text = getData(url, index)
        await event.edit(text, parse_mode="html")


CMD_HELP.update({
    "github_api_interface":
        ".git <user>/<repo>\
        \nGets the updated release of the specified user/repo combo"})
