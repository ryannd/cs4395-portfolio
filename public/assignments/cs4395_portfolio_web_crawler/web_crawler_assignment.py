# CS 4395.001 Portfolio Assignment - Web Crawler
# Ryan Dimaranan and Hannah Valena

import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import os
import nltk
import math
import pickle
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

# crawl start_url, find and return relevant links. num_links is the number of links to return 
def web_crawler(start_url, num_links):
  # keeping track of crawled sites
  relevant_sites = []
  num_sites = 0
  # recursively crawl websites for related sites
  def crawl(url):
    nonlocal num_sites
    nonlocal relevant_sites

    if num_sites > num_links:
      return

    # get data from current site crawled
    req = requests.get(url)
    data = req.text
    soup = BeautifulSoup(data, features="html5lib")
    links = soup.findAll('a')
    # keep track of sites to recursively crawl
    local_sites = []
    i = 0
    # find at least 5 sites to crawl, stop crawling when found enough sites
    while len(local_sites) < 5 and i < len(links) and len(relevant_sites) < num_links:
      link_str = str(links[i].get('href')).split('#')[0]

      # get only relevant links and ignore social media sites 
      if link_str.startswith('http') and link_str.find('space') != -1 and not any(link_str.find(link) != -1 for link in ['twitter','facebook','pinterest','youtube','reddit', 'instagram', 'flickr', 'shop', 'subscribe', 'images']):
        try:
          link_str = re.sub('https', 'http', link_str)
          urlopen(Request(link_str, headers = {'User-Agent': 'Mozilla/5.0'}))

          # ignore duplicates
          if not any(link_str in link for link in relevant_sites):
            local_sites.append(link_str)
            relevant_sites.append(link_str)
            num_sites += 1
        except:
          pass
      i += 1

    # find websites inside other websites
    for link in local_sites:
      crawl(link) 
  # start crawling
  crawl(start_url)
  return relevant_sites

  
# scrape each url in urls and store the scraped text in scraped_paths_path
def web_scraper(urls, scraped_pages_path):
  # create directory to store scraped pages
  if not os.path.exists(scraped_pages_path):
    os.makedirs(scraped_pages_path)

  # scrape and store text from each url
  for url in urls:
    req = Request(url, headers = {'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req)
    soup = BeautifulSoup(html.read(), 'html.parser')
    
    # remove certain elements
    for element in soup(["script", "style", "footer", "header", "aside", "iframe"]):
      element.extract()

    # set file name as the web page's title
    file_name = soup.title.text.split('/')[0]

    # store page's text in a file
    with open(os.path.join(scraped_pages_path, file_name), 'w') as f:
      f.write(soup.get_text())


# clean the text from scraped_pages_path and store in clean_text_path    
def clean_text(scraped_pages_path, clean_text_path):
  # create directory to store cleaned text
  if not os.path.exists(clean_text_path):
    os.makedirs(clean_text_path)

  # clean text from each scraped page 
  for filename in os.listdir(scraped_pages_path):
    f = os.path.join(scraped_pages_path, filename)
    with open(f, 'r') as content:
      # perform cleaning: lowercase, remove extra spaces, ensure a space after punctuation
      content = content.read().lower()
      content = ' '.join(content.split())
      content = re.sub(r'(?<=[.,?!:;])(?=[^\s])', r' ', content)
      content = re.sub(r'\b[$:]\b', ' \g<0> ', content)
      
      sentences = sent_tokenize(content)
      
      # store cleaned text in a new file
      with open(os.path.join(clean_text_path, filename), 'w') as f:
        for sent in sentences:
          f.write(sent + '\n')
          

# merge 2 dicts, append values for shared keys. return merged dict
def merge_dict(dict1, dict2):
    for i in dict2.keys():
        if i not in dict1:
          dict1[i] = dict2[i]
        else:
          dict1[i] += dict2[i]
    return dict1


# find and return key terms in clean_text_path based on tf-idf. num_terms is the number of terms to extract
def extract_key_terms(clean_text_path, num_terms):
  vocab = set()
  vocab_by_doc = []
  num_pages = 0
  tf_dict_all = {}
  
  for filename in os.listdir(clean_text_path):
    with open(os.path.join(clean_text_path, filename), 'r') as f:
      num_pages += 1
      
      # create tf dict for current file
      tf_dict = create_tf_dict(f.read())

      # update vocabulary set
      vocab_by_doc.append(tf_dict.keys())
      vocab = vocab.union(set(tf_dict.keys()))

      # update tf dict for all files
      tf_dict_all = merge_dict(tf_dict_all, tf_dict)

  # create idf dict
  idf_dict = {}
  for term in vocab:
    temp = ['x' for v in vocab_by_doc if term in v]
    idf_dict[term] = math.log((1 + num_pages) / (1 + len(temp)))

  # create tf-idf dict 
  tf_idf_dict = {}
  for t in tf_dict_all.keys():
    tf_idf_dict[t] = tf_dict_all[t] * idf_dict[t]

  # get terms by highest weights
  terms_sorted = sorted(tf_idf_dict.items(), key=lambda x:x[1], reverse=True)
  return [term[0] for term in terms_sorted][:num_terms]


# create and return a term frequency dict based on text
def create_tf_dict(text):
  tf_dict = {}

  # preprocessing
  tokens = word_tokenize(text)
  tokens = [t for t in tokens if t.isalpha() and t not in stopwords.words('english')]

  # get term frequencies
  token_set = set(tokens)
  tf_dict = {t:tokens.count(t) for t in token_set}

  # normalize term frequency with number of tokens
  for t in tf_dict.keys():
    tf_dict[t] = tf_dict[t] / len(tokens)

  return tf_dict


# build and return knowledge base dict, where key = term, value = list of sentences from clean_text_path containing term
# pickle dict and store files in knowledge_base_path
def build_knowledge_base(terms, clean_text_path, knowledge_base_path):
  knowledge_base = {}

  # create knowledge base folder if needed
  if not os.path.exists(knowledge_base_path):
    os.makedirs(knowledge_base_path)

  # build base for each term
  for term in terms:
    relevant_sentences = find_relevant_sentences(term, clean_text_path)

    # update knowledge base
    if term in knowledge_base:
      knowledge_base.get(term).extend(relevant_sentences)
    elif term not in knowledge_base:
      knowledge_base[term] = relevant_sentences

  # create pickle file for knowledge base dict
  print("Dumping knowledge base dict to pickle file...\n")
  pickle.dump(knowledge_base, open(os.path.join(knowledge_base_path, 'knowledge_base.p'), 'wb'))

  # (extra) create file for each term in knowledge base for easier viewing/access
  print("Creating knowledge base text files for each term...\n")
  for key, value in knowledge_base.items():
    with open(os.path.join(knowledge_base_path, key), 'w') as f:
      f.write("\n".join(value))
  
  return knowledge_base


# find relevant sentences for term in clean_text_path
def find_relevant_sentences(term, clean_text_path):
  relevant_sentences = []

  for filename in os.listdir(clean_text_path):
    with open(os.path.join(clean_text_path, filename), 'r') as f:
      sentences = sent_tokenize(f.read())
      relevant_sentences.extend([x for x in sentences if re.search(term, x)])
  
  return relevant_sentences


def main():
  # find a list of relevant URLs based on a start URL
  print("Starting web crawler...\n")
  start_url = 'https://www.cnet.com/science/features/every-major-space-event-in-2022-nasas-moon-mission-spacex-launches-meteor-showers-and-more/'
  num_links = 15
  relevant_sites = web_crawler(start_url, num_links)

  # output relevant URLs
  print(f'Relevant Sites based on {start_url}:')
  i = 0
  for site in relevant_sites:
    i += 1
    print(f'{i}. {site}')
    
  # loop through URLs, scrape all text from each page, and store text in its own file within scraped_pages directory
  print("\nStarting web scraper...\n")
  scraped_pages_path = 'scraped_pages'
  web_scraper(relevant_sites, scraped_pages_path)

  # clean files in scraped_pages directory and store cleaned files in clean_text directory
  print("Cleaning text and creating output files...\n")
  clean_text_path = 'clean_text'
  clean_text(scraped_pages_path, clean_text_path)

  # extract key terms based on tf-idf
  print("Extracting 40 key terms...\n")
  num_terms = 40
  key_terms = extract_key_terms(clean_text_path, num_terms)
  print(f'Top {num_terms} key terms: {key_terms}\n')

  # manually determine top key terms based on personal domain knowledge
  top_key_terms = ['webb', 'dart', 'falcon', 'asteroid', 'didymos', 'dimorphos', 'spacex', 'rover', 'russia', 'rocket']
  print(f"The top {len(top_key_terms)} key terms are: {top_key_terms}\n")

  # build a knowledge base dict based on top key terms, with key = term, value = list of sentences from clean_text containing term
  print("Building a knowledge base...\n")
  knowledge_base_path = 'knowledge_base'
  knowledge_base = build_knowledge_base(top_key_terms, clean_text_path, knowledge_base_path)

if __name__ == '__main__':
  main()
