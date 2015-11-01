import csv, os, pdb

from chardet.universaldetector import UniversalDetector

from datetime import datetime
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext as _

from .models import WordEntry

DICTIONARY_CSV_FIELDS = {
    'id': 'ID',
    'relative_url': 'URL',
    'title': 'TITULO',
    'word': 'PALAVRA',
    'short_description': 'DESCRICAO CURTA',
    'languages': 'LINGUAS',
    'scientific_name': 'NOME CIENTIFICO',
    'audio_file': 'ARQUIVO DE AUDIO',
    'phonetics': 'FONETICA',
    'meaning': 'SIGNIFICADO',
    'curiosities': 'CURIOSIDADES',
    'pictures': 'IMAGENS',
    'pictures_description': 'IMAGENS DESCRICAO',
    'tags': 'TAGS',
    'portuguese_terms':'TERMOS EM PORTUGUES',
    'meta_tags':'META TAGS',
    'types':'TIPO',
    'word_functions':'FUNCAO GRAMATICAL'    
}

if hasattr(settings, 'DICTIONARY_CSV_FIELDS'):
    if settings.DICTIONARY_CSV_FIELDS:
        DICTIONARY_CSV_FIELDS = settings.DICTIONARY_CSV_FIELDS

def import_csv(file_path, user):

    csv_log = open(file_path + '.log', 'w')
    
    _write_on_log(csv_log, 0, _('success upload - starting reading'))

    #encoding = _detect_charset(file_path)
    #pdb.set_trace()
    #_write_on_log(csv_log, 0, _('Encoding found: ' + encoding))    
        
    with open(file_path, encoding='latin-1') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        line = 1
        _write_on_log(csv_log, 0, _('looking for header'))

        header = _find_header(csv_reader)
        
        _write_on_log(csv_log, 0, _('Header found at line') + str(header['line']))
        
        for row in csv_reader:
            if line <= header['line']:
                line += 1
                continue
            
            if WordEntry.objects.filter(id=row[header['id']]).exists(): 
                word_entry = WordEntry.objects.get(id=row[header['id']])
            else:
                word_entry = WordEntry()    
            
            word_entry.author = user
            word_entry.relative_url = row[header['relative_url']]
            word_entry.title  = row[header['title']]
            word_entry.word = row[header['word']]
            word_entry.short_description = row[header['short_description']]
            word_entry.scientific_name = row[header['scientific_name']]
            word_entry.audio_file = row[header['audio_file']]
            word_entry.phonetics = row[header['phonetics']]
            word_entry.meaning = row[header['meaning']]
            word_entry.curiosities = row[header['curiosities']]
    
            word_entry.save()
            
            #tags
            #languages
            #pictures
            #portuguese_terms
        
            line += 1
    
    os.remove(file_path)
    csv_log.close()

def _detect_charset(file_path):
    pdb.set_trace()
    detector = UniversalDetector()
    for line in open(file_path):
        detector.feed(line)
        if detector.done: break
    print(detector.result)
    return detector.result['encoding']

def _find_header(csv_reader):
    
    header = {}

    line = 1
    pdb.set_trace()
    for row in csv_reader:
        header_found = True
        for key, column in DICTIONARY_CSV_FIELDS.items():
            if not column in row:
                header_found = False
                break
            header[key] = row.index(column)
        if header_found:
            break
            
        line += 1
    if not header_found:
        raise CSVImportException(_('CSV Header not found. Check your CSV and try again'))
        
    header['line'] = line
    return header

def _write_on_log(csv_log, line, msg):
    #pdb.set_trace()
    csv_log.write(datetime.now().strftime("%y-%m-%d %H:%M") + ': ' + _('LINE') + str(line) + ': ' + msg)
    
class CSVImportException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)