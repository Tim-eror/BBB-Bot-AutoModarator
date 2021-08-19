# BBB-Bot-AutoModarator
Hi, this is a little handmade side Projects so don’t await to many changes in the next time
## What Is this?
This is a Bot that is made to add commands and auto moderation to the BigBlueButton (BBB) chat. 
But if you want you can use my code to run your own on commands for the BBB chat 
## What does it do?
Currently the following services are available:
-	/help for help
-	/frage to send an audio ping at the bot owner 
-	/mic to send another audio ping at the bot owner
## Why does it exist?
Why not?
## How does it work?
I use selenium to start an automated browser instance to interfere with the web-application and read the chat. If somebody writs a message its checks and if it’s a command its executed. 
## Why does it work this way?
Well first, I’m a programming newling so it could be that there is a better solution that I don’t know. If you want to do better, well I’m not stopping you.

I chose this approach because it’s the only way to interfere with BBB without knowing the sever-secrets. 
I know that there is a BBB-API for this kind of work, but I can’t interfere with it because as I said, I don’t know the Sever secrets. 
