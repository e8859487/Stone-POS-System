import pickle
import pathlib
lastLoad = 0
def saveToPickle(data):
    with open('photoPath.pickle', 'wb') as f:
        pickle.dump(data, f)

ret = None
def loadFromPickle():
    global ret
    if ret is not None:
        return ret
    (__file__).split('/')
    with open(pathlib.Path(__file__).parent.as_posix() + '/photoPath.pickle', 'rb') as f:
        ret = pickle.load(f)
    return ret
