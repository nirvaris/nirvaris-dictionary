import csv, os, pdb, re, sys

from chardet.universaldetector import UniversalDetector
from datetime import datetime

from django.conf import settings
from django.db import transaction
from django.contrib import messages
from django.utils.translation import ugettext as _

from .models import WordEntry, Tag, MetaTag, PortugueseTerm, Language, Tag, Picture

DICTIONARY_CSV_FIELDS = {
    'id': 'ID',
    'relative_url': 'URL',
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
    'types':'TIPO',
    'word_functions':'FUNCAO GRAMATICAL'    
}

if hasattr(settings, 'DICTIONARY_CSV_FIELDS'):
    if settings.DICTIONARY_CSV_FIELDS:
        DICTIONARY_CSV_FIELDS = settings.DICTIONARY_CSV_FIELDS

TAG_CSV_FIELDS = {
    'name': 'NAME',
    'display': 'DISPLAY'    
}

if hasattr(settings, 'TAG_CSV_FIELDS'):
    if settings.TAG_CSV_FIELDS:
        TAG_CSV_FIELDS = settings.TAG_CSV_FIELDS

LANGUAGE_CSV_FIELDS = {
    'name': 'NAME',
    'location': 'LOCATION'    
}

if hasattr(settings, 'LANGUAGE_CSV_FIELDS'):
    if settings.LANGUAGE_CSV_FIELDS:
        LANGUAGE_CSV_FIELDS = settings.LANGUAGE_CSV_FIELDS

class CSVImportException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)  

def import_language_csv(request, file_path):
    
    is_to_commit = True
    log_file_path = file_path + '.log'
    csv_log = open(log_file_path, 'w')
    language_saved = 0
    
    _write_on_log(csv_log, 0, _('success upload - starting reading'))
    try:

        with open(file_path, encoding='latin-1') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            line = 0
            _write_on_log(csv_log, line, _('looking for header'))

            header = _find_header(csv_reader, LANGUAGE_CSV_FIELDS)
            
            _write_on_log(csv_log, header['line'], _('Header found'))
            with transaction.atomic():
                for row in csv_reader:
                    line += 1
                    if line <= header['line']:
                        continue
                    try:

                        if Language.objects.filter(name__iexact=row[header['name']]).exists():
                            language = Language.objects.get(name__iexact=row[header['name']])
                            language.location = row[header['location']]
                        else:
                            language = Language(name=row[header['name']],location=row[header['location']])
                        language.save()
                        language_saved += 1

                    except:
                        is_to_commit = False
                        _write_on_log(csv_log, line, _('[ERROR CODE 9000] Unexpected error: ') + str(sys.exc_info()[1]))
                        
                if not is_to_commit:
                    raise CSVImportException('[ERROR CODE 9000] Errors have happened. Transaction was canceled.')



    except CSVImportException as csv_excp:
        #pdb.set_trace()
        is_to_commit = False
        _write_on_log(csv_log, line, csv_excp.value)
    except:
        is_to_commit = False
        _write_on_log(csv_log, line, _('[ERROR CODE 9010] Unexpected error: message: ') + str(sys.exc_info()[1]))        
    
    #pdb.set_trace()
    
    if is_to_commit:
        messages.success(request, _('File uploaded with success. Check the log for more details.'))
        _write_on_log(csv_log, line, _('[SUCCESS] The file was saved. Total of tags saved: ' + str(language_saved)))
    else:
        messages.error(request, _('All process were canceled. File uploaded with ERRORS. Check the log for more details.'))

        
    os.remove(file_path)
    csv_log.close()
    return log_file_path

def import_tag_csv(request, file_path):
    
    is_to_commit = True
    log_file_path = file_path + '.log'
    csv_log = open(log_file_path, 'w')
    tag_saved = 0
    
    regex = '[\.\\\\\&\?\(\)\<\>\/\@\!\$\#\£\€\§\±\*\^\%\:\;\`\~\,\\\'\\"\[\]\{\}\+éáíóúâêîôûàèìòùãõñçü].+'
    
    
    _write_on_log(csv_log, 0, _('success upload - starting reading'))
    try:

        with open(file_path, encoding='latin-1') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            line = 0
            _write_on_log(csv_log, line, _('looking for header'))

            header = _find_header(csv_reader, TAG_CSV_FIELDS)
            
            _write_on_log(csv_log, header['line'], _('Header found'))
            with transaction.atomic():
                for row in csv_reader:
                    line += 1
                    if line <= header['line']:
                        continue
                    try:
                        
                        name_lower = row[header['name']].lower()
                        if re.search(re.compile(regex),name_lower):
                            is_to_commit = False
                            _write_on_log(csv_log, line, _('[ERROR CODE 1100] Invalid character for tag name.'))
                            continue
                        #pdb.set_trace()
                        if Tag.objects.filter(name__iexact=name_lower).exists():
                            tag = Tag.objects.get(name__iexact=name_lower)
                            tag.display = row[header['display']]
                        else:
                            tag = Tag(name=name_lower,display=row[header['display']])
                        tag.save()
                        tag_saved += 1

                    except:
                        is_to_commit = False
                        _write_on_log(csv_log, line, _('[ERROR CODE 9000] Unexpected error: ') + str(sys.exc_info()[1]))
                        
                if not is_to_commit:
                    raise CSVImportException('[ERROR CODE 9000] Errors have happened. Transaction was canceled.')



    except CSVImportException as csv_excp:
        #pdb.set_trace()
        is_to_commit = False
        _write_on_log(csv_log, line, csv_excp.value)
    except:
        is_to_commit = False
        _write_on_log(csv_log, line, _('[ERROR CODE 9010] Unexpected error: message: ') + str(sys.exc_info()[1]))        
    
    #pdb.set_trace()
    
    if is_to_commit:
        messages.success(request, _('File uploaded with success. Check the log for more details.'))
        _write_on_log(csv_log, line, _('[SUCCESS] The file was saved. Total of tags saved: ' + str(tag_saved)))
    else:
        messages.error(request, _('All process were canceled. File uploaded with ERRORS. Check the log for more details.'))

        
    os.remove(file_path)
    csv_log.close()
    return log_file_path


def import_csv(request, file_path, user):

    is_to_commit = True
    log_file_path = file_path + '.log'
    csv_log = open(log_file_path, 'w')
    word_saved = 0
    
    _write_on_log(csv_log, 0, _('success upload - starting reading'))
    try:
        
        with open(file_path, encoding='latin-1') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            line = 0
            _write_on_log(csv_log, line, _('looking for header'))

            header = _find_header(csv_reader, DICTIONARY_CSV_FIELDS)
            
            _write_on_log(csv_log, header['line'], _('Header found'))
            with transaction.atomic():
                for row in csv_reader:
                    line += 1
                    if line <= header['line']:
                        continue
                    try:
                        if row[header['id']].isdigit() and WordEntry.objects.filter(id=row[header['id']]).exists(): 
                            word_entry = WordEntry.objects.get(id=row[header['id']])
                            if word_entry.relative_url != row[header['relative_url']]:
                                _write_on_log(csv_log, line, _('[ERROR CODE 1000] ID and relative_url does not match.'))
                                is_to_commit = False
                                continue
                        else:
                            if row[header['id']].isdigit():
                                _write_on_log(csv_log, line, _('[ERROR CODE 1001] ID not found.'))
                                is_to_commit = False
                                continue
                            if WordEntry.objects.filter(relative_url=row[header['relative_url']]).exists():
                                _write_on_log(csv_log, line, _('[ERROR CODE 1003] URL already exists.'))
                                is_to_commit = False
                                continue                            
                            word_entry = WordEntry() 

                        word_entry.author = user
                        word_entry.relative_url = row[header['relative_url']]
                        word_entry.word = row[header['word']]
                        word_entry.short_description = row[header['short_description']]
                        word_entry.scientific_name = row[header['scientific_name']]
                        word_entry.audio_file = row[header['audio_file']]
                        word_entry.phonetics = row[header['phonetics']]
                        word_entry.meaning = row[header['meaning']]
                        word_entry.curiosities = row[header['curiosities']]
                        word_entry.is_published = False
                        
                        word_entry.save()
                        
                        # FOR TAGS
                        if row[header['tags']] == '':
                            _write_on_log(csv_log, line, _('[ERROR CODE 1004] TAGS cannot be empty.'))
                            is_to_commit = False
                            continue

                        tags = row[header['tags']].split(',')
                        tag_not_exists = False
                        word_entry.tags.clear()
                        #pdb.set_trace()
                        for tag in tags:
                            if not Tag.objects.filter(name=tag.strip().lower()).exists():
                                _write_on_log(csv_log, line, _('[ERROR CODE 1005] Tag does not exist: ' + tag.lower()))
                                tag_not_exists = True
                            else:
                                word_entry.tags.add(Tag.objects.get(name=tag.strip().lower()))
                        
                        if tag_not_exists:
                            is_to_commit = False
                            continue

                        word_entry.save()
                        
                        # FOR LANGUAGES 
                        if row[header['languages']] == '':
                            _write_on_log(csv_log, line, _('[ERROR CODE 1006] LANGUAGES cannot be empty.'))
                            is_to_commit = False
                            continue
                            
                        languages = row[header['languages']].split(',')
                        language_not_exists = False
                        word_entry.languages.clear()
                        for language in languages:
                            if not Language.objects.filter(name=language.strip()).exists():
                                _write_on_log(csv_log, line, _('[ERROR CODE 1007] Language does not exist: ' + language))
                                language_not_exists = True
                            else:
                                word_entry.languages.add(Language.objects.get(name=language.strip()))
                        
                        if language_not_exists:
                            is_to_commit = False
                            continue

                        word_entry.save()
                        
                        # FOR PORTUGUESE TERMS
                        
                        #word_entry.portuguese_terms.clear()
                        for pt_delete in word_entry.portuguese_terms.all():
                            pt_delete.delete()
                        
                        
                        if row[header['portuguese_terms']] != '':
                            portuguese_terms = row[header['portuguese_terms']].split(',')
                            nu_order = 0;
                            for portuguese_term in portuguese_terms:
                                port_term  = PortugueseTerm(name=portuguese_term.strip(),display_order=nu_order, word_entry=word_entry)
                                port_term.save()
                                nu_order += 1;
                                #word_entry.portuguese_terms.add(port_term)
                            
                            word_entry.save()
                        
                        # FOR META-TAGS

                        for mt_delete in word_entry.meta_tags.all():
                            mt_delete.delete()
                            
                        meta_tag = MetaTag(word_entry=word_entry, name='description', property='description', content=row[header['short_description']])
                        meta_tag.save()
                        
                        
                        #if row[header['meta_tags']] != '':
                        #    meta_tag = MetaTag(name='keywords', property='keywords', content=row[header['meta_tags']])
                        #    meta_tag.save()
                        #    word_entry.meta_tags.add(meta_tag)
                        
                        #pictures
                        #word_entry.pictures.clear()
                        
                        for pc_delete in word_entry.pictures.all():
                            pc_delete.delete()
                            
                        if row[header['pictures']] != '':
                            pictures = row[header['pictures']].split(',')
                            descriptions = None
                            if row[header['pictures_description']] != '':
                                descriptions = row[header['pictures_description']].split(',')
                            desc_to_use=''
                            
                            nu_order = 0;
                            for picture in pictures:
                                if descriptions:
                                    desc_to_use = descriptions[nu_order]
                                pic = Picture(word_entry=word_entry,file_name=picture.strip(), description=desc_to_use, display_order=nu_order)
                                pic.save()
                                nu_order += 1;

                            word_entry.save()

                        word_saved += 1

                    except:
                        is_to_commit = False
                        _write_on_log(csv_log, line, _('[ERROR CODE 9000] Unexpected error saving word entry: message: ') + str(sys.exc_info()[1]))
                if not is_to_commit:
                    raise CSVImportException('[ERROR CODE 9000] Errors have happened. Transaction was canceled. No data was saved.')

    except CSVImportException as csv_excp:
        #pdb.set_trace()
        is_to_commit = False
        _write_on_log(csv_log, line, csv_excp.value)
    except:
        is_to_commit = False
        _write_on_log(csv_log, line, _('[ERROR CODE 9010] Unexpected error: message: ') + str(sys.exc_info()[1]))        
    
    #pdb.set_trace()
    
    if is_to_commit:
        messages.success(request, _('File uploaded with success. Check the log for more details.'))
        _write_on_log(csv_log, line, _('[SUCCESS] The file was saved. Total of words saved: ' + str(word_saved)))
    else:
        messages.error(request, _('All process were canceled. File uploaded with ERRORS. Check the log for more details.'))

        
    os.remove(file_path)
    csv_log.close()
    return log_file_path

def _find_header(csv_reader, CSV_FIELDS):
    
    header = {}
    try:
        line = 0
        #pdb.set_trace()
        for row in csv_reader:
            header_found = True
            for key, column in CSV_FIELDS.items():
                if not column in row:
                    header_found = False
                    break
                header[key] = row.index(column)
            if header_found:
                break
            
            line += 1
        if not header_found:
            raise CSVImportException(_('[ERROR CODE 1002] Header not found. All process was cancelled.'))
    except:
        raise CSVImportException(_('[ERROR CODE 1002] Header not found. All process was cancelled.'))
        
    header['line'] = line
    return header

def _write_on_log(csv_log, line, msg):
    #pdb.set_trace()
    csv_log.write('[' + datetime.now().strftime("%y-%m-%d %H:%M") + '] [' + _('LINE') + ' ' + str(line) + '] ' + msg + '\n')
    
  