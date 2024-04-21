import requests
import sqlite3
from xml.etree import ElementTree

def perform_esearch(database, retmax, term):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": database,
        "retmax": retmax,
        "term": term
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.text
    else:
        print("ESearch request failed with status code:", response.status_code)
        print("Response content:", response.text)
        return None

def perform_efetch(database, ids):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    fetched_records = []
    # Splitting ids into batches to avoid URI too large error
    batch_size = 200  # Adjust based on the server's limitations
    for i in range(0, len(ids), batch_size):
        batch_ids = ids[i:i+batch_size]
        params = {
            "db": database,
            "id": ",".join(batch_ids),
            "retmode": "xml"
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            fetched_records.append(response.text)
        else:
            print("EFetch request failed with status code:", response.status_code)
            print("Response content:", response.text)
    return fetched_records

def parse_efetch_response(responses):
    records = []
    for response in responses:
        root = ElementTree.fromstring(response)
        for doc in root.iter("PubmedArticle"):
            record = {}
            article = doc.find(".//Article")
            record["title"] = article.findtext(".//ArticleTitle")
            record["abstract"] = article.findtext(".//AbstractText")
            authors = article.findall(".//Author")
            record["authors"] = [{"name": (author.findtext(".//LastName") or "") + " " + (author.findtext(".//ForeName") or "")} for author in authors]
            records.append(record)
    return records

def insert_records_into_db(records):
    conn = sqlite3.connect('pubmed_articles.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS articles
                 (title TEXT, abstract TEXT, authors TEXT)''')
    for record in records:
        authors = ', '.join([author['name'].strip() for author in record['authors']])
        c.execute("INSERT INTO articles (title, abstract, authors) VALUES (?, ?, ?)",
                  (record['title'], record['abstract'], authors))
    conn.commit()
    conn.close()



# Insert_records_into_db function remains the same

def main():
    # Retrieve 5,000 PubMed IDs
    esearch_response = perform_esearch(database="pubmed", retmax=5000, term="Inflammatory")
    if esearch_response:
        esearch_root = ElementTree.fromstring(esearch_response)
        id_list = [id_node.text for id_node in esearch_root.findall(".//Id")]
        if id_list:
            efetch_responses = perform_efetch(database="pubmed", ids=id_list)
            if efetch_responses:
                records = parse_efetch_response(efetch_responses)
                insert_records_into_db(records)
                print(f"Inserted {len(records)} records into the database.")
            else:
                print("EFetch response is empty.")
        else:
            print("No PubMed IDs obtained from ESearch.")
    else:
        print("ESearch response is empty.")

if __name__ == "__main__":
    main()
