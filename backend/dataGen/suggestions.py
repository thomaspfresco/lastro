'''
/dataGen/suggestions.py
-> generate suggestions based on a project/video properties
'''

from database.setup import executeQueriesSQL
from dataGen.descriptions import describeDirectSuggestion, describeDisruptiveSuggestion
import random
import asyncio

# ignore when splitting by space
wordsToIgnore = [
    "de", "da", "do", "das", "dos",
    "e", "a", "o", "as", "os",
    "em", "no", "na", "nos", "nas",
    "um", "uma", "uns", "umas",
    "que", "não", "eu", "tu", "ele", "ela", "nós", "vós", "eles", "elas",
    "me", "te", "se", "nos", "vos",
    "meu", "minha", "teu", "tua", "seu", "sua",
    "este", "esta", "esse", "essa", "aquele", "aquela",
    "com", "sem", "para", "por", "sobre", "sob",
    "mas", "mais", "menos", "muito", "pouco",
    "já", "ainda", "sempre", "nunca",
    # Verb "ser"
    "sou", "és", "é", "somos", "sois", "são",
    "era", "eras", "éramos", "éreis", "eram",
    "fui", "foi", "fomos", "fostes", "foram",
    "serei", "será", "seremos", "sereis", "serão",
    "seria", "serias", "seríamos", "seríeis", "seriam",
    "seja", "sejas", "sejamos", "sejais", "sejam",
    "fosse", "fosses", "fôssemos", "fôsseis", "fossem",
    "for", "fores", "formos", "fordes", "forem",
    "ser", "sendo", "sido",
    # Verb "estar"
    "estou", "estás", "está", "estamos", "estais", "estão",
    "estava", "estavas", "estávamos", "estáveis", "estavam",
    "estive", "esteve", "estivemos", "estivestes", "estiveram",
    "estarei", "estará", "estaremos", "estareis", "estarão",
    "estaria", "estarias", "estaríamos", "estaríeis", "estariam",
    "esteja", "estejas", "estejamos", "estejais", "estejam",
    "estivesse", "estivesses", "estivéssemos", "estivésseis", "estivessem",
    "estiver", "estiveres", "estivermos", "estiverdes", "estiverem",
    "estar", "estando", "estado",
]

# 3 direct suggestions, different probabilities
nDirect = 3
directOptions = [
    {"field": "title", "p": 80},
    {"field": "author", "p": 90},
    {"field": "category", "p": 75},
    {"field": "date", "p": 90},
    {"field": "direction", "p": 25},
    {"field": "sound", "p": 5},
    {"field": "production", "p": 5},
    {"field": "support", "p": 5},
    {"field": "assistance", "p": 2},
    {"field": "research", "p": 2},
    {"field": "location", "p": 90},
    {"field": "instruments", "p": 80},
    {"field": "keywords", "p": 50}
]

# 2 diruptive suggestions, same probability
nDisruptive = 2
disruptiveOptions = [
    {"matchField": "author", "excludeField": "category"},
    {"matchField": "author", "excludeField": "location"},
    {"matchField": "author", "excludeField": "instruments"},
    {"matchField": "category", "excludeField": "author"},
    {"matchField": "category", "excludeField": "location"},
    {"matchField": "category", "excludeField": "instruments"},
    {"matchField": "location", "excludeField": "author"},
    {"matchField": "location", "excludeField": "category"},
    {"matchField": "location", "excludeField": "instruments"},
    {"matchField": "instruments", "excludeField": "author"},
    {"matchField": "instruments", "excludeField": "location"},
    {"matchField": "instruments", "excludeField": "category"},
    {"matchField": "author", "excludeField": "date"},
    {"matchField": "date", "excludeField": "author"},
]

# ==================================================
# methods
# ==================================================

def hasFieldData(field, project):
    """
    Quickly check if a field has usable data without executing queries.
    Returns True if the field exists and has non-empty value.
    """
    value = getattr(project, field, None)
    if not value:
        return False
    if isinstance(value, str) and value.strip() == "":
        return False
    return True

async def buildQueryAndExecute(field, project):
    """
    Build and execute a SQL query for a given field and project.
    Returns a tuple: (query_string, results_array)

    This avoids double execution by running the query once and returning both
    the query string (for description generation) and results.

    Strategy:
    1. If field is "date" -> match by year only using LIKE 'year-%'
    2. If value contains ", " -> split and use OR
    3. Otherwise -> try exact LIKE match
    4. If no results -> split by space and use OR (ignoring insignificant words)

    project: The project object to build the query from
    field: The field name to query on
    """
    value = getattr(project, field, None)

    if not value:
        return None, None

    # Build exclusion clause to exclude current project
    exclude_clause = f" AND id != {project.id}"

    # Special handling for date field
    if field == "date":
        try:
            year = value.strftime('%Y-%m-%d').split('-')[0]
            query = f"SELECT * FROM projects WHERE date LIKE '{year}-%'{exclude_clause}"
            #print(f"[Query - date year] {query}")
            results = await asyncio.to_thread(executeQueriesSQL, [query])
            return query, (results[0] if results else None)
        except:
            return None, None

    value_str = str(value)

    # Check if value contains ", "
    if ", " in value_str:
        # Split by ", " and create OR conditions
        elements = [elem.strip() for elem in value_str.split(", ")]
        conditions = [f"{field} LIKE '%{elem}%'" for elem in elements if elem]
        where_clause = " OR ".join(conditions)
        query = f"SELECT * FROM projects WHERE ({where_clause}){exclude_clause}"
        #print(f"[Query - comma split] {query}")
        results = await asyncio.to_thread(executeQueriesSQL, [query])
        return query, (results[0] if results else None)
    else:
        # Try exact match first
        query_exact = f"SELECT * FROM projects WHERE {field} LIKE '%{value_str}%'{exclude_clause}"
        #print(f"[Query - exact match] {query_exact}")

        # Execute query to check if it returns results
        results = await asyncio.to_thread(executeQueriesSQL, [query_exact])

        if results and results[0]:  # Has results
            #print(f"[Query - exact match SUCCESS] Found {len(results[0])} results")
            return query_exact, results[0]
        else:
            #print(f"[Query - exact match FAILED] No results, trying word split...")
            # Split by space and filter out insignificant words
            words = [word.strip() for word in value_str.split(" ")]
            coreWords = [word for word in words if word.lower() not in wordsToIgnore and word]

            if coreWords:
                conditions = [f"{field} LIKE '%{word}%'" for word in coreWords]
                where_clause = " OR ".join(conditions)
                query = f"SELECT * FROM projects WHERE ({where_clause}){exclude_clause}"
                #print(f"[Query - word split] {query}")
                results = await asyncio.to_thread(executeQueriesSQL, [query])
                return query, (results[0] if results else None)
            else:
                # Fallback to exact match if no significant words (already executed above)
                #print(f"[Query - fallback to exact] {query_exact}")
                return query_exact, (results[0] if results else None)

async def getDirect(project):
    # Pre-filter options to only include fields with data
    validOptions = [opt for opt in directOptions if hasFieldData(opt["field"], project)]

    if not validOptions:
        return []

    # Sort by weight (descending) for better prioritization
    validOptions.sort(key=lambda x: x["p"], reverse=True)

    # Execute queries in parallel for top candidates
    # Try more than nDirect to account for potential empty results
    candidateCount = min(len(validOptions), nDirect * 2)
    candidates = validOptions[:candidateCount]

    # Execute all candidate queries concurrently using asyncio
    tasks = [buildQueryAndExecute(opt["field"], project) for opt in candidates]
    results_list = await asyncio.gather(*tasks, return_exceptions=True)

    # Map successful results
    results_map = {}
    for opt, result in zip(candidates, results_list):
        if isinstance(result, Exception):
            continue
        query, results = result
        if query and results:
            results_map[opt["field"]] = (query, results, opt)

    # Select nDirect results using weighted random from successful queries
    if not results_map:
        return []

    available = list(results_map.values())
    weights = [opt["p"] for _, _, opt in available]

    # Randomly select nDirect items (or fewer if not enough results)
    numToSelect = min(nDirect, len(available))
    selected_items = random.choices(available, weights=weights, k=numToSelect)

    # Build final suggestions
    selected = []
    for query, results, opt in selected_items:
        description = describeDirectSuggestion(query, opt["field"])
        selected.append({
            "description": description,
            "projects": results
        })

    return selected

async def executeDisruptiveQuery(option, project):
    """
    Execute a single disruptive query and return the result.
    Returns (option, description, projects) or None if no results.
    """
    # Pre-check if both fields have data
    if not hasFieldData(option["matchField"], project):
        return None

    # Build and execute match query for the matchField
    match_query, match_results = await buildQueryAndExecute(option["matchField"], project)

    if not match_query:
        return None

    # Get the exclude field value
    exclude_value = getattr(project, option["excludeField"], None)

    if exclude_value:
        # Special handling for date field in exclude
        if option["excludeField"] == "date":
            try:
                year = exclude_value.strftime('%Y-%m-%d').split('-')[0]
                exclude_condition = f" AND date NOT LIKE '{year}-%'"
            except:
                exclude_condition = ""
        else:
            exclude_value_str = str(exclude_value)

            # Handle comma-separated values
            if ", " in exclude_value_str:
                elements = [elem.strip() for elem in exclude_value_str.split(", ")]
                not_conditions = [f"{option['excludeField']} NOT LIKE '%{elem}%'" for elem in elements if elem]
                exclude_condition = " AND " + " AND ".join(not_conditions)
            else:
                # Single value
                exclude_condition = f" AND {option['excludeField']} NOT LIKE '%{exclude_value_str}%'"

        # Combine match query with exclude condition
        final_query = match_query.replace(" AND id !=", exclude_condition + " AND id !=")

        # Execute the disruptive query
        results = await asyncio.to_thread(executeQueriesSQL, [final_query])

        if results and results[0]:
            # Generate dynamic description
            description = describeDisruptiveSuggestion(option["matchField"], option["excludeField"])
            return (option, description, results[0])
    else:
        # No exclude value, use match results (already executed)
        if match_results:
            # Use direct description as fallback
            description = describeDirectSuggestion(match_query, option["matchField"])
            return (option, description, match_results)

    return None

async def getDisruptive(project):
    # Pre-filter options to only include those with valid match fields
    validOptions = [opt for opt in disruptiveOptions if hasFieldData(opt["matchField"], project)]

    if not validOptions:
        return []

    # Randomize order for variety
    random.shuffle(validOptions)

    # Try more candidates in parallel to account for failures
    candidateCount = min(len(validOptions), nDisruptive * 3)
    candidates = validOptions[:candidateCount]

    # Execute all candidate queries concurrently using asyncio
    tasks = [executeDisruptiveQuery(opt, project) for opt in candidates]
    results_list_raw = await asyncio.gather(*tasks, return_exceptions=True)

    # Filter out None and exceptions
    results_list = [r for r in results_list_raw if r and not isinstance(r, Exception)]

    # Randomly select nDisruptive from successful results
    if not results_list:
        return []

    numToSelect = min(nDisruptive, len(results_list))
    selected_items = random.sample(results_list, numToSelect)

    # Build final suggestions
    selected = []
    for _, description, projects in selected_items:
        selected.append({
            "description": description,
            "projects": projects
        })

    return selected

# ==================================================
# main
# ==================================================

def getSuggestions(project):
    """
    Generate suggestions for a project.
    Returns a list of 5 suggestions (3 direct + 2 disruptive),
    each with a description and projects array.
    Suggestions and projects are randomly ordered.
    """
    # Run async functions in sync context
    return asyncio.run(_getSuggestionsAsync(project))

async def _getSuggestionsAsync(project):
    """
    Async implementation of getSuggestions.
    Runs direct and disruptive suggestions in parallel.
    """
    # Get 3 direct and 2 disruptive suggestions concurrently
    direct, disruptive = await asyncio.gather(
        getDirect(project),
        getDisruptive(project)
    )

    # Combine results
    result = direct + disruptive

    # Shuffle projects within each suggestion
    for suggestion in result:
        random.shuffle(suggestion["projects"])

    # Shuffle the suggestions themselves
    random.shuffle(result)
    #result.sort(key=lambda x: len(x["projects"]), reverse=True)

    return result