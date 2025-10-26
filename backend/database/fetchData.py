'''
/database/fetchData.py
-> handle of the csv reading and db writing
'''

from io import StringIO
import requests, pandas as pd
from dotenv import load_dotenv
import os, time

from database.models import db, Project
from utilities.vimeo.setup import getVimeoDate

load_dotenv()

# ==================================================
# global vars
# ==================================================

# string for operations report
report = ""
unchangedStart = None
unchangedEnd = None
checkpointCommit = False

# Track consecutive nan links
nanStart = None
nanEnd = None

categories = ["Artesanato","Dança","Comida","Histórias","Música","Tradição Oral","Poesia","Práticas Religiosas e Ritos","Paisagens Sonoras"]

GOOGLE_SHEETS_URL = os.getenv("GOOGLE_SHEETS_URL")

# ==================================================
# auxiliar methods
# ==================================================

def separateElements(string):
    if not isinstance(string, str):
        return []

    delimiters = ['\n', ', ', ',', ' e ', ' & ']
    fragments = [string]
    
    for delimiter in delimiters:
        new_fragments = []
        for fragment in fragments:
            new_fragments.extend(fragment.split(delimiter))
        fragments = new_fragments
    
    fragments = [f.strip() for f in fragments if f.strip()]
    
    return fragments

def concatStrings(strings):
    result = ""

    for s in strings:
        if isinstance(s, str):
            result = result + ", " + s
    
    return result.replace('\n', ', ')[2:]

def appendReport(msg):
    global report
    report = report + '\n' + msg

def flushBatch():
    global unchangedStart, unchangedEnd
    if unchangedStart is not None:
        if unchangedStart == unchangedEnd:
            appendReport(f"<span>No changes at line {unchangedStart}.<br></span>")
        else:
            appendReport(f"<span>No changes lines {unchangedStart} to {unchangedEnd}.<br></span>")
        unchangedStart = unchangedEnd = None

def flushNanBatch():
    global nanStart, nanEnd
    if nanStart is not None:
        if nanStart == nanEnd:
            appendReport(f"<span>Line {nanStart} — not a valid link (nan).<br></span>")
        else:
            appendReport(f"<span>Lines {nanStart} to {nanEnd} — not a valid link (nan).<br></span>")
        nanStart = nanEnd = None

def resetBoundaries():
    global unchangedStart, unchangedEnd
    unchangedStart = unchangedEnd = None

# ==================================================
# POST and PUT handle
# ==================================================

def insertProject(pid,p,cleanedLink,lineIndex):
    global checkpointCommit
    date = getVimeoDate(pid)
   
    if date == "RATE_LIMIT_EXCEEDED": 
        checkpointCommit = True
        print("Sleeping for 1 minute to prevent blocking.")
        time.sleep(61)
        date = getVimeoDate(pid)
   
    if isinstance(date, str) and "error" in date:
        flushBatch()
        resetBoundaries()
        flushNanBatch()
        appendReport(f"<span>Line {lineIndex} — Error: {pid} — {date}.<br></span>")
        return

    newProject = Project(
        id=pid, # use the vimeo id as project row id
        link=cleanedLink,
        title=p['Tema'] if isinstance(p['Tema'], str) else None,
        author=p['Nome'] if isinstance(p['Nome'], str) else None,
        category=separateElements(p['Categorias'] if isinstance(p['Categorias'], str) else None),
        date=date,

        direction=separateElements(p['Realizador'] if isinstance(p['Realizador'], str) else None),
        sound=separateElements(p['Som'] if isinstance(p['Som'], str) else None),
        production = separateElements(p['Produção'] if isinstance(p['Produção'], str) else None),
        support = separateElements(p['Apoio'] if isinstance(p['Apoio'], str) else None),
        assistance = separateElements(p['Assistência'] if isinstance(p['Assistência'], str) else None),
        research = separateElements(p['Pesquisa'] if isinstance(p['Pesquisa'], str) else None),
        
        location=concatStrings([
            p['Região'] if isinstance(p['Região'], str) else None,
            p['Distrito/Ilha'] if isinstance(p['Distrito/Ilha'], str) else None,
            p['Concelho'] if isinstance(p['Concelho'], str) else None,
            p['Local'] if isinstance(p['Local'], str) else None
        ]),

        instruments = separateElements(p['Instrumentos'] if isinstance(p['Instrumentos'], str) else None),
        
        keywords = separateElements(concatStrings([
            p['Palavras Chave'] if isinstance(p['Palavras Chave'], str) else None,
            p['Conceitos-chave'] if isinstance(p['Conceitos-chave'], str) else None
        ])),
        infoPool = concatStrings([
            p['História (textos que acompanham vídeos)'] if isinstance(p['História (textos que acompanham vídeos)'], str) else None,
            p['Outras Informações'] if isinstance(p['Outras Informações'], str) else None,
            p['Biografias'] if isinstance(p['Biografias'], str) else None
        ])
    )

    db.session.add(newProject)
    appendReport("<span>Line " + str(lineIndex) + " — Created new project: " + str(pid) + ".<br></span>")

def updateProject(existingProject, p, lineIndex,cleanedLink):
    global unchangedStart, unchangedEnd
    changes = []
    
    updates = [
        ('title', p['Tema'] if isinstance(p['Tema'], str) else None),
        ('author', p['Nome'] if isinstance(p['Nome'], str) else None),
        ('link', cleanedLink),
        ('category',separateElements(p['Categorias'] if isinstance(p['Categorias'], str) else None)),

        ('direction', separateElements(p['Realizador'] if isinstance(p['Realizador'], str) else None)),
        ('sound', separateElements(p['Som'] if isinstance(p['Som'], str) else None)),
        ('production', separateElements(p['Produção'] if isinstance(p['Produção'], str) else None)),
        ('support', separateElements(p['Apoio'] if isinstance(p['Apoio'], str) else None)),
        ('assistance', separateElements(p['Assistência'] if isinstance(p['Assistência'], str) else None)),
        ('research', separateElements(p['Pesquisa'] if isinstance(p['Pesquisa'], str) else None)),
        
        ('location', concatStrings([
            p['Região'] if isinstance(p['Região'], str) else None,
            p['Distrito/Ilha'] if isinstance(p['Distrito/Ilha'], str) else None,
            p['Concelho'] if isinstance(p['Concelho'], str) else None,
            p['Local'] if isinstance(p['Local'], str) else None
        ])),
        
        ('instruments', separateElements(p['Instrumentos'] if isinstance(p['Instrumentos'], str) else None)),
        
        ('keywords', separateElements(concatStrings([
            p['Palavras Chave'] if isinstance(p['Palavras Chave'], str) else None,
            p['Conceitos-chave'] if isinstance(p['Conceitos-chave'], str) else None
        ]))),
        ('infoPool', concatStrings([
            p['História (textos que acompanham vídeos)'] if isinstance(p['História (textos que acompanham vídeos)'], str) else None,
            p['Outras Informações'] if isinstance(p['Outras Informações'], str) else None,
            p['Biografias'] if isinstance(p['Biografias'], str) else None
        ]))
    ]

    # avoid unecessary access to Vimeo API
    if getattr(existingProject, "date") is None:
        global checkpointCommit
        date = getVimeoDate(existingProject.id)

        if date == "RATE_LIMIT_EXCEEDED": 
            checkpointCommit = True
            print("Sleeping for 1 minute to prevent blocking.")
            time.sleep(61)
            date = getVimeoDate(existingProject.id)

        if isinstance(date, str) and "error" in date:
            flushBatch()
            resetBoundaries()
            flushNanBatch()
            appendReport(f"<span>Line {lineIndex} — Error: {existingProject.id} — {date}.<br></span>")
            return
        
        updates.append(("date", date))
    
    for field, new_val in updates:
        print(field,new_val)
        if getattr(existingProject, field) != new_val:
            setattr(existingProject, field, new_val)
            changes.append(field)
    
    if changes:
        flushBatch()
        appendReport(f"<span>Line {lineIndex} — Updated {existingProject.id}: {', '.join(changes)}.<br></span>")
    else:
        if unchangedStart is None:
            unchangedStart = lineIndex
        unchangedEnd = lineIndex

# ==================================================
# fetch logic
# ==================================================

def fetchCSV():
    global report, unchangedStart, unchangedEnd, checkpointCommit, nanStart, nanEnd
    visitedIds = {}  # Dictionary to store pid -> first line number mapping
    duplicateIds = {}  # Dictionary to group duplicates by pid: {pid: [line1, line2, ...]}

    # fetch CSV data (certificates handle), UTF-8 encoding not to loose chars like 'Ç'
    response = requests.get(GOOGLE_SHEETS_URL)
    response.raise_for_status()
    response.encoding = 'utf-8'

    df = pd.read_csv(StringIO(response.text))

    report = f"<h1>CSV fetched with success!</h1><h3> {len(df)} lines found.</h3>"
    unchangedStart = unchangedEnd = None
    nanStart = nanEnd = None

    for lineIndex, p in enumerate(df.iloc, 1):

        print(f"{lineIndex}/{len(df)}")
        lineIndex = lineIndex + 1 # header compensation

        cleanedLink = p['Link'].replace(' ', '').replace('\n', '') if isinstance(p['Link'], str) else p['Link']
        if (isinstance(cleanedLink, str) and 'vimeo.com/' in cleanedLink and cleanedLink[-1].isdigit() == False): 
            cleanedLink = cleanedLink[:-1]
       
        # check if link exists and is valid
        if not isinstance(cleanedLink, str) or 'vimeo.com/' not in cleanedLink or not cleanedLink[-1].isdigit(): 
            if pd.isna(cleanedLink) or str(cleanedLink).lower() == 'nan':
                flushBatch()
                if nanStart is None:
                    nanStart = lineIndex
                nanEnd = lineIndex
                continue
            else:
                flushBatch()
                flushNanBatch()
                appendReport(f"<span>Line {lineIndex} — not a valid link ({cleanedLink}).<br></span>")
                resetBoundaries()
                continue

        flushNanBatch()

        pid = int(cleanedLink.split("/")[-1])

        # Check for duplicates
        if pid in visitedIds:
            # Add to duplicates tracking
            if pid not in duplicateIds:
                duplicateIds[pid] = [visitedIds[pid]]  # Start with first occurrence
            duplicateIds[pid].append(lineIndex)  # Add current duplicate
            
            # Handle unchanged tracking for duplicates
            if unchangedStart is None:
                unchangedStart = lineIndex
            unchangedEnd = lineIndex
            continue
        
        # Add to visited IDs with line number
        visitedIds[pid] = lineIndex

        existingProject = Project.query.filter_by(id = pid).first()
        
        if existingProject:
            updateProject(existingProject, p, lineIndex, cleanedLink)
        else:
            flushBatch()
            insertProject(pid, p, cleanedLink, lineIndex)
            time.sleep(1)
        
        if checkpointCommit:
            db.session.commit()
            checkpointCommit = False
    
    flushBatch()
    flushNanBatch()
    
    # Add duplicate summary to report
    if duplicateIds:
        appendReport(f"<h3>Duplicate Summary:</h3>")

        for pid, lines in duplicateIds.items():
            if len(lines) == 2:
                appendReport(f"<span>- https://vimeo.com/{pid} repeated at lines {lines[0]} and {lines[1]}<br></span>")
            else:
                lines_str = ', '.join(map(str, lines[:-1])) + f" and {lines[-1]}"
                appendReport(f"<span>- https://vimeo.com/{pid} repeated at lines {lines_str}<br></span>")
    
    appendReport(f"<h3>{len(Project.query.all())} objects on the database.</h3>")

    db.session.commit()

    return report