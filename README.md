# Table of Content

- [Goal](#goal)
- [Project planning](#project-planning-and-difficulties)
- [Conclusion](#conclusion)

Note: This project is from 2021 and may no longer work

# Goal

Write an web interface / API, from Stryder (the name given for the players statistics backend of Apex Legends), to anyone.

# Project planning and difficulties

For calling Stryder, you need to specify an user id of an user to get his statistics. The best way to get an uid by an username for a player, is to use the EA Origin launcher friend research.

So, I needed to write a script that imitates Origin Laucher for login an user and get an auth token, and an other script to search others users and get their uid. I found two scripts to do that, they were dated from ~2 years not working, but they gave me importants informations on the complex process of login in Origin. My script is written [here](https://github.com/jeremie-j/OriginAPI/blob/master/modules/origin_api.py), and (at this time) it work from scratch with an email and password of an Origin Account.

For the Stryder part, with only the right endpoint, the uid and hardware of a player, you can get his stats.

From here, there are two issues:

- Stryder is used for the banner in the game, and send you only the informations displayed in the banner of a player.
  <img width="392" alt="image" src="https://user-images.githubusercontent.com/64561439/166124200-faafd8ae-4554-4e11-90dd-012f41e4e23a.png">
  e.g, for this Player, the only informations I can get from Stryder, is the legend played, the skin, the pose, the banner background, max 3 badges and max 3 trackers and their values.

Since Stryder return values for the legend selected in the lobby for a player. The strategy is regularly repeat this request and append the data of a player in my database to append new legend,trackers,badges and others informations.

- Stryder response look like this:

```
"cdata1": 2147483648,
"cdata2": 1409694078,
"cdata3": 493570024,
"cdata4": 566328574,
"cdata5": 941740319,
"cdata6": 1774065557,
"cdata7": 3,
"cdata8": 1488777442,
"cdata9": 2,
"cdata10": 1488777442,
"cdata11": 2,
"cdata12": 1509839340,
"cdata13": 2,
"cdata14": 1905735931,
"cdata15": 2,
"cdata16": 1905735931,
"cdata17": 2,
"cdata18": 913787992,
"cdata19": 2147483648,
"cdata20": 2147483648,
"cdata21": 2147483648,
"cdata22": 2147483648,
"cdata23": 1,
"cdata24": 41,
"cdata25": 2147483648,
"cdata26": 2147483648,
"cdata27": 2147483648,
"cdata28": 2147483648,
"cdata29": 2147483648,
"cdata30": 2147483648,
"cdata31": 0,
```

So I needed a mapping for which "cdata" correspond to which information. And an another mapping for the values of theses "cdata", some of them are only int value (e.g. "cdata23": 1, correspond to the level of the player, lvl 1). But some are pairs of cdata, for tracker, one cdata is for the name, and the next one is for the value, so i needed to map every tracker names, badges names, skins names, poses names, banner backgrounds to their ids, (e.g. 1545736565 is for tracker "Season 12 kills" for the legends ash")

Since there is 23 badges, and at least 21 trackers for each legends (20 of them at that time). I would have needed to map more than 900 values to a name. I wrote a script to call an already existant api for apex legends (apexlegendsstatus.com), call stryder with the same player, get the id from stryder, and the corresponding string from Apex Legends Status. It worked well, but I never run the script long enough to map every values of the games.

# Conclusion

This projet was very interesting, I saw the basics of reverse engeenering. I came to something that work and I am happy with that. Maintaining the code is a nightmare with my level, recently, Apex legends change the names of a lot of trackers in the game, my mapping is not longuer up to date. Since the start of this project, ssh pinning has also been added to the game, so spoofing the backend endpoint has became really difficult. Some functionalities that I wanted in the API require data miningwhich is out my range for now.
