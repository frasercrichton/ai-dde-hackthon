import logging

logger = logging.getLogger(__name__)


class DocumentParser:

    def format_documents_for_chroma(self, documents):
        formatted = []
        for doc in documents:
            metadata = doc.get('metadata', {})

            if 'tags' in metadata and isinstance(metadata['tags'], list):
                for tag in metadata['tags']:
                    metadata[tag] = True
                del metadata['tags']

            formatted.append(
                {
                    **({'metadata': metadata} if metadata is not None else {}),
                    'text': doc['text'],
                }
            )
        return formatted

    def parse_for_chroma(self, documents, embeddings_processor):
        logger.info(f'parsing {len(documents)} documents.')
        # update this to make these unique
        return [
            {
                **document,
                'id': f"{document.get('metadata').get('headers')}-{str(i)}",
                'embedding': embeddings_processor.create_embeddings(document['text']),
            }
            for i, document in enumerate(documents)
        ]
