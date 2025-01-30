# 🎨 Product Picasso  
*Where INGCO Data Meets Shopify Artistry*  

Transform raw product data into masterpieces with this creative merger that paints perfect Shopify listings! 🖌️

# INGCO Product Data Processor

A Streamlit application that automates merging INGCO product data with Shopify templates while scraping product images directly from the INGCO website.

## 🌟 Features

- **Automated Image Scraping**: Directly fetches product images from INGCO.com
- **Data Processing**:
  - Processes INGCO price list (Excel)
  - Merges with Shopify template (CSV)
  - Auto-generates complete product catalog
- **Cloud Ready**: Deployable on Streamlit Community Cloud
- **One-Click Export**: Generates Shopify-ready CSV template

## 📋 Prerequisites

- Python 3.8+
- Streamlit account (for cloud deployment)
- Chrome browser components (automatically handled in cloud)

## 🚀 Installation

1. Clone repository:
```bash
git clone https://github.com/yourusername/ingco-product-processor.git
cd ingco-product-processor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🖥️ Usage

1. Run the app locally:
```bash
streamlit run app.py
```

2. In the app:
   - Upload your Shopify template CSV
   - Upload INGCO price list Excel file
   - Click "Process Files"
   - Download merged CSV when ready

3. Required files format:
   - **Price List**: Excel (.xlsx) with columns:
     ```
     Ingco item No. | Product name | Description & Features | Type | Unit | uniform Retail Prices
     ```
   - **Shopify Template**: CSV with Shopify's product template structure

## ☁️ Streamlit Cloud Deployment

1. Create new repository with:
   - `app.py`
   - `requirements.txt`
   - `packages.txt`

2. On Streamlit Community Cloud:
   - Connect your GitHub account
   - Select repository and branch
   - Set main file path to `app.py`
   - Click "Deploy"

## 📂 Project Structure

```
├── app.py                 # Main application code
├── requirements.txt       # Python dependencies
├── packages.txt           # System dependencies
└── README.md              # This documentation
```

## ⚠️ Important Notes

- Website structure changes on INGCO.com will break image scraping
- First run may take 2-5 minutes for browser setup
- Maintain original column names in input files
- Test with small files before processing full catalog

## 🛠️ Troubleshooting

Common issues:
- **ChromeDriver errors**: Ensure requirements match Chrome version
- **Element not found**: Check INGCO.com for layout changes
- **Encoding issues**: Verify files are UTF-8 encoded
- **Memory errors**: Process in smaller batches

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

## 🤝 Contribution

Contributions welcome! Please:
1. Fork the repository
2. Create your feature branch
3. Submit a pull request

---

**Note**: This is an unofficial project not affiliated with INGCO or Shopify. Use at your own discretion.