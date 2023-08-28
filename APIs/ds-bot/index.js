class Command {
  constructor(str,mtd){
      this.str = ""+str;
      this.mtd = mtd;
  }
}

class Nomination {
  constructor(id)
  {
    this.id = id;
    this.state = "nominating";
    this.options = [];
  }
}


// Require the necessary discord.js classes
const { Client, Intents, Message } = require('discord.js');
const Discord = require('discord.js');
const { token } = require('./config.json');
const { prefix } = require('./config.json');


// Create a new client instance
//const client = new Client({ intents: [Intents.FLAGS.GUILDS] });
/*const  client = new Discord.Client({
  intents: [
    "GUILDS",
    "GUILD_MESSAGES"
  ]

});*/

const myIntents = new Intents([
 "GUILDS",
 "GUILD_MESSAGES",
 "GUILD_MESSAGE_REACTIONS",
 "DIRECT_MESSAGES",
 "DIRECT_MESSAGE_REACTIONS"
]);
const client = new Discord.Client({intents : myIntents});


// When the client is ready, run this code (only once)
client.once('ready', () => {
  console.log("Ready!");
	console.log(`Logged in as ${client.user.tag}`);
    
});

/*client.on("messageCreate", async (Client, msg) => {
    //if(msg.author.bot) return;
    //if(msg.author === client) return;

    console.log(msg);

    if(msg === 'truco') msg.channel.send("6");

});*/

/*client.on('interactionCreate', async interaction => {
	//if (!interaction.isCommand()) return;

	if (interection === 'ping') {
		await interaction.reply('Pong!');
	} else if (interaction === 'server') {
		await interaction.reply('Server info.');
	} else if (interaction === 'user') {
		await interaction.reply('User info.');
	}
});*/

const nominations = [];

const commands = [
  new Command("ping",function(m) {m.channel.send("Pong! :)")}),

  new Command("nomear", function(m){
    for(var i = 0; i < nominations.length; i++)
    {
      if(nominations[i].id == m.guild.id && nominations[i].state == "nominating")
      {
        m.reply("Uma nomeação já foi iniciada nesse servidor, finalize-a utilizando %finish");
        return;
      }
    }
    /*if(nominations.includes(m.guild.id))
    {
      m.channel.send("Uma nomeação já foi iniciada nesse servidor");
    }*/

    nominations.push(new Nomination(m.guild.id));

    m.channel.send("Nomeação iniciada!");
  }),

  new Command("add", function(m)
  {
    const nominating = false;
    const index = 0;
    for(var i = 0; i < nominations.length; i++)
    {
      if(nominations[i].id == m.guild.id && nominations[i].state == "nominating")
      {
        nominating = true;
        index = i;
      }
    }
    if(!nominating)
    {
      m.reply("Esse servidor não tem uma nomeação aberta para adição no momento, tente criar uma ou esperar a atual acabar");
      return;
    }

    const arg = m.content.split("add",1).join();
    nominations[i].options.push("arg");
    m.reply("Opção " + arg + "adicionada!");

  })
];



client.on("messageCreate", (message) => { // When a message is created
    
    if(!message.content.startsWith(prefix)) return;
    const command = message.content.split(prefix).join('');

    for(var i = 0; i < commands.length; i++)
    {
        if(command == commands[i].str) commands[i].mtd(message);
    }


})



// Login to Discord with your client's token
client.login(token);


