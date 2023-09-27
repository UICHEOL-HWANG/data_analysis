# bestseller_scraper.py
import requests
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import sqlite3
from sqlalchemy import create_engine


def extract_bookinfo(yy, mon, book_list):
    """_summary_

    Args:
        yy (_type_): _description_
        mon (_type_): _description_
        book_list (_type_): _description_

    Returns:
        _type_: _description_

    extract_bookinfo(yy, mon, book_list):
    yes24에서 책 1권의 정보를 추출 하는 함수
    yy : year
    mon : month
    book_list : 책 목록 데이터
    """
    bookList = []
    for book in book_list:
        book_dict = {}
        title = book.select_one(".gd_name").text
        if book.select(".gd_nameE"):
            subtitle = book.select_one(".gd_nameE").text
        elif book.select(".gd_nameF"):
            subtitle = book.select_one(".gd_nameF").text
        else:
            subtitle = None
        link = "https://www.yes24.com/" + book.select_one(".gd_name")["href"].strip()
        author = (
            [i.get_text().strip() for i in book.select_one(".authPub.info_auth > a")]
            if book.select_one(".authPub.info_auth > a") is not None
            else "None"
        )
        publisher = (
            book.select_one(".authPub.info_pub > a").text.strip()
            if book.select_one(".authPub.info_pub > a") is not None
            else "None"
        )
        publish_date = (
            book.select_one(".authPub.info_date").text.strip()
            if book.select_one(".authPub.info_date") is not None
            else "None"
        )
        price = (
            book.select_one(".txt_num .yes_b").text.strip() + "원"
            if book.select_one(".txt_num .yes_b") is not None
            else 0
        )
        review = (
            book.select_one(".rating_rvCount .txC_blue").text.strip()
            if book.select_one(".rating_rvCount .txC_blue") is not None
            else 0
        )
        review_link = (
            book.select_one(".rating_rvCount > a")["href"].strip()
            if book.select_one(".rating_rvCount > a") is not None
            else "None"
        )
        star_pont = (
            book.select_one(".rating_grade .yes_b").text.strip()
            if book.select_one(".rating_grade .yes_b") is not None
            else 0
        )
        tag = (
            [i.get_text().strip() for i in book.select(".info_row.info_tag > .tag > a")]
            if book.select(".info_row.info_tag > .tag > a") is not None
            else "None"
        )

        book_dict["년"] = yy
        book_dict["월"] = mon
        book_dict["제목"] = title
        book_dict["부제목"] = subtitle
        book_dict["링크"] = link
        book_dict["작가"] = author
        book_dict["출판사"] = publisher
        book_dict["출판일"] = publish_date
        book_dict["가격"] = price
        book_dict["리뷰"] = review
        book_dict["리뷰링크"] = review_link
        book_dict["별점"] = star_pont
        book_dict["태그"] = tag

        bookList.append(book_dict)
    return bookList


# 추출한 링크 내 세부정보 추출
def detail_page_info(url):
    detail_result = []
    for index, url2 in enumerate(url[:1]):
        detail_dict = {}
        print(f"{index}/{len(url)} 데이터 추출 중")
        r2 = requests.get(url2)
        soup2 = bs(r2.text, "lxml")
        book_id = url2.split("/")[-1]
        if soup2.select_one("div.infoSetCont_wrap tr:nth-child(2) > td") != None:
            if (
                "쪽수"
                in soup2.select_one("div.infoSetCont_wrap tr:nth-child(2) > th").text
            ):
                if (
                    len(
                        soup2.select_one(
                            "div.infoSetCont_wrap tr:nth-child(2) > td"
                        ).text.split("|")
                    )
                    == 3
                ):
                    page, weight, size = soup2.select_one(
                        "div.infoSetCont_wrap tr:nth-child(2) > td"
                    ).text.split("|")
                elif (
                    len(
                        soup2.select_one(
                            "div.infoSetCont_wrap tr:nth-child(2) > td"
                        ).text.split("|")
                    )
                    == 2
                    and soup2.select_one(
                        "div.infoSetCont_wrap tr:nth-child(2) > td"
                    ).text.split("|")[1][-2:]
                    == "mm"
                ):
                    page, size = soup2.select_one(
                        "div.infoSetCont_wrap tr:nth-child(2) > td"
                    ).text.split("|")
                    weight = 0
            elif (
                "쪽수"
                in soup2.select_one("div.infoSetCont_wrap tr:nth-child(3) > th").text
            ):
                if (
                    len(
                        soup2.select_one(
                            "div.infoSetCont_wrap tr:nth-child(3) > td"
                        ).text.split("|")
                    )
                    == 3
                ):
                    page, weight, size = soup2.select_one(
                        "div.infoSetCont_wrap tr:nth-child(3) > td"
                    ).text.split("|")
                elif (
                    len(
                        soup2.select_one(
                            "div.infoSetCont_wrap tr:nth-child(3) > td"
                        ).text.split("|")
                    )
                    == 2
                    and soup2.select_one(
                        "div.infoSetCont_wrap tr:nth-child(3) > td"
                    ).text.split("|")[1][-2:]
                    == "mm"
                ):
                    page, size = soup2.select_one(
                        "div.infoSetCont_wrap tr:nth-child(3) > td"
                    ).text.split("|")
                    weight = 0
            elif (
                "쪽수"
                in soup2.select_one("div.infoSetCont_wrap tr:nth-child(4) > th").text
            ):
                if (
                    len(
                        soup2.select_one(
                            "div.infoSetCont_wrap tr:nth-child(4) > td"
                        ).text.split("|")
                    )
                    == 3
                ):
                    page, weight, size = soup2.select_one(
                        "div.infoSetCont_wrap tr:nth-child(4) > td"
                    ).text.split("|")
                elif (
                    len(
                        soup2.select_one(
                            "div.infoSetCont_wrap tr:nth-child(4) > td"
                        ).text.split("|")
                    )
                    == 2
                    and soup2.select_one(
                        "div.infoSetCont_wrap tr:nth-child(4) > td"
                    ).text.split("|")[1][-2:]
                    == "mm"
                ):
                    page, size = soup2.select_one(
                        "div.infoSetCont_wrap tr:nth-child(4) > td"
                    ).text.split("|")
                    weight = 0
        else:
            page = 0
            weight = 0
            size = ""
        category = list(
            {
                i.text
                for i in soup2.select(
                    "div.infoSetCont_wrap > dl:nth-child(1) > dd > ul a"
                )
                if soup2.select("div.infoSetCont_wrap > dl:nth-child(1) > dd > ul a")
                != None
            }
        )
        book_intro = (
            soup2.select_one(".infoWrap_txtInner").get_text()
            if soup2.select_one(".infoWrap_txtInner") != None
            else ""
        )
        pub_book_intro = (
            soup2.select_one(".infoWrap_txt").get_text()
            if soup2.select_one(".infoWrap_txt") != None
            else ""
        )

        time.sleep(5)
        detail_dict["ID"] = book_id
        detail_dict["페이지"] = page
        detail_dict["무게"] = weight
        detail_dict["사이즈"] = size
        detail_dict["카테고리"] = category
        detail_dict["책소개"] = book_intro
        detail_dict["출판사리뷰"] = pub_book_intro
        detail_result.append(detail_dict)  # 결과를 detail_result 리스트에 추가

    return detail_result


def to_db(df):
    for col in df.columns:
        df[col] = df[col].apply(str)
        engine = create_engine("splite:///yes24.db", echo=False)
        conn = engine.raw_connection()
        df.to_sql("yes_final_fn", con=conn, if_exists="append")
