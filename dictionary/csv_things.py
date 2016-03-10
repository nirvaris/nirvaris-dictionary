import csv, os, pdb, re, sys


from datetime import datetime

from django.conf import settings
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import mail_admins
from django.utils.translation import ugettext as _

from .models import WordEntry, Tag, Language, Tag, Picture, WordContent, WordClass, WordComment

DICTIONARY_CSV_FIELDS = {
    'id': 'ID',
    'relative_url': 'URL',
    'word': 'PALAVRA',
    'languages': 'LINGUAS',
    'short_description': 'DESCRICAO CURTA',
    'words_related':'PALAVRAS RELACIONADAS',
    'word_classes':'FUNCAO GRAMATICAL',
    'audio_file': 'ARQUIVO DE AUDIO',
    'phonetics': 'FONETICA',
    'content_id': 'CONTEUDO ID',
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

def import_comments_csv(request, file_path):

    log_file_path = file_path + '.log'
    csv_log = open(log_file_path, 'w')

    with open(file_path, encoding='latin-1') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        with transaction.atomic():
            line = 0
            for row in csv_reader:
                line += 1
                try
                    if not WordEntry.objects.filter(word=row[0]).exists():
                        continue

                    word_entry = WordEntry.objects.filter(word=row[0])[0]

                    if User.objects.filter(email=row[3]).exists():
                        user = User.objects.filter(email=row[3])[0]
                    else:
                        email=row[3]
                        if User.objects.filter(email=email).exists():
                            user = User.objects.get(email=email)
                        else:
                            user = User(username=email[0:29], email=email)
                            name = row[2]
                            first_name = name.split(' ')[0].strip()
                            last_name = name.replace(first_name, '').strip()

                            user.first_name = first_name[0:29]
                            user.last_name = last_name[0:29]

                            user.save()
                    comment = WordComment(author=user, word_entry=word_entry, author_ip=row[4],content=row[6], is_approved=True)
                    comment.save()
                except:
                    _write_on_log(csv_log, line, row)

    csv_log.close()

#0post_title,
#1comment_ID,
#2comment_author
#3,comment_author_email
#4,comment_author_IP
#5,comment_date_gmt
#6,comment_content
#7,comment_parent

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

            header = _find_header(csv_log, csv_reader, LANGUAGE_CSV_FIELDS)
            if not header:
                raise CSVImportException(_('[ERROR CODE 1002] Header not found. All process was cancelled.'))

            _write_on_log(csv_log, header['line'], _('Header found'))
            with transaction.atomic():
                for row in csv_reader:
                    line += 1
                    if line <= header['line']:
                        continue
                    try:

                        row_empty = True
                        for r in row:
                            if r != '':
                                row_empty = False
                        if row_empty:
                            _write_on_log(csv_log, line, _('[ROW EMPTY]'))
                            continue

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

            header = _find_header(csv_log, csv_reader, TAG_CSV_FIELDS)
            if not header:
                raise CSVImportException(_('[ERROR CODE 1002] Header not found. All process was cancelled.'))

            _write_on_log(csv_log, header['line'], _('Header found'))
            with transaction.atomic():
                for row in csv_reader:
                    line += 1
                    if line <= header['line']:
                        continue
                    try:
                        row_empty = True
                        for r in row:
                            if r != '':
                                row_empty = False
                        if row_empty:
                            _write_on_log(csv_log, line, _('[ROW EMPTY]'))
                            continue

                        name_lower = row[header['name']].lower().strip()
                        if re.search(re.compile(regex),name_lower):
                            is_to_commit = False
                            _write_on_log(csv_log, line, _('[ERROR CODE 1100] Invalid character for tag name.'))
                            continue
                        #pdb.set_trace()
                        if Tag.objects.filter(name__iexact=name_lower).exists():
                            tag = Tag.objects.get(name__iexact=name_lower)
                            tag.display = row[header['display']].strip()
                        else:
                            tag = Tag(name=name_lower,display=row[header['display']].strip())
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


    print('start import csv')
    is_to_commit = True
    log_file_path = file_path + '.log'
    csv_log = open(log_file_path, 'w')
    word_saved = 0
    w_r = {}
    _write_on_log(csv_log, 0, _('success upload - starting reading'))
    try:

        with open(file_path, encoding='latin-1') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            line = 0
            _write_on_log(csv_log, line, _('looking for header'))

            header = _find_header(csv_log, csv_reader, DICTIONARY_CSV_FIELDS)
            if not header:
                raise CSVImportException(_('[ERROR CODE 1002] Header not found. All process was cancelled.'))

            _write_on_log(csv_log, header['line'], _('Header found'))
            with transaction.atomic():
                for row in csv_reader:
                    line += 1
                    if line <= header['line']:
                        continue
                    try:
                        row_empty = True
                        for r in row:
                            if r != '':
                                row_empty = False
                        if row_empty:
                            _write_on_log(csv_log, line, _('[ROW EMPTY]'))
                            continue


                        # FOR THE CONTENT
                        word_content = None
                        if row[header['content_id']].isdigit() and WordContent.objects.filter(id=row[header['content_id']]).exists():
                            if row[header['content']].split()=='':
                                _write_on_log(csv_log, line, _('[ERROR CODE 1016] CONTENT ID was found but content is blank.'))
                                is_to_commit = False
                                continue

                            word_content = WordContent.objects.get(id=row[header['content_id']])
                            word_content.author = user
                            word_content.content = row[header['content']]
                            word_content.save()

                        else:
                            if row[header['content_id']].isdigit():
                                _write_on_log(csv_log, line, _('[ERROR CODE 1015] CONTENT ID not found.'))
                                is_to_commit = False
                                continue
                            if row[header['content']].split()!='':
                                word_content = WordContent()
                                word_content.author = user
                                word_content.content = row[header['content']]
                                word_content.save()


                        # FOR THE WORD
                        if row[header['id']].isdigit() and WordEntry.objects.filter(id=row[header['id']]).exists():
                            word_entry = WordEntry.objects.get(id=row[header['id']])
                            if word_entry.relative_url != row[header['relative_url']].strip():
                                _write_on_log(csv_log, line, _('[ERROR CODE 1000] ID and relative_url does not match.'))
                                is_to_commit = False
                                continue
                        else:
                            if row[header['id']].isdigit():
                                _write_on_log(csv_log, line, _('[ERROR CODE 1001] ID not found.'))
                                is_to_commit = False
                                continue
                            if WordEntry.objects.filter(relative_url=row[header['relative_url']].strip()).exists():
                                _write_on_log(csv_log, line, _('[ERROR CODE 1003] URL already exists: ' + row[header['relative_url']]))
                                is_to_commit = False
                                continue
                            word_entry = WordEntry()

                        word_entry.author = user
                        word_entry.relative_url = row[header['relative_url']].strip()
                        word_entry.word = row[header['word']].strip()

                        if row[header['audio_file']] != '':
                            word_entry.audio_file = row[header['audio_file']].strip()

                        if row[header['phonetics']] != '':
                            word_entry.phonetics = row[header['phonetics']].strip()

                        word_entry.short_description = row[header['short_description']].strip()
                        word_entry.is_published = False
                        word_entry.word_content = word_content
                        word_entry.save()

                        # FOR TAGS
                        if not _save_many_to_many_field(csv_log, line, word_entry.tags, Tag, DICTIONARY_CSV_FIELDS['tags'], row[header['tags']], False):
                            is_to_commit = False
                            continue
                        else:
                            word_entry.save()

                        # FOR LANGUAGES
                        if not _save_many_to_many_field(csv_log, line, word_entry.languages, Language, DICTIONARY_CSV_FIELDS['languages'], row[header['languages']], False):
                            is_to_commit = False
                            continue
                        else:
                            word_entry.save()

                        # FOR WORD CLASSES
                        if not _save_many_to_many_field(csv_log, line, word_entry.word_classes, WordClass, DICTIONARY_CSV_FIELDS['word_classes'], row[header['word_classes']], True):
                            is_to_commit = False
                            continue
                        else:
                            word_entry.save()

                        #pictures
                        for pc_delete in word_content.pictures.all():
                            pc_delete.delete()

                        if row[header['pictures']] != '':
                            pictures = row[header['pictures']].replace('\'','').split(',')
                            descriptions = None
                            if row[header['pictures_description']] != '':
                                descriptions = row[header['pictures_description']].split(',')
                            desc_to_use=''

                            nu_order = 0;
                            for picture in pictures:
                                if descriptions:
                                    try:
                                        desc_to_use = descriptions[nu_order]
                                    except:
                                        pass
                                pic = Picture(word_content=word_content,file_name=picture.strip(), description=desc_to_use.strip(), display_order=nu_order)
                                pic.save()
                                nu_order += 1;

                            word_entry.save()

                        else:
                            word_entry.save()

                        if row[header['words_related']]!='':
                            w_r[row[header['relative_url']]] = []
                            words_related = row[header['words_related']].split(',')
                            for word_related in words_related:
                                w_r[row[header['relative_url']]].append(word_related.strip())

                        word_saved += 1

                    except:
                        print(str(sys.exc_info()[1]))
                        is_to_commit = False
                        _write_on_log(csv_log, line, _('[ERROR CODE 9000] Unexpected error saving word entry: message: ') + str(sys.exc_info()[1]))

                _words_related(csv_log, w_r)

                if not is_to_commit:
                    raise CSVImportException('[ERROR CODE 9000] Errors have happened. Transaction was canceled. No data was saved.')

    except CSVImportException as csv_excp:
        #pdb.set_trace()
        print(str(sys.exc_info()[1]))
        is_to_commit = False
        _write_on_log(csv_log, line, csv_excp.value)
    except:
        is_to_commit = False
        print(str(sys.exc_info()[1]))
        _write_on_log(csv_log, line, _('[ERROR CODE 9010] Unexpected error: message: ') + str(sys.exc_info()[1]))

    #pdb.set_trace()

    if is_to_commit:
        messages.success(request, _('File uploaded with success. Check the log for more details.'))
        _write_on_log(csv_log, line, _('[SUCCESS] The file was saved. Total of words saved: ' + str(word_saved)))
    else:
        messages.error(request, _('All process were canceled. File uploaded with ERRORS. Check the log for more details.'))

    print('finished import csv')
    os.remove(file_path)
    csv_log.close()
    send_email('File Finished',log_file_path)
    return log_file_path

def _words_related(csv_log, w_r):

    _write_on_log(csv_log, 0, _('Add related words'))
    not_found = ''
    for key, related in w_r.items():
        word_entry = WordEntry.objects.get(relative_url=key)
        for r in related:
            if not WordEntry.objects.filter(relative_url=r).exists():
                not_found += ' ' + r
            else:
                word_entry.words_related.add(WordEntry.objects.get(relative_url=r))
        word_entry.save()
    if not_found.strip()!='':
        _write_on_log(csv_log, 0, _('[ERROR CODE 2009] these related word where not found, so were not added: ' + not_found))


def _save_words_related(csv_log, line, word_entry,  field_csv_value):


    field_csv_value = field_csv_value.strip()

    if field_csv_value == '':
        return True

    field_values = field_csv_value.split(',')

    word_entry.words_related.clear()
    field_value_not_exists = False

    for field_value in field_values:

        field_value = field_value.strip().lower()

        if not WordEntry.objects.filter(relative_url__iexact=field_value).exists():
            _write_on_log(csv_log, line, _('[ERROR CODE 1009] relative_url does not exist: ' + field_value))
            field_value_not_exists = True
        else:
            word_entry.words_related.add(WordEntry.objects.get(relative_url__iexact=field_value))

    if field_value_not_exists:
        return False

    return True

def _save_many_to_many_field(csv_log, line, word_entry_list, fieldClass,header, field_csv_value, can_be_empty):


    field_csv_value = field_csv_value.strip()

    if field_csv_value == '':
        if can_be_empty:
            return True;
        else:
            _write_on_log(csv_log, line, _('[ERROR CODE 1008] ' + header + ' cannot be empty.'))
            return False

    field_values = field_csv_value.split(',')

    word_entry_list.clear()
    field_value_not_exists = False

    for field_value in field_values:

        field_value = field_value.strip().lower()

        if not fieldClass.objects.filter(name__iexact=field_value).exists():
            _write_on_log(csv_log, line, _('[ERROR CODE 1009] ' + header + ' does not exist: ' + field_value))
            field_value_not_exists = True
        else:
            word_entry_list.add(fieldClass.objects.get(name__iexact=field_value))

    if field_value_not_exists:
        return False

    return True

def _find_header(csv_log, csv_reader, CSV_FIELDS):

    header = {}
    try:
        line = 0
        #pdb.set_trace()
        for row in csv_reader:

            header_log = ''
            found_some_header = False
            header_found = True
            for key, column in CSV_FIELDS.items():
                if not column in row:
                    header_found = False
                    header_log += ' ' + column
                else:
                    found_some_header = True
                    header[key] = row.index(column)

            if found_some_header:
                break
            line += 1

        if not header_found:
            _write_on_log(csv_log, line, _('[ERROR CODE 1002] Header not found: ' + header_log.strip()))
    except:
        header_found = False
        _write_on_log(csv_log, line,_('[ERROR CODE 1002] Header not found. All process was cancelled.'))

    if not header_found:
        return None
    else:
        header['line'] = line
        return header

def _write_on_log(csv_log, line, msg):
    #pdb.set_trace()
    csv_log.write('[' + datetime.now().strftime("%y-%m-%d %H:%M") + '] [' + _('LINE') + ' ' + str(line+1) + '] ' + msg + '\n')

def send_email(html_message, log_file_path):
    today_is = datetime.now().isoformat()
    with open(log_file_path,'r') as log_f:
        for l in log_f:
            html_message += l

    mail_admins('[DTG] Import Finished - ' + str(today_is), '', html_message=html_message)
