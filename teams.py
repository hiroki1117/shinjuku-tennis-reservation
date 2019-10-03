import pymsteams

def sendToTeams(data, url):
    myTeamsMessage = pymsteams.connectorcard(url)
    message = ""
    for key, value in data.items():
        if value == '×':
            continue
        message += key + " " + value + '</br>'
        
    if message == "":
        return

    myTeamsMessage.title("テニスコート状況")
    myTeamsMessage.text(message)
    myTeamsMessage.send()