import csv, os, pdb

from datetime import datetime

from django.contrib import messages
from django.utils.translation import ugettext as _

from .models import WordEntry

def import_csv(file_path, user):

    csv_log = open(file_path + '.log', 'w')
    
    _write_on_log(csv_log, _('success upload - starting reading'))
    
    with open(file_path, 'r') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(rdr)
        line = 2
        for row in rdr:
            pdb.set_trace()
            if WordEntry.objects.filter(id=row[0]).exists(): 
                word_entry = WordEntry.objects.get(id=row[0])
            else:
                word_entry = WordEntry()    
            
            word_entry.author = user
            word_entry.relative_url = row[1]
            word_entry.title  = row[2]
            word_entry.word = row[3]
            word_entry.short_description = row[5]
            word_entry.scientific_name = row[6]
            word_entry.audio_file = row[7]
            word_entry.phonetics = row[8]
            word_entry.meaning = row[9]
            word_entry.curiosities = row[10]
    
            word_entry.save()
            #tags
            #languages
            #pictures
            #portuguese_terms
        
            line += 1
    
    os.remove(file_path)
    csv_log.close()

def _write_on_log(csv_log, msg):
    
    csv_log.write(datetime.now().strftime("%y-%m-%d %H:%M") + ': ' + msg)