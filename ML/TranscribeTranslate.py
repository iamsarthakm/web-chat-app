from google.oauth2 import service_account
credentials = service_account.Credentials.from_service_account_file('MajorProject-4da08da4abe8.json')


#This transliterate_text(text, target='hi') function can fail anytime as this is not supported by Google's official API.
#The official API for transliteration was deprecated long back
def transliterate_text(text, target='hi'):
    from google.transliteration import transliterate_text
    result = transliterate_text(text, lang_code=target)
    return (result)

def translate_text(text, target='en'):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client(credentials=credentials)

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)
    from bs4 import BeautifulSoup
    htmlfreetext = BeautifulSoup(result["translatedText"], features="html.parser")
    translated_text= htmlfreetext.get_text()
    return (translated_text)


def detect_language(text):

    """Detects the text's language."""
    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client(credentials=credentials)

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    result = translate_client.detect_language(text)

    return result["language"]


def transcribe_audio(file_input):
    from google.cloud import speech_v1p1beta1 as speech
    client = speech.SpeechClient(credentials=credentials)

    speech_file = file_input
    first_lang = "en-us"
    second_lang = "hi-in"
    #third_lang = "ta-in"

    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=48000,
        audio_channel_count=2,
        language_code=first_lang,
        alternative_language_codes=[second_lang],   #add third_lang in the list of alternative_language_codes
                                                    #if needed but it might affect the accuracy
    )

    response = client.recognize(config=config, audio=audio)

    lis=[]
    for i, result in enumerate(response.results):
        alternative = result.alternatives[i]
        lis.append(alternative.transcript)
        lis.append(result.language_code)

    return (lis[0], lis[1])

