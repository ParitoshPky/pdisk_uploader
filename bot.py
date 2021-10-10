from os import environ
import os
import time
from urllib.parse import urlparse
import aiohttp
from pyrogram import Client, filters
from bs4 import BeautifulSoup
import requests
import re

API_ID = environ.get('API_ID')
API_HASH = environ.get('API_HASH')
BOT_TOKEN = environ.get('BOT_TOKEN')
PDISK_API_KEY = environ.get('PDISK_API_KEY')
THUMB_URL = environ.get('THUMB_URL', 'https://telegra.ph/file/1181d9119a13988dfe29c.jpg')
CHANNEL = environ.get('CHANNEL')
bot = Client('pdisk bot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=0)


@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**𝗛𝗘𝗟𝗟𝗢🎈{message.chat.first_name}!**\n\n"
        "𝐈'𝐦 𝐚 𝐏𝐝𝐢𝐬𝐤 𝐔𝐩𝐥𝐨𝐚𝐝𝐞𝐫 𝐛𝐨𝐭. 𝐉𝐮𝐬𝐭 𝐬𝐞𝐧𝐝 𝐦𝐞 𝐥𝐢𝐧𝐤 𝐨𝐫 𝐅𝐮𝐥𝐥 𝐩𝐨𝐬𝐭... \n 𝐓𝐡𝐢𝐬 𝐛𝐨𝐭 𝐢𝐬 𝐦𝐚𝐝𝐞 𝐛𝐲 @ParitoshPky_Official💖")


@bot.on_message(filters.text & filters.private)
async def pdisk_uploader(bot, message):
    new_string = str(message.text)
    try:
        pdisk_link = await multi_pdisk_up(new_string)
        await message.reply(f'{pdisk_link}', quote=True)
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)


@bot.on_message(filters.photo & filters.private)
async def pdisk_uploader(bot, message):
    new_string = str(message.caption)
    try:
        pdisk_link = await multi_pdisk_up(new_string)
        if(len(pdisk_link) > 1020):
            await message.reply(f'{pdisk_link}', quote=True)
        else:
            await bot.send_photo(message.chat.id, message.photo.file_id, caption=f'{pdisk_link}')
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)


async def get_ptitle(url):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    for title in soup.find_all('title'):
        pass
    title = list(title.get_text())
    title = title[8:]
    str = 't.me/' + CHANNEL + ' '
    for i in title:
        str = str + i
    lst = list(html_text.split(","))
    c = 0
    for i in lst:
        if ("""videoid""" in i):
            found = lst[c]
            break
        c += 1

    # pdisk.net link
    pdisk_video_id = list(found.split(":"))
    video_id = pdisk_video_id[2]
    video_id = list(video_id.split(","))
    v_id = video_id[0]
    v_len = len(v_id)
    v_id = v_id[1:v_len - 2]

    v_url = 'https://www.pdisks.com/share-video?videoid=' + v_id
    res = [str, v_url]
    return res


async def pdisk_up(link):
    if ('pdisk' in link or 'kuklink' in link or 'kofilink' in link or 'cofilink' in link or 'bit' in link or link in 'vdshort' or link in 'vidrivers'):
        res = await get_ptitle(link)
        title_pdisk = res[0]
        link = res[1]
    else:
        title_new = urlparse(link)
        title_new = os.path.basename(title_new.path)
        title_pdisk = '@' + CHANNEL + title_new
    res = requests.get(
        'http://linkapi.net/open/create_item?link_type=link&content_src=' + link + '&source=2000&cover_url='+THUMB_URL+'&api_key=' + PDISK_API_KEY + '&dir_id=0&title=' + title_pdisk + '&description=Join_' + CHANNEL + '_for_more_like_this')
    data = res.json()
    data = dict(data)
    print(data)
    v_id = data['data']['item_id']
    v_url = 'https://www.pdisk.me/share-video?videoid=' + v_id
    return (v_url)


async def multi_pdisk_up(ml_string):
    new_ml_string = list(map(str, ml_string.split(" ")))
    new_ml_string = await remove_username(new_ml_string)
    new_join_str = "".join(new_ml_string)

    urls = re.findall(r'(https?://[^\s]+)', new_join_str)

    nml_len = len(new_ml_string)
    u_len = len(urls)
    url_index = []
    count = 0
    for i in range(nml_len):
        for j in range(u_len):
            if (urls[j] in new_ml_string[i]):
                url_index.append(count)
        count += 1
    new_urls = await new_pdisk_url(urls)
    url_index = list(dict.fromkeys(url_index))
    i = 0
    for j in url_index:
        new_ml_string[j] = new_ml_string[j].replace(urls[i], new_urls[i])
        i += 1

    new_string = " ".join(new_ml_string)
    return await addFooter(new_string)


async def new_pdisk_url(urls):
    new_urls = []
    for i in urls:
        time.sleep(0.2)
        new_urls.append(await pdisk_up(i))
    return new_urls


async def remove_username(new_List):
    for i in new_List:
        if('@' in i or 't.me' in i or 'https://bit.ly/3m4gabB' in i or 'https://bit.ly/pdisk_tuts' in i or 'telegra.ph' in i):
            new_List.remove(i)
    return new_List


async def addFooter(str):
    footer = """
━━━━━━━━━━━━━━━
⚙️ How to Download / Watch Online or Change Audio : https://bit.ly/pdisk_tuts
━━━━━━━━━━━━━━━
⭐️JOIN CHANNEL ➡️ t.me/""" + CHANNEL
    return str + footer

bot.run()
