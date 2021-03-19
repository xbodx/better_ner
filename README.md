## Pyenv
```
pyenv install --list
pyenv install 3.9.2
pyenv versions
pyenv local 3.9.2
```

## Venv
python -m venv .nlp_first_spacy_env

.\.nlp_first_spacy_env\Scripts\activate.bat 
-- vs
source ./.nlp_first_spacy_env/bin/activate

python -m pip install --upgrade pip


# Python packages
```
pip install nltk spacy stanza deeppavlov pandas tabulate
python -m spacy download en_core_web_sm
