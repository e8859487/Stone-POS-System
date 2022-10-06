import pickle

lastLoad = 0
def saveToPickle(data):
    with open('photoPath.pickle', 'wb') as f:
        pickle.dump(data, f)

ret = None
def loadFromPickle():
    global ret
    if ret is not None:
        return ret

    with open('static/photoGallery/photoPath.pickle', 'rb') as f:
        ret = pickle.load(f)
    return ret
