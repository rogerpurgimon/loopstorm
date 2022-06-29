# Loopstorm
This project is made to help musicians and non-musicians to create their own songs with loops in such a simple way. The creative control of producers is restricted by their abilities as a sound editor, not to mention the time they are able to invest performing that editing, the copyright issues and so on. That’s why this tool could be used to avoid all these restrictions and could help to perform a good beat for a song.

## Description
Loopstorm is drum looper based on similarity to mashup the loop. The system loads a set of drum loops and slices sounds automatically. There is a master loop you can select. Similarity levels are utilized to replace slices in the master loop with the most similar slices in the other loops.


The application will start from an input user that decides the main loop, imported from the collaborative database of Creative Commons Licensed sounds, [Freesound][1]. This loop will be divided into slices, representing a kick or a snare, for example, and the system will load several drum loops. The software does preprocessing, including the automatic slicing and the extraction of features that are computed with [Essentia][2], the open source library for audio analysis and audio-based music information retrieval, With all the information it displays the similarity results.

The application will start from an input user that decides the main loop, imported from the collaborative database of Creative Commons Licensed sounds, [Freesound][1]. This loop will be divided into slices, representing a kick or a snare, for example, and the system will load several drum loops. The software does preprocessing, including the automatic slicing and the extraction of features that are computed with [Essentia][2], the open source library for audio analysis and audio-based music information retrieval. With all the information it displays the similarity results.


## Getting Started
### Dependencies
The programming language used in this project is Python. We recommend Linux as the operating system. In case of using MacOS the installation is a bit cumbersome. Same happens with Windows, an Ubuntu environment is needed (WSL) and a display server is also needed in order to run the GUI application in the Windows device. We do not require a high processor speed, or a lot of system memory and storage space. What we need is audio hardware to be able to listen to the  drum loops, could be headphones or speakers. We recommend good quality headphones in order to appreciate the difference between the original loop and the new one. 

The code also requires some essential requirements such as imports, for instance, there is AudioExtractor.py, a script from which we obtain the MFCCs from the slices given by the onset detector. In this case, we mainly need NumPy and Essentia, which is the tool we are going to use the most in terms of developing the automatic slicing with the onset detection method and in order to compute the Mel-Frequency Cepstrum coefficients.

Nonetheless, other scripts need different imports from libraries like SciPy, IPython in order to play the audios, Scikit-learn or Matplotlib that will be useful in the development process to test all the implementations. And PyQt5 in order to visualize the interface. All the specific versions of each library are specified in the requirements.txt file.

In order to make the installation of these libraries and packages easier, all of them are in a requirements.txt with the minimum version necessary.


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
Distributed under the MIT License. See ``` LICENSE ``` for more information.

## Aknowledgments
Fisrt of all, we would like to thank Xavier Lizarraga Seijas for having monitored the project.
Here, there's a list of reference we would like to give credit:

* Crute, A. (2020, September 14). [Getting creative with LoopMash in Cubase. MusicTech.][8]
* [ADSR, Transfuser 2 by Air Music Tech - Melodic & Rhythmic Groove-Creation Instrument for Mac/Windows - ADSR Sounds ][9]
* Sigurdsson, S., Petersen, K. B., & Lehn-Schiøler, T. (2006, October). [Mel Frequency Cepstral Coefficients: An Evaluation of Robustness of MP3 Encoded Music. In ISMIR (pp. 286-289).][10]
* Heittola, T., & Klapuri, A. (2002, October). [Locating Segments with Drums in Music Signals. In ISMIR.][11]
* Tutzer, F. (2011). [Drum rhythm retrieval based on rhythm and sound similarity. Master's thesis, Departament of Information and Communication Technologies Universitat Pompeu Fabra, Barcelona.][12]

[1]:https://freesound.org/ "Freesound"
[2]:https://github.com/MTG/essentia

[3]:https://github.com/rogerpurgimon/loopstorm/blob/main/requirements.txt

[4]:https://github.com/Uriiol1808
[5]:https://github.com/u172926
[6]:https://github.com/leonardbalm
[7]:https://github.com/rogerpurgimon
[8]:https://musictech.com/tutorials/cubase/getting-creative-with-loopmash-in-cubase/
[9]:https://www.adsrsounds.com/product/software/air-music-tech-transfuser-2-groove-creation-instrument/
[10]:https://www.academia.edu/29410364/Mel_frequency_cepstral_coefficients_An_evaluation_of_robustness_of_mp3_encoded_music
[11]:https://www.researchgate.net/publication/2537192_Locating_Segments_with_Drums_in_Music_Signals
[12]:https://vdocument.in/drum-rhythm-retrieval-based-on-rhythm-and-sound-mtgupfedututzer-felix-master-thesis-2011pdf.html?page=1
