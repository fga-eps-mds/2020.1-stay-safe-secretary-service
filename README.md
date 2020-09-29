# fga-eps-mds-2020.1-stay-safe-secretary-service

Secretary service of Stay Safe project

## Run Flask API
If you haven't build yet:
<pre><code>$ docker-compose build web db </code></pre>

After that you just need to run:
<pre><code>$ docker-compose up web db</code></pre>

To have access to pdb when running, use the following command:
<pre><code>$ docker-compose run --service-ports api python -u main.py</code></pre>

## Run pylint
```bash
$ docker-compose run api sh -c "pylint **/*.py"
```

## Run tests
```bash
$ docker-compose run api pytest
```

## Run Crawlers
<pre><code>$ docker-compose run crawler_crimes scrapy crawl spider_name</code></pre>

## Crontab
Crontab is a time-based job scheduler in Unix-like operating systems, it doesn't need to install if you're using a Unix based SO.

### Setting Crontab
Enter the following command to edit your crontab file:
<pre><code>$ crontab -e</code></pre>
If it's empty you should set the first line of the file with:
<pre><code>SHELL=/bin/bash</code></pre>
After that you just need to set the command to run a job.

#### Example
To run a sh file at 2am of the first day of the month:
<pre><code>0 2 1 * * /home/user/stay-safe/src/crawlers/df.sh</code></pre>
To understand more about crontab schedule expressions click [here](https://crontab.guru)

Every sh file must be in the correct permission, to set the correct permission run:
<pre><code>chmod +x script-name-here.sh</code></pre>
