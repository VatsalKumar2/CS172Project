import scrapy
import os
import hashlib
from urllib.parse import urlparse


class InternshipSpider(scrapy.Spider):
    name = "internship_spider"

    def __init__(self, seed_file="seeds.txt", max_pages=100, max_hops=3,
                 output_dir="./crawled_pages", allowed_domains_filter=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.max_pages             = int(max_pages)
        self.max_hops              = int(max_hops)
        self.output_dir            = output_dir
        self.allowed_domain_filter = allowed_domains_filter  # e.g. ".edu" or ".gov"
        self.visited_urls          = set()   # deduplication
        self.pages_crawled         = 0

        os.makedirs(self.output_dir, exist_ok=True)

        # seed the URL
        self.start_urls = []
        try:
            with open(seed_file, "r") as f:
                for line in f:
                    url = line.strip()
                    if url and url.startswith("http"):
                        self.start_urls.append(url)
            self.logger.info(f"Loaded {len(self.start_urls)} seed URLs from {seed_file}")
        except FileNotFoundError:
            self.logger.error(f"Seed file '{seed_file}' not found!")

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={"hops": 0},       # track how many hops from seed
                errback=self.handle_error
            )

    def parse(self, response):
        # This is to check limit of max page
        if self.pages_crawled >= self.max_pages:
            return

        url      = response.url
        hops     = response.meta.get("hops", 0)

        # ── deduplication: skip if already visited ──
        url_hash = hashlib.md5(url.encode()).hexdigest()
        if url_hash in self.visited_urls:
            return
        self.visited_urls.add(url_hash)

        # DOMAIN FILTERING
        if self.allowed_domain_filter:
            parsed = urlparse(url)
            if not parsed.netloc.endswith(self.allowed_domain_filter):
                self.logger.debug(f"Skipping (domain filter): {url}")
                return

        # Saving HTML
        filename = os.path.join(self.output_dir, f"{url_hash}.html")
        with open(filename, "wb") as f:
            f.write(response.body)

        self.pages_crawled += 1
        self.logger.info(
            f"[{self.pages_crawled}/{self.max_pages}] "
            f"Crawled (hop {hops}): {url}"
        )

        #  refrain from bloating
        if hops < self.max_hops and self.pages_crawled < self.max_pages:
            for href in response.css("a::attr(href)").getall():
                next_url = response.urljoin(href)

                # HTTP VALIDATION ONLY HTTP AND HTTPS 
                if not next_url.startswith("http"):
                    continue

                # Handles duplication
                next_hash = hashlib.md5(next_url.encode()).hexdigest()
                if next_hash in self.visited_urls:
                    continue

                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse,
                    meta={"hops": hops + 1},
                    errback=self.handle_error
                )

    def handle_error(self, failure):
        self.logger.warning(f"Failed to crawl: {failure.request.url}")