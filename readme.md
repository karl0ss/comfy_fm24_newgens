# Comfy UI NewGens
Use ComfyUI to generate NewGen images for Football Manager 2024
# Intro
![enter image description here](https://preview.redd.it/comfy-fm24-newgens-v0-8vf2u79pn17e1.png?width=1080&crop=smart&auto=webp&s=e2e3d39d559507e7b2fee7150fc14cfdefb23c15)
-   "There are 10000s of faces out there already"
-   "There are tools that work the same already?"  
-   "Have you got nothing better to do with your time?"
    
[Example video here](https://www.youtube.com/watch?v=mcGj3_nbV0A)

These are some of the questions I think you are going to ask me, but I present to you somehting I have been working on,  **Comfy FM24 NewGens**
# The Idea
Taking some inspiration from  [fm-ai-face-generator](https://github.com/emilmirzayev/fm-ai-face-generator), but not wanting to pay for a hosted service (I already have AI  _stuff_  setup on my home server) I started to rewrite chunks to make compatible with a hosted Comfy UI instance, after awhile, I had rewritten so much, that this is now a new beast in itself..

Also taking inspiration from  [NewGAN-Manager](https://github.com/franl08/NewGAN-Manager)  and reworking some of thier code for my uses.

Thanks to both!

So what does this do? Why would you want to use it? (you probably wont but personally, I like a bit more personallisation from my NewGens, some, I get quite attached to :) )

 -   This will create images for your NewGens, based off of information provided from the FM database, making a players image more unique to that player
 -   download the images to the specified output directory, all processed players image will be saved as their  **uid**  from the game
 -   remove all the background from the generated faces
 -   create the needed config file for FM to load the faces,
 -   you can then rename the generated folder and place it in your  **graphics**  folder as you would noramlly and voila!
   

# Install Guide

- Use Git to checkout this repo
- You need to get a `rtf` file of the players you want to add images for, to do this you need the view and filter supplied with the project
- Copy the `filters` and `views` folder over to your `Football Manager 2024` data folder, this may create these folders, or may just add the contained files into your existing folders
  - Included is the original `is newgen` filter created by the NewGAN-Manager team and a new view created by myself to get the needed data
  - If you follow [this video](https://youtu.be/pmdIkhfmY6w?t=564) it will show you how to export the `rtf` file, you want to use our view, not the view in the video
