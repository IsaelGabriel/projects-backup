const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => res.send("Chaaamaaa"));

app.listen(port, () => console.log(`Datribo listening at http://localhost:${port}`));

//bot code

const { prefix, token } = require('./config.json');
const Discord = require('discord.js');
const { AssertionError } = require('assert');
const client = new Discord.Client();

client.once('ready', () => {
	console.log('Ready!');
});


client.login(token);

client.on('message', message => {
    if (message.author.bot) return;
    if (message.author == client.user) return;
    if (!message.content.startsWith(prefix))
    {
        const mess = message.content.toLowerCase();
        if(mess.includes('truco')) message.channel.send("6");
        return;
    }
    if (message.channel.type === "dm") return;
    var i = 0;
    const args = message.content.slice(prefix.length).trim().split(' ');
    const command = args.shift().toLowerCase();
    switch (command)
    {
        case 'tiro':
            i = 1
        break;

        case 'server':
            var embed = new Discord.MessageEmbed()
            .setColor('RANDOM')
            .setTitle(`**SERVER INFO**`)
            .setDescription(`Estou no server: ${message.guild.name}!\nCom ${message.guild.memberCount} usuários.`)
            .setTimestamp()
            .setFooter(`Comando solicitado por: ${message.author.username}`);
            message.channel.send({embed});
        break;

        case 'uinfo':
            i = 2
        break;

        case 'ping':
            i = 3
        break;

        case 'join':
            join(message.member.voice.channel)
        break;

        case 'help':
            message.channel.send(`Estou aqui para ajudar\n${prefix}tiro atira me alguem!!!`)
        break;
    }

    if(i != 0)
    {
        const taggedUser = message.mentions.users.first();
        const target = (taggedUser)? taggedUser : message.author;
        if(i == 1)
        {
            if(args.length && !taggedUser)
            {
                message.channel.send('Desculpe, insira um usuário valido');
            }else
            {
                var embed = new Discord.MessageEmbed()
                .setColor('RANDOM')
                .setTitle(`**:gun:TIRO:gun:**`)
                .setDescription(`:gun: **POW!** Acabo de executar ${target}! :gun:`)
                .setTimestamp()
                .setFooter(`Contratado por: ${message.author.username}`);
                message.channel.send({embed});
            }
        }else if (i == 2)
        {
            if(args.length && !taggedUser)
            {
                message.channel.send('Desculpe, insira um usuário valido');
            }else
            {
                var embed = new Discord.MessageEmbed()
                .setColor('RANDOM')
                .setTitle(`**USER INFO**`)
                .setDescription(`${target}\nUser: ${target.username}\nID: ${target.id}`)
                .setTimestamp()
                .setFooter(`Comando solicitado por: ${message.author.username}`);
                message.channel.send({embed});
            }
        }else if (i == 3)
        {
            var embed = new Discord.MessageEmbed()
            .setColor('RANDOM')
            .setTitle(`**PING**`)
            .setDescription(`:ok_hand:Latência é **${Date.now() - message.createdTimestamp}ms**.:ok_hand:\n:ok_hand:Latência API é **${Math.round(client.ws.ping)}ms**.:ok_hand:`)
            .setTimestamp()
            .setFooter(`Ping solicitado por: ${message.author.username}`);
            message.channel.send({embed});
        }
    }
    
});

/*async function play(voiceChannel) {
	const connection = await voiceChannel.join();
	connection.play('audio.mp3');
}*/

async function join(vc)
{
    const connection = await vc.join();
}