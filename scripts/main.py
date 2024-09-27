import os
import pandas as pd
import logging
import time
from PyPDF2 import PdfReader

# Global variables to control processing and hold report data
is_processing = False
report_data = []

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log', filemode='a')

# Direct paths to the files
treaty_slip_path = r"/data/BICOR-MEDICAL QS-3RD QTR 2020-  KENYA RE- NAIROBI.PDF"
claims_bordereaux_path = r"/data/Medical quota share treaty  3rd Qtr 2020.xlsx"
ceadent = r"/data/Medical Quota share slip.pdf"

def process_files_directly(treaty_slip_path, claims_bordereaux_path):
    global is_processing
    global report_data
    is_processing = True
    start_time = time.time()

    try:
        logging.info("Starting to process files directly")

        # Process claims bordereaux (Excel file)
        claims_data = extract_excel_data(claims_bordereaux_path, sheet_name="claims bordereaux")
        if claims_data is not None:
         
            print("Extracted Claims Bordereaux Data:")
            print(claims_data)  # Print the entire DataFrame
            print("-" * 40)  
            
            process_claim_data(claims_data, os.path.basename(claims_bordereaux_path))

        # Process treaty slip (PDF file)
        treaty_data = extract_pdf_data(treaty_slip_path)
        if treaty_data is not None:
            logging.info(f"Processed treaty slip from {os.path.basename(treaty_slip_path)}")

        logging.info("Processing complete.")
        generate_excel_report()

    except Exception as e:
        logging.error(f"Error during file processing: {e}")
    finally:
        is_processing = False

def extract_excel_data(file_path, sheet_name):
    try:
        # Load the specified worksheet in the Excel file
        data = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
        logging.info(f"Data extracted from {file_path}, worksheet: {sheet_name}")
        return data
    except Exception as e:
        logging.error(f"Error reading {file_path}: {e}")
        return None

def extract_pdf_data(file_path):
    try:
        text = ""
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
        logging.info(f"Data extracted from {file_path}")
        return text
    except Exception as e:
        logging.error(f"Error reading {file_path}: {e}")
        return None

def process_claim_data(data, file_name):
    global report_data
    
    if isinstance(data, pd.DataFrame):
        # Assuming 'Paid Loss' is a column in the claims bordereaux sheet
        paid_loss = data.get('Paid Loss', 0).sum()  # Adjust based on your actual data structure
        
        underwriting_year = "2024"  # Example, adjust as necessary

        report_data.append({
            'File Name': file_name,
            'Paid Loss': paid_loss,
            'Underwriting Year': underwriting_year,
        })

        # Print the extracted data to console
        print("Extracted Claims Data:")
        print(data)  # Print the entire DataFrame
        print("-" * 40)

def generate_excel_report():
    if report_data:
        report_df = pd.DataFrame(report_data)
        report_path = "Claims_Report.xlsx"  # Save report in the current directory
        report_df.to_excel(report_path, index=False)
        logging.info(f"Report generated: {report_path}")
    else:
        logging.info("No data to generate report.")

def stop_processing():
    global is_processing
    is_processing = False
    logging.info("Processing manually stopped.")

def main():
    # Process the files directly without the done projects folder concept
    process_files_directly(treaty_slip_path, claims_bordereaux_path)

if __name__ == "__main__":
    main()
