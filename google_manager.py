import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime

SPREADSHEET_NAME = "Good Will Hunt DB"

class GoogleManager:
    def __init__(self, credentials):
        self.creds = credentials
        self.drive_service = build("drive", "v3", credentials=self.creds)
        self.sheets_service = build("sheets", "v4", credentials=self.creds)

    def find_or_create_db(self):
        """Finds the 'Good Will Hunt DB' spreadsheet or creates it if missing."""
        query = f"name = '{SPREADSHEET_NAME}' and mimeType = 'application/vnd.google-apps.spreadsheet' and trashed = false"
        results = self.drive_service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
        files = results.get('files', [])

        if files:
            spreadsheet_id = files[0]['id']
            st.toast(f"Found existing database: {SPREADSHEET_NAME}", icon="📂")
        else:
            st.toast("Database not found. Creating a new one...", icon="✨")
            spreadsheet_id = self._create_new_db()
        
        return spreadsheet_id

    def _create_new_db(self):
        """Creates a new spreadsheet with the required tabs and headers."""
        spreadsheet = {
            'properties': {'title': SPREADSHEET_NAME},
            'sheets': [
                {'properties': {'title': 'Job Profiles'}},
                {'properties': {'title': 'Jobs Tracker'}}
            ]
        }
        spreadsheet = self.sheets_service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
        spreadsheet_id = spreadsheet.get('spreadsheetId')

        # Initialize Headers
        self._setup_headers(spreadsheet_id)
        
        # Add Sample Data
        self._add_sample_data(spreadsheet_id)
        
        return spreadsheet_id

    def _add_sample_data(self, spreadsheet_id):
        """Adds a sample row to Jobs Tracker to demonstrate the UI."""
        sample_row = [[
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Example Corp",
            "AI Engineer",
            "85",
            "https://docs.google.com/...",
            "Pending"
        ]]
        body = {'values': sample_row}
        self.sheets_service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range="'Jobs Tracker'!A2",
            valueInputOption="RAW",
            body=body
        ).execute()

    def _setup_headers(self, spreadsheet_id):
        """Sets up the column headers for both sheets."""
        headers = {
            'Job Profiles': [["Profile ID", "Title", "Location", "Keywords", "Status"]],
            'Jobs Tracker': [["Date", "Company", "Position", "Match Score", "Resume URL", "Status"]]
        }

        for sheet_name, header_row in headers.items():
            body = {'values': header_row}
            self.sheets_service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=f"'{sheet_name}'!A1",
                valueInputOption="RAW",
                body=body
            ).execute()

    def load_sheet_data(self, spreadsheet_id, sheet_name):
        """Reads data from a specific sheet and returns a Pandas DataFrame."""
        result = self.sheets_service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=f"'{sheet_name}'!A:Z"
        ).execute()
        values = result.get('values', [])

        if not values:
            return pd.DataFrame()
        
        # Convert to DataFrame using first row as header
        df = pd.DataFrame(values[1:], columns=values[0])
        return df

    def sync_data(self, spreadsheet_id, sheet_name, df):
        """Overwrites the sheet with the provided DataFrame."""
        # Convert all columns to string for consistency in Sheets
        data = [df.columns.tolist()] + df.astype(str).values.tolist()
        body = {'values': data}
        
        # Clear existing content first to avoid ghost rows
        self.sheets_service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range=f"'{sheet_name}'!A:Z"
        ).execute()

        # Update with new data
        self.sheets_service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=f"'{sheet_name}'!A1",
            valueInputOption="RAW",
            body=body
        ).execute()
