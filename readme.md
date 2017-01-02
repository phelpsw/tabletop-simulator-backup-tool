## (Tabletop Simulator)[http://berserk-games.com/tabletop-simulator/] Backup Tool

This tool locally downloads all content for tabletop simulator games.  Helpful
if playing games without internet access or if the original content is taken
offline.

Initially inspired from this (project)[https://github.com/theFroh/ttsunhoster].
Which was badly broken but provided some helpful insights.  Additionally useful
was this Tabletop Simulator save file format (reference)[http://tabletopsimulator.gamepedia.com/Save_File_Format].

Everything we care about occurs in this directory (ubuntu):
```
/home/$USER/My Games/Tabletop Simulator/Mods/
```

Or (windows)
```
C:\Users\$USER\Documents\My Games\Tabletop Simulator\Mods\
```


Games are divided into three key parts.
 1. The json manifest file is the heart of a mod.  Found in the ```Workshop```
directory named with a 9 digit number ie ```123456789.json```
 2. Images found in the ```Images``` subdirectory
 3. Models found in the ```Models``` subdirectory

As a tree:
```
/home/$USER/My Games/Tabletop Simulator/Mods
├── Assetbundles
│   ├── somefile.unity3d
├── Images
│   ├── backedupimage1.png
│   ├── backedupimage2.png
│   ├── backedupimage3.png
├── Models
│   ├── model1.obj
│   ├── model2.obj
│   ├── model3.obj
└── Workshop
    ├── 123456789.json
    ├── 912345678.json
    ├── Thumbnails
    │   ├── 123456789.png
    │   ├── 912345678.png
    └── WorkshopFileInfos.json
```

### Usage

 1. Subscribe to a game using steam workshop
 2. Find the numeric .json file in the Workshop directory that corresponds to
the new game.
 3. Back it up
 ```
python3 backup.py --output "/home/$USER/My Games/Tabletop Simulator/Mods/" ~/My\ Games/Tabletop\ Simulator/Mods/Workshop/123456789.json
 ```

