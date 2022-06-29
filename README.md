# Loopstorm
This project is made to help musicians and non-musicians to create their own songs with loops in such a simple way. The creative control of producers is restricted by their abilities as a sound editor, not to mention the time they are able to invest performing that editing, the copyright issues and so on. That’s why this tool could be used to avoid all these restrictions and could help to perform a good beat for a song.

## Description
Loopstorm is drum looper based on similarity to mashup the loop. The system loads a set of drum loops and slices sounds automatically. There is a master loop you can select. Similarity levels are utilized to replace slices in the master loop with the most similar slices in the other loops.


The application will start from an input user that decides the main loop, imported from the collaborative database of Creative Commons Licensed sounds, [Freesound][1]. This loop will be divided into slices, representing a kick or a snare, for example, and the system will load several drum loops. The software does preprocessing, including the automatic slicing and the extraction of features that are computed with [Essentia][2], the open source library for audio analysis and audio-based music information retrieval, With all the information it displays the similarity results.

The application will start from an input user that decides the main loop, imported from the collaborative database of Creative Commons Licensed sounds, [Freesound][1]. This loop will be divided into slices, representing a kick or a snare, for example, and the system will load several drum loops. The software does preprocessing, including the automatic slicing and the extraction of features that are computed with [Essentia][2], the open source library for audio analysis and audio-based music information retrieval. With all the information it displays the similarity results.


## Getting Started
### Dependencies

### Installing
1. Clone the repository
  ```sh
  git clone https://github.com/rogerpurgimon/loopstorm.git
  ```

2. Install essentia. Read the installation instructions for your current OS:
    * https://essentia.upf.edu/installing.html
3. Install the [requirements][3]:
<br/>In linux:

```sh
pip install -r requirements.txt
```


### Executing program
Click in the image to watch the video:
[![Watch the video](https://user-images.githubusercontent.com/47043537/176453552-ea58d8a1-7e4d-4652-9820-c57c2fd4108d.PNG)](https://drive.google.com/file/d/1HDuZrbd0VSElPXVJa_I8fys9b9Il735X/view?usp=sharing)

## Help

## Authors
  * [Oriol Marín Esclasans][4]
  * [Edgar Espinós Murria][5]
  * [Leonardo Enzo Barros Souza Cidreira][6]
  * [Roger Purgimon Serra][7]

## License
Distributed under the Appache License. See ``` LICENSE ``` for more information.

## Aknowledgments


[1]:https://freesound.org/ "Freesound"
[2]:https://github.com/MTG/essentia

[3]:https://github.com/rogerpurgimon/loopstorm/blob/main/requirements.txt

[4]:https://github.com/Uriiol1808
[5]:https://github.com/u172926
[6]:https://github.com/leonardbalm
[7]:https://github.com/rogerpurgimon
