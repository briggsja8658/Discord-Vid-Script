import os
import sys
import time
import json
import datetime
import requests
import subprocess
import importlib.util
import googleapiclient
import googleapiclient.discovery
from typing import Final


class Config:
    #log_file: Final = "/home/briggsja/YT-to-discord-script/log_file.txt"
    log_file: Final = "log_file.txt"
    check_interval: Final = 1800
    
    test_channel: Final = "test"
    hardware_channel: Final = "hardware"
    networking_channel: Final = "networking"
    programming_channel: Final = "programming"
    mental_health_channel: Final = "mental-health"
    
    google_api_key: Final = 'AIzaSyAU523FX0kHP11IwJLcn2sWtvbRH5ovlzw'
    #json_file_path: Final = "/home/briggsja/YT-to-discord-script/discord_vid_state.json"
    json_file_path: Final = "./discord_vid_state.json"

    non_sense_url: Final = "https://discord.com/api/webhooks/1259606243115405344/EKI9T-96XX2l1Ky4_6VjxWIiAFB1sc2ypkxtkd3bjDDTpM8PmF7s-Jf2jra2AC3-ckcV"
    programming_url: Final = "https://discord.com/api/webhooks/1259609694553641021/bvUudFGOCLv41oi2XxzESZT1Y8BKzwrCvlLGFh9fgDqwXZO8eWonD1Q5Ro9XNzPvJdV6"
    networking_url: Final = "https://discord.com/api/webhooks/1376607648539087080/bFeDJm-Yc4Yqkw5whTaI1Mze7K__TqyY3uW3UVXYodIpwr2zryNF8W8jj_SjrsAvVL_e"
    mental_health_url: Final = "https://discord.com/api/webhooks/1376608620426428536/Z6149ZHAOe-auxzxOZN0ezUOoTlh9e4yjdGZeXusmlUWckr9L5HdT7XGgHL7GebirwBv"
    hardware_url: Final = "https://discord.com/api/webhooks/1376608800303218708/CzqHLqKm_c0cHeG8IzV21doBj9WQ14ZhAcT-SPXgjv9_vaz-9kjSnAG6lxTJ1MRtYfI5"
    test_url: Final = "https://discord.com/api/webhooks/1376616860786884609/xbHEJovhT-tdvVvpCLXHZksFKQ7i7KN9IsltNWh2l5NCbX6guoUNrChRHQ1YlkL24tWv"


class Tools:
    def check_libs(self, current_libs):
        """Check to see if imports are installed on the server. If not install them"""
        x = 0
        while x < len(current_libs):
            if importlib.util.find_spec(current_libs[x]) is None:
                print(f"{current_libs[x]} not found. Installing...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", current_libs[x]])
            x+=1

    def log_event(self, message):
        """Log event to log file"""
        with open(config.log_file, 'a') as file:
            file.write(f"{message}\n")


    def ms_to_readable_time(self, ms):
        """Convert milsecond to a readable time of year-month-day hour:min"""
        dt_object = datetime.datetime.fromtimestamp(ms)
        readable_time = dt_object.strftime('%Y-%m-%d %H:%M')
        return readable_time



class DiscordWebHook:
    
    
    def __init__(self):
        pass

    def post_new_vid(self, current_channel, current_channel_type):

        if current_channel_type == config.hardware_channel:
            requests.post(
                config.hardware_url, 
                data = json.dumps({
                    'content' : f'New video from {current_channel["channel_name"]}\nhttps://www.youtube.com/watch?v={current_channel["last_vid_id"]}',
                    'allowed_mentions': { 'parse': [] }, 'avatar_url' : "./pictures/Hardware Icon.webp", 'embeds' : [{ "color" : "#000dff" }]
                }),
                headers={'Content-Type': 'application/json'}
            )
        elif current_channel_type == config.programming_channel:
            requests.post(
                config.programming_url, 
                data = json.dumps({
                    'content' : f'New video from {current_channel["channel_name"]}\nhttps://www.youtube.com/watch?v={current_channel["last_vid_id"]}',
                    'allowed_mentions': { 'parse': [] }, 'avatar_url' : "./pictures/Programming Icon.webp", 'embeds' : [{ "color" : "#ff830e" }]
                }),
                headers={'Content-Type': 'application/json'}
            )
        elif current_channel_type == config.networking_channel:
            requests.post(
                config.networking_url, 
                data = json.dumps({
                    'content' : f'New video from {current_channel["channel_name"]}\nhttps://www.youtube.com/watch?v={current_channel["last_vid_id"]}',
                    'allowed_mentions': { 'parse': [] }, 'avatar_url' : "./pictures/Networking Icon.webp", 'embeds' : [{ "color" : "#00ff2f" }]
                }),
                headers={'Content-Type': 'application/json'}
            )
        elif current_channel_type == config.test_channel:
            result = requests.post(
                config.test_url, 
                headers={'Content-Type': 'application/json'},
                json = {
                    'content' : f'New video from {current_channel["channel_name"]}\nhttps://www.youtube.com/watch?v={current_channel["last_vid_id"]}',
                    'allowed_mentions': { 'parse': [] }, 
                    'avatar_url' : "./pictures/Learning-Content-Logo.png", 
                    'embeds' : [{ "color" : "#ffffff" }]
                }
            )
            print(result)



class YouTube:
    
    def __init__(self):
        self.channels = self.init_state()
        self.youtube_api = googleapiclient.discovery.build('youtube', 'v3', developerKey=config.google_api_key)
    

    def init_state(self):
        if os.path.exists(config.json_file_path) == False:
            with open(config.json_file_path, 'w') as file:
                json.dump({}, file, indent=4)


        #2 is the default value of an empty json file
        if os.path.getsize(config.json_file_path) <= 2:         
            state_data = [
                #Hardware Channels
                {"channel_name":"Linus Tech Tips" , "channel_id":"@LinusTechTips" , "last_vid_id":"" , "channel_type":config.hardware_channel},
                {"channel_name":"Level 1 Techs" , "channel_id":"@Level1Techs" , "last_vid_id":"" , "channel_type":config.hardware_channel},
                {"channel_name":"GamersNexus" , "channel_id":"@GamersNexus" , "last_vid_id":"" , "channel_type":config.hardware_channel},
                {"channel_name":"Paul's Hardware" , "channel_id":"@paulshardware" , "last_vid_id":"" , "channel_type":config.hardware_channel},
                {"channel_name":"Serve The Home" , "channel_id":"@ServeTheHomeVideo" , "last_vid_id":"" , "channel_type":config.hardware_channel},
                {"channel_name":"Jayz Two Cents" , "channel_id":"@JayzTwoCents" , "last_vid_id":"" , "channel_type":config.hardware_channel},
                {"channel_name":"Actually Hardcore Overclocking" , "channel_id":"@ActuallyHardcoreOverclocking" , "last_vid_id":"" , "channel_type":config.hardware_channel},
                {"channel_name":"Storage Review" , "channel_id":"@StorageReview" , "last_vid_id":"" , "channel_type":config.hardware_channel},

                #Networking Channels
                {"channel_name":"Redhat" , "channel_id":"@redhat" , "last_vid_id":"" , "channel_type":config.networking_channel},
                {"channel_name":"Craft Computing" , "channel_id":"@CraftComputing" , "last_vid_id":"" , "channel_type":config.networking_channel},
                {"channel_name":"Level 1 Linux" , "channel_id":"@Level1Linux" , "last_vid_id":"" , "channel_type":config.networking_channel},
                {"channel_name":"Lawrence Systems" , "channel_id":"@LAWRENCESYSTEMS" , "last_vid_id":"" , "channel_type":config.networking_channel},
                {"channel_name":"Network Chuck" , "channel_id":"@NetworkChuck" , "last_vid_id":"" , "channel_type":config.networking_channel},

                #Programming Channels
                {"channel_name":"Prime Time-agen" , "channel_id":"@ThePrimeTimeagen" , "last_vid_id":"" , "channel_type":config.programming_channel},
                {"channel_name":"Theo Browne" , "channel_id":"@t3dotgg" , "last_vid_id":"" , "channel_type":config.programming_channel},
                {"channel_name":"Tina Huang" , "channel_id":"@TinaHuang1" , "last_vid_id":"" , "channel_type":config.programming_channel},
                {"channel_name":"The Vim-eagen" , "channel_id":"@TheVimeagen" , "last_vid_id":"" , "channel_type":config.programming_channel},
                {"channel_name":"Backend Banter" , "channel_id":"@backendbanterfm" , "last_vid_id":"" , "channel_type":config.programming_channel},
                {"channel_name":"TJ Devries" , "channel_id":"@teej_dv" , "last_vid_id":"" , "channel_type":config.programming_channel},
                {"channel_name":"The Prime-agen" , "channel_id":"@ThePrimeagen" , "last_vid_id":"" , "channel_type":config.programming_channel},
                {"channel_name":"Low Level Learning" , "channel_id":"@LowLevelLearning" , "last_vid_id":"" , "channel_type":config.programming_channel},
                {"channel_name":"Frontend Masters" , "channel_id":"@FrontendMasters" , "last_vid_id":"" , "channel_type":config.programming_channel},
                {"channel_name":"Theo Browne Rants" , "channel_id":"@theorants" , "last_vid_id":"" , "channel_type":config.programming_channel},
                {"channel_name":"Google Developers" , "channel_id":"@GoogleDevelopers" , "last_vid_id":"" , "channel_type":config.programming_channel},
                {"channel_name":"Developer Voices" , "channel_id":"@DeveloperVoices" , "last_vid_id":"" , "channel_type":config.programming_channel},
                {"channel_name":"NVIDIA Design Studio" , "channel_id":"@NVIDIA-Studio" , "last_vid_id":"" , "channel_type":config.programming_channel},
                {"channel_name":"Onur Mutlu" , "channel_id":"@OnurMutluLectures" , "last_vid_id":"" , "channel_type":config.programming_channel},
                {"channel_name":"John Blow" , "channel_id":"@jblow888" , "last_vid_id":"" , "channel_type":config.programming_channel},
                {"channel_name":"Continuous Delivery" , "channel_id":"@ContinuousDelivery" , "last_vid_id":"" , "channel_type":config.programming_channel},
                {"channel_name":"Brian Will" , "channel_id":"@briantwill" , "last_vid_id":"" , "channel_type":config.programming_channel},
                {"channel_name":"NVIDIA" , "channel_id":"@NVIDIA" , "last_vid_id":"" , "channel_type":config.programming_channel},
                {"channel_name":"Ginger Bill" , "channel_id":"@GingerGames" , "last_vid_id":"" , "channel_type":config.programming_channel},
                {"channel_name":"NVIDIA Developer" , "channel_id":"@NVIDIADeveloper" , "last_vid_id":"" , "channel_type":config.programming_channel},
                {"channel_name":"Code Aesthetic" , "channel_id":"@CodeAesthetic" , "last_vid_id":"" , "channel_type":config.programming_channel},
                {"channel_name":"Matteo Collina" , "channel_id":"@adventuresinnodeland" , "last_vid_id":"" , "channel_type":config.programming_channel},
                {"channel_name":"Pirate Software" , "channel_id":"@PirateSoftware" , "last_vid_id":"" , "channel_type":config.programming_channel},
                {"channel_name":"AI Flux" , "channel_id":"@aifluxchannel" , "last_vid_id":"" , "channel_type":config.programming_channel},

                #Mental Health Channels
                {"channel_name":"Healthy Gamer" , "channel_id":"@HealthyGamerGG" , "last_vid_id":"" , "channel_type":config.mental_health_channel},
                {"channel_name":"Man Talks" , "channel_id":"@ManTalks" , "last_vid_id":"" , "channel_type":config.mental_health_channel},
                {"channel_name":"Modern Wisdom" , "channel_id":"@ChrisWillx" , "last_vid_id":"" , "channel_type":config.mental_health_channel},
                {"channel_name":"I Wish You Knew" , "channel_id":"@iwishyouknewpodcast" , "last_vid_id":"" , "channel_type":config.mental_health_channel},
                {"channel_name":"Jeremy Ethier" , "channel_id":"@JeremyEthier" , "last_vid_id":"" , "channel_type":config.mental_health_channel},
                {"channel_name":"Model Health Show" , "channel_id":"@TheShawnModel" , "last_vid_id":"" , "channel_type":config.mental_health_channel},
                {"channel_name":"Rikki and Jimmy" , "channel_id":"@rikkiandjimmyonrelationships" , "last_vid_id":"" , "channel_type":config.mental_health_channel},
                {"channel_name":"Charisma on Command" , "channel_id":"@Charismaoncommand" , "last_vid_id":"" , "channel_type":config.mental_health_channel},
                {"channel_name":"Thais Gibson" , "channel_id":"@ThePersonalDevelopmentSchool" , "last_vid_id":"" , "channel_type":config.mental_health_channel},
                {"channel_name":"Courtney Ryan" , "channel_id":"@CourtneyRyan" , "last_vid_id":"" , "channel_type":config.mental_health_channel},
                {"channel_name":"Adam Lane Smith" , "channel_id":"@AttachmentAdam" , "last_vid_id":"" , "channel_type":config.mental_health_channel},
                {"channel_name":"The Space" , "channel_id":"@sutcliffedavid" , "last_vid_id":"" , "channel_type":config.mental_health_channel},
                {"channel_name":"Matthew Hussey" , "channel_id":"@thematthewhussey" , "last_vid_id":"" , "channel_type":config.mental_health_channel},
                {"channel_name":"Lynn Everly" , "channel_id":"@Lynneverly" , "last_vid_id":"" , "channel_type":config.mental_health_channel},
                {"channel_name":"Diary of a CEO" , "channel_id":"@TheDiaryOfACEO" , "last_vid_id":"" , "channel_type":config.mental_health_channel},
                {"channel_name":"Lewis Howes" , "channel_id":"@lewishowes" , "last_vid_id":"" , "channel_type":config.mental_health_channel},
                {"channel_name":"Science of People" , "channel_id":"@ScienceOfPeople" , "last_vid_id":"" , "channel_type":config.mental_health_channel},
                {"channel_name":"Ben Greenfield" , "channel_id":"@bengreenfieldlife" , "last_vid_id":"" , "channel_type":config.mental_health_channel},
                {"channel_name":"Andrew Huberman" , "channel_id":"@hubermanlab" , "last_vid_id":"" , "channel_type":config.mental_health_channel},
            ]

            

            with open(config.json_file_path, 'w') as file:
                json.dump(state_data, file, indent=4)
            
        if os.path.getsize(config.json_file_path) > 2:
            with open(config.json_file_path, 'r') as file:
                state_data = json.load(file)

        return state_data


    def get_last_vid_id(self, current_channel):
        try:
            response = self.youtube_api.channels().list(
                part='contentDetails',
                forHandle=self.channels[current_channel]["channel_id"]
            ).execute()

            playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

            video = self.youtube_api.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=1
            ).execute()

            return video['items'][0]['contentDetails']['videoId']
        except Exception as error:
            tools.log_event(f'There was an error getting YouTube Data\n{error}')
    

    def save_state(self):
        with open(config.json_file_path, 'w') as file:
            json.dump(self.channels, file, indent=4)



#Objects
config = Config()
tools = Tools()
discord = DiscordWebHook()
youtube_data = YouTube()


while True:
    current_time = time.time()
    tools.log_event(f'Last video check was at {tools.ms_to_readable_time(current_time)}')
    x=0
    while x < len(youtube_data.channels):
        current_vid_id = youtube_data.get_last_vid_id(x)
        if current_vid_id != None:
            if youtube_data.channels[x]["last_vid_id"] != current_vid_id: 
                youtube_data.channels[x]["last_vid_id"] = current_vid_id
                tools.log_event(f'New video from {youtube_data.channels[x]["channel_name"]} @ {tools.ms_to_readable_time(current_time)}')
                youtube_data.save_state()
                current_channel_type = ""
                if youtube_data.channels[x]["channel_type"] == config.hardware_channel : current_channel_type = config.hardware_channel
                elif youtube_data.channels[x]["channel_type"] == config.networking_channel : current_channel_type = config.networking_channel
                elif youtube_data.channels[x]["channel_type"] == config.programming_channel : current_channel_type = config.programming_channel
                elif youtube_data.channels[x]["channel_type"] == config.mental_health_channel : current_channel_type = config.mental_health_channel
                else : current_channel_type = config.test_channel
                discord.post_new_vid(youtube_data.channels[x], current_channel_type)
        else:
            x = len(youtube_data.channels)
        x += 1
    time.sleep(config.check_interval)
