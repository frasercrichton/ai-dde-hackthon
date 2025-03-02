from email import header
import pytest
import json

from src.pdf_pipeline import PDFProcessor

from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level="DEBUG", catch=True)


class TestPDFPipeline:

    pages = None
    pdf_processor = None
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        logger.info("test")
        self.pdf_processor = PDFProcessor()

        with open("./team-red/test/data/pages.json", "r", encoding="utf-8") as file:
            self.pages = json.load(file)

    def test_get_pages(self):
        pages = self.pdf_processor.get_pages('./team-red/test/data/Leiden Guidelines on the Use of DDE in ICCTs_20220404.pdf')
        assert len(pages) == 55

    def test_remove_page_numbers(self):
        text = self.pdf_processor.remove_page_numbers(str(self.pages))
        assert text == 'gg'

    def test_remove_footnotes(self):

        text_with_foonotes = "Summaries. Practitioners can also consult the KGF's\npublications Prosecution of International Crimes Using DDE in National Courts, DDE in UN\nHuman Rights Fact-Finding Missions, and DDE in International Criminal Law for further\ninsight. Available online from the Leiden DDE Database, these companion documents provide\n2 Braga Da Silva, R., Updating the Authentication of Digital Evidence in the International Criminal Court,\nInternational Criminal Law Review 1-24 (2021) [2].\n3 International Bar Association, Evidence Matters in ICC Trials (August 2016) 19.\n4 Alexa Koenig and others, Digital Fingerprints: Using Electronic Evidence to Advance Prosecutions at the\nInternational Criminal Court (Human Rights Center, UC Berkeley School of Law 2014) fn 2, citing Stephen\nMason, International Electronic Evidence (British Institute of International and Comparative Law 2008)."

        text_without_footnotes = "Summaries. Practitioners can also consult the KGF's\npublications Prosecution of International Crimes Using DDE in National Courts, DDE in UN\nHuman Rights Fact-Finding Missions, and DDE in International Criminal Law for further\ninsight. Available online from the Leiden DDE Database, these companion documents provide"

        text = self.pdf_processor.remove_footnotes(text_with_foonotes)
        print(text)
        assert text == text_without_footnotes

    def test_get_main_content(self):
        pages = self.pdf_processor.get_main_content(pages_array=self.pages)
        print(pages)
        assert len(pages) == 0

    def test_group_text_by_headers(self):
        pages = ['']
        pages = self.pdf_processor.group_text_by_headers(pages_array=pages)
        assert len(pages) == 3

    def test_extract_subsections(self):
        pages = ['']
        pages = self.pdf_processor.extract_subsections(pages_array=pages)
        assert len(pages) == 3

    def test_remove_header_prefix(self):
        header = self.pdf_processor.remove_prefix(regex=PDFProcessor.HEADER_REGEX, text='F. Audio Recordings')
        assert header == 'Audio Recordings'

    def test_remove_subheader_prefix(self):
        header = self.pdf_processor.remove_prefix(regex=PDFProcessor.SUBHEADER_REGEX, text='F.5. Insufficient authentication goes to the weight of audio recordings rather than their admissibility.')
        assert header == 'Insufficient authentication goes to the weight of audio recordings rather than their admissibility.'


