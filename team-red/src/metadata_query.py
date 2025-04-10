class MetadataQuery:
    def createFilters(self, headers: list = None, tags: list = None, context=None):
        filter_dict = {'$or': []}
        or_filter = filter_dict['$or']

        if headers:
            if (tags and len(headers) == 1) or len(headers) > 1:
                or_filter.append({'headers': {'$in': headers}})
            else:
                del filter_dict['$or']
                filter_dict['headers'] = headers[0]

        if tags:
            if len(tags) > 1 or (len(tags) == 1 and headers):
                for tag in tags:
                    or_filter.append({tag: True})
            else:
                del filter_dict['$or']
                filter_dict[tags[0]] = True
             
        return filter_dict
