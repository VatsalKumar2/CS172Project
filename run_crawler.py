import argparse
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spider import InternshipSpider


def main():
    parser = argparse.ArgumentParser(description="CS172 Web Crawler")
    parser.add_argument("--seed-file",   default="seeds.txt",      help="Path to seed URLs file")
    parser.add_argument("--max-pages",   type=int, default=10000,   help="Max number of pages to crawl")
    parser.add_argument("--max-hops",    type=int, default=6,       help="Max hops away from seed URLs")
    parser.add_argument("--output-dir",  default="./crawled_pages", help="Directory to store HTML files")
    parser.add_argument("--domain-filter", default=None,            help="Only crawl this domain e.g. .edu or .gov")
    args = parser.parse_args()

    # ── print run config ──
    print("=" * 50)
    print("  CS172 Web Crawler")
    print("=" * 50)
    print(f"  Seed file    : {args.seed_file}")
    print(f"  Max pages    : {args.max_pages}")
    print(f"  Max hops     : {args.max_hops}")
    print(f"  Output dir   : {args.output_dir}")
    print(f"  Domain filter: {args.domain_filter or 'none'}")
    print("=" * 50)

    # Load scrapy
    os.environ["SCRAPY_SETTINGS_MODULE"] = "settings"
    settings = get_project_settings()

    # Run spider.py
    process = CrawlerProcess(settings)
    process.crawl(
        InternshipSpider,
        seed_file            = args.seed_file,
        max_pages            = args.max_pages,
        max_hops             = args.max_hops,
        output_dir           = args.output_dir,
        allowed_domains_filter = args.domain_filter
    )
    process.start()

    
    total_files = len([f for f in os.listdir(args.output_dir) if f.endswith(".html")])
    total_size  = sum(
        os.path.getsize(os.path.join(args.output_dir, f))
        for f in os.listdir(args.output_dir)
        if f.endswith(".html")
    )
    print("=" * 50)
    print(f"  THIS IS TO TEST AND OUTPUT OUR CS172 PART A DATA: ")
    print(f"  TEST 1- SEE HOW MANY PAGES CRAWLED : {total_files}")
    print(f"  TEST 2 - SEE THE SIZE   : {total_size / 1e6:.2f} MB")
    print(f"  TEST 3 - DISPLAY THE DIRECTORY    : {args.output_dir}")
    print("=" * 50)


if __name__ == "__main__":
    main()