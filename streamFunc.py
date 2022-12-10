import oAuth as oAuth

youtube  = None

def Authenticate(tokenOld,client_id):
    creds = oAuth.Authenticate(tokenOld,client_id)
    return creds


def GetStreamID(creds):
    youtube  = oAuth.build('youtube', 'v3', credentials = creds)

    streamIdRequest = youtube.liveBroadcasts().list(
                    part="snippet",
                    broadcastStatus="active"
                    )
    streamIdresponse = streamIdRequest.execute()

    for item in streamIdresponse['items']:
        if 'liveChatId' in item['snippet']:
            liveChatId = item['snippet']['liveChatId']

    #print(liveChatId)
    return [youtube,liveChatId]
    



def StreamReadMssg(creds,nextPageId = None):
    [youtube,liveChatId] = GetStreamID(creds)
    
    mssgText = []
    streamReadRequest = youtube.liveChatMessages().list(
                        liveChatId = liveChatId,
                        part = "snippet",
                        pageToken = nextPageId
                    )

    streamReadResponse = streamReadRequest.execute()
    
    nextPageId = streamReadResponse["nextPageToken"] 
    for item in streamReadResponse['items']:
        if 'textMessageDetails' in item['snippet']:
            if 'messageText' in item['snippet']['textMessageDetails']:
                mssgText.append(item['snippet']['textMessageDetails']['messageText'])
    #print(streamReadResponse)
    return [nextPageId,mssgText]



# writing the messages  
def StreamChatWrite(creds,mssg):
    [youtube,liveChatId] = GetStreamID(creds)
    steamWriteRequest = youtube.liveChatMessages().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "liveChatId": liveChatId,
                            "type": "textMessageEvent",
                            "textMessageDetails": {
                                "messageText": mssg                    
                            }
                        }
                    }
                )

    steamWriteResponse = steamWriteRequest.execute()
    #print(steamWriteResponse)
    return steamWriteResponse


