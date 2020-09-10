# fga-eps-mds-2020.1-stay-safe-secretary-service

Secretary service of Stay Safe project

## Run
If you haven't build yet:
<pre><code>$ docker-compose up --build</code></pre>

After that you just need to run:
<pre><code>$ docker-compose up</code></pre>

## Crawlers
Enter the directory of the crawler uf wanted.
If you haven't build yet:
<pre><code>$ docker build -t crawler_uf .</code></pre>

After that run:
<pre><code>$ docker run crawler_uf scrapy crawl spider_name</code></pre>
