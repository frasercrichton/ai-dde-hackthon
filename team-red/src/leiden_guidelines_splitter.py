from langchain_text_splitters import RecursiveCharacterTextSplitter

class LeidenGuidelinesSplitter(RecursiveCharacterTextSplitter):
    # Precise retrieval (fact lookup)	500-800	~75-120 tokens	Good for finding specific definitions or rules
    # Balanced approach	800-1200	~120-180 tokens	Works well for most legal documents
    # Context-heavy (complex analysis)	1200-2000	~180-300 tokens	For sections needing full context
    def __init__(self):
        super().__init__(
            chunk_size=1200,
            chunk_overlap=0,
            separators=self._get_legal_separators(),
            keep_separator=True,
            is_separator_regex=True,
        )

    def _get_legal_separators(self):
        return [
            '\n\n',  # best: split at paragraph boundaries
            '\n',  # next best: line breaks
            '. ',  # sentence boundary
            ' ',  # fallback to words
            '',  # character-level if needed
        ]
