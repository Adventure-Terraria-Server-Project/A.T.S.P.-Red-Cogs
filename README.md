# A.T.S.P.-Red-Cogs
Plugins for the [Discord bot Red](https://github.com/Cog-Creators/Red-DiscordBot)  
These cogs are either self-coded or modified from others. I'll definitely link to source.  
These cogs are being used on the [A.T.S.P.](https://yamahi.eu) [Discord Server](https://s.yamahi.eu/chat) for several different tasks.

Install repo  
`[p]cog repo add atsp https://github.com/Nama/A.T.S.P.-Red-Cogs`  

## ProtonDB
Get tier from [ProtonDB](https://www.protondb.com)

* pdb

## ToDo
**No, these are not things which I have to do. It's a cog!**  

Every user has his own ToDo list, on which they can add and remove single entries.  
Install cog  
`[p]cog install atsp todo`
* Commands *Use with your prefix*
  * help todo
  * todo  
    *Shows your own ToDo list*
  * todo add  
    *Add a new ToDo - limited to 200 characters*
* todo insert  
    *Insert a new ToDo to a position*
* todo rm Index-Number  
    *Remove a ToDo*

## Reminder
**"Forked" from [RemindMe](https://github.com/Twentysix26/Red-Cogs/)**  
Reminds you, or someone else after a specific time amount in a channel. Needs **python-dateutil** now!  
Install cog  
`[p]cog install atsp reminder`

### Commands
* forgetme  
  *Removes all your active reminders*
* remind  
  *Either reminds you "me" or reminds another user. You need to use their username.*

# Archive?
I dont plan to update the below cogs
## Messages
Greet new members and use a broadcast with a delay on a channel  
Allows only Administrators to use the commands.  
`[p]msgs start` is autostarted  
Install cog  
`[p]cog install atsp messages`

### Commands
* welcome
  * chan  
    *Set the channel on which to greet the new members*
  * text  
    *Define the welcome message. To mention the member, put in the text `member.mention`*
* msgs
  * add  
    *Add a message to the broadcast*
  * chan  
    *Set the channel for the broadcast*
  * delay  
    *The delay in __seconds__ between the messages*
  * list  
    *Show the delay, channel and all added messages*
  * rm  
    *Remove a message from the broadcast*
  * start  
    *Start the broadcast. Channel, delay and at least one message need to be set.*  
    *Autostarts on cog loading*
  * stop  
    *Stop the broadcast. Happens also if you add or remove messages from the broadcast.*

## NitroBoost
Shows a list of members who are boosting the server. Also posts if a member starts or stops boosting the server.

### Commands
* booster  
  *Shows the list*

## VoteUtils
Reaction based commands for raffles and votes

Install cog  
`[p]cog install atsp voteutils`

### Commands
* votes  
  *Shows the messages of the last 20 days with the amount of :thumbsup: emojis as a ranking from the specified channel*
  * chan  
    *Set the channel where the messages with the vote are*
* raffle  
  *Chooses a random winner from the message with the specified emoji*