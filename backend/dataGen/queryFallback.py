'''
/dataGen/queryFallback.py
-> Multi-level fallback system for handling queries with no results
'''

import re

# ==================================================
# Constants
# ==================================================

# Columns to exclude from single-term wildcard search
EXCLUDED_COLUMNS = {'date', 'keywords', 'infoPool', 'id', 'link', 'created_at'}

# All searchable columns in the projects table
SEARCHABLE_COLUMNS = [
    'title', 'author', 'category', 'direction', 'sound',
    'production', 'support', 'assistance', 'research',
    'location', 'instruments'
]

# ==================================================
# Term Extraction Methods
# ==================================================

def extractTermsFromQuery(query):
    """
    Extract search terms wrapped in '% %' from SQL query.
    Also detect if there's a date filter.

    Args:
        query: SQL query string

    Returns:
        dict: {
            'terms': [list of search terms found between % %],
            'dateTerm': str or None (year found in date filter),
            'hasDateFilter': bool
        }
    """
    result = {
        'terms': [],
        'dateTerm': None,
        'hasDateFilter': False
    }

    # Extract all terms between LIKE '%term%'
    # Pattern: LIKE '%something%' or LIKE "%something%"
    termPattern = r"LIKE\s+['\"]%([^%]+?)%['\"]"
    matches = re.findall(termPattern, query, re.IGNORECASE)

    # Check if any term is in a date column
    datePattern = r"date\s+LIKE\s+['\"]%(\d{4})[^'\"]*%['\"]"
    dateMatch = re.search(datePattern, query, re.IGNORECASE)

    if dateMatch:
        result['dateTerm'] = dateMatch.group(1)
        result['hasDateFilter'] = True

    # Collect all non-date terms
    for match in matches:
        term = match.strip()
        # Skip if it's a year (4 digits)
        if term and not re.match(r'^\d{4}$', term):
            if term not in result['terms']:
                result['terms'].append(term)

    return result

def extractTermsFromQueries(queries):
    """
    Extract all unique terms from a list of queries.

    Args:
        queries: List of SQL query strings

    Returns:
        dict: Combined extraction results from all queries
    """
    allTerms = []
    dateTerm = None
    hasDateFilter = False

    for query in queries:
        extracted = extractTermsFromQuery(query)
        allTerms.extend(extracted['terms'])

        if extracted['dateTerm']:
            dateTerm = extracted['dateTerm']
            hasDateFilter = True

    # Remove duplicates while preserving order
    uniqueTerms = []
    for term in allTerms:
        if term not in uniqueTerms:
            uniqueTerms.append(term)

    return {
        'terms': uniqueTerms,
        'dateTerm': dateTerm,
        'hasDateFilter': hasDateFilter
    }

# ==================================================
# Fallback Level Methods
# ==================================================

def buildSingleTermFallback(term, dateFilter=None):
    """
    Level 1 Fallback: Single non-date term found.
    Try every searchable column (except excluded ones) and group results.

    Args:
        term: The single search term to look for
        dateFilter: Optional year/date to filter by

    Returns:
        list: [{
            'query': SQL query string,
            'description': Description for this group,
            'column': Column name being searched
        }]
    """
    queries = []

    for column in SEARCHABLE_COLUMNS:
        baseQuery = f"SELECT * FROM projects WHERE {column} LIKE '%{term}%'"

        # Add date filter if provided
        if dateFilter:
            baseQuery += f" AND date LIKE '%{dateFilter}%'"

        baseQuery += ";"

        # Build description based on column
        columnDescriptions = {
            'title': f"Projetos com '{term}' no título",
            'author': f"Projetos de autores relacionados a '{term}'",
            'category': f"Projetos do género '{term}'",
            'direction': f"Projetos com direção de '{term}'",
            'sound': f"Projetos com som de '{term}'",
            'production': f"Projetos com produção de '{term}'",
            'support': f"Projetos com apoio de '{term}'",
            'assistance': f"Projetos com assistência de '{term}'",
            'research': f"Projetos com pesquisa de '{term}'",
            'location': f"Projetos em localizações relacionadas a '{term}'",
            'instruments': f"Projetos com instrumentos '{term}'"
        }

        queries.append({
            'query': baseQuery,
            'description': columnDescriptions.get(column, f"Projetos com '{term}' em {column}"),
            'column': column
        })

    return queries

def buildKeywordsFallback(term, dateFilter=None):
    """
    Level 2 Fallback: Search in keywords column.

    Args:
        term: The search term
        dateFilter: Optional year/date to filter by

    Returns:
        dict: Single query for keywords search
    """
    query = f"SELECT * FROM projects WHERE keywords LIKE '%{term}%'"

    if dateFilter:
        query += f" AND date LIKE '%{dateFilter}%'"

    query += ";"

    return {
        'query': query,
        'description': f"Outros projetos relacionados a '{term}'",
        'column': 'keywords'
    }

def buildMultiTermFallback(terms, dateFilter=None):
    """
    Level 3 Fallback: Multiple non-date terms found.
    Search keywords column with OR joining all terms.

    Args:
        terms: List of search terms
        dateFilter: Optional year/date to filter by

    Returns:
        dict: Query joining all terms with OR
    """
    # Build OR conditions for all terms
    conditions = [f"keywords LIKE '%{term}%'" for term in terms]
    whereClause = " OR ".join(conditions)

    query = f"SELECT * FROM projects WHERE ({whereClause})"

    if dateFilter:
        query += f" AND date LIKE '%{dateFilter}%'"

    query += ";"

    termsStr = "', '".join(terms)
    return {
        'query': query,
        'description': f"Projetos relacionados a '{termsStr}'",
        'column': 'keywords'
    }

def buildSplitWordsFallback(term, dateFilter=None, maxWords=5):
    """
    Level 2.5 Fallback: Split multi-word term into individual words.
    Search keywords with OR joining individual words (limit to maxWords).

    Args:
        term: Multi-word search term to split
        dateFilter: Optional year/date to filter by
        maxWords: Maximum number of words to use (default 5)

    Returns:
        dict: Query with split words joined by OR, or None if single word
    """
    # Split by spaces and filter out stop words/very short words
    words = [w.strip() for w in term.split() if len(w.strip()) > 2]

    # Only use this fallback if we have multiple meaningful words
    if len(words) <= 1:
        return None

    # Limit to maxWords
    words = words[:maxWords]

    # Build OR conditions for all words
    conditions = [f"keywords LIKE '%{word}%'" for word in words]
    whereClause = " OR ".join(conditions)

    query = f"SELECT * FROM projects WHERE ({whereClause})"

    if dateFilter:
        query += f" AND date LIKE '%{dateFilter}%'"

    query += ";"

    wordsStr = "', '".join(words)
    return {
        'query': query,
        'description': f"Projetos relacionados a '{wordsStr}'",
        'column': 'keywords_split',
        'words': words
    }

def buildRandomFallback():
    """
    Final Fallback: Return 100 random projects.

    Returns:
        dict: Query for random projects
    """
    return {
        'query': "SELECT * FROM projects ORDER BY RANDOM() LIMIT 100;",
        'description': "Sem potenciais resultados para a sua pesquisa. Continue a Explorar!",
        'column': 'random'
    }

# ==================================================
# Helper Functions
# ==================================================

def extractProjectIds(results):
    """
    Extract project IDs from a result set.

    Args:
        results: List of project dictionaries

    Returns:
        set: Set of project IDs
    """
    if not results:
        return set()
    return {project.get('id') for project in results if project.get('id') is not None}

def hasDuplicateProjects(newResults, existingGroups):
    """
    Check if newResults contains exactly the same projects as any existing group.

    Args:
        newResults: List of projects to check
        existingGroups: List of existing group dictionaries with 'results' key

    Returns:
        bool: True if an identical set exists, False otherwise
    """
    newIds = extractProjectIds(newResults)

    if not newIds:
        return False

    for group in existingGroups:
        existingIds = extractProjectIds(group['results'])
        if newIds == existingIds:
            return True

    return False

# ==================================================
# Main Fallback Orchestrator
# ==================================================

def applyFallback(originalQueries):
    """
    Apply multi-level fallback based on terms extracted from queries.

    Args:
        originalQueries: List of SQL queries that returned no results

    Returns:
        dict: {
            'queries': [list of fallback queries],
            'descriptions': [list of descriptions],
            'results': [list of result arrays],
            'fallback_level': str
        }
    """
    from database.setup import executeQueriesSQL

    # Extract terms from the original queries
    extracted = extractTermsFromQueries(originalQueries)
    terms = extracted['terms']
    dateFilter = extracted['dateTerm']

    print(f"DEBUG FALLBACK: Extracted terms: {terms}")
    print(f"DEBUG FALLBACK: Date filter: {dateFilter}")

    nonDateCount = len(terms)

    # LEVEL 1: Single non-date term - search all columns
    if nonDateCount == 1:
        term = terms[0]
        print(f"DEBUG FALLBACK: Single term '{term}' - searching all columns")

        fallbackQueries = buildSingleTermFallback(term, dateFilter)

        # Execute and collect results
        allResults = executeQueriesSQL([q['query'] for q in fallbackQueries])

        # Filter out empty results and keep only groups with results
        # Also check for duplicate project sets
        validGroups = []
        for i, res in enumerate(allResults):
            if res and len(res) > 0:
                # Only add if this group doesn't have the same projects as an existing group
                isDuplicate = hasDuplicateProjects(res, validGroups)
                if isDuplicate:
                    print(f"DEBUG FALLBACK: Skipping duplicate group for column '{fallbackQueries[i]['column']}' with {len(res)} projects")
                else:
                    print(f"DEBUG FALLBACK: Adding group for column '{fallbackQueries[i]['column']}' with {len(res)} projects")
                    validGroups.append({
                        'query': fallbackQueries[i]['query'],
                        'description': fallbackQueries[i]['description'],
                        'results': res
                    })

        print(f"DEBUG FALLBACK: Found {len(validGroups)} unique groups with results")

        # Always check keywords fallback, regardless of how many groups we have
        print(f"DEBUG FALLBACK: Checking keywords fallback (currently have {len(validGroups)} groups)")
        keywordsQuery = buildKeywordsFallback(term, dateFilter)
        keywordsResults = executeQueriesSQL([keywordsQuery['query']])[0]

        if keywordsResults and len(keywordsResults) > 0:
            # Only add if not duplicate
            isDuplicate = hasDuplicateProjects(keywordsResults, validGroups)
            if isDuplicate:
                print(f"DEBUG FALLBACK: Skipping keywords fallback - duplicate projects ({len(keywordsResults)} projects)")
            else:
                print(f"DEBUG FALLBACK: Adding keywords fallback with {len(keywordsResults)} projects")
                validGroups.append({
                    'query': keywordsQuery['query'],
                    'description': keywordsQuery['description'],
                    'results': keywordsResults
                })
        else:
            print(f"DEBUG FALLBACK: Keywords fallback returned no results")

        # If still no results, try splitting multi-word terms
        if not validGroups:
            print(f"DEBUG FALLBACK: No results found - trying split words fallback")
            splitWordsQuery = buildSplitWordsFallback(term, dateFilter)

            if splitWordsQuery:
                print(f"DEBUG FALLBACK: Split '{term}' into words: {splitWordsQuery['words']}")
                splitWordsResults = executeQueriesSQL([splitWordsQuery['query']])[0]

                if splitWordsResults and len(splitWordsResults) > 0:
                    print(f"DEBUG FALLBACK: Split words fallback found {len(splitWordsResults)} projects")
                    validGroups.append({
                        'query': splitWordsQuery['query'],
                        'description': splitWordsQuery['description'],
                        'results': splitWordsResults
                    })
                else:
                    print(f"DEBUG FALLBACK: Split words fallback returned no results")
            else:
                print(f"DEBUG FALLBACK: Term '{term}' is single word - skipping split words fallback")

        # If still no results, go to final fallback
        if not validGroups:
            print(f"DEBUG FALLBACK: No results found - returning random projects")
            randomQuery = buildRandomFallback()
            randomResults = executeQueriesSQL([randomQuery['query']])[0]

            return {
                'queries': [randomQuery['query']],
                'descriptions': [randomQuery['description']],
                'results': [randomResults],
                'fallback_level': 'random'
            }

        return {
            'queries': [g['query'] for g in validGroups],
            'descriptions': [g['description'] for g in validGroups],
            'results': [g['results'] for g in validGroups],
            'fallback_level': 'single_term_multi_column'
        }

    # LEVEL 2: Multiple non-date terms - search keywords with OR
    elif nonDateCount > 1:
        print(f"DEBUG FALLBACK: Multiple terms {terms} - searching keywords with OR")

        multiTermQuery = buildMultiTermFallback(terms, dateFilter)
        multiTermResults = executeQueriesSQL([multiTermQuery['query']])[0]

        if multiTermResults and len(multiTermResults) > 0:
            return {
                'queries': [multiTermQuery['query']],
                'descriptions': [multiTermQuery['description']],
                'results': [multiTermResults],
                'fallback_level': 'multi_term_keywords'
            }

        # No results - go to final fallback
        print(f"DEBUG FALLBACK: No results found - returning random projects")
        randomQuery = buildRandomFallback()
        randomResults = executeQueriesSQL([randomQuery['query']])[0]

        return {
            'queries': [randomQuery['query']],
            'descriptions': [randomQuery['description']],
            'results': [randomResults],
            'fallback_level': 'random'
        }

    # LEVEL 3: No meaningful terms - return random
    else:
        print(f"DEBUG FALLBACK: No terms found - returning random projects")
        randomQuery = buildRandomFallback()
        randomResults = executeQueriesSQL([randomQuery['query']])[0]

        return {
            'queries': [randomQuery['query']],
            'descriptions': [randomQuery['description']],
            'results': [randomResults],
            'fallback_level': 'random'
        }
