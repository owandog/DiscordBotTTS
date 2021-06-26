async def textfunc(message):
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