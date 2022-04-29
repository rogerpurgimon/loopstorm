# Loopstorm

Loopstorm is drum looper based on similarity to mashup the loop. The system loads a set of drum loops and slices sounds automatically. There is a master loop you can select. Similarity levels are utilized to replace slices in the master loop with the most similar slices in the other loops.

The application will start from an input user that decides the main loop, imported from the collaborative database of Creative Commons Licensed sounds, [Freesound][1]. This loop will be divided into slices, representing a kick or a snare, for example, and the system will load several drum loops. The software does preprocessing, including the automatic slicing and the extraction of features that are computed with [Essentia][2], the open source library for audio analysis and audio-based music information retrieval. With all the information it displays the similarity results.

[1]:https://freesound.org/ "Freesound"
[2]:https://github.com/MTG/essentia
