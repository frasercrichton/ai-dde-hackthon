import json
import re
import sys
from email import header

import pytest
from loguru import logger
from src.pdf_processor import PDFProcessor

logger.remove()
logger.add(sys.stdout, level='DEBUG', catch=True)


class TestPDFPipeline:
    pages = None
    pdf_processor = None
    single_pages = None
    sections = None

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        logger.info('test')
        self.pdf_processor = PDFProcessor()

        with open('./team-red/test/data/pages.json', 'r', encoding='utf-8') as file:
            self.pages = json.load(file)

        with open(
            './team-red/test/data/single_pages.json', 'r', encoding='utf-8'
        ) as file:
            self.single_pages = json.load(file)

        with open('./team-red/test/data/sections.json', 'r', encoding='utf-8') as file:
            self.sections = json.load(file)

    def test_get_pages(self):
        pages = self.pdf_processor.get_pages_from_pdf(
            './team-red/test/data/Leiden Guidelines on the Use of DDE in ICCTs_20220404.pdf'
        )
        print([page[:200] for page in pages[10:26]])
        assert len(pages) == 55

    def test_exclude_cover_page(self):
        pages_array = ['cover', 'table of contents', 'introduction']
        pages = self.pdf_processor.exclude_cover_page(pages_array)
        assert pages == ['table of contents', 'introduction']

    def test_exclude_table_of_contents(self):
        pages_array = ['table of contents', 'introduction with space ']
        pages = self.pdf_processor.exclude_table_of_contents(pages_array)
        assert pages == ['introduction with space '], f' seems wrong {pages}'

    def test_get_leiden_guidelines(self):
        pages_array = [
            'I. Introduction',
            'content',
            'II. The Leiden Guidelines \n text',
            'A.2. A video and its associated transcripts and translations must be seen as forming integral parts of the same evidence.',
        ]
        pages = self.pdf_processor.get_leiden_guidelines(pages_array)

        assert pages == [
            'II. The Leiden Guidelines \n text',
            'A.2. A video and its associated transcripts and translations must be seen as forming integral parts of the same evidence.',
        ]

    def test_get_leiden_guidelines_sections(self):
        shortened_pages = [page[:200] for page in self.single_pages]

        pages = self.pdf_processor.get_leiden_guidelines_sections(shortened_pages)
        print(shortened_pages)
        section_headers = [section.get('section', '') for section in pages]
        section_text = [section.get('text', '') for section in pages]
        assert section_headers == [
            'A. Videos',
            'B. Photographs',
            'C. Aerial and Satellite Images',
        ]
        matches = re.findall(r'\bA\.\d+\.', section_text[0])
        assert matches == [
            'A.4.',
            'A.6.',
            'A.7.',
        ], 'Some A.x. sections are missing or extra ones exist!'

    # def test_get_leiden_guidelines_extract_sub_sections(self):
    #     pages = self.pdf_processor.extract_subsections(self.sections)[0]

    #     section_headers = [
    #         sub_section.get('subheader', '')
    #         for sub_section in pages.get('subsections', '')
    #     ]

    #     section_text = [
    #         sub_section.get('text', '') for sub_section in pages.get('subsections', '')
    #     ]
    #     print(section_text)

    #     assert section_headers == [
    #         'A. When a witness appears on a video that the party intends to tender\ninto evidence, the video should be tendered through the witness during the\nexamination-in-chief and not through the bar table.',
    #         'A.6. Videos can be admitted into evidence if relevance and prima facie\nauthenticity is demonstrated by providing information about the date, the\nlocation, the events depicted, the author, the source,\nChamber in Ntaganda declined to admit a video where the Prosecution was only able to provide\nthe date the video had been broadcast, but not the date the video had been shot.',
    #         'A.7. Video evidence of interviews conducted during an armed conflict by a\nparty to the conflict may not be objective and reliable and therefore low\nprobative value may be attached to the video.',
    #         None,
    #     ]

        # matches = re.findall(r'\bA\.\d+\.', section_text[0])
        # assert matches == ["A.4.", "A.6.", "A.7."], (
        #     "Some A.x. sections are missing or extra ones exist!"
        # )

    # *****

    def test_remove_page_numbers(self):
        # text = self.pdf_processor.remove_page_numbers(str(self.pages[4]))
        text = self.pdf_processor.remove_page_numbers(
            'Criminal Court (Human Rights Center, UC Berkeley School of Law 2014) fn 2, citing Stephen\nMason, International Electronic Evidence (British Institute of International and Comparative Law 2008).\n4'
        )
        print(text)
        # text.endswith('\n4'):
        assert (
            text
            == 'Criminal Court (Human Rights Center, UC Berkeley School of Law 2014) fn 2, citing Stephen\nMason, International Electronic Evidence (British Institute of International and Comparative Law 2008).'
        )

    def test_remove_footnotes(self):

        text_with_footnotes = "Summaries. Practitioners can also consult the KGF's\npublications Prosecution of International Crimes Using DDE in National Courts, DDE in UN\nHuman Rights Fact-Finding Missions, and DDE in International Criminal Law for further\ninsight. Available online from the Leiden DDE Database, these companion documents provide\n2 Braga Da Silva, R., Updating the Authentication of Digital Evidence in the International Criminal Court,\nInternational Criminal Law Review 1-24 (2021) [2].\n3 International Bar Association, Evidence Matters in ICC Trials (August 2016) 19.\n4 Alexa Koenig and others, Digital Fingerprints: Using Electronic Evidence to Advance Prosecutions at the\nInternational Criminal Court (Human Rights Center, UC Berkeley School of Law 2014) fn 2, citing Stephen\nMason, International Electronic Evidence (British Institute of International and Comparative Law 2008)."

        expected_text_without_footnotes = "Summaries. Practitioners can also consult the KGF's\npublications Prosecution of International Crimes Using DDE in National Courts, DDE in UN\nHuman Rights Fact-Finding Missions, and DDE in International Criminal Law for further\ninsight. Available online from the Leiden DDE Database, these companion documents provide"

        text = self.pdf_processor.remove_footnotes(text_with_footnotes)
        assert text == expected_text_without_footnotes

    def test_remove_header_prefix(self):
        header = self.pdf_processor.remove_prefix(
            regex=PDFProcessor.HEADER_REGEX, text='F. Audio Recordings'
        )
        assert header == 'Audio Recordings'

    def test_remove_subheader_prefix(self):
        header = self.pdf_processor.remove_prefix(
            regex=PDFProcessor.SUBHEADER_REGEX,
            text='F.5. Insufficient authentication goes to the weight of audio recordings rather than their admissibility.',
        )
        assert (
            header
            == 'Insufficient authentication goes to the weight of audio recordings rather than their admissibility.'
        )
