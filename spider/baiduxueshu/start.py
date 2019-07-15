from scrapy import cmdline

# cmdline.execute("scrapy crawl paper -L ERROR".split())


if __name__ == '__main__':
    cmdline.execute("scrapy crawl paper_new".split())
    pass
