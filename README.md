#Nirvaris Dictionary

A simple Django app to for a dictionary. You can add words, or entry words, have a search, a entry word template, with some tags for categorize them, a form for quick search, and comments in blog style

you add the entry words and tags via django admin interface and they will be avaliable in your website.

You can also import the wrod in CSV

you use it like:

<your-url>/dictionary/<relative_url> -> return the blog post

<your-url>/dictionary/<tag>/<tag>... -> return the a list of post whithin these tags.


#Quick start

To install the Dictionary, use pip from git:

```
pip install git+https://github.com/nirvaris/nirvaris-dictionary
```

- Add _dictionary_ to your INSTALLED_APPS settings like this::

```
    INSTALLED_APPS = (
        ...,
        'n_profile',
        'themedefault',
        'dictionary',
    )
```


- You have to run migrate, as it uses the db to store the words, oomments and meta-tags. 

- you hvae to add the app url to your url file

```
url(r'^dictionary/', include('dictionary.urls')),
```