# app.py
import streamlit as st
import pandas as pd
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#titile
st.title("🛠️ INGCO-Shopify Auto-Painter")
#subtitle
st.subheader("Turn Price Lists into Ready-to-Sell Masterpieces - No Brush Required!")

# bottom info
st.markdown(
    """
    Maged never paid me for this amazing hardwork! 😂
    """
)

# Configuration
INGCO_URL = "https://www.ingco.com/eg-en/products?pageNum=1&pageSize=4000"

@st.cache_resource
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    return webdriver.Chrome(options=options)

def scrape_image_links():
    driver = get_driver()
    try:
        driver.get(INGCO_URL)
        
        # Handle privacy policy
        try:
            privacy_button_xpath = "/html/body/div[2]/div/div[2]/div/div[1]/button"
            accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, privacy_button_xpath))
            )
            accept_button.click()
            time.sleep(1)
        except Exception as e:
            st.warning(f"Privacy policy handling failed: {str(e)}")

        # Wait for product grid
        target_xpath = "/html/body/div/div/div/section/main/div[1]/div/div/div[3]/div"
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, target_xpath))
        )

        # Extract content
        content = driver.find_element(By.XPATH, target_xpath).get_attribute("innerHTML")
        
        # Process images
        pattern = r'src="([^"]*)"'
        matches = re.findall(pattern, content)
        
        data = [
            (re.search(r'/([^/]+)\.[^/.]+$', match).group(1), match) 
            for match in matches 
            if re.search(r'/([^/]+)\.[^/.]+$', match)
        ]
        
        return pd.DataFrame(data, columns=['sku', 'link'])

    except Exception as e:
        st.error(f"Scraping failed: {str(e)}")
        return None
    finally:
        driver.quit()

# File uploaders
template_file = st.file_uploader("Upload Shopify Template CSV", type=['csv'])
price_file = st.file_uploader("Upload INGCO Price Excel File", type=['xlsx'])

if st.button('Process Files'):
    if template_file and price_file:
        with st.spinner('Scraping product images... (this may take a while)'):
            imagelinks = scrape_image_links()
            
        if imagelinks is not None:
            try:
                with st.spinner('Processing data...'):
                    # Process template file
                    template = pd.read_csv(template_file)
                    template = template.head(0)

                    # Process price file
                    df = pd.read_excel(price_file)
                    
                    # Clean price data
                    df = df.dropna(subset=['Unnamed: 0'])
                    df = df.drop(index=0).reset_index(drop=True)
                    df.columns = df.iloc[0]
                    df = df[1:].reset_index(drop=True)
                    df = df.iloc[:, :9]
                    df = df.drop(columns=['Price FOB Shanghai by USD', 'Picture', 'Packed by'])
                    df = df.rename(columns={
                        'uniform Retail Prices': 'price',
                        'Description & Features': 'desc',
                        'Product name': 'name',
                        'Ingco item No.': 'sku',
                        'Type': 'type',
                        'Unit': 'unit'
                    })

                    # Merge data
                    merged = pd.merge(imagelinks, df, on='sku')

                    # Column mapping and transformation
                    column_mapping = {
                        'sku': 'Variant SKU',
                        'link': 'Image Src',
                        'type': 'Type',
                        'name': 'Title',
                        'desc': 'Body (HTML)',
                        'unit': 'Variant Grams',
                        'price': 'Variant Price'
                    }
                    merged_renamed = merged.rename(columns=column_mapping)

                    # Combine with template
                    final_output = pd.concat([template, merged_renamed], ignore_index=True)

                    # Create download link
                    csv = final_output.to_csv(index=False).encode('utf-8')
                    st.success("Processing completed successfully!")
                    
                    st.download_button(
                        label="Download Processed CSV",
                        data=csv,
                        file_name='processed_output.csv',
                        mime='text/csv',
                    )
                    
            except Exception as e:
                st.error(f"Data processing failed: {str(e)}")
    else:
        st.warning("Please upload both template and price files to proceed.")