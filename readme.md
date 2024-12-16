
# Comfy UI NewGens

Use ComfyUI to generate NewGen images for Football Manager 2024

# Intro

![enter image description here](https://raw.githubusercontent.com/karl0ss/comfy_fm24_newgens/refs/heads/main/photo-collage.png)

- "There are 10000s of faces out there already"
- "There are tools that work the same already?"
- "Have you got nothing better to do with your time?"

[Example video here](https://www.youtube.com/watch?v=mcGj3_nbV0A)

  

These are some of the questions I think you are going to ask me, but I present to you somehting I have been working on, **Comfy FM24 NewGens**

# The Idea

Taking some inspiration from [fm-ai-face-generator](https://github.com/emilmirzayev/fm-ai-face-generator), but not wanting to pay for a hosted service (I already have AI _stuff_ setup on my home server) I started to rewrite chunks to make compatible with a hosted Comfy UI instance, after awhile, I had rewritten so much, that this is now a new beast in itself..

  

Also taking inspiration from [NewGAN-Manager](https://github.com/franl08/NewGAN-Manager) and reworking some of thier code for my uses.

  

Thanks to both!

  

So what does this do? Why would you want to use it? (you probably wont but personally, I like a bit more personallisation from my NewGens, some, I get quite attached to :) )

  

- This will create images for your NewGens, based off of information provided from the FM database, making a players image more unique to that player
- download the images to the specified output directory, all processed players image will be saved as their **uid** from the game
- remove all the background from the generated faces
- create the needed config file for FM to load the faces,
- you can then rename the generated folder and place it in your **graphics** folder as you would noramlly and voila!

  

# Install Guide

  
Things you will need that I will not be going over on how to setup.

 - Python installed
 - Git installed
 - A ComfyUI installation (On hosted server, or [portable](https://github.com/YanWenKun/ComfyUI-Windows-Portable))
	 - My suggestion it to use the [Realistic Vision 6](https://civitai.com/models/4201/realistic-vision-v60-b1) model

If you have that, then carry on for Windows instructions 
 - Use Git to checkout this repo
 - You need to get a `rtf` file of the players you want to add images for, to do this you need the view and filter supplied with the project
 - Copy the `filters` and `views` folder over to your `Football Manager 2024` data folder in `Documents`, this may create these folders, or may just add the contained files into your existing folders
	 - You can use `python INSTALL_VIEW_AND_FILTER.py` to do this automatically 
 - Included is the original `is newgen` filter created by the NewGAN-Manager team and a new view created by myself to get the needed data
 - If you follow [this video](https://youtu.be/pmdIkhfmY6w?t=564) it will show you how to export the `rtf` file, you want to use our view, not the view in the video
 - Once you have your `rtf` file add it to the root of the current repo
 - Create a python virtual environment `python -m venv venv`
 - Activate the venv `.\venv\Scripts\activate`
 - Install the requirements `pip install -r requirements.txt`
 - Copy the `user_config.cfg.sample` to `user_config.cfg` and make the needed changes
	 - football_manager_version - Version of FM to generate for. Defautls to `2024`
	 - output_dir - Where to save the generated set. Defaults to `./generated_images/`
	 - comfyui_url - HTTP location of your comfyui installation. 
	 - model - Model to be used, by default `realisticVisionV60B1_v51HyperVAE.safetensors` is set, this is my suggested model at the moment.
- At this point you should be able to run and start to generate by running the command `python comfy_fm_newgen.py --rtf_file ExportedFile.rtf`
	- ExportedFile is the name of the file that you exported and saved with your newgen list


You should get some console output of the progress, good luck!

Open an issue here if your having problems

Thanks