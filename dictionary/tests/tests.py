import pdb
import re

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from ..models import WordEntry, Tag, MetaTag, Comment


class PostViewTestCase(TestCase):

    def setUp(self):
        self.c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        self.author = self._create_author()
        self.tag_tree = self._create_tag_tree()
        self.tag_cityname = self._create_tag_cityname()
        self.word_itauba = self._create_word_itauba()
        self.excited_comment_user = self._create_comment_user()

    def tearDown(self):
        ...                  

    def test_get_post_meta_tag(self):
    
        c = self.c

        response = c.get('/dictionary/itauba')
        
        content = str(response.content)        
        #pdb.set_trace()
        self.assertTrue(re.search(re.compile('<meta.+?name="keywords"'), content),
        'Meta tag name not found')

        self.assertTrue(re.search(re.compile('<meta.+?name="description"'), content),
        'Meta tag description not found')

        self.assertTrue(re.search(re.compile('<meta.+?property="twitter:card"'), content),
        'Meta tag twitter:card not found')

    def _create_word_itauba(self):
        
        word = WordEntry(author=self.author, relative_url='itauba',title='itauba uma árvore',short_description='Itaúba é uma árvore e também uma cidade do Mato Grosso')
        word.save()
        
        meta_tag = MetaTag(word_entry=word, name='keywords',content='some key words')
        meta_tag.save()
        
        meta_tag = MetaTag(word_entry=word, name='description',content='some description')
        meta_tag.save()        
        
        meta_tag = MetaTag(word_entry=word, property='twitter:card',content='sumary')
        meta_tag.save()
        
        return word


    def _create_tag_tree(slef):
        tag = Tag(name='tree')
        tag.save()
        return tag
    
    def _create_tag_cityname(slef):
        tag = Tag(name='cityname')
        tag.save()
        return tag
 
    def _create_comment_user(self):
     
        user = User(first_name='Exited', last_name='Comment User',email='excited@comment.user.com',username='excited')
        user.save()
        return user
        
    def _create_author(self):
        
        user = User(first_name='Jack', last_name='Daniels',email='jack@daniels.com',username='jack')
        user.save()
        return user
