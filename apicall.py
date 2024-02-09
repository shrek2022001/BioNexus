import requests
from xml.etree import ElementTree

def perform_esearch(database, retmax, term):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": database,
        "retmax": retmax,
        "term": term  # Add search term parameter
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
    params = {
        "db": database,
        "id": ",".join(ids),
        "retmode": "xml"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.text
    else:
        print("EFetch request failed with status code:", response.status_code)
        print("Response content:", response.text)
        return None

def parse_efetch_response(response):
    root = ElementTree.fromstring(response)
    records = []
    for doc in root.iter("PubmedArticle"):
        record = {}
        article = doc.find(".//Article")
        record["Title"] = article.findtext(".//ArticleTitle")
        record["Abstract"] = article.findtext(".//AbstractText")
        authors = article.findall(".//Author")
        record["Authors"] = ", ".join([author.findtext(".//LastName") + " " + author.findtext(".//ForeName") for author in authors])
        records.append(record)
    return records

def main():
    # Perform ESearch to retrieve PubMed IDs
    esearch_response = perform_esearch(database="pubmed", retmax=10, term="cancer")
    if esearch_response:
        esearch_root = ElementTree.fromstring(esearch_response)
        id_list = [id_node.text for id_node in esearch_root.findall(".//Id")]
        print("PubMed IDs:", id_list)  # Print PubMed IDs obtained from ESearch
        if id_list:
            # Perform EFetch to retrieve detailed information for PubMed records
            efetch_response = perform_efetch(database="pubmed", ids=id_list)
            if efetch_response:
                # Parse EFetch response
                records = parse_efetch_response(efetch_response)
                # Print detailed information for each record
                for i, record in enumerate(records, start=1):
                    print("Record", i)
                    print("Title:", record.get("Title"))
                    print("Authors:", record.get("Authors"))
                    print("Abstract:", record.get("Abstract"))
                    print()
            else:
                print("EFetch response is empty.")
        else:
            print("No PubMed IDs obtained from ESearch.")
    else:
        print("ESearch response is empty.")

if __name__ == "__main__":
    main()
