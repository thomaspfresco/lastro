'''
/dataGen/queries.py
-> define all the methods for user prompt handle/process
'''

from database.setup import db, executeQueriesSQL, recordInteraction
from database.models import serializeProjectMinimal
from ai.llm.setup import queryLLM
from dataGen.queryFallback import applyFallback
import requests
import random

# ==================================================
# methods
# ==================================================

def detectContextualIntent(prompt):
    """
    Use the router model to detect if the user prompt contains contextual references.
    Returns tuple: (field, operator) where:
    - field: 'category', 'author', 'location', 'date', or None
    - operator: 'equal', 'different', or None
    """
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'context-router-lastro',
                'prompt': prompt,
                'stream': False
            },
            timeout=10
        )

        if response.status_code == 200:
            output = response.json().get('response', '').strip().lower()
            print(f"DEBUG: Router model output: '{output}'")

            # Parse output format: "field-operator"
            if '-' in output:
                parts = output.split('-')
                if len(parts) == 2:
                    field, operator = parts

                    # Validate field
                    if field in ['category', 'author', 'location', 'date', 'instruments']:
                        # Validate operator
                        if operator in ['equal', 'different']:
                            return (field, operator)
                    elif field == 'none' and operator == 'none':
                        return (None, None)

            print(f"DEBUG: Router model output invalid format: '{output}'")
            return (None, None)
    except Exception as e:
        print(f"DEBUG: Router model error: {e}")
        return (None, None)

    return (None, None)

def buildContextualQuery(contextType, operator, project):
    """
    Build a SQL query directly based on the context type, operator, and project data.
    Returns a dict with query, description, and field info.

    Args:
        contextType: 'category', 'author', 'location', 'date', or 'instruments'
        operator: 'equal' or 'different'
        project: Project object with the current project data
    """
    # Extract year from date (handle both string and datetime objects)
    year = str(project.date.year) if hasattr(project.date, 'year') else str(project.date)[:4]

    if operator == 'equal':
        queries = {
            'category': {
                'query': f"SELECT * FROM projects WHERE category LIKE '%{project.category}%';",
                'description': f"Projetos do género {project.category}",
                'field': 'category',
                'value': project.category
            },
            'author': {
                'query': f"SELECT * FROM projects WHERE author LIKE '%{project.author}%';",
                'description': f"Projetos de {project.author}",
                'field': 'author',
                'value': project.author
            },
            'location': {
                'query': f"SELECT * FROM projects WHERE location LIKE '%{project.location}%';",
                'description': f"Projetos em {project.location}",
                'field': 'location',
                'value': project.location
            },
            'date': {
                'query': f"SELECT * FROM projects WHERE date LIKE '%{year}%';",
                'description': f"Projetos de {year}",
                'field': 'date',
                'value': year
            },
            'instruments': {
                'query': f"SELECT * FROM projects WHERE instruments LIKE '%{project.instruments}%';",
                'description': f"Projetos com {project.instruments}",
                'field': 'instruments',
                'value': project.instruments
            }
        }
    else:  # operator == 'different'
        queries = {
            'category': {
                'query': f"SELECT * FROM projects WHERE category NOT LIKE '%{project.category}%';",
                'description': f"Projetos de género diferente de {project.category}",
                'field': 'category',
                'value': project.category
            },
            'author': {
                'query': f"SELECT * FROM projects WHERE author NOT LIKE '%{project.author}%';",
                'description': f"Projetos de outros autores (não {project.author})",
                'field': 'author',
                'value': project.author
            },
            'location': {
                'query': f"SELECT * FROM projects WHERE location NOT LIKE '%{project.location}%';",
                'description': f"Projetos de outras localizações (não {project.location})",
                'field': 'location',
                'value': project.location
            },
            'date': {
                'query': f"SELECT * FROM projects WHERE date NOT LIKE '%{year}%';",
                'description': f"Projetos de outros anos (não {year})",
                'field': 'date',
                'value': year
            },
            'instruments': {
                'query': f"SELECT * FROM projects WHERE instruments NOT LIKE '%{project.instruments}%';",
                'description': f"Projetos com outros instrumentos (não {project.instruments})",
                'field': 'instruments',
                'value': project.instruments
            }
        }

    return queries.get(contextType)

def stripQueries(text):

    result = {
        "queries": [],
        "descriptions": [],
        "results": []
    }

    lines = text.strip().split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # isolate query
        if line.startswith('QUERY:'):
            query = line[6:].strip()
            if not query.endswith(';'):
                query += ';'
            result["queries"].append(query)        
        
        # isolate description
        elif line.startswith('DESC:'):
            result["descriptions"].append(line[5:].strip())
        
    return result

# ==================================================
# main
# ==================================================

def handleQuery(data):
    print(data)

    currentPrompt = data["currentPrompt"]
    currentProjectId = data.get("currentProjectId")

    contextProject = None
    contextType = None
    contextOperator = None

    # Check if user is on a project page and uses contextual references
    if currentProjectId:
        contextType, contextOperator = detectContextualIntent(currentPrompt)

    # If contextual intent detected, build query directly in Python (fast path)
    if contextType and contextOperator:
        from database.models import Project
        project = Project.query.get(currentProjectId)

        if project:
            print(f"DEBUG: Contextual intent '{contextType}-{contextOperator}' detected! Building query directly.")

            contextProject = {
                "title": project.title,
                "author": project.author,
                "id": project.id
            }

            # Build SQL query directly without LLM
            queryInfo = buildContextualQuery(contextType, contextOperator, project)

            result = {
                "queries": [queryInfo['query']],
                "descriptions": [queryInfo['description']],
            }

            rawResults = executeQueriesSQL(result["queries"])

            # Check if any results were found
            has_results = any(len(queryResult) > 0 for queryResult in rawResults)

            # Apply fallback system if no results
            if not has_results:
                print("DEBUG: No contextual results found - applying fallback system")
                fallback_result = applyFallback(result["queries"])

                # Update result with fallback data
                result["queries"] = fallback_result["queries"]
                result["descriptions"] = fallback_result["descriptions"]
                rawResults = fallback_result["results"]
                result["fallback_applied"] = True
                result["fallback_level"] = fallback_result["fallback_level"]
            else:
                result["fallback_applied"] = False

            # Shuffle results before serialization
            for queryResult in rawResults:
                random.shuffle(queryResult)

            result["results"] = [
                [serializeProjectMinimal(p) for p in queryResult]
                for queryResult in rawResults
            ]
            result["contextProject"] = contextProject

            return result

    # Default path: Use LLM for normal queries
    print("DEBUG: Using LLM for query generation")
    modelOutput = queryLLM(currentPrompt, data["previousQueries"])
    print(modelOutput)

    #interactionId = recordInteraction(data,modelOutput)

    result = stripQueries(modelOutput)
    rawResults = executeQueriesSQL(result["queries"])

    # Check if any results were found
    has_results = any(len(queryResult) > 0 for queryResult in rawResults)

    # Apply fallback system if no results
    if not has_results:
        print("DEBUG: No results found - applying fallback system")
        fallback_result = applyFallback(result["queries"])

        # Update result with fallback data
        result["queries"] = fallback_result["queries"]
        result["descriptions"] = fallback_result["descriptions"]
        rawResults = fallback_result["results"]
        result["fallback_applied"] = True
        result["fallback_level"] = fallback_result["fallback_level"]
    else:
        result["fallback_applied"] = False

        # Check if we should add keyword expansion
        # Count total projects and main terms
        from dataGen.queryFallback import extractTermsFromQueries, buildMultiTermFallback, hasDuplicateProjects

        total_projects = sum(len(queryResult) for queryResult in rawResults)
        extracted = extractTermsFromQueries(result["queries"])
        main_terms = extracted['terms']
        date_filter = extracted['dateTerm']

        print(f"DEBUG: Total projects: {total_projects}, Main terms count: {len(main_terms)}")

        # If 2 or fewer main terms and less than 10 total projects, add keyword search
        if len(main_terms) <= 2 and len(main_terms) > 0 and total_projects < 10:
            print(f"DEBUG: Checking keyword expansion group for terms: {main_terms}")

            # Build keyword search with OR joining all terms
            keyword_query_info = buildMultiTermFallback(main_terms, date_filter)
            keyword_results = executeQueriesSQL([keyword_query_info['query']])[0]

            # Only add if we got results from keyword search and they're not duplicates
            if keyword_results and len(keyword_results) > 0:
                # Check if keyword results are duplicate of existing results
                existingGroups = [{'results': r} for r in rawResults]
                isDuplicate = hasDuplicateProjects(keyword_results, existingGroups)

                if isDuplicate:
                    print(f"DEBUG: Skipping keyword expansion - duplicate projects ({len(keyword_results)} projects)")
                else:
                    print(f"DEBUG: Adding keyword expansion with {len(keyword_results)} additional projects")
                    result["queries"].append(keyword_query_info['query'])
                    result["descriptions"].append(keyword_query_info['description'])
                    rawResults.append(keyword_results)

    # Shuffle results before serialization
    for queryResult in rawResults:
        random.shuffle(queryResult)

    # Minimize payload for explore results
    result["results"] = [
        [serializeProjectMinimal(project) for project in queryResult]
        for queryResult in rawResults
    ]

    #print(result)

    return result