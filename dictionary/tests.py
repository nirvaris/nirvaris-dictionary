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
        self.tag_cook = self._create_tag_cook()
        self.tag_vegan = self._create_tag_vegan()
        self.word_itauba = self._create_word_itauba()
        self.excited_comment_user = self._create_comment_user()

    def tearDown(self):
        ...                  

    def test_word_new_comment_existing_author(self):
        
        total_comments = Comment.objects.all().count()
        total_users = User.objects.all().count()
        c = self.c
        
        word_content = 'If you know him as long as I know, you know his name is John'
        
        response = c.word('/blog/nice_word_cook', {
            'name':'John Daniels',
            'email': 'excited@comment.user.com',
            'word_id': self.word_cook.id,
            'content': word_content,
            'anti_spam_token':'1234',
            'anti_spam_hidden':'1234',
            'anti_spam_no_hidden':'',
        })        
    
        self.assertEquals(total_comments+1,Comment.objects.all().count())
        
        self.assertEquals(total_users,User.objects.all().count())
  
    def test_word_new_comment_new_author(self):
        
        total_comments = Comment.objects.all().count()
        total_users = User.objects.all().count()
        c = self.c
        
        word_content = 'If you know him as long as I do, you would know his name is John'
        
        response = c.word('/blog/nice_word_cook', {
            'name':'John Daniels',
            'email': 'john@daniels.com',
            'word_id': self.word_cook.id,
            'content': word_content,
            'anti_spam_token':'1234',
            'anti_spam_hidden':'1234',
            'anti_spam_no_hidden':'',            
        })        
    
        self.assertEquals(total_comments+1,Comment.objects.all().count())
        
        self.assertEquals(total_users+1,User.objects.all().count())
        
        new_user = User.objects.latest('id')
        new_comment = Comment.objects.latest('id')

        self.assertEqual(new_user,new_comment.author)

    def test_word_new_comment_with_name_no_email(self):

        c = self.c
        
        total_comments = Comment.objects.all().count()
        
        word_content = 'This is a comment from Jack Daniels already in the DB'
        
        response = c.word('/blog/nice_word_cook', {
            'name': 'No Email',
            'word_id': self.word_cook.id,
            'content': word_content,
            'anti_spam_token':'1234',
            'anti_spam_hidden':'1234',
            'anti_spam_no_hidden':'',            
        })        
    
        self.assertEquals(total_comments,Comment.objects.all().count())
           
    def test_word_new_comment_with_email_no_name(self):

        c = self.c
        
        total_comments = Comment.objects.all().count()
        
        word_content = 'This is a comment from Jack Daniels already in the DB'
        
        response = c.word('/blog/nice_word_cook', {
            'email': 'excited@comment.user.com',
            'word_id': self.word_cook.id,
            'content': word_content,
            'anti_spam_token':'1234',
            'anti_spam_hidden':'1234',
            'anti_spam_no_hidden':'',            
        })        
    
        self.assertEquals(total_comments,Comment.objects.all().count())
        
    def test_word_new_comment_no_author(self):
        
        total_comments = Comment.objects.all().count()
        
        c = self.c
        
        word_content = 'This is a comment worded via comment form'
        
        response = c.word('/blog/nice_word_cook', {
            'word_id':self.word_cook.id,
            'content': word_content,
            'anti_spam_token':'1234',
            'anti_spam_hidden':'1234',
            'anti_spam_no_hidden':'',            
        })        
    
        self.assertEquals(total_comments+1,Comment.objects.all().count())
        
        response = c.get('/blog/nice_word_cook')       
        
        self.assertNotIn(word_content, str(response.content))

    def test_get_comment_not_approved(self):
        
        comment = Comment(author=self.excited_comment_user,is_approved=False, word=self.word_cook, content='A comment from an Excited user')
        comment.save()
        
        c = self.c

        response = c.get('/blog/nice_word_cook')       
        
        self.assertNotIn(comment.content, str(response.content))

        
    def test_get_comment_with_author(self):
        
        comment = Comment(author=self.excited_comment_user,is_approved=True, word=self.word_cook, content='A comment from an Excited user')
        comment.save()
        
        c = self.c

        response = c.get('/blog/nice_word_cook')       
        
        self.assertIn(comment.content, str(response.content))
        self.assertIn(self.excited_comment_user.get_full_name(), str(response.content))         
            
    def test_get_comment_no_author(self):
        
        comment = Comment(word=self.word_cook,is_approved=True, content='some very nice comment comment')
        comment.save()
        
        c = self.c

        response = c.get('/blog/nice_word_cook')       
        
        self.assertIn(comment.content, str(response.content)) 
    
    def test_get_word_view(self):

        c = self.c

        response = c.get('/blog/nice_word_cook')
        
        self.assertEquals(response.status_code,200,'blog word')
        
        self.assertTrue(isinstance(response.context['word'], Post))
        
        self.assertTrue(any(self.word_cook.template in t.name for t in response.templates))
        
        self.assertIn(self.word_cook.content, str(response.content))

    def test_get_word_meta_tag(self):
    
        c = self.c

        response = c.get('/blog/nice_word_cook')
        
        content = str(response.content)        
        #pdb.set_trace()
        self.assertTrue(re.search(re.compile('<meta.+?name="keywords"'), content),
        'Meta tag name not found')

        self.assertTrue(re.search(re.compile('<meta.+?name="description"'), content),
        'Meta tag description not found')

        self.assertTrue(re.search(re.compile('<meta.+?property="twitter:card"'), content),
        'Meta tag twitter:card not found')
    
    def _create_word_cook(self):
        
        word = Post(author=self.author, relative_url='nice_word_cook',title='this is a nice word cook',content='<p>This is the word content</p>')
        word.save()
        
        meta_tag = MetaTag(word=word, name='keywords',content='some key words')
        meta_tag.save()
        
        meta_tag = MetaTag(word=word, name='description',content='some description')
        meta_tag.save()        
        
        meta_tag = MetaTag(word=word, property='twitter:card',content='sumary')
        meta_tag.save()
        
        return word

        
    def _create_tag_cook(slef):
        tag = Tag(name='cook')
        tag.save()
        return tag
    
    def _create_tag_vegan(slef):
        tag = Tag(name='vegan')
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