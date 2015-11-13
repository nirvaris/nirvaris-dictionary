import csv, os, pdb, re, sys


from datetime import datetime

from django.conf import settings
from django.db import transaction
from django.contrib import messages
from django.utils.translation import ugettext as _

from .models import WordEntry, Tag, Language, Tag, Picture

DICTIONARY_CSV_FIELDS = {
    'id': 'ID',
    'relative_url': 'URL',
    'word': 'PALAVRA',
    'languages': 'LINGUAS',
    'short_description': 'DESCRICAO CURTA',
    'words_related':'PALAVRAS RELACIONADAS',
    'word_functions':'FUNCAO GRAMATICAL',
    'audio_file': 'ARQUIVO DE AUDIO',
    'phonetics': 'FONETICA',
    'content_id': 'ID CONTEUDO',
    'content': 'CONTEUDO',
    'pictures': 'IMAGENS',
    'pictures_description': 'IMAGENS DESCRICAO',
    'tags': 'TAGS'
    
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


def export_csv(request):
    ...

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
                        pdb.set_trace()

                        # FOR THE CONTENT
                        word_content = None
                        if row[header['content_id']].isdigit() and WordContent.objects.filter(id=row[header['content_id']]).exists(): 
                            if row[header['short_description']].split()=='' or row[header['content']].split()=='':
                                _write_on_log(csv_log, line, _('[ERROR CODE 1016] CONTENT ID was found but short description or content is blank.'))
                                is_to_commit = False
                                continue

                            word_content = WordContent.objects.get(id=row[header['content_id']])
                            word_content.author = user
                            word_content.short_description = row[header['short_description']]
                            word_content.content = row[header['content']]
                            word_content.save()

                        else:
                            if row[header['content_id']].isdigit():
                                _write_on_log(csv_log, line, _('[ERROR CODE 1015] CONTENT ID not found.'))
                                is_to_commit = False
                                continue
                            if row[header['short_description']].split()!='' and row[header['content']].split()!='':
                                word_content = WordContent()
                                word_content.author = user
                                word_content.short_description = row[header['short_description']]
                                word_content.content = row[header['content']]
                                word_content.save()

                        #check in RELATED TERMS
                        if not word_content:
                            words_related = row[header['words_related']].split(',')
                            for word_related in words_related:
                                try:
                                    word_r = WordEntry.objects.get(relative_url=word_related)
                                    word_content = word_r.word_content
                                except:
                                    continue

                        if not word_content:
                            _write_on_log(csv_log, line, _('[ERROR CODE 1020] No content or related words were found.'))
                            is_to_commit = False
                            continue
                                
                        # FOR THE WORD
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
                        word_entry.audio_file = row[header['audio_file']]
                        word_entry.phonetics = row[header['phonetics']]
                        word_entry.is_published = False
                        word_entry.content = word_content
                        word_entry.save()

                        # FOR TAGS
                        if not _save_many_to_many_field(csv_log, line, word_entry, 'Tag', DICTIONARY_CSV_FIELDS['tags'], row[header['tags']]):
                            is_to_commit = False
                            continue
                        
                        # FOR LANGUAGES 
                        if not _save_many_to_many_field(csv_log, line, word_entry, 'Language', DICTIONARY_CSV_FIELDS['languages'], row[header['languages']]):
                            is_to_commit = False
                            continue

                            continue

                        #pictures

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

def _save_many_to_many_field(csv_log, line, word_entry, fieldClassName,header, field_csv_value, can_be_empty):

    field_csv_value = field_csv_value.strip()
    
    if field_csv_value == '':
        if can_be_empty:
            return True;
        else:
            _write_on_log(csv_log, line, _('[ERROR CODE 1008] ' + header + ' cannot be empty.'))
            return False

    field_values = field_csv_value.split(',')

    word_entry.tags.clear()
    fieldClass = getattr(models, fieldClassName)
    
    field_value_not_exists = False
    
    for field_value in field_values:
        
        field_value = field_value.strip().lower()
        
        if not fieldClass.objects.filter(name__iexact=field_value).exists():
            _write_on_log(csv_log, line, _('[ERROR CODE 1009] ' + header + ' does not exist: ' + field_value))
            field_value_not_exists = True
        else:
            word_entry.word_types.add(fieldClass.objects.get(name__iexact=field_value))
    
    if field_value_not_exists:
        return False

    word_entry.save() 
    return True

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
    
  