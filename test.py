import logging
from datetime import datetime
import nltk
import pandas
import spacy
import stanza
from deeppavlov import configs, build_model, Chainer

from duration import duration

LOGGER_FORMAT = u'%(asctime)s %(levelname)-8s: %(message)s # %(filename)s%(name)s[%(lineno)d]¬'

__formatter = logging.Formatter(fmt=LOGGER_FORMAT)
__logging_level = logging.ERROR


def logging_setup_all():
    # 'stanza', 'tensorflow', 'nltk' and other
    for name in logging.Logger.manager.loggerDict:
        logging_setup(name)


def logging_setup(name):
    logger = logging.getLogger(name)
    logger.setLevel(__logging_level)
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            handler.setFormatter(__formatter)

logging_setup_all()

DEFAULT_LANGUAGE_NLTK: str = 'russian'

sentence = "Где приземлился Гагарин? " \
           "Главные герои в Теории Большого Взрыва. " \
           "Путину как боженьке можно! " \
           "Есть ли жизнь на Марсе? " \
           "Почему канализационные люки круглые? " \
           "Когда чемпионат мира? " \
           "Кто жёлтый МТС, Билайн, Мегафон? " \
           "Важную роль сыграл Сталин во Второй Мировой войне? " \
           "Где утонул Титаник? " \
           "Что ты думаешь о Бари Алибасове?"

sentence = sentence.replace('.', '. ').replace('!', '! ').replace('?', '? ')
sentences = nltk.sent_tokenize(sentence, language=DEFAULT_LANGUAGE_NLTK)


'''
nlp = spacy.load("ru_core_news_lg")
doc = nlp(text)

print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

for entity in doc.ents:
    print(entity.text, entity.label_)
'''

DEFAULT_LANGUAGE_STANZA: str = 'ru'
stanza.download(DEFAULT_LANGUAGE_STANZA)

result = []
stanza_normal = []
stanza_normal_du = []
stanza_pipeline = stanza.Pipeline(lang='ru', processors='tokenize,ner')
deeppavlov_model: Chainer = build_model(configs.ner.ner_rus_bert, True)

for sentence in sentences:

    start = datetime.now()
    doc = stanza_pipeline(sentence)
    stanza_ner = ', '.join([f'{ent.text} - {ent.type}' for ent in doc.ents])
    stanza_du = duration(datetime.now() - start)

    start = datetime.now()
    doc = stanza_pipeline(sentence.lower())
    stanza_lower_ner = ', '.join([f'{ent.text} - {ent.type}' for ent in doc.ents])
    stanza_lower_du = duration(datetime.now() - start)

    start = datetime.now()
    doc = deeppavlov_model([sentence])
    pause ...
    # todo:
    # Доброй ночи, сладких снов,
    # Шлю тебе свою любовь,
    # Сновидений пожелаю,
    # Свою нежность посылаю!
    #
    # Пусть тебе приснится сон,
    # И хорошим будет он,
    # Будешь ночью отдыхать,
    # Волшебство во сне встречать!
    deeppavlov_ner = ', '.join([f'{ent.text} - {ent.type}' for ent in doc.ents - bla bla bla])
    deeppavlov_du = duration(datetime.now() - start)

    result.append([sentence,
                   stanza_ner, stanza_du,
                   stanza_lower_ner, stanza_lower_du,
                   deeppavlov_ner, deeppavlov_du])


pandas.set_option('display.max_rows', 500)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 5000)
df = pandas.DataFrame(result, columns=['sentence',
                                       'stanza Normal', 'du',
                                       'stanza lower', 'du',
                                       'deeppavlov Normal', 'du'])
print(df.to_markdown(headers='keys'))
