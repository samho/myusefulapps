# -*-coding:utf-8-*-

import urllib
import requests
import re
from bs4 import BeautifulSoup
import redis
import time
import os
import sys
from urllib.parse import quote


class JAVMenuCrawler:
    REDIS_TABLE = {"DOWNLOADED_SET": "downloaded_set",
                   "RES_TO_DOWNLOAD_LIST": "res_todownload_list",
                   "PAGE_TO_DOWNLOAD_LIST": "page_todownload_list"
                   }
    REDIS_PASS = "m40Lpre#lfr$vlq"
    STORE_ROOT_PATH = "d:\workspace\download"
    # RES_PATH = os.path.join(STORE_ROOT_PATH, time.strftime('%Y%m%d'))
    RES_PATH = os.path.join(STORE_ROOT_PATH, "")
    # TORRENT_REFERER_PRE = "http://1re.re/d.php?d="
    TORRENT_REFERER_PRE = "http://1on.re/d.php?d="

    def get_str_urlencode(self, str):
        url = "http://javtorrent.re/tag/" + quote(str, 'utf-8')
        return url

    def download(self, url):
        print("Download: ", url)
        try:
            html = requests.get(url).content.decode("utf-8")
        except Exception as e:
            print("Download error: ", e.reason)
            html = None
        return html

    def download_res(self, url, num_retries=2):
        print("Download: ", url)
        try:
            html = requests.get(url).content
            # print(html)
        except urllib.error.URLError as e:
            print("Download error: ", e.reason)
            html = None
            if num_retries > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    return download(url, num_retries - 1)
        return html

    def get_redis_conn(self, password="", host="localhost", port=6379, db=0):
        if password == "":
            password = self.REDIS_PASS
        conn = redis.Redis(host, port, db, password, decode_responses=True)
        return conn

    def close_redis_conn(self, conn):
        conn.close()

    def is_exists_res(self, conn, res_designation):
        is_exists = conn.exists("res:" + res_designation)
        return is_exists

    def is_exists_res_downloaded(self, conn, res_designation):
        img_res = "res:" + res_designation + "|img"
        torrent_res = "res:" + res_designation + "|torrent"
        is_exists_img = conn.sismember(self.REDIS_TABLE["DOWNLOADED_SET"], img_res)
        is_exists_torrent = conn.sismember(self.REDIS_TABLE["DOWNLOADED_SET"], torrent_res)
        return is_exists_img and is_exists_torrent

    def get_res_count(self):
        conn = self.get_redis_conn(host="192.168.233.128")
        reses = conn.llen(self.REDIS_TABLE["RES_TO_DOWNLOAD_LIST"])
        self.close_redis_conn(conn)
        return reses

    def new_res_download_task(self, conn, url, designation):
        conn.lpush(self.REDIS_TABLE["RES_TO_DOWNLOAD_LIST"], "res:" + designation + "|" + url)

    def get_res_download_task(self, conn):
        return conn.rpop(self.REDIS_TABLE["RES_TO_DOWNLOAD_LIST"])

    def get_pages_count(self):
        conn = self.get_redis_conn(host="192.168.233.128")
        pages = conn.llen(self.REDIS_TABLE["PAGE_TO_DOWNLOAD_LIST"])
        self.close_redis_conn(conn)
        return pages

    def new_page_download_task(self, conn, url, designation):
        conn.lpush(self.REDIS_TABLE["PAGE_TO_DOWNLOAD_LIST"], "res:" + designation + "|" + url)

    def get_page_download_task(self, conn):
        return conn.rpop(self.REDIS_TABLE["PAGE_TO_DOWNLOAD_LIST"])

    def save_res_hash(self, conn, res, group):
        res_key = "res:" + res["Designation"]
        conn.hmset(res_key, {
            "name": res["Name"],
            "designation": res["Designation"],
            "details_page": res["Details_url"],
            "cover_image": res["Cover_img_link"],
            "seed_url": res["Torrent_link"],
            "tags": res["tags"],
            "group": group,
        })

        return res_key

    def save_downloaded_set(self, conn, res_key):
        # res_key = "res:" + res["Designation"]
        conn.sadd(self.REDIS_TABLE["DOWNLOADED_SET"], res_key)

        return res_key

    def get_info_from_detail_page(self, url):
        # 打开details页面
        html = self.download(url)
        soup = BeautifulSoup(html)
        # 获取movie的tag信息
        movie_details = soup.select("#app > div > div > div.container-fluid.p-0 > div > div.col-md-9.px-0 > div.col-12.left-wrapper.mb-3 > div > div > div:nth-child(7)")
        tags = []
        for tag in movie_details[0].find_all("a"):
            tags.append(tag.get_text().strip())
        # 获取 magnet link信息
        magnet_content = soup.select("#content1")[0].select(".table-responsive")
        magnet_links = []
        if len(magnet_content) > 0:
            for btn in magnet_content[0].find_all('button'):
                magnet_links.append(btn["data-clipboard-text"])
        details_info = {"tags": tags, "magnet_links": magnet_links}

        return details_info

    def save_res_magnet_to_file(self):
        conn = self.get_redis_conn(host="192.168.233.128")
        res_value = self.get_page_download_task(conn)
        print(res_value)
        res_key = res_value.split("|")[0]
        res_url = res_value.split("|")[1]
        res_group = self.get_res_group(res_key)
        designation = res_key.split(":")[1]
        store_path_prefix = os.path.join(self.RES_PATH, res_group)
        if not os.path.exists(store_path_prefix):
            os.makedirs(store_path_prefix)

        # 从detail 页面获取tags 和 magnet link
        details_info = self.get_info_from_detail_page(res_url)

        # 更新 movie tag key内容
        tag_key = res_key + "|tags"
        for tag in details_info["tags"]:
            conn.sadd(tag_key, tag)

        # 更新 magnet link key 内容
        torrent_key = res_key + "|torrent"
        # 创建magnet link 文件
        store_file_path = os.path.join(store_path_prefix, designation.upper() + " -Magnet Links.txt")
        f = open(store_file_path, "w")
        for link in details_info["magnet_links"]:
            conn.sadd(torrent_key, link)
            f.write(link +"\n")

        f.close()
        self.save_downloaded_set(conn, torrent_key)
        self.close_redis_conn(conn)

    def save_res_cover_to_file(self):
        conn = self.get_redis_conn(host="192.168.233.128")
        res_value = self.get_res_download_task(conn)
        print(res_value)
        res_key = res_value.split("|")[0]
        res_url = res_value.split("|")[1]
        res_group = self.get_res_group(res_key)
        designation = res_key.split(":")[1]
        store_path_prefix = os.path.join(self.RES_PATH, res_group)
        if not os.path.exists(store_path_prefix):
            os.makedirs(store_path_prefix)

        store_file_path = os.path.join(store_path_prefix, designation.upper() + " - Cover.jpg")
        if res_url == "":
            print("There is not any Cover file could be downloaded automatically.")
        else:
            html = self.download_res(res_url)
            self.save_downloaded_set(conn, res_key + "|img")

            f = open(store_file_path, "wb")
            f.write(html)
            f.close()

        self.close_redis_conn(conn)

    def get_res_list(self, html):
        res_info = []
        soup = BeautifulSoup(html)
        main_content = soup.select(".card-deck")
        div_list = main_content[0].select(".px-1")
        for div in div_list:
            res = {}
            if " " in str(div.find_all('h5')[0].get_text()):
                res["Designation"] = str(div.find_all('h5')[0].get_text()).strip().split()[0]
            else:
                res["Designation"] = str(div.find_all('h5')[0].get_text()).strip()
            res["Name"] = str(div.find_all('p')[0].get_text()).strip()
            res["Details_url"] = str(div.find_all('a')[0]["href"]).strip()
            res["Cover_img_link"] = str(div.find_all('img')[1]["data-src"]).strip()
            res_info.append(res)
        return res_info

    def get_res_name(self, key):
        conn = self.get_redis_conn(host="192.168.233.128")
        res_name = conn.hget(key, "name")
        self.close_redis_conn(conn)
        return res_name

    def get_res_tags(self, key):
        conn = self.get_redis_conn(host="192.168.233.128")
        res_tags = conn.hget(key, "tags")
        self.close_redis_conn(conn)
        return str(res_tags).split(",")

    def get_res_group(self, key):
        conn = self.get_redis_conn(host="192.168.233.128")
        res_group = conn.hget(key, "group")
        self.close_redis_conn(conn)
        return res_group

    # 从指定URL中，获取需要资源内容，即想要获取的movies

    def get_res(self, url, group="Others"):
        print(url)
        # 获取redis数据库连接，
        conn = self.get_redis_conn(host="192.168.233.128")

        # 获取页面内容
        html = self.download(url)
        if html is None:
            return None

        # 获取所有movie的详细信息
        res_info = self.get_res_list(html)
        # print(res_info)

        for res in res_info:
            # 判断该番号movie是否需要爬取
            if self.is_exists_res(conn, res["Designation"]):
                print("The Video resource %s is exists." % res["Designation"])
                # 判断封面图片，种子或者磁力链接是否需要爬取
                if self.is_exists_res_downloaded(conn, res["Designation"]):
                    print("The torrent seed and Cover image have been downloaded too.")
                    continue
                else:
                    # 如果封面图片,种子或磁力链接未爬取，加入爬取队列中
                    print(
                        "But the torrent and Cover seems not downloaded, call dowload_res method to download them.")
                    self.new_res_download_task(conn, res["Cover_img_link"], res["Designation"])
                    self.new_page_download_task(conn, res["Details_url"], res["Designation"])
                    continue
            else:
                # 该番号movie未爬取，创建该番号的爬取任务
                self.new_page_download_task(conn, res["Details_url"], res["Designation"])
                self.new_res_download_task(conn, res["Cover_img_link"], res["Designation"])
                res["tags"] = "res:" + res["Designation"] + "|tags"
                res["Torrent_link"] = "res:" + res["Designation"] + "|torrent"
                self.save_res_hash(conn, res, group)
                print(
                    "The resource record of %s has been created, and resources download tasks have been created." % res[
                        "Designation"])
        self.close_redis_conn(conn)
        return True


if __name__ == "__main__":
    crawler = JAVMenuCrawler()

    # crawler.get_info_from_detail_page("https://javmenu.com/zh/LUXU-1610")
    # crawler.get_info_from_detail_page("https://javmenu.com/zh/MDVR-146")

    actor = "LUXU"
    download_url = "https://javmenu.com/zh/code/LUXU?page=2"
    html = crawler.get_res(download_url, actor)
    if html is None:
        print("[ERROR] %s is not exists." % download_url)
        sys.exit(1)
    else:
        print(html)
    # crawler.get_res_list(html)
    pages_need_to_download = crawler.get_pages_count()
    for page_num in range(pages_need_to_download):
        crawler.save_res_magnet_to_file()
        time.sleep(5)

    res_need_to_download = crawler.get_res_count()
    for res_num in range(res_need_to_download):
        crawler.save_res_cover_to_file()
        time.sleep(10)
