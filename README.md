**Setup AQgraph in a development environment on Ubuntu**

Install and configure apache, memcached and mod-wsgi-py3 (config not covered here). This is a brief overview. Ensure you secure and configure your installation correctly in production.

    sudo apt-get install apache2
    sudo apt-get install libapache2-mod-wsgi-py3
    sudo apt-get install memcached

Make a directory to serve from

    mkdir /var/www/graphs

Install pip and setup virtualenv

    sudo apt-get install -y python3-pip
    alias pip=pip3
    source ~/.bashrc
    pip install virtualenv

Activate the virtual environment

    source venv/bin/activate

Install the pre-reqs into your virtual environment

    pip install Flask
    pip install Flask-cached
    pip install python-memcached

Deactivate the virtual environment 

    deactivate

Grab the code

    git clone https://github.com/ConnectedHumber/AQgraph.git

You need a wsgi file. Start with something like this.  Put it here **/var/www/graphs/graphs.wsgi**

    #!/usr/bin/python
    activate_this = '/var/www/graphs/venv/bin/activate_this.py'
    with open(activate_this) as file_:
        exec(file_.read(), dict(__file__=activate_this))
    
    import sys
    import logging
    logging.basicConfig(stream=sys.stderr)
    sys.path.insert(0,"/var/www/graphs/AQgraph")
    
    from aq import app as application

Finally, setup a vhost in apache with the **WSGIScriptAlias** directive pointing at **/var/www/graphs/graphs.wsgi**

Finally

    systemctl restart apache2

When you want to pull the latest changes just cd to AQgraph and run

    git pull
                    
