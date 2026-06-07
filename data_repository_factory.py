import GlobalSettings

_repo = None


def get_repository():
    global _repo
    if _repo is not None:
        return _repo

    backend = GlobalSettings.DATA_BACKEND
    if backend == 'firestore':
        from firestore_repository import FirestoreRepository
        _repo = FirestoreRepository()
    else:
        from google_sheets_repository import GoogleSheetsRepository
        _repo = GoogleSheetsRepository()
    return _repo
