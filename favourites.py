import random 

import subprocess

def open_image_of_lutfa():
  paths = [
          ["/home/aizen/Downloads/1f73b4ea-67fd-4569-bf88-8cfc353e467e.jpeg"],
          ["/home/aizen/Pictures/Screenshot 2026-05-23 155403.png"]
  ]
  file_path = random.choice(paths)
  final_path = file_path[0]
  subprocess.run(["xdg-open", final_path])

musics = [
  ["https://music.youtube.com/watch?v=bnqV2jpYf5Y&list=RDAMVMbnqV2jpYf5Y"],
  ["https://music.youtube.com/watch?v=I_ohtoZwJjY&list=LM"],
  ["https://music.youtube.com/watch?v=ZYP84UHWOOI&list=LM"],
  ["https://music.youtube.com/watch?v=bE4iy13IUMA&list=LM"],
  ["https://music.youtube.com/watch?v=pm2QaHKaKRo&list=LM"],
]

music_choice = random.choice(musics)
# print(music_choice[0])
facebook_id = "https://www.facebook.com/profile.php?id=61577523290863"