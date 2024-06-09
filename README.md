# PyWebRadio
A program that plays audio like a radio station to a browser and/or Discord bot

Originally created for my own internet radio station, [98.6 WCCK](https://wcckdeadfm.com), now re-mastered and available for anyone to use.

# Installation
Download the program and run the executable, all config files should be created automatically. Make sure to leave the `End`, `Jingles`, and `Music` folders alone for now.

To stream audio to the web you'll need a virtual audio cable of your choosing. Once you've downloaded and setup your VAC, **set your system's default input device to the VAC's output** and set either your default system output or the program's output to the VAC's input. I've been using [VB-Audio's VAC](https://vb-audio.com/Cable/) for this project, but you can use whichever one you'd like.
> [!WARNING]
> The program will stream whatever device is set as its input to the web, ***including microphones***. Make sure to double check that your inputs and outputs are set correctly before making your site public.
If you decide to use VB-Audio's VAC, your audio settings should look something like this

To stream audio through a Discord bot, you'll need to download [ffmpeg](https://ffmpeg.org/) and place `ffmpeg.exe` in the program's folder next to the executible.



# Setup
To be able to stream audio properly to the web, you'll need a virtual audio cable of your choosing. 
