from collections import namedtuple

TranslateResponseModel = namedtuple('TranslateResponseModel', ['sourceText', 'translatedText', 'detectedSourceLanguage'])
TranslateRequestModel = namedtuple('TranslateRequestModel', ['source', 'target_language'])

PreparedTitleModel = namedtuple('PreparedTitle', ['title_eng', 'title_rus', 'title_kor', 'cover', 'isbn', 'keyword',
                                                  'datetime', 'description'])
