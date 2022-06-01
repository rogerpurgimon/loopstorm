import essentia
from essentia.standard import *
import IPython.display
import matplotlib.pyplot as plt

from AudioExtractor import AudioExtractor
from AudioManager import AudioManager

if __name__ == '__main__':
    #load loops
    loop = MonoLoader(filename='../loops/audio1.wav')()
    loop1 = MonoLoader(filename='../loops/audio2.wav')()
    loop2 = MonoLoader(filename='../loops/audio3.wav')()
    #instance AudioManager
    manager = AudioManager()

    #save data of the slices and save mfccs for each loop
    manager.add_slice(loop, 0)
    manager.add_mfccs(loop, 0)


    manager.add_slice(loop1, 1)
    manager.add_mfccs(loop1, 1)

    manager.add_slice(loop2, 2)
    manager.add_mfccs(loop2, 2)

    #compute euclidean distance and save the index and specific loop of the most similar slice among all the slices
    manager.similarity()

    print(manager.d['main_loop']['slices'][1]['info']) #slice audio information of the first slice in main loop (not time stamps)
                                                        #(conté el data perquè tu li passis això i et faci un display de la slice)

    print('\n', manager.d['main_loop']['slices'][1]['mfccs'])
    print('\n', manager.d['main_loop']['slices'][1]['similarity'])






