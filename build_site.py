#!/usr/bin/env python3
"""Generate static HTML pages for KG Portfolio."""

import os
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
PROJECTS_DIR = ROOT / "projects"
RESUME_SRC = Path("/home/kg/Jobs/Kevin Guerra.pdf")
RESUME_ASSET = "assets/Kevin-Guerra.pdf"

OWNER = "Kevin Alexander Guerra"
OWNER_SHORT = "Kevin"
SITE_NAME = "KG PORTFOLIO"
COPYRIGHT_YEAR = "2026"
CONTACT_EMAIL = "kevingnet1@gmail.com"
SITE_BASE_URL = os.getenv("SITE_BASE_URL", "https://kevingnet.github.io/kg-portfolio").rstrip("/")
SITE_TAGLINE = (
    "Software developer portfolio — enterprise systems, security, embedded, "
    "cloud, and performance optimization across Google, Disney, VMware, and more."
)
DEFAULT_OG_IMAGE = "assets/images/profile.jpeg"

# Applied to any scraped/mirrored HTML as well — longest phrases first
BRANDING_REPLACEMENTS = [
    ("Ismael Guerra Dominguez", OWNER),
    ("Portfolio of Ismael Guerra", f"Portfolio of {OWNER}"),
    ("Ismael Guerra", OWNER),
    ("Hello, my name is Ismael,", f"Hello, my name is {OWNER_SHORT},"),
    ("my name is Ismael", f"my name is {OWNER_SHORT}"),
    ("IGD PORTFOLIO", SITE_NAME),
    ("IGD Portfolio", f"{SITE_NAME}"),
    ("IGD", "KG"),
    ("Ismael", OWNER_SHORT),
]


def apply_branding(text: str) -> str:
    for old, new in BRANDING_REPLACEMENTS:
        text = text.replace(old, new)
    return text

NAV = [
    ("Portfolio", "index.html"),
    ("Services", "services.html"),
    ("Samples", "samples.html"),
    ("About", "about.html"),
]

SOCIAL = {
    "linkedin": "https://www.linkedin.com/in/kevin-guerra-36151446/",
    "github": "https://github.com/iguerranet",
}

CAROUSEL_LOGOS = [
    ("electrosonic", "jpeg"), ("voltdelta", "jpeg"), ("hpe", "jpeg"),
    ("hypermedia", "jpeg"), ("spirent", "jpeg"), ("surfware", "jpeg"),
    ("netpulse", "jpeg"), ("knulrd", "jpeg"), ("butterfleye", "jpeg"),
    ("directv", "jpeg"), ("opentv", "jpeg"), ("disney", "jpeg"),
    ("yahoo", "jpeg"), ("guidance", "jpeg"), ("motorola", "jpeg"),
    ("dolby", "jpeg"), ("veritas", "jpeg"), ("vmware", "jpeg"),
    ("google", "jpeg"), ("facebook", "jpeg"),
]

# name, image file (without ext), image ext, project slug, card description
PORTFOLIO = [
    ("Google", "google", "jpeg", "google",
     "Localization, Maps, Hardware Analytics, Speech Ops, YouTube, HR. C++, Java, Python, RBAC/OAuth2, GIS, Postgres, Dart."),
    ("DirecTV", "directv", "jpeg", "directv",
     "Automation Engineer, created OCR system and test automation tools. C++, Python."),
    ("JakeKnows", "company", "png", "jakeknows",
     "Architecture, Design and Development of distributed web system, database driven. Application backend for mobile apps for Sony, to enable job applicants to submit resumes. C#, C++, MSSql, Python."),
    ("Disney", "disney", "jpeg", "disney",
     "Developed web apps. Software Deployer/Updater. Networking tools for Netware. C/C++, Visual Basic, MS Sql, MS Access, ASP."),
    ("Electrosonic", "electrosonic", "jpeg", "electrosonic",
     "Developed second version of a Scheduler to automate Video Server, Robotic devices, Networking Devices, etc... Developed Remote Control system for scheduler through Email. Developed various tools for integration."),
    ("VoltDelta", "voltdelta", "jpeg", "voltdelta",
     "Developed Phone Switch Simulator to be able to test software. Developed X25 Network Connector. C++."),
    ("Vmware", "vmware", "jpeg", "vmware",
     "Developed Test Development Framework replacing Perl legacy system with over 1 million lines of code in 60k loc. Python."),
    ("HMS", "hypermedia", "jpeg", "hms",
     "Developed Input Validation Library. Tools for penetration testing. Site analysis networking tools. Audited code from other developers for Security and Privacy compliance. C++, Python, Bash."),
    ("Surfware", "surfware", "jpeg", "surfware",
     "Developed enhancements and new features for CNC Metal Cutting Software and interfaces for Autocad and Solidworks. C++."),
    ("Motorola", "motorola", "jpeg", "motorola",
     "Developed Closed Captioning Module for Setup Boxes. C++."),
    ("OpenTV", "opentv", "jpeg", "opentv",
     "Developed Enhancements and New Features for Local Advertisement Scheduler Application. C#, C++, Python."),
    ("Spirent", "spirent", "jpeg", "spirent",
     "Developed Scripting Interface for Tcl to enable Automation and Instrumentation of Networking Tester Appliance and Equipment. C++, Tcl."),
]

SAMPLES = [
    ("Hive Mapper - Drone Navigation, C++",
     "The goal is to navigate a drone through an airport in the shortest time possible. The airport is composed of several interconnected circular roads, and the drone's position is described by a road name and the degrees clockwise around the road's circumference. The drone can transfer between roads at points of intersection. One week for completion.",
     "https://github.com/kevingnet/HiveMapperDrone", "https://github.com/iguerranet/HiveMapperDrone"),
    ("Magazine - Node.js REST EC2 App",
     "Magazine sample app using Angular, Node.js with REST API for EC2 deployment. One week for completion.",
     "https://github.com/kevingnet/magazine", "https://github.com/iguerranet/magazine"),
    ("Game of Life - Java",
     "Conway's Game of Life - Java implementation. One day to develop.",
     "https://github.com/kevingnet/GameOfLife", "https://github.com/iguerranet/GameOfLife"),
    ("Word Finder - C++",
     "Find Longest Word Made of Other Words. Program reads a file containing a sorted list of words (one word per line, no spaces, all lower case), then identifies the longest word in the file that can be constructed by concatenating copies of shorter words also found in the file.",
     "https://github.com/kevingnet/WordFinder", "https://github.com/iguerranet/WordFinder"),
    ("Virtual Coffee Machine",
     "Cloud app on AWS using Docker containers. Server is a NodeJS app with a simple API (level(GET), brew, refill (POST). A Client in TypeScript accesses those APIs to operate. 6 days to complete.",
     "https://github.com/iguerranet/coffee.bitnami", "https://github.com/iguerranet/coffee.bitnami"),
    ("Flux - Electric Vehicle",
     "Project Plan - 30, 60 and 90 days. Developed plan in two days. Look at Diagram and Architecture Document.",
     "https://github.com/kevingnet/FluxElectricVehicle", "https://github.com/iguerranet/FluxElectricVehicle"),
    ("Time Server - Client/Server, TypeScript, JavaScript, SQL, Python",
     "Time Server sample app using Angular, Node.js with REST API for EC2 deployment. One week to develop.",
     "https://github.com/kevingnet/time_server", "https://github.com/iguerranet/time_server"),
]


def rel_prefix(depth: int) -> str:
    return "../" * depth if depth else ""


def carousel(depth: int = 0) -> str:
    p = rel_prefix(depth)
    imgs = "\n".join(
        f'      <img src="{p}assets/images/{name}.{ext}" alt="{name}">'
        for name, ext in CAROUSEL_LOGOS
    )
    return f"""  <div class="logo-carousel">
    <div class="logo-carousel-track">
{imgs}
    </div>
  </div>"""


def header(active: str, depth: int = 0) -> str:
    p = rel_prefix(depth)
    links = "\n".join(
        f'        <li><a href="{p}{href}" class="{"active" if label == active else ""}">{label}</a></li>'
        for label, href in NAV
    )
    return f"""  <div class="top-bar">
    <img class="profile-thumb" src="{p}assets/images/profile.jpeg" alt="{OWNER}">
    <a href="{p}index.html" class="site-brand">{SITE_NAME}</a>
  </div>
  <div class="nav-wrap">
    <ul class="site-nav">
{links}
    </ul>
  </div>
{carousel(depth)}"""


def footer(depth: int = 0) -> str:
    p = rel_prefix(depth)
    return f"""  <footer class="site-footer">
    <div class="footer-social">
      <a href="{SOCIAL["linkedin"]}" target="_blank" rel="noopener" title="LinkedIn">
        <img src="{p}assets/images/linkedin.png" alt="LinkedIn">
      </a>
      <a href="{SOCIAL["github"]}" target="_blank" rel="noopener" title="GitHub">
        <img src="{p}assets/images/github.jpeg" alt="GitHub">
      </a>
      <a href="mailto:{CONTACT_EMAIL}" title="Email">{CONTACT_EMAIL}</a>
    </div>
    <p class="footer-copy">&copy; {COPYRIGHT_YEAR} {OWNER}. <a href="{p}{RESUME_ASSET}">Resume (PDF)</a></p>
  </footer>"""


def page(
    title: str,
    active: str,
    body: str,
    depth: int = 0,
    *,
    description: str | None = None,
    slug_path: str | None = None,
    og_image: str | None = None,
) -> str:
    p = rel_prefix(depth)
    desc = description or SITE_TAGLINE
    if slug_path is None:
        slug_path = {
            "Portfolio": "index.html",
            "Services": "services.html",
            "Samples": "samples.html",
            "About": "about.html",
        }.get(active, "index.html")
    canon = f"{SITE_BASE_URL}/{slug_path.replace('index.html', '').rstrip('/')}"
    if canon.endswith("/") and slug_path != "index.html":
        canon = canon.rstrip("/")
    if slug_path == "index.html":
        canon = f"{SITE_BASE_URL}/"
    img_rel = (og_image or DEFAULT_OG_IMAGE).removeprefix("../")
    og_img = f"{SITE_BASE_URL}/{img_rel}"
    full_title = f"{title} | {SITE_NAME}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{full_title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canon}">
  <link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:title" content="{full_title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canon}">
  <meta property="og:image" content="{og_img}">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{full_title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{og_img}">
  <link rel="stylesheet" href="{p}css/style.css">
</head>
<body>
{header(active, depth)}
  <main>
{body}
  </main>
{footer(depth)}
  <script src="{p}js/carousel.js"></script>
</body>
</html>
"""

PROJECTS = {
    "google": {
        "title": "Google Projects",
        "intro": """<p>Localization Tools: Added new features and enhancements to in-house localization tools</p>
<p>avik/babel: Web app, Android Screen Shotting app, System to enable translation verification world wide employees to verify translations in their native language(s) and compare Android and Web apps with English so as to ascertain correctness.</p>
<p>GoogleEarth: Converted to Open Source, Upgraded most libraries to newer versions, Performed Code Optimizations.</p>
<p>Hardware Analytics Tools and Apps: Created new apps and provided enhancements to existing ones.</p>
<p>Devices Apps and Tools: Provided enhancements and fixes.</p>
<p>YouTube Apps: Developed Internal Web Applications, Microservices for use by Teams.</p>
<p>HR App: Helped to create 2nd version of HR Payroll Processing Application as Microservices, using the latest technologies and best practices.</p>""",
        "tech": "Java, C/C++, Python, Postgres, JavaScript, Image Processing, Octa Trees, Optimization, OAuth2 Authentication, RBAC (MAC, DAC) Authorization, HTML5, Dart, CSS, Angular, TypeScript, GCP, Google Cloud Platform, AppEngine, BigQuery, BigTable, Microservices, Borg, Protobuf, Guice Guava",
        "sections": [
            ("Localization", "Web and Android Application", """<p>Web Applications Development. Object Oriented Software Development in Java and Python. Learned Google technology stack, several enterprise applications, including one with over 60,000 lines of code, web based and android in about 2 months.</p>
<p>Reverse engineering of Java code.</p>
<p>Provided enhancements and fixed issues in existing applications in Python. Used cloud technologies such as DataStore, AppEngine plus other APIs. Developed new architecture, designed, coded, wrote unit, integration and performance tests, including database storage for a global impact in production application replacing the web based system of ~45k LOC with ~16k LOC in Java for the backend and ~6k LOC for the front end in Dart. Inclusive Role Based Authentication and Resource Authorization Security Module that I wrote in ~2k LOC. The new system provides numerous enhancements, including simplified workflow with very highly performant operation, saving the company about 1/2 million dollars projected for the first year, for vendor expenses plus great time savings for users. Security Module (RBAC, MAC, DAC, Authentication and Authorization,) Memcache, HTML5, CSS, Spring, Hybernate, JDO, Leadership in bringing a project stalled for two years, to completion in 7 months.</p>"""),
            ("Maps Google Earth", "C++, Python Application — Open Sourced", """<p>Develop enhancements and maintain the Google Earth Enterprise and related products.</p>
<p>Developed optimizations to python XML processing, decreasing processing time 11 times, this was a three prong approach: Rearranging python code to move the more likely branches to the top, Importing to postgres using file based process and Added C++ and Python code to calculate geospatial data, taking into consideration point invariant and therefore avoiding that extra calculation.</p>
<p>Developed optimizations for C++ by using more modern libraries. C++, Python, JavaScript, Postgres, Image Processing.</p>"""),
            ("Hardware Analytics", "Python, Angular, JavaScript, Typescript, SQL, BigQuery, Microservices.", """<p>Architecture and Design, Developed and maintained solutions for the Hardware Analytics Team.</p>
<p>Developed authentication and authorization mechanisms to enhance security and compliance with privacy policies. Developed solutions for auditing, automatic alerts. Improved efficiency and optimized solutions and applications. Cloud development using Borg and related systems.</p>"""),
            ("Google Devices", "Python, Java, Angular, Javascript, Microservices.", """<p>Improved Speech Data Collection Tools team to automate and simplify data collection. Created a testing framework for 1st and 3rd party devices.</p>"""),
            ("YouTube", "Java, C++, Python, Angular, JavaScript, SQL, BigQuery, Microservices.", """<p>Architecture and Design, Developed and maintained solutions for the YouTube Team. Applications needed to be secure and privacy aware. Provided data pipelines to proprietary graphical query application. Mentored other team members.</p>"""),
            ("HR - Finance", "Java, Guice, Protobuf, Microservices.", """<p>Designed, Developed and tested the new version of application for HR Team. Java and Micro-Services. Heavy use of dependency injection, patterns, Guice, protobuf, and other internal and open source tools. Application was highly secure and addressed privacy concerns.</p>"""),
        ],
    },
    "directv": {
        "title": "DirecTV Projects",
        "intro": """<ul>
<li>redrat_scripter: red rat code for infrared transceiver, usb, perl client that reads scripts and sends commands to server that uses sockets</li>
<li>redrat_blaster: used in server farm to blast with random IR messages to discover software errors</li>
<li>USB Device Driver: Modified to minimize memory usage and avoid excess of object recreation</li>
<li>ScreenCapture Control: ActiveX control to capture screens using various devices, creates images</li>
<li>Image Processing Code: binarize images, crop selected window</li>
<li>ScreenReader: Perform OCR on selected window</li>
<li>ScreenScraper: Perform OCR on a whole screen</li>
<li>AbbyReader OCR Instrumentation System, used by Server</li>
<li>OCR Server: Uses Abby Reader System, receives an image as input, performs OCR on it and returns text to the client, over TCP/IP Network.</li>
<li>OCR Server Tester: Performs various tests on the server.</li>
<li>OCR Client: Takes video screen shots with ScreenCapture, does some image processing, including adapted FFT algorithm, binarizes image, sends image to server, receives text, client is instrumented via javascript, usually from Test Director Web App.</li>
<li>OCR Client Blaster: Performance tester for OCR System.</li>
</ul>""",
        "tech": "C/C++, JavaScript, Perl, ACE Framework, ActiveX, COM, Win32, USB Device Driver Development, OCR, Machine Vision, Image Processing, FFT, Fast (Discrete) Fourier Transform, Heuristics Methods for Machine Vision, Image Database Retrieval System using above and FFT, Image Binarization, Image Capture, Embedded, Web Based Test: Test Director",
        "work": """<h2>Work Performed</h2>
<p>Envisioned, promoted, architected, designed and developed software infrastructure for Automation system in C++, ActiveX, COM and Win32. The Client/Server system uses ACE Framework design and architecture patterns and drives video capture devices to acquire and process images, perform OCR and recognition of other artifacts using the Fast Fourier Transform algorithm and other methods in Machine Vision.</p>
<p>Invented algorithms using kernel methods and decision trees for analysis of image data and comparison for recognition. This was done in an incredible short time working independently, this took about one month of research and implementation.</p>
<p>Envisioned, promoted, designed and developed Linux Socket C++ Server and Perl Client script processing Automation application for driving libusb based RedRat infrared Transceiver concurrent multiple devices. A RedRat is a device that can read and replicate remote control signals. ANSI C, C++, OOP, Patterns, Image Processing, JavaScript, Test Director, Visual Studio, DirectX, USB Devices.</p>
<p>Applications and ActiveX controls were used from Test Directors and instrumented using javascript.</p>""",
    },
    "jakeknows": {
        "title": "JakeKnows Projects",
        "intro": """<p><strong>Web App and Engine:</strong> System Service that provides data to the Web App, a Web Bot collects information about users on the web, from various sites and calculates how trustworthy the user identity is based on the data found. Android and iPhone apps were developed by another team, and these apps interfaced with the backend. The backend was always ready with the data to be served, via caching and other mechanisms, so that a web call would be orders of magnitude faster as opposed to the usual web apps that get the data as needed, for each call.</p>
<p><strong>Sony App:</strong> Provide Job Applicants with Access to Sony Jobs Database and Apply for Jobs. This application was developed very fast in a matter of 3 or 4 weeks to deployment, sold to Sony. The application used the code generators and the code base from the app above so code reuse was at a maximum.</p>""",
        "tech": "C#, C/C++, Python, SQL, MSSQL, IIS, SOAP, WSDL, WCF, Web Services, Code Generation",
        "work": """<h2>Work Performed</h2>
<p>Web Applications Development. Assimilated legacy server application in order to develop new architecture and design. Developed back end server for job application system for mobile devices for iPhone and Android.</p>
<p>Developed architecture, design and code for the new Identity Engine. The engine is a business core application intended to provide positive identification of an individual via digital activity harvested in diverse ways using patented technologies.</p>""",
    },
    "disney": {
        "title": "Disney Projects",
        "intro": """<ul>
<li>CorpPurch: Request purchases</li>
<li>DialIn_OutRequest: Request dial in/out access</li>
<li>HRTS: Request hardware</li>
<li>IPAging: IP Accounting</li>
<li>IPListing: IP Listings</li>
<li>ISTechDBAccess: Request database access</li>
<li>PeopleSoftLoginRequest: Request PeopleSoft access</li>
<li>SuggestionToTechServices: Send a suggestion to Tech Services Team</li>
<li>UpdateStudioDirectory: self explanatory</li>
<li>Commissary: Used by all Disney Studios Personnel to view commissary menu.</li>
<li>NWConnect: Netware connector ActiveX control.</li>
<li>GenericUpdater: Update software from a remote location using Netware NWConnect</li>
<li>GenericDeployer: Update software to a remote location using Netware NWConnect, VB application.</li>
<li>SendMail: Send email control to be used from Visual Basic applications, ActiveX</li>
</ul>""",
        "tech": "C/C++, Assembly, Visual Basic, Microsoft Access, Visual Studio, ASP, Active Server Pages, Windows Development, DLL Development, Databases: MS Access, MSSQL, Email Delivery through MAPI API, Win32, Mac OS, IIS, Internet Information Server, Microsoft SQL Server",
        "work": """<h2>Work Performed</h2>
<p>Designed and developed multithreaded network connector in C++ for Novell and Windows networks. Developed Macintosh version later.</p>
<p>Developed software updater in C++ that used the network connector. User base of 10,000 worldwide. Developed Macintosh version.</p>
<p>Designed and developed software deployment application in Visual Basic which helped other development teams.</p>
<p>Completed and improved food menu system for Marriott food management at the Disney Commissary. Used Visual Basic and MS Access. It printed on paper and output to a web page.</p>
<p>Converted CGI and Visual Basic applications to internet applications.</p>
<p>Developed Management Information System, Projects Management System and numerous database driven internet applications. Using IIS, ASP, MS SQL, Stored Procedures, MS Access, Java and VB Scripts and COM. Applications had to run in PC, Macintosh and UNIX platforms with MS Internet Explorer and Netscape in several versions. Designed graphics.</p>
<p>Conceived and developed Mail ActiveX control in Visual C++ used by internet applications and other programming teams.</p>
<p>Conceived and developed ActiveX control that extended Visual Basic by intercepting Windows messages and providing Events for custom processing of those messages.</p>
<p>Maintained and added features to other applications and tools. Collaborated in Y2K project, analyzed software and promoted necessary changes. Designed and Administered databases in MS SQL and MS Access.</p>""",
    },
    "electrosonic": {
        "title": "Electrosonic Projects",
        "intro": """<ul>
<li>CommLib: DLL, rewrote winsock to handle double buffering for better performance</li>
<li>MonitorDLL: DLL to monitor computers, servers or other devices through CommLib Winsock TCP/IP</li>
<li>LiquidAudio streaming control: Designed as an ActiveX control, used to stream audio</li>
<li>ESCAN Application and related tools</li>
<li>ESCAN: 2nd version of the Scheduler — visually script and schedule devices locally or remote</li>
<li>SiteLinx: connect two ESCAN servers through email</li>
<li>PC_Monitor: Win32 app to monitor a PC</li>
<li>PC_Server: Win32 app to monitor a Video Server</li>
<li>DeviceSimulator: Create devices for testing or simulation</li>
<li>XML ActiveX control: import data from a database and export to xml files</li>
<li>Email ActiveX control: used to send/read email</li>
<li>Custom Applications: Voting System for the SHOA Foundation, Event generation devices for AMNH, etc.</li>
</ul>""",
        "tech": "C/C++, TCP/IP, Win32, WinDbg, WinSock, DDK, Device Driver Development, COM+, ActiveX, Windows Applications, DLL Development, Multi-Threading, XML, MAPI, TAPI, RAS, MPEG encoding/decoding, TV Closed Captioning, GUI UX/UI Heavy Development, Printing, Embedded, Robotics, Video/Audio Streaming, Databases, Scheduling, Event Driven Programming, Remote Control through Email",
        "work": """<h2>Work Performed</h2>
<p>Designed, coded, tested, profiled and documented applications and tools and proposed changes and additions. Responsible for full development cycle. Worked in team environments. Served as mentor to other programmers and technicians.</p>
<p>Conceived, designed and developed application for remote control and monitoring using C++, COM+, MAPI, TAPI, RAS.</p>
<p>Improved serial port and internet connectivity DLL which provided support for most applications. Developed second version, maximized capacity and transfer speed using C++, raw sockets, multi-threading, network events and double buffering.</p>
<p>Took ownership of application that controls and interacts with network and embedded devices. Developed protocols, device interfaces, ActiveX and ATL controls; extended application's and device's capabilities. Developed second version with many enhancements: MDI GUI, scripting capabilities, XML format, device triggers, email reporting plus many others.</p>
<p>Developed applications, tools and controls to support projects: Database, printing, MPEG encoding, hardware programming, device driver interface for video hardware to output graphics and text to TV screens, magnetic cards scanning, touch panels, Real Audio streaming control and device.</p>
<p>Adapted and implemented systems and applications for: American Museum of Natural History in New York, Museum of Tolerance in Beverly Hills, The Country Music Hall of Fame in Nashville, The Shoa Foundation in Universal Studios and others.</p>""",
    },
    "voltdelta": {
        "title": "Volt Delta Projects",
        "intro": """<ul>
<li>Phone Switch Simulator: C++ app that was used to test other applications instead of using a real phone switch which cost $1,000/hr at AT&amp;T</li>
<li>X.25 Relay: C++ app, used special hardware in a computer/server to interface with X.25 networks, it connected TCP/IP networks to them</li>
<li>StarStationManager: Manage X.25 work stations</li>
<li>StarTreeList: Visualize X.25 networks</li>
</ul>""",
        "tech": "C/C++, X.25 Networking, TCP/IP Networking, Windows Development, DLL Development, Win32, MSSQL, Visual Studio",
        "work": """<h2>Work Performed</h2>
<p>Designed and developed X.25 and TCP/IP network connector in C++ used by Telephone Switch Simulator.</p>
<p>Led team developing Telephone Switch Simulator in C++ saving time and money by allowing testing of programs in-house.</p>
<p>Developed other tools using web technologies, MS SQL, Stored Procedures and Visual Studio.</p>""",
    },
    "vmware": {
        "title": "Vmware Projects",
        "intro": """<ul>
<li>Gemini: Automation Framework to instrument virtual and non-virtual servers, workstations and appliances, such as ESX, HBR</li>
<li>SSH Connector: Used by Gemini to securely connect and send commands to devices above</li>
<li>Log Framework: Used by Gemini to log to terminal or html documents</li>
</ul>""",
        "tech": "Python, Perl, Virtualization, Networking, Automation, QA, Script Instrumentation, Framework Development, Test Development, SSH",
        "work": """<h2>Work Performed</h2>
<p>Architected, designed and implemented a new testing framework for the QA department.</p>
<p>Replaced old framework mostly perl based with a lot of python. Original framework was over 80kloc, new framework is 8kloc, 8 times faster. Used object orientation, functional and meta programming as paradigms.</p>""",
    },
    "hms": {
        "title": "Hypermedia Projects",
        "intro": """<ul>
<li>Input Validation Library: used by in-house web applications to provide security, prevent sql injection and other exploits</li>
<li>Tools: For penetration testing, web site accounting and monitoring</li>
</ul>""",
        "tech": "C/C++, Java, Python, Perl, Web Applications, Security, Library Development, Linux, Security, Privacy, ECommerce, Code Analysis, Code Security Reviews",
        "work": """<h2>Work Performed</h2>
<p>Developed in-house web applications making use of best user interface methodologies.</p>
<p>Analyzed applications to find security vulnerabilities, documented findings, proposed changes. Mostly in Linux. Malware detection and fixes.</p>
<p>Participated in the development process contributing security related advice and trained development groups on best practices.</p>
<p>Developed tools and scripts including an input validation library which uses regular expressions and is assembly optimized for speed, including several automatic features freeing developers from most of the responsibility of input validation.</p>
<p>Developed interfaces to this library for Java, C and Perl in a Linux environment.</p>""",
    },
    "surfware": {
        "title": "Surfware Projects",
        "intro": """<ul>
<li>Surfcam: Added features and enhancements</li>
<li>SolidWorks/Autocad Import/Export App: windows app to export/import data from surfcam files to/from</li>
</ul>""",
        "tech": "C/C++, C#, CAD/CAM, CNC, milling machine codes, generated by surfcam from 3d models, Databases, Win32, COM, VBA, DirectX, OpenGL, Autocad, Solidworks, 3D",
        "work": """<h2>Work Performed</h2>
<p>Developed, designed and re-factored code for CAD/CAM systems in C++, C#, in a windows environment.</p>
<p>Implemented features for the 4 and 5 axis subsystem. Envisioned and Architected tools to improve the development process.</p>
<p>Updated and redesigned code and database business applications in MS SQL, VBA and MS Access.</p>
<p>Designed and coded Perl scripts to process text and expedite the development process. Developed plugins for applications such as Solid Works in C++, ActiveX and Parasolid CAD/CAM Kernel, used OpenGL and DirectX. Debugged and fixed application.</p>""",
    },
    "motorola": {
        "title": "Motorola Projects",
        "intro": """<p><strong>Closed Captioning Embedded Module</strong></p>
<p>C/C++, Closed Captioning, OCAP, Embedded, Set Top Boxes</p>""",
        "tech": "C/C++, Closed Captioning, OCAP, Embedded, Set Top Boxes",
        "work": """<h2>Work Performed</h2>
<p>Developed, designed and coded software in a distributed team, agile environment for Linux and embedded systems. The system is embedded in a Set Top Box, it provides Closed Captioning capabilities. Redesign was done to provide exceptional performance eliminating memory allocation completely after initialization.</p>""",
    },
    "opentv": {
        "title": "OpenTV Projects",
        "intro": """<p><strong>Dynamic Scheduler:</strong> Resolved Issues and Enhanced Win32 C# App, used for Local Advertisement Scheduling</p>""",
        "tech": "C#, C/C++, Python, Perl, Oracle, Big Data Import, Win32, Scheduling, Web Services, SOAP, SQL, Stored Procedures, IIS, MVC, .NET, XML",
        "work": """<h2>Work Performed</h2>
<p>Developed software enhancements and bug fixes for application used by major cable companies worldwide. The application was very complex containing over a million lines of code.</p>""",
    },
    "spirent": {
        "title": "Spirent Projects",
        "intro": """<ul>
<li>Tlc Interface: replaced old Tcl code base and converted it to C++, resulting in only one line of tcl code from several thousands.</li>
<li>Mainline: Helped to create second version of embedded application that drives a network testing appliance and can be scripted and instrumented using tcl.</li>
</ul>""",
        "tech": "C/C++, Tcl, Network Testing, Automation, Script Instrumentation, Linux Embedded, ACE Framework, SWIG",
        "work": """<h2>Work Performed</h2>
<p>Developed new user interface for next generation system using SWIG for creation of tcl accessibility layer.</p>
<p>Developed new commands for the network testing system.</p>
<p>Re-factored code to later reuse for the new design. Network Programming, ACE Framework, OOD, Visual Studio.</p>""",
    },
}


def project_body(slug: str) -> str:
    p = PROJECTS[slug]
    parts = [
        '    <a href="../index.html" class="back-link">&larr; Back to Portfolio</a>',
        f'    <h1 class="page-title">{p["title"]}</h1>',
        '    <div class="content-section">',
        p["intro"],
        f'      <p class="tech-tags">{p["tech"]}</p>',
    ]
    if "sections" in p:
        for h2, h3, content in p["sections"]:
            parts.append(f'      <h2>{h2}</h2>')
            parts.append(f'      <h3>{h3}</h3>')
            parts.append(content)
    if "work" in p:
        parts.append(p["work"])
    parts.append("    </div>")
    return "\n".join(parts)


def main():
    assets = ROOT / "assets"
    assets.mkdir(exist_ok=True)
    if RESUME_SRC.is_file():
        shutil.copy2(RESUME_SRC, assets / "Kevin-Guerra.pdf")
    elif not (assets / "Kevin-Guerra.pdf").is_file():
        print(f"warn: resume not found at {RESUME_SRC}")

    cards = "\n".join(
        f"""      <div class="portfolio-item">
        <a href="projects/{slug}.html">
          <div class="logo-wrap"><img src="assets/images/{img}.{ext}" alt="{name}"></div>
          <span class="company-name">{name}</span>
          <span class="company-desc">{desc}</span>
        </a>
      </div>"""
        for name, img, ext, slug, desc in PORTFOLIO
    )
    (ROOT / "index.html").write_text(
        page(
            "Portfolio",
            "Portfolio",
            f"""    <h1 class="page-title">My Portfolio</h1>
    <p class="page-intro">Welcome to my portfolio. Here you'll find a selection of my work. Explore my projects to learn more about what I do.</p>
    <div class="portfolio-grid">
{cards}
    </div>""",
            description="Selected software projects at Google, Disney, VMware, DirecTV, and other companies.",
        )
    )

    services = "\n".join(
        f"      <li>{s}</li>"
        for s in [
            "IDEATION", "WEB &amp; CLOUD DEVELOPMENT", "SECURITY &amp; PRIVACY",
            "REVERSE ENGINEERING", "DATABASES", "CONSULTING",
            "CUSTOM APPLICATIONS", "PERFORMANCE OPTIMIZATION",
            "EMBEDDED SYSTEMS", "IMAGE PROCESSING",
        ]
    )
    (ROOT / "services.html").write_text(
        page(
            "Services",
            "Services",
            f'    <h1 class="page-title">My Services</h1>\n    <ul class="services-list">\n{services}\n    </ul>',
            slug_path="services.html",
            description="Consulting and development: web, cloud, security, embedded systems, and performance optimization.",
        )
    )

    samples_html = "\n".join(
        f"""      <div class="sample-entry">
        <h2><a href="{gh1}" target="_blank" rel="noopener">{title}</a></h2>
        <p>{desc}</p>
        <div class="sample-links">
          <a href="{gh1}" target="_blank" rel="noopener">GitHub (kevingnet)</a>
          <a href="{gh2}" target="_blank" rel="noopener">GitHub (iguerranet)</a>
        </div>
      </div>"""
        for title, desc, gh1, gh2 in SAMPLES
    )
    (ROOT / "samples.html").write_text(
        page(
            "Samples",
            "Samples",
            f'    <h1 class="page-title">Projects Samples</h1>\n    <div class="content-section">\n{samples_html}\n    </div>',
            slug_path="samples.html",
            description="Open-source sample projects on GitHub — C++, Java, Node.js, TypeScript, and AWS.",
        )
    )

    (ROOT / "about.html").write_text(
        page(
            "About",
            "About",
            f"""    <div class="about-layout">
      <img class="about-hero-img" src="assets/images/hero.jpg" alt="{OWNER}">
      <div class="about-bio">
        <h1>BIO</h1>
        <p>Hello, my name is Kevin, I'm a software developer, my career started as a hobby and I'm still passionate about computer programming and software development. I've had the opportunity and privilege to work on many types of projects ranging from tools, to custom apps, web sites, embedded systems, robotics, optimization, networking, databases, security and privacy, virtualization, and many others...</p>
        <p>I pride myself in developing good quality software that is fast and responsive, with fewer lines of code, code generation, best practices using a variety of tools and technologies. I guarantee my work and I'm highly productive, you might say that I'm a team of developers in one — see my <a href="{RESUME_ASSET}">resume (PDF)</a> for illustrations of the technologies I've used and the companies I've worked for.</p>
        <p>Please see the services section for a partial list of what I can do for your company. The Portfolio section contains projects with more detail than the resume, plus sample code on GitHub. Contact: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p>
        <h2>Personal</h2>
        <ul>
          <li>Sports oriented, weight training, tennis, ping-pong, could do over 1500 push-ups in high school.</li>
          <li>Autodidact, studied many subjects in Computer Science and other subjects, continuous development.</li>
          <li>Solved Rubik's cube in middle school on average 11.2 seconds, best time 9.4 seconds. Early 80s world record was 19 seconds, 2018 record is 3.47, 2008 record was 9.18. <a href="https://www.recordholders.org/en/list/rubik.html" target="_blank" rel="noopener">Rubik's cube records</a></li>
        </ul>
      </div>
    </div>""",
            slug_path="about.html",
            description=f"About {OWNER} — software developer, autodidact, and portfolio author.",
            og_image="assets/images/hero.jpg",
        )
    )

    PROJECTS_DIR.mkdir(exist_ok=True)
    for slug in PROJECTS:
        proj = PROJECTS[slug]
        (PROJECTS_DIR / f"{slug}.html").write_text(
            page(
                proj["title"],
                "Portfolio",
                project_body(slug),
                depth=1,
                slug_path=f"projects/{slug}.html",
                description=f"{proj['title']} — {OWNER}.",
            )
        )

    stale = PROJECTS_DIR / "hypermedia.html"
    if stale.exists():
        stale.unlink()

    print(f"Generated {len(PROJECTS) + 4} HTML pages in {ROOT}")


if __name__ == "__main__":
    main()
