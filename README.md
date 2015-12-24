=====
Nirvaris Dictionary
=====

A simple Django app to for a dictionary. You can add words, or entry words, have a search, a entry word template, 
with some tags for categorize them, a form for quick search, and comments in blog style

you add the entry words and tags via django admin interface and they will be avaliable in your website.

you use it like:

<your-url>/dictionary/<relative_url> -> return the blog post

<your-url>/dictionary/<tag>/<tag>... -> return the a list of post whithin these tags.


Quick start
-----------

To install the Dictionary, use pip from git:

pip install git+https://github.com/nirvaris/nirvaris-dictionary

1. Add "dictionary" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'dictionary',
    )

2. You have to run makemigrations and migrate, as it uses the db to store the words, oomments and meta-tags. 

3. Copy the templates on the app's template folder to your application template folders
	These templates are used to render the posts. You should use them for your own style
	
4. you hvae to add the app url to your url file:  url(r'^dictionary/', include('blog.urls')),