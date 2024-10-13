import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to extract meta tags from a URL
def extract_meta_tags(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract meta tags
        meta_data = {
            'URL': url,
            'Title': soup.title.string if soup.title else 'N/A',
            'Description': soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else 'N/A',
            'Keywords': soup.find('meta', attrs={'name': 'keywords'})['content'] if soup.find('meta', attrs={'name': 'keywords'}) else 'N/A',
            'Canonical': soup.find('link', attrs={'rel': 'canonical'})['href'] if soup.find('link', attrs={'rel': 'canonical'}) else 'N/A',
            'Robots': soup.find('meta', attrs={'name': 'robots'})['content'] if soup.find('meta', attrs={'name': 'robots'}) else 'N/A',
            'Author': soup.find('meta', attrs={'name': 'author'})['content'] if soup.find('meta', attrs={'name': 'author'}) else 'N/A',
            'Publisher': soup.find('meta', attrs={'name': 'publisher'})['content'] if soup.find('meta', attrs={'name': 'publisher'}) else 'N/A',
            'Language': soup.find('html')['lang'] if soup.find('html').has_attr('lang') else 'N/A'
        }
        return meta_data
    except requests.exceptions.RequestException as e:
        return {'URL': url, 'Error': str(e)}

# Streamlit app
def main():
    st.title("Meta Tag Scraper for SEO")
    st.write("Enter the list of URLs you want to extract meta tags from.")

    # User input
    urls = st.text_area("Enter URLs (one per line):")
    if st.button("Extract Meta Tags"):
        if urls:
            url_list = urls.split('\n')
            results = []
            for url in url_list:
                url = url.strip()
                if url:
                    meta_data = extract_meta_tags(url)
                    results.append(meta_data)
            
            # Display results
            df = pd.DataFrame(results)
            st.write("### Extracted Meta Tags:")
            st.dataframe(df)
            
            # Option to download the results
            csv = df.to_csv(index=False)
            st.download_button(label="Download CSV", data=csv, file_name="meta_tags.csv", mime="text/csv")
        else:
            st.warning("Please enter at least one URL.")

if __name__ == "__main__":
    main()