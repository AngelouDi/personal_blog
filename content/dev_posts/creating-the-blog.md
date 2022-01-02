title: Creating a simple blog site based on flask and markdown
description: My journey (and possibly a guide) on a website like this
date: 02/01/2022
tags: flask, blog, markdown, heroku
These days I gave my first attempt creating this website. 
As of now it's a simple site based on *flask* and hosted on *heroku*. The posts are written on *markdown*, and *metadata* such as:

1. title
2. description
3. tags
4. date

can be included.

This will be a simple guide showing you how I managed to set it up and deploy it online.

# Setting up

For starters, I used as a baseline [this](https://www.jamesharding.uk/posts/simple-static-markdown-blog-in-flask/) guide (Thank you James). I am not gonna get into details about this, you can follow it and then continue on this reading.

## Creating a layout

I needed to have a coherent site and every endpoint to have the same base. So I created a `layout.html` file:

```
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  {% block head %}
  {% endblock %}
</head>
<body>
{% include 'nav.html' %}
  {% block content %}
  {% endblock %}
</body>
</html>
```

This gives us the ability to generate every site dynamicaly. For example:

```
{% extends "layout.html" %}
{% block content %}
<h1> Header </h1>
{% endblock %}
```

would put itself between the block content of the layout html. You can also add to the head part etc.

I also created a `nav.html` for the navbar to have it separate.

My `post.html` looks like this:

```
{% extends "layout.html" %}

{% block head %}
    <link rel="stylesheet" href="{{ url_for('static',filename='edited_pygment.css') }}">
{% endblock %}

{% block content %}
<div class="markdown">
    <h1 style="text-align: center; padding: 0px; border: none; color: var(--main-color)">{{ post.title }}</h1>
    <p style="text-align: center; padding: 0px; font-style: italic; font-size: small;">{{ post.date }}</p>
    {{ post.html|safe }}
</div>

{% endblock %}
```

## Different types of blog posts

I wanted to have two seperate types of blogs, a personal post list, and a more tech fouced one. In order to do that I had two ideas in mind:

1. Add metadata to describe the type of post and fetch them based on that.

2. Add different folders for each type of post.

In the end I opted for the second as I thought it would be easier to manage in the long run. Both are just as easy to create.

What I did was create in the content file two folders
`dev_posts, personal_posts` and put the different kind of posts in there.

I also create a separate html file for displaying the posts:
I named it `posts_block.html`:

```
{% for post in posts %}
<div class="posts_div content">
    <div class="post_title">
        <a class='post_title' , href="/{{post.path}}">
            {{ post.title }}
        </a>
    </div>
    <div class="post_description">
        {{ post.description }}
    </div>
    <div class="post_metadata">
        <span>{{ post.date }}</span>
        <span>{{ post.tags }}</span>
    </div>
</div>
{% endfor %}
```

As you can see I also added attributes for the description and various tags. 

Now everytime you want to include a list of posts in the site you can just add `{% include 'posts_block.html' %}` in the html.

I created two endpoints: `/dev_posts, /personal_posts` and sorted the posts based on the date:
```
@app.route("/dev_posts/")
def dev_posts():
    posts = [p for p in flatpages if p.path.startswith(DEV_POSTS_DIR)]
    posts.sort(key=lambda item: datetime.strptime(item['date'], "%d/%m/%Y"), reverse=True)
    return render_template('posts.html', posts=posts)


@app.route("/personal_posts/")
def personal_posts():
    posts = [p for p in flatpages if p.path.startswith(PERSONAL_POSTS_DIR)]
    posts.sort(key=lambda item: datetime.strptime(item['date'], "%d/%m/%Y"), reverse=True)
    return render_template('posts.html', posts=posts)


@app.route('/dev_posts/<name>/')
def dev_post(name):
    path = '{}/{}'.format(DEV_POSTS_DIR, name)
    post = flatpages.get_or_404(path)
    return render_template('post.html', post=post)


@app.route('/personal_posts/<name>/')
def personal_post(name):
    path = '{}/{}'.format(PERSONAL_POSTS_DIR, name)
    post = flatpages.get_or_404(path)
    return render_template('post.html', post=post)
```

that pass the different posts from the different subfolders to the `posts.html`:

```
{% extends "layout.html" %}
{% block content %}
{% include 'posts_block.html' %}
{% endblock %}
```

which puts the `posts_blog.html` into the layout.

Now you can have different kind of posts on different endpoints.

You can also add all kinds of posts to the main page:

```
@app.route('/')
def index():
    posts = [p for p in flatpages]
    posts.sort(key=lambda item: datetime.strptime(item['date'], "%d/%m/%Y"), reverse=True)
    return render_template('index.html', posts=posts)
```

by adding ```{% include 'posts_block.html' %}``` to your index.html.


## Syntax higlight and Stylizing

For syntax highlighting I am using pygments and adding `FLATPAGES_MARKDOWN_EXTENSIONS = ['codehilite', 'fenced_code']` these two extensions.

I wanted a dark theme for my site therefore I had to edit the pygments css: I generated it using

```
@app.route('/pygments.css')
def pygments_css():
    return pygments_style_defs('tango'), 200, {'Content-Type': 'text/css'}
```

grabbed it, and edited the colors and added new classes to make it look good. I then linked it staticaly and removed that endpoint.


# Deploying

## Heroku

For deploying it I opted for heroku as it's free and supports custom domains.

You will need to add `gunicorn==xx.x.x` to your requirements.txt and create a `procfile`
```
web: gunicorn app:app
```

Now you can just push to your heroku remote.

Adding your domain to heroku is as simple as `heroku domains:add www.domain.tld`.
You **MUST** include the *www* subdomain in order to make it work as far as I know.

## Domain

For my domain provided I used [namecheap](namecheap.com) and added

Grab your *CNAME* target using `heroku domains` and add a *URL Redirect Record* *@* pointing to `http://www.domain.tld
`

# Up to you
There are many ways to improve the site adding new endpoints, apis, and whatnot. The sky is the limit and this is a tiny piece of land.

I hope you found this helpful, bye!


