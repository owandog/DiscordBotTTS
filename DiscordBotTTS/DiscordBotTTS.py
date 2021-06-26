import discord
import html
from discord.channel import VoiceChannel
from discord.player import FFmpegPCMAudio
from google.cloud import texttospeech
import re

Discord_TOKEN = "ODU4MTY3NTA3Njk2NDg0Mzcy.YNaMxQ.tIV9JUwdz-UUREkoVZDprvPdO0A"
client = discord.Client()

voiceChannel: VoiceChannel 
messageChannel = None

@client.event
async def on_ready():
    print('Login!')
    
@client.event
async def on_message(message):
    global voiceChannel
    global messageChannel

    if message.author.bot:
        return
    if message.content == 'dog!c':
        if message.author.voice is None:
            await message.channel.send('ワーウ？(ボイスチャンネルがわからないみたい)')
            return
        
        if messageChannel == None:
            messageChannel = message.channel

            voiceChannel = await VoiceChannel.connect(message.author.voice.channel)
            await messageChannel.send('ワン！(TtSDogがやってきた！)')
            return

        else:
            await message.channel.send('ワウーン...(TtSDogは他のボイスチャンネルで働いてるみたい)')
            return
    
    if message.content == 'dog!dc':
        if message.channel == messageChannel:
            voiceChannel.stop()
            await voiceChannel.disconnect()
            await messageChannel.send('ワオーン！(TtSDogはお家に帰ります)')
            messageChannel = None
            return
        else:
            await message.channel.send('ワウー？(TtSDogは他のテキストチャンネルで呼ばれたみたい)')
            await message.channel.send(messageChannel.name)
            return
        
    if message.channel == messageChannel:
        play_voice(message.content)
    
def text_to_ssml(text):
    pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    if re.match(pattern, text):
        text = "URL読めないって"
    elif len(text) > 30:
        text = text[0:30]

    escaped_lines = html.escape(text)
    ssml = "{}".format(
        escaped_lines
    )
    return ssml

def ssml_to_speech(ssml, file, language_code, gender):
    ttsClient = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=ssml)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, ssml_gender=gender
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = ttsClient.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    with open(file, "wb") as out:
        out.write(response.audio_content)
        print("Audio content written to file " + file)
    return file

def play_voice(text):
    ssml = text_to_ssml(text)
    file = ssml_to_speech(ssml, "voice.mp3", "ja-JP", texttospeech.SsmlVoiceGender.MALE)
    voiceChannel.play(FFmpegPCMAudio(executable="D:\\Work\\Dev\\ffmpeg\\bin\\ffmpeg.exe", source=file))
    
@client.event
async def on_voice_state_update(member, before, after):
    global voiceChannel
    global messageChannel
    if member.bot:
        return
    if after.channel == None:
        if len(before.channel.members) == 1:
            voiceChannel.stop()
            await voiceChannel.disconnect()
            await messageChannel.send('ワオーン！(ひとりで寂しくなったのでTtSDogはお家に帰ります)')
            messageChannel = None

client.run(Discord_TOKEN)

