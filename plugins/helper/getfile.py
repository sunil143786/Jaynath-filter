# This code has been modified by @Safaridev
# Please do not remove this credit
from pyrogram import filters, Client, enums
import bs4, requests, re, asyncio
import os, traceback, random
from os import environ
from utils import temp, get_poster
from info import ADMINS
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def modify_instagram_link(link):
    if "instagram.com" in link:
        try:
            link = link.replace("instagram.com", "ddinstagram.com")
        except Exception:
            link = link.replace("instagram.com", "ddinstagram.com")
    return link

@Client.on_message(filters.command('getfile'))
async def getfile(client, message):
    try:
        if message.from_user.id not in ADMINS:
            await message.reply("Only admins can access this command")
            return
        reply_message = message.reply_to_message
        video = None
        if reply_message and reply_message.video:
            video = reply_message.video

        query = message.text.split(" ", 1)
        if len(query) < 2:
            return await message.reply_text("<b>Usage:</b> /getfile <movie_name> <optional_video_link>\n\nExample: /getfile Money Heist")
        msg = await message.reply("please wait..")
        full_text = query[1].strip()
        video_link = None
        match = re.search(r"(http[s]?://\S+)", full_text)
        if match:
            video_link = modify_instagram_link(match.group(0)) 
            file_name = full_text.replace(match.group(0), "").strip() 
        else:
            file_name = full_text
        movie_details = await get_poster(file_name)
        file_link = f"https://t.me/{temp.U_NAME}?start=getfile-{file_name.replace(' ', '-').lower()}"
        if not movie_details:
            await msg.delete()
            return await message.reply_text(f"No results found for {file_name} on IMDB.")

        poster = movie_details.get('poster', None)
        movie_title = movie_details.get('title', 'N/A')
        genres = movie_details.get('genres', 'N/A')
        rating = movie_details.get('rating', 'N/A')
        plot = movie_details.get('plot', 'N/A')
        year = movie_details.get('year', 'N/A')

        caption_text = (
            f"<b>🔖Title: {movie_title}</b>\n"
            f"<b>🎬 Genres: {genres}</b>\n"
            f"<b>⭐️ Rating: {rating}/10</b>\n"
            f"<b>📆 Year: {year}</b>\n\n"
            f"<a href={file_link}>┏━━━━━━━━━━━┓\n┃📺 ᴡᴀᴛᴄʜ ɪɴ 𝐇𝐃  ┃\n┗━━━━━━━━━━━┛</a>\n"
            f"⚙️  ● 𝟺𝟾𝟶ᴘ |  ○𝟽𝟸𝟶ᴘ |  ● 𝟷𝟶𝟾𝟶ᴘ\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬"
        )

        if video:
            await msg.delete()
            await message.reply_video(
                video=video.file_id,
                caption=caption_text,
                parse_mode=enums.ParseMode.HTML
            )
        elif video_link:
            await msg.delete()
            await message.reply_video(
                video=video_link,
                caption=caption_text,
                parse_mode=enums.ParseMode.HTML
            )
        else:
            if poster:
                await msg.delete()
                await message.reply_photo(
                    poster,
                    caption=caption_text, 
                    parse_mode=enums.ParseMode.HTML
                ) 
            else:
                await msg.delete()
                await message.reply_text(
                    text=caption_text, 
                    parse_mode=enums.ParseMode.HTML
                ) 
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")

# insta reel download
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Length": "99",
    "Origin": "https://saveig.app",
    "Connection": "keep-alive",
    "Referer": "https://saveig.app/en",
}

@Client.on_message(filters.regex(r'https?://.*instagram[^\s]+') & ~filters.channel)
async def link_handler(client, message):
    link = message.text
    global headers
    try:
        m = await message.reply_sticker("CAACAgUAAxkBAAITAmWEcdiJs9U2WtZXtWJlqVaI8diEAAIBAAPBJDExTOWVairA1m8eBA")
        url = link.replace("instagram.com", "ddinstagram.com").replace("==", "%3D%3D")

        if url.endswith("="):
            url = url[:-1]
            dump_file = await message.reply_video(url, caption=f"ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏ <a href=https://t.me/{temp.U_NAME}>{temp.B_NAME}</a>")
        else:
            dump_file = await message.reply_video(url, caption=f"ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏ <a href=https://t.me/{temp.U_NAME}>{temp.B_NAME}</a>")

        await m.delete()

    except Exception as e:
        try:
            if "/reel/" in url:
                ddinsta = True 
                getdata = requests.get(url).text
                soup = bs4.BeautifulSoup(getdata, 'html.parser')
                meta_tag = soup.find('meta', attrs={'property': 'og:video'})
                try:
                    content_value = f"https://ddinstagram.com{meta_tag['content']}"
                except:
                    content_value = None
                if not meta_tag:
                    ddinsta = False
                    meta_tag = requests.post("https://saveig.app/api/ajaxSearch", data={"q": link, "t": "media", "lang": "en"}, headers=headers)
                    if meta_tag.ok:
                        res = meta_tag.json()
                        meta_links = re.findall(r'href="(https?://[^"]+)"', res['data']) 
                        content_value = meta_links[0] if meta_links else None
                    else:
                        return await message.reply("Oops, something went wrong.")

                if content_value:
                    try:
                        if ddinsta:
                            dump_file = await message.reply_video(content_value, caption=f"ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏ <a href=https://t.me/{temp.U_NAME}>{temp.B_NAME}</a>")
                        else:
                            dump_file = await message.reply_video(content_value, caption=f"ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏ <a href=https://t.me/{temp.U_NAME}>{temp.B_NAME}</a>")
                    except:
                        downfile = f"{os.getcwd()}/{random.randint(1,10000000)}"
                        with open(downfile, 'wb') as x:
                            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                            x.write(requests.get(content_value, headers=headers).content)
                        dump_file = await message.reply_video(downfile, caption=f"ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏ <a href=https://t.me/{temp.U_NAME}>{temp.B_NAME}</a>")

            elif "/p/" in url or "stories" in url:
                meta_tag = requests.post("https://saveig.app/api/ajaxSearch", data={"q": link, "t": "media", "lang": "en"}, headers=headers)
                if meta_tag.ok:
                    res = meta_tag.json()
                    meta_links = re.findall(r'href="(https?://[^"]+)"', res['data']) 
                else:
                    return await message.reply("Oops, something went wrong.")

                for link in meta_links:
                    try:
                        dump_file = await message.reply_video(link, caption=f"ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏ <a href=https://t.me/{temp.U_NAME}>{temp.B_NAME}</a>")
                        await asyncio.sleep(1)
                    except:
                        pass 

        except KeyError:
            await message.reply("400: Sorry, Unable To Find It. Make Sure It's Publicly Available :)")
        except Exception as e:
            error_trace = traceback.format_exc()
            print(f"Instagram Error: {e}\nTraceback: {error_trace}")
            await message.reply("400: Sorry, Unable To Find It. Try another or report it to support.")

        finally:
            if 'dump_file' in locals():
                pass
                #await dump_file.delete()  # Remove forwarding to DUMP_GROUP
            await m.delete()
