/* global createImageBitmap */

function loadImageWithImageTag(src) {
    return new Promise((resolve, reject) => {
        const img = new Image;
        img.crossOrigin = '';
        img.src = src;
        img.onload = () => { resolve(img); };
        img.onerror = () => { reject(img); };
    });
}

function createWorker(f) {
    return new Worker(URL.createObjectURL(new Blob([`(${f})()`])));
}

const worker = createWorker(() => {
    self.addEventListener('message', e => {
        const src = e.data;
        fetch(src, { mode: 'cors' })
            .then(response => response.blob())
            .then(blob => createImageBitmap(blob))
            .then(bitmap => {
                self.postMessage({ src, bitmap }, [bitmap]);
            });
    });
});

function loadImageWithWorker(src) {
    return new Promise((resolve, reject) => {
        function handler(e) {
            if (e.data.src === src) {
                worker.removeEventListener('message', handler);
                if (e.data.error) {
                    reject(e.data.error);
                }
                resolve(e.data.bitmap);
            }
        }
        worker.addEventListener('message', handler);
        worker.postMessage(src);
    });
}
