import requests
import json
import youtube_dl
import os


def convert(link):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            }],
            }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            title = info_dict.get('title', None).replace('"','').replace(' ','_').replace('$','S')+'.mp3'
            ydl_opts['outtmpl']=title
    except:
        title='Vaporwave'
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
    return title

def update(token,offset):
    url='https://api.telegram.org/bot{}/getUpdates?timeout=100&offset={}'.format(token,offset)
    updates=json.loads(requests.get(url).text)
    return updates

def send_message(user_id,txt,token):
    url='https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(token,user_id,txt)
    response=json.loads(requests.get(url).text)
    if not response['ok']:
        print"Something goes wrong..."

def send_audio(user_id,location,token):
    print location
    url='https://api.telegram.org/bot{}/sendaudio'.format(token)
    files={'audio':open('./{}'.format(location),'rb').read()}
    data={'chat_id':user_id,'title':location}
    json_re = requests.post(url,files=files,data=data).text
    response=json.loads(json_re)
    if not response['ok']:
        print"Something goes wrong..."
        print response

def bot():
    print"bot started..."
    token = '742559632:AAHQPRMS6Tgu-syXC4btko2ayLJzpKTn1OA'
    offset=None
    while True:
        updates=update(token,offset)
        if updates['ok']:
            if len(updates['result'])<1:
                continue
        else:
            continue
        print"Message recived..."
        offset=updates['result'][0]['update_id']+1
        url=updates['result'][0]['message']['text']
        user_id=updates['result'][0]['message']['from']['id']
        if user_id != 436507942 and user_id != 56165526 and user_id != 322182250 and user_id != 639592445:
            send_message(user_id,"You aren't allowed to use this bot..",token)
            continue
        if url[:8]!='https://':
            send_message(user_id,"Incorect url please check it...",token)
            continue
        try:
            send_message(user_id,"Start converting(that can take minutes)...",token)
            mp3=convert(url)
            send_audio(user_id,mp3,token)
            send_message(user_id,"Bot created by @Oliva_0.",token)
        except Exception as e:
            print e
            send_message(user_id,"Something goes wrong...\nretry...",token)

if __name__ == '__main__':
    bot()
