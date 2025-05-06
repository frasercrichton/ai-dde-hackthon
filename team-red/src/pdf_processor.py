from ast import keyword
import pdfplumber
import re

# pymupdf


class PDFProcessor:
    HEADER_REGEX = r'^[A-Z]\.\s'
    SUBHEADER_REGEX = r'^[A-Z]\.\d\.\s'

    pdf_path = None

    def __init__(self, pdf_path=None):
        self.pdf_path = pdf_path

    # 1) get pages
    def get_pages_from_pdf(self, pdf_path):
        pages = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                pages.append(page.extract_text())
        return pages

    # 2) exclude the cover
    def remove_cover_page(self, pages_array):
        filtered_pages = []

        for page_number, text in enumerate(pages_array):
            if page_number != 0:
                filtered_pages.append(text)

        return filtered_pages

    # 3) exclude table of contents
    def remove_table_of_contents(self, pages_array):
        filtered_pages = []
        # TODO should really check for format
        for page_number, text in enumerate(pages_array):
            if page_number != 0:
                filtered_pages.append(text)

        return filtered_pages

    # 4) get Leiden Guidelines
    def get_guidelines(self, pages):
        # II. The Leiden Guidelines
        # •	^ → Matches the start of the string (optional, remove if matching anywhere).
        # •	II → Matches the literal “II”.
        # •	\. → Matches the dot (.) after “II” (escaped with \ since . is a special character in regex).
        # •	  (space) → Matches the space after the dot.
        # •	The Leiden Guidelines → Matches the exact phrase.
        # •	\s* → Matches zero or more trailing spaces (optional).

        leiden_guidelines_regex = r'^II\. The Leiden Guidelines\s*'
        # get all pages subsequent to
        start_index = next(
            (
                i
                for i, page in enumerate(pages)
                if re.search(leiden_guidelines_regex, page, re.MULTILINE)
            ),
            None,
        )

        if start_index is not None:
            result = pages[start_index:]
        else:
            result = []  # No match found, return empty list

        return result

    # 6) test_get_leiden_guidelines_sections
    def get_top_level_sections(self, pages):

        section_pattern = re.compile(r'^([A-Z])\.[^\d].*?(?:\n|$)', re.MULTILINE)

        sections = []
        current_section = None

        for page in pages:
            matches = list(section_pattern.finditer(page))
            if matches:
                for match in matches:
                    if current_section:
                        # Store previous section before starting a new one
                        sections.append(current_section)

                    # Start a new section
                    section_title = match.group(0).strip()  # Capture full section title
                    section_text = page[
                        match.end() :
                    ].strip()  # Capture ALL text after the title
                    current_section = {
                        'section_title': self.remove_prefix(
                            regex=PDFProcessor.HEADER_REGEX, text=section_title
                        ),
                        'text': section_text,
                    }
            else:
                # Append additional text to the current section
                if current_section:
                    current_section['text'] += '\n' + page.strip()

        # Append the last section after looping
        if current_section:
            sections.append(current_section)

        return sections

    # 7) test_get_leiden_guidelines_sub_sections
    def get_subsections(self, grouped_data):
        subsection_pattern = r'(?P<subheader>[A-Z]\.\d+\.\s.*?\.)'  # Refined pattern
        results = []

        for group in grouped_data:
            header = group['section_title']
            text = group['text']

            subsections = []
            last_pos = 0

            matches = list(re.finditer(subsection_pattern, text, re.DOTALL))
            # print(f'matches {matches}')
            for idx, match in enumerate(matches):
                subheader = match.group('subheader').strip()
                start_idx = match.end()
                end_idx = matches[idx + 1].start() if idx + 1 < len(matches) else None
                subsection_text = (
                    text[start_idx:end_idx].strip()
                    if end_idx
                    else text[start_idx:].strip()
                )

                subsections.append(
                    {
                        'subheader': self.remove_prefix(
                            regex=PDFProcessor.SUBHEADER_REGEX, text=subheader
                        ),
                        'text': subsection_text,
                    }
                )
                last_pos = match.end()

            # Handle any remaining text that does not belong to a subsection
            if last_pos < len(text.strip()):
                remaining_text = text[last_pos:].strip()
                # print(remaining_text)
                if remaining_text:
                    subsections.append({'subheader': None, 'text': remaining_text})

            results.append({'header': header, 'subsections': subsections})

        return results

    def extract_footnotes(self, text):

        pattern = r'(?m)^(\d+)\s+(.*?)(?=\n\d+\s|\Z)'

        # Extract footnotes into dict
        footnotes = {}
        for match in re.finditer(pattern, text, re.DOTALL):
            number = int(match.group(1))
            content = match.group(2).strip()
            footnotes[number] = content

        # Remove footnotes from the original text
        clean_text = re.sub(pattern, '', text, flags=re.DOTALL)

        # Final structure
        result = {'text': clean_text.strip(), 'footnotes': footnotes}

        return result

    def remove_page_numbers(self, text):
        """
        Removes page numbers that appear as '\n4', '\n5', etc.
        """
        PAGE_NUMBERS = r'\n\d+$'

        clean_text = re.sub(PAGE_NUMBERS, '', text, flags=re.MULTILINE)
        return clean_text
        # extrapolations_pattern = (
        #     r'^\s*THE\s+EXTRAPOLATIONS\s+DOCUMENT(?:\s*\n\s*|\s+)*\d+\s*$'
        # )

        # dangling_page_number = r'\n\d+\s*$'
        # # r"^\s*\d+\s*$"
        # clean_text = re.sub(extrapolations_pattern, '', text, flags=re.MULTILINE)
        # return re.sub(dangling_page_number, '', clean_text, flags=re.MULTILINE)

    def get_keywords(self, text):
        keyword_block = re.sub(r'^Keywords\s*(?:\n|$)', '', text)
       
        print(keyword_block)
        keywords = keyword_block.split(';')
        return {'keywords': keywords}

    def remove_prefix(self, regex, text):
        if text is not None:
            return re.sub(regex, '', text)
