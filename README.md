# 📚 Book Data Scraper (Scrapy Training Project)

This repository contains a training project utilizing the **Scrapy** framework in Python to perform web scraping on multiple online book stores. The goal is to extract structured data about books and output the results into **CSV** files.

This project serves primarily for **training and demonstration purposes** to showcase core Scrapy concepts like defining multiple spiders, item pipelines, and exporting data using the built-in Feed Exporters.

---

## ✨ Features

* **Framework:** Built using **Scrapy**, a fast and powerful Python web scraping framework and **scrapy-playwright** to handle pages that require JavaScript.
* **Target Websites:** Scrapes data from **iranketab, fidibo, taaghche**.
* **Data Output:** Extracted data is saved into individual **CSV files** for each spider.
* **Data Fields:** (Specify the main data points you extract, e.g., Title, Author, Price, URL, Rating).

---

## ⚠️ Disclaimer
This project is for educational purposes only. Please be mindful of the robots.txt file and the Terms of Service of any website you intend to scrape. 
The scraping targets used in this repository are for demonstration and learning purposes.

---
## 🚀 Getting Started

Follow these steps to set up and run the scraping project locally.

### Prerequisites

You need **Python 3.x** and **Scrapy** installed on your system.

```bash
# Install Scrapy
pip install scrapy
pip install scrapy-playwright
