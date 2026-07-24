# Development Portfolio Compilation

**Archive root:** `/media/kg/fecd6373-9e9f-486b-b9b8-f798dc71fc77/all/Development`  
**Compiled:** 2026-06-26  
**Purpose:** Exhaustive inventory of every project directory — structure, purpose, technologies, patterns, and relationships — for portfolio and resume updates.

**Author signatures found in code/docs:** Kevin Guerra, Ismael Guerra (same contributor across most professional work).

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Career Timeline & Technology Evolution](#career-timeline--technology-evolution)
3. [Cross-Portfolio Patterns](#cross-portfolio-patterns)
4. [Project Groupings & Relationships](#project-groupings--relationships)
5. [Directory-by-Directory Reference](#directory-by-directory-reference)
6. [Portfolio Highlights (Resume Bullets)](#portfolio-highlights-resume-bullets)
7. [Security & Publication Notes](#security--publication-notes)

---

## Executive Summary

| # | Directory | Files | Era | Domain | Primary Stack |
|---|-----------|------:|-----|--------|---------------|
| 01 | Access! | 0 | 2023 | Placeholder | — |
| 02 | BumperShop | 4 | 2002 | Auto shop accounting | Access |
| 03 | Disney | 1,610 | 1990s–2013 | Studio IT / deployment | VB6, VC6, ASP, Access |
| 04 | Electrosonic | 8,150+ | 1990s–2012 | Broadcast AV monitoring | MFC C++, CJ60 |
| 05 | Volt | 233 | 1990s–2009 | X.25 telecom gateway | MFC C++, LayGO |
| 06 | LaBumpers | 6,518+ | 2001–2015 | Bumper reconditioning e-commerce | GAE Java, Dart |
| 07 | PosDev | 100 | 1999–2012 | Floral POS (Palm) | Palm C, MFC |
| 08 | FotografiaBlancarte | 2 | 2002 | Photography studio | Access |
| 09 | Pleiades | 4 | 2004–2013 | Blind factory production | Access |
| 10 | TelVista | 63 | 2003–2023 | Telecom workflow consultancy | C# WinForms |
| 11 | Enigma | 33 | 2004 | Music video production | Premiere, 3ds Max |
| 12 | Nokio | 22 | 2004 | Insurance quote forms | HTML, PHP |
| 13 | PuntaBandaData | 950+ | 2003–2013 | Mexican retail POS | VB.NET, C#, SQL Server |
| 15 | HMS | 1,082 | 2003–2012 | Web application security | C++, Perl, Java, FastCGI |
| 16 | Spirent | 876+ | 2004–2006 | Telecom test automation | C++, Tcl, COM |
| 18 | DirecTV | 2,957 | 2004–2012 | STB QA automation | C/C++, Perl, ACE, OCR |
| 19 | Surfware | 28,924 | 2006–2012 | CAD/CAM (SURFCAM) | C++/CLI, MFC, Parasolid |
| 22 | Motorola | 1,071 | 2009–2011 | OCAP closed captioning | C++, KreaTV HAL |
| 23 | Yahoo | 6,269+ | ~2010s | Search engine SQA | C++, TCL, Make |
| 24 | JakeKnows | 16,755+ | 2010s | Social/contact platform | C# WCF, ASP.NET |
| 25 | OpenTV | 116 | ~2000s | TV ad scheduling | C++ VS6 |
| 26 | Google | 4,529+ | 2010s | App review / AViK | Java GAE, GWT, Dart |
| 27 | Vmware | 1,569 | ~2010s | HBR test automation | Python, YAML |
| 28 | Knurld | 1,715 | ~2010s | Voice biometrics | Python, Flask, Qt |
| 29 | Butterfleye | 948 | ~2010s | IoT camera cloud | Python, live555, Protobuf |
| 30 | Thuuz | 11 | ~2010s | Sports broadcast ingest | Python, XML-RPC, AWS |
| 32 | Chase | 573 | Dec 2017 | Game of Life interview | Java Swing |
| 33 | HiveMapper | 134 | Dec 2017–Jan 2018 | Drone pathfinding interview | C++, Boost Graph |
| — | graphics | 78 | 1997–2009 | Design assets | Photoshop |
| — | WEBSITE | 16 | 2012 | Green Leaf wellness brand | Illustrator |
| — | work | 11,768+ | 2010s | JakeKnows + career archive | C#, reference docs |

**Total tracked projects:** 31 numbered/special directories spanning ~1990s through 2023.

---

## Career Timeline & Technology Evolution

```
1990s          VB6 / VC6 / MFC / Access / Classic ASP / Palm OS
               ├── Disney studio IT, Electrosonic ESCAN, Volt X.25, PosDev Palm POS

2000–2004      .NET 1.x, SQL Server, PHP
               ├── TelVista workflow, PuntaBanda POS, Nokio insurance forms

2003–2006      Security C++, Tcl automation, telecom test
               ├── HMS libinval, Spirent TestCenter SAL, DirecTV RedRat

2006–2012      Industrial CAD/CAM, embedded TV, Yahoo search QA
               ├── Surfware SURFCAM 5-axis, Motorola CC renderer, Yahoo Inktest

2010–2015      Cloud (GAE), mobile backends, voice/IoT
               ├── LaBumpers, Google Antaeus/AViK, JakeKnows, Knurld, Butterfleye

2017–2018      Interview takehomes
               ├── Chase GameOfLife (Java), HiveMapper DroneNavigator (C++)
```

---

## Cross-Portfolio Patterns

| Pattern | Where Used |
|---------|------------|
| **Producer/consumer messaging** | Disney Generic Updater, Electrosonic SiteLinx, LaBumpers command/strategy BLL |
| **Gateway/relay** | Volt X.25→TCP, Electrosonic SiteLinx LAN→WAN |
| **Microsoft Application Blocks** | TelVista WorkFlowApp, PuntaBandaData (Data, Exception, Logging, UI Process) |
| **Strategy / command dispatch** | JakeKnows 100+ strategy operations, LaBumpers ControllerImpl, HiveMapper Planner algorithms |
| **Code generation from schema** | JakeKnowsCodeGen (SPs, web methods, table classes), Spirent XSD→C++ codegen |
| **Client/server test automation** | DirecTV dtvrrd/dtvrrc, Spirent SAL/sTcl, Vmware Gemini actor model |
| **Multi-language FFI libraries** | HMS libinval (C++ core + Perl XS + Java JNI) |
| **XML-driven plugin frameworks** | Spirent stcFramework.xml BLL, Yahoo cluster TCL configs |
| **Regression harness + deploy configs** | Yahoo Inktest, Spirent Phoenix P2 docs |
| **Rule-driven validation** | HMS PCREBinGen (XML→PCRE binary), Zeus WAF rules |
| **WCF / service-oriented backends** | JakeKnows EngineServices, TaskServices |
| **App Engine BLL + RBAC** | Google Antaeus, LaBumpers (shared patterns) |
| **Protobuf RPC over SSL** | Butterfleye camera↔cloud protocol |
| **Actor / multiton domain models** | OpenTV BLLService multiton, Vmware Gemini Machine/ReplicationGroup |

---

## Project Groupings & Relationships

### Related project clusters (same product / employer)

```
BumperShop (02) ──evolved into──▶ LaBumpers (06)
    Access MDB era                    GAE Java + Dart cloud app (labumpers.com)

Electrosonic (04) ◀──shared assets──▶ graphics/escan/
    ESCAN / SiteLinx product          UI chrome, SiteLinx user guide docs

LaBumpers (06) ◀──fork──▶ Google (26) / git/l10n-avik/
    Same business domain              Antaeus API, AndroidScreenGenerator, Bumpers1

JakeKnows (24) ═══ canonical ═══ work/JakeKnows/
    Full solution tree                Partial extracts + passport career archive
    └── work/ top-level copies: JakeKnowsWebService, JakeKnowsComponent,
        JakeKnowsEngineServices, JakeKnowsCodeGen

HMS (15) ──contractor work on──▶ Spirent (16)/hms/
    Security libraries                SAL scripting layer for TestCenter

DirecTV (18) ◀──standards overlap──▶ Motorola (22)/refs/
    CEA-608/708 CC specs              Same broadcast caption standards

Surfware (19)/new feature/ ◀──mirrors──▶ Velocity4/SCMachiningVOB/Milling/New5Axis/
    5-axis development branch         Production VOB copy

Google (26)/babel/ ◀──duplicate trees──▶ antaeus/, dart/, android/
    Multiple copies of Antaeus, Dart clients, AViK tooling

Vmware (27)/gemini/g/gemini*         Historical framework version clones

HiveMapper (33) ◀──sequential interview──▶ Chase (32)
    Dec 2017 takehomes (LinkedIn thread confirms order)

Thuuz (30)                          Minimal config-only snapshot (scoring logic not present)
```

### Solution file groupings

| Master Solution | Directory | Sub-projects |
|-----------------|-----------|--------------|
| `surfcam-msc.sln` | 19 Surfware | SCVOB + SCCommonCompVOB + SCGUIVOB + SCMachiningVOB + SCModelingVOB |
| `trnsltrs.sln` | 19 Surfware | 50+ CAD format translators |
| `TestCenter.sln` | 16 Spirent | UI + BLL + Automation + traffic plugins |
| `JakeKnowsEngineServices2012.sln` | 24 / work | Engine + WebService + CodeGen + TaskServices + installers |
| `SPAPuntaBanda.sln` + 55 `.sln` | 13 PuntaBandaData | POS suite + MS Application Blocks |
| `WorkFlowApp.sln` | 10 TelVista | C# workflow engine |
| `DynSchLib.dsp` | 25 OpenTV | TV ad scheduling static library |

---

## Directory-by-Directory Reference

---

### 01 Access!

**Status:** Empty placeholder (0 files, mtime 2023-01-02). Likely reserved for Microsoft Access projects; Access work lives under Disney `Access/` and other dirs.

---

### 02 BumperShop

**Client:** Auto body / bumper shop (precursor to La Bumpers)  
**Files:** 4 (all Access databases)

```
02 BumperShop/
├── BumperShop.mdb          (3.3 MB, 2002)
└── Accounting/
    ├── AA.MDB, AATABLES.MDB, AA_Backup.MDB
```

**Technologies:** Microsoft Access  
**Purpose:** Small-shop accounting for bumper reconditioning business.

---

### 03 Disney — Walt Disney Studio IT

**Files:** ~1,610 | **Era:** 1990s–2013

**Purpose:** Internal studio IT — software deployment, Novell admin, intranet ASP apps, OCX controls, commissary/calendar systems.

**Structure:**
```
03 Disney/
├── Access/          Projects.mdb, Menu97, AUTOUSER
├── C/               Generic Updater (Updater.c), NWConnect
├── C++/             Generic Updater 32-bit, OCX (MessageBlaster), SendMail (ATL/MFC)
├── Visual Basic/    apiary (Novell), Calendar/FIS, Commissary, Deployer, HRTS, Updater
├── WebApps/asp/     CorpPurch, HRTS, IPAging, Studio411, PeopleSoftLoginReq
├── SQL/             SQL scripts
└── graphics/        UI assets (2013)
```

**Key project groups:**

| Group | Technology | Purpose |
|-------|------------|---------|
| Generic Updater | C/C++/VB | Deploy film studio software via INI/registry; mutex `FILMISUPDATER` |
| NetWare Admin (apiary) | VB6 | Bindery, directory, print queue utilities |
| OCX / ActiveX | ATL/COM | MessageBlaster controls, SMTP mail OCX |
| Intranet WebApps | Classic ASP | Corporate purchasing, IP aging, HRTS, PeopleSoft |
| Commissary / Calendar | VB6 + Access | Studio commissary + FIS calendar |

**Technologies:** VB6, VC6 C/C++, MFC, ATL/COM/OCX, Classic ASP, Access, SQL Server, Novell NetWare API  
**Patterns:** Client/server updater, INI/registry config, producer/consumer (HRTS)  
**Author:** Kevin Guerra (Generic Updater headers)

---

### 04 Electrosonic — ESCAN Broadcast Suite

**Files:** ~8,150–13,990 | **Era:** 1990s–2012  
**Client:** Electrosonic (broadcast systems integrator)

**Purpose:** Broadcast/AV facility monitoring, scheduling, and network product distribution (ESCAN ecosystem).

**Structure:**
```
04 Electrosonic/
├── CJ60 Extension Library/    CodeJock UI framework demos
├── Clients/                   Client configs
└── ESCAN/                     Main product (~13K files)
    ├── In Progress/           Active development
    │   ├── ESCAN.dsw          Core MDI app
    │   ├── SiteLinx/          LAN/WAN distributor (TCP/IP + MAPI)
    │   ├── Scheduler/, schedulerV2/, schedule/
    │   ├── PC_Monitor/, PC_Server/, MonitorDLL/, Devices/
    │   └── CommLib/, InstallShield/
    ├── Docs/SiteLinx/         User guides
    └── Older/                 Legacy iterations
```

**Solution clusters:** ESCAN core, SiteLinx (ESCP.dsw), Scheduling, Monitoring (PC_Monitor/Server), CJ60 UI framework.

**Technologies:** VC6 MFC C++, CodeJock CJ60, MAPI, TCP/IP, InstallShield  
**Patterns:** MDI desktop apps, DLL shared libs, producer/consumer network messaging, device monitoring  
**Docs:** SiteLinx uses ES4000 protocol; addressing `[Site Name:Node Name]`; author Kevin Guerra @ electrosonic-ca.com

**Related:** `graphics/escan/` contains duplicate SiteLinx UI assets and user guides.

---

### 05 Volt — X.25 Telecom Gateway

**Files:** 233 | **Era:** 1990s–2009

**Purpose:** X.25-to-TCP/IP gateway using Emulex xp8400 + LayGO stack; MFC network management utilities.

**Structure:**
```
05 Volt/
├── X25/
│   ├── X25Relay/              Main gateway GUI (PVC-per-TCP-port)
│   ├── X25RelayService/       Windows NT service wrapper
│   ├── X25TCPClient/          TCP test client + hex editor
│   ├── CommLib/               CommLib.dll
│   └── config/                *.cfg, X25Relay.mdb
├── star/                      Star MDI app + Star.mdb
└── StarTreeList*, StarStationMgmt/   Tree-view DB utilities
```

**Technologies:** VC6 MFC, Winsock, ADO, LayGO X.25 API, NT Services  
**Patterns:** Gateway/relay, socket listeners per PVC, config-driven stack  
**Databases:** Access (X25Relay.mdb, Star.mdb)

---

### 06 LaBumpers — Bumper Reconditioning E-Commerce

**Files:** ~6,518–18,425 | **Era:** 2001–2015  
**Business:** LA Bumpers LLC (labumpers.com) — California bumper reconditioning since 1987

**Purpose:** Online catalog, production status tracking, customer portal by repair order number.

**Structure:**
```
06 LaBumpers/
├── Bumpers/                   Main GAE application
│   ├── src/com/la/bumpers/    Java backend (91 files)
│   ├── war/                   Dart→JS frontend, Bootstrap
│   ├── dart/                  Babel, API client generators
│   └── endpoint-libs/
├── git/                       Version history (Bumpers, l10n-avik, carlogo)
├── BumpersReadyingForDeployment/
├── *.mdb, *.rpt               Legacy Access + Crystal Reports
├── logos/, pic/, html/        Marketing assets
└── realestatebyelsa/          Side project
```

**Application stack:**
- **Backend:** Google App Engine Java — `ControllerImpl` (command/strategy), `ApiEndpoint` (Cloud Endpoints), Task Queue, OAuth
- **Frontend:** Dart compiled to JS, Bootstrap CSS
- **Legacy:** Access MDB, Crystal Reports, CSV exports
- **Security layer:** RBAC/MAC/DAC in BLL

**Technologies:** GAE, Java servlets, Cloud Endpoints, Dart, Python, Ruby, Access, AWS/GCP  
**Patterns:** Command/strategy BLL, async task queue, REST API, Guava EventBus  
**Related:** `git/l10n-avik/` connects to Google Antaeus work; shares domain with `26 Google`

---

### 07 PosDev — Positive Developments / Allstate Floral

**Files:** 100 | **Era:** 1999–2012

**Purpose:** Palm OS POS for floral retail + Windows GTL file transfer utility.

**Structure:**
```
07 PosDev/
├── AllState/Allstate Floral Transmit/    Palm v1
├── AllState/Allstate Floral V2/          Palm v2 + barcode (ScanMgr.lib)
├── Allstate Floral V2/                   Expanded v2 tree
└── SendGTL/                              MFC Windows app (Positive Developments)
```

**Technologies:** Palm OS C (CodeWarrior .mcp), MFC VC6, barcode scanning  
**Patterns:** Screen-based Palm UI, PDI file format, serial comms  
**Author credit:** v2.07 bug fixes by KG (Kevin Guerra)

---

### 08 FotografiaBlancarte

**Files:** 2 — `Fotografia.mdb` (2.2 MB, 2002), logo JPG  
**Purpose:** Photography studio business database (Mexican business)

---

### 09 Pleiades — Blind Factory Production

**Files:** 4 Access databases  
**Purpose:** Window shade / blind factory production tracking ("Fabrica de Persianas")

```
09 Pleiades/
└── Project 000 - Blind Factory/
    ├── Data.mdb, Program.mdb
    ├── Fabrica de Persianas - Produccion.mdb
Serializer.mdb (root)
```

---

### 10 TelVista — Telecom Workflow Consultancy

**Files:** 63 | **Era:** 2003–2023

**Purpose:** Business process automation consultancy + reusable workflow engine. Clients: TELMEX, Mexicana Airlines.

**Structure:**
```
10 TelVista/
├── WorkFlowApp/               JakeKnowsEngineServices2012-era C# WinForms
│   ├── WorkFlowApp.sln
│   ├── WorkFlowEngine.cs      (Visual UML 3.20 generated, Sept 2003)
│   └── ExceptionManagement/
├── Project 000 - Test/        TELMEX account processing prototype
├── Project 001 - Mexicana/    Mexicana Airlines appointment scheduling
└── Documentation/             Full SDLC doc set (Proposal → Testing, 11 docs)
```

**Technologies:** C# WinForms (.NET 1.x), MS Application Blocks (Data, Exception Management), SQL Server, Access  
**Patterns:** Workflow engine, UML-driven design, timer-driven record processing

---

### 11 Enigma — Music Video Production

**Files:** 33 — media only, no source code  
**Content:** 9 Adobe Premiere projects, 15 AVI renders, 7 MP3 stems, 2 3ds Max scenes  
**Purpose:** Music video edits for Enigma (electronic artist), 2004  
**Tracks referenced:** Orbital, Komodo, Timo Maas, Liquidism, Heiko

---

### 12 Nokio — Insurance Quote Forms

**Files:** 22 | **Era:** 2004

**Purpose:** Online insurance quote request forms (business, home, auto, motorcycle).

**Structure:**
```
12 Nokio/
├── *.html, *.htm              Static form pages (root)
└── nokio/                     Deployable PHP version
    ├── *insurance.php         Mail submission backend
    └── FIELDS.txt             Field schema (ALL, BUSINESS, AUTO, HOME)
```

**Technologies:** HTML forms, PHP mail(), Windows registry snippet  
**Patterns:** Form → email relay; static + PHP duplicate versions

---

### 13 PuntaBandaData — Mexican Retail POS Ecosystem

**Files:** ~950–1,268 | **Era:** 2003–2013

**Purpose:** Complete retail POS + customer/associate management for Punta Banda store (Spanish-language retail/cooperative).

**Structure:**
```
13 PuntaBandaData/
├── PuntaBanda_Data.MDF        SQL Server 2000 (1.6 GB)
├── PuntaBanda.sql             Schema scripts
├── dbPOS.mdb, POS.MDB         Access legacy
├── SPAPuntaBanda/             VB.NET SPA (address/person/postal codes)
└── Visual Studio Projects/    55 .sln files
    ├── POS/, POSvb/, POSCashRegister/
    ├── BarcodeLabelsPrinter/, Printer/
    ├── RenameFiles/, ValidationTextControl/
    └── MS Application Blocks (Data, Exception, Logging, UI Process)
```

**Solution families:** POS suite, SPAPuntaBanda, Barcode/Printer utilities, MS App Blocks infrastructure.

**Technologies:** VB.NET, C#, WinForms, ASP.NET samples, SQL Server, Access  
**Patterns:** Application Blocks, mixed VB/C# class libraries, SPA WinForms navigation  
**Database tables:** tbl_Addresses, tbl_PersonContacts, tbl_EmploymentPositions, FK relationships

---

### 15 HMS — Web Application Security

**Files:** ~1,082–1,091 | **Era:** 2003–2012  
**Domain:** Enterprise web security for HMS / exshot.com

**Purpose:** Reusable input validation library, WAF-style filtering, centralized authentication, vulnerability scanning.

**Structure:**
```
15 HMS/
├── src/libinval/              Input Validation Library (primary deliverable)
│   ├── src/, src2/            C++ core (two generations)
│   ├── perl/InVal/            Perl XS bindings
│   └── java/                  JNI Java bindings
├── src/PCREBinGen/            XML validation rules → binary .pcre
├── auth-0-7MODIFIED/
│   ├── neti/                  FastCGI auth handler
│   ├── netidb/                User DB generator (Oracle/PostgreSQL via Perl)
│   ├── savitri/               ISAPI HTTP filter + UDP log server
│   └── ip_blocker/            ISAPI IP blocking filter
├── nikto-checksites/          Custom Nikto scanner + zeus-rules.txt (900+ rules)
└── doc/                       Design docs, security guide v2.0 (Nov 2003)
```

**Technologies:** C/C++, Perl XS, Java JNI, PCRE, FastCGI, ISAPI, Xerces XML, MD5 cookies, Nikto  
**Architecture:** Multi-language FFI library; XML→PCRE rule pipeline; pre-fork FastCGI auth; defense in depth (app + edge + audit layers)  
**Author:** Ismael Guerra on primary design documents

**Notable:** 900+ Zeus WAF rules covering shell injection, path traversal, SQLi; static analysis pipeline (flawfinder, splint, ITS4, RATS).

---

### 16 Spirent — TestCenter / Phoenix P2

**Files:** ~876–4,169 | **Era:** 2004–2006  
**Domain:** Network/telecom test equipment automation

**Structure:**
```
16 Spirent/
├── mainline/                  Spirent TestCenter product source
│   ├── TestCenter.sln         Master VS2005 solution
│   ├── framework/
│   │   ├── bll/cmscore/       COM core (colib, HWMgr, Messenger)
│   │   ├── automation/scripting/stc/  Tcl scripting bridge
│   │   ├── def/stcFramework.xml     XML-driven BLL object model
│   │   └── il/                Instrument Layer (HAL, sysmgrd)
│   └── content/traffic/       L2/L3 traffic, RIP routing plugins
├── hms/                       Contractor deliverables (Ismael Guerra)
│   ├── automation/sal/        Scripting Abstraction Layer (C++ DLL)
│   └── automation/sTcl/       Tcl extension wrapping SAL
└── p2/                        Phoenix P2 architecture docs (20 files)
```

**SAL API (authored by Ismael Guerra):** `salCreate`, `salSet`, `salGet`, `salPerform`, `salReserve`, `salSubscribe`  
**Technologies:** C++, Tcl/Tk, COM/DCOM, CORBA/IDL, XML/XSD codegen, Python 2.3 build tools, ACE, CppUnit, SWIG  
**Patterns:** XML-driven plugin framework, BLL abstraction, MockServer test doubles

**Phoenix P2 docs:** Tcl DSL with create/config/get/perform/reserve/release/connect/subscribe commands.

---

### 18 DirecTV — Set-Top Box QA Automation

**Files:** ~2,957–3,087 | **Era:** 2004–2012  
**Domain:** HR20 HD-DVR functional/regression testing

**Structure:**
```
18 DirecTV/
├── redrat/                    RedRat IR remote automation (core)
│   ├── dtvrr.reactor/         ACE Reactor server (production, port 7070)
│   ├── dtvrr.ACEReactor/, dtvrr.ACE/, dtvrr.C/
│   └── DTV_RedRat/            Windows COM wrapper
├── automation/                19 OCR/screen-reader projects
│   ├── DTVOCRClient/Server/
│   ├── AbbyyOCRClient/Server/ (ABBYY FineReader)
│   └── DTVScreenReader/Scraper/ChannelNumberReader/
├── lirc/                      Linux LIRC + RedRat3 drivers
├── rrtests/                   Regression tests (LiveTV, DVR, parental controls)
├── stb_scripts/               SSH STB management
└── doc/                       CDI scripting ref, CEA-608/708, UEG UI specs
```

**RedRat script DSL:** `channel 7`, `sleep 5`, `loop 10 channel+ endl`, `keypad ~search_term`, `setredrat SN`  
**Technologies:** C, C++ ACE Reactor, Perl dtvrrc, COM/ATL OCR, LIRC, libusb, ABBYY FineReader, SSH/Expect  
**Author:** Ismael Guerra (README.redrat, 169 lines); built on John Schmerge's original RedRat code

**Regression tests:** LiveTV miniguide/favorites/search, DVR trick-play, parental controls, OSD screensaver, setup.

---

### 19 Surfware — SURFCAM Velocity4 CAD/CAM

**Files:** ~28,924–49,000 | **Era:** 2006–2012 | **Largest portfolio directory**

**Purpose:** Professional CNC programming — 2.5/3/5-axis milling, turning, EDM, post-processing, machine verification.

**Structure:**
```
19 Surfware/
├── Velocity4/                 Main product (ClearCase VOBs)
│   ├── SCVOB/SCCommon/       surfcam-msc.sln (master)
│   ├── SCCommonCompVOB/      Math, Dsp, DB, XML, Voronoi, NCData, Patterns
│   ├── SCGUIVOB/             15+ MFC dialog libraries (NCPost, MachSim, Tooling)
│   ├── SCMachiningVOB/       Milling/New3Axis, New5Axis, Turning, EDM
│   └── SCModelingVOB/        Geometry, Wireframe
├── new feature/Milling/New5Axis/   5-axis development (Ismael Guerra)
├── translators/               50+ CAD format converters (trnsltrs.sln)
├── dev/                       LicenseGeneration (Sentinel HASP), TestFarm, Digitizer
├── thirdparty/                Boost, OpenVRML, ModuleWorks, Vroni
└── archive/                   Legacy sc2000.1, FlexLM
```

**5-Axis work (Ismael Guerra):** ToolAxisDirectionLimitsParams, gouge checking, cut control — C++/CLI managed parameter classes.

**Technologies:** C++, C++/CLI, MFC, COM/ATL, DirectX, Parasolid, ModuleWorks MachSim, Sentinel HASP, InstallShield, log4c, Python post-processors  
**Patterns:** VOB modular monolith, plugin translators, managed/unmanaged interop, enterprise licensing platform

**955 total .sln/.vcproj files.**

---

### 22 Motorola — OCAP Closed Captioning

**Files:** 1,071 | **Era:** 2009–2011  
**Domain:** Motorola/Broadcom set-top platform

**Purpose:** OCAP-compliant closed captioning renderer — parse EIA-608/708 from MPEG transport streams, render via KreaTV graphics HAL.

**Structure:**
```
22 Motorola/
├── ocap/component/            libclosedcaptioningrenderer.so
│   ├── parser/                Parse608, Parse708, Window*, Commands
│   ├── eia708/                EIA708Parser, Service, Packet
│   ├── display/               TDisplay, TWindow
│   ├── font/                  TFont, TPixmapBuffer
│   ├── vbi/                   VBIManager
│   └── xds/                   XDSManager
├── ocap/tools/                CCParser debug tool (FLTK UI, mock HAL)
├── refs/                      11 CEA/EIA standard PDFs
└── streams/                   Test transport streams (.srt, .trp, .ts)
```

**Technologies:** C++ (-Werror -pedantic), KreaTV GFX HAL, FLTK, embedded Linux common.mk, Broadcom Nexus  
**Patterns:** Hysteresis-based DVS-053/157 and 608/708 auto-detection; dual-parser pipeline; mock HAL for desktop dev

**Packet formats:** DVS-157_608, DVS-053_608, DVS-053_708

---

### 23 Yahoo — Search Engine SQA

**Files:** ~6,269–11,387

**Purpose:** Yahoo Search infrastructure — regression testing (Inktest), proxy/cluster configuration, query scraping, secore C++ search engine.

**Structure:**
```
23 Yahoo/search/
├── secore/                    Search engine core (C++)
│   ├── idpd/                  IDP daemon
│   ├── libs/                  cache, rpc, logging, prisma, datahighway
│   └── proxy/modules/         blender, spellchecker, normalization
├── sqa/
│   ├── inkproxyreg/deploy_config/    50+ cluster config variants
│   └── secore/inksereg/              Inktest regression harness
├── clusterConfig-bling/       Production bling proxy configs (*.tcl)
├── alf/                       ALF framework (base, idp, tagd)
└── tools/                     scrape-bling.py, analyze-scrape.py
```

**Technologies:** C/C++, Make, TCL, Perl, Python, XML configs  
**Architecture:** Inktest pipeline (deploy → dbconverter → diffreg); TCL cluster globals + per-module .cfg; IDP proxy module pipeline

---

### 24 JakeKnows — Social/Contact Platform

**Files:** ~16,755–29,357 | **Era:** 2010s

**Purpose:** Device-centric contact management, group messaging, commerce, profile sharing ("SWaG") for mobile clients.

**Structure:**
```
24 JakeKnows/JakeKnows/
├── JakeKnowsEngineServices2012.sln    Master solution
├── JakeKnowsComponent/                Business logic + 100+ strategy operations
├── JakeKnowsEngineServices/           WCF host (PerCall, Multiple concurrency)
├── JakeKnowsWebService/               ASMX SOAP facade (~5600+ lines)
├── JakeKnowsTask*, jakeTask/          Background job processing
├── JakeKnowsCodeGen/                  Schema→SP/WS/table generator
├── JakeKnowsDataSP/                   Stored procedures
├── WindowsServiceWCF/                 Service hosting
├── ServiceStation0412/                ASMX hosting experiments
└── work/                              Deployment, headwidget, VJIL, SonyTaleo
```

**Technologies:** C# .NET 4.0, WCF, ASMX, SQL Server, log4net, ASP.NET WebForms, PHP reporting, Twilio SMS  
**Architecture:** Strategy pattern (100+ StrategyOperation enum values); code generation from SQL schema; 46 documented WS calls for mobile app  
**Integrations:** Sony Taleo HR, VJIL messaging/video, JulieKnows white-label

**Canonical copy also at:** `work/JakeKnows/` (see work section).

---

### 25 OpenTV — TV Ad Scheduling

**Files:** 116 | **Era:** ~2000s

**Purpose:** Dynamic scheduling of TV advertising spots into breaks — placement, inventory, manual overrides, customer separation.

**Structure:**
```
25 OpenTV/
├── DynSchLib/                 VS6 static library (.dsp)
│   ├── Core2/                 Refactored scheduler (SchedulingCore2, BLLService multiton)
│   ├── SchedulingCore.*       Legacy core
│   └── BreakList*, ScheduleGroup*, Finalize*, AllocateInventory*
└── bk/                        Backup Core2 work-in-progress
```

**Technologies:** C++ VS6, STL, template .inl, FSM (GroupFSM)  
**Patterns:** Multiton BLLService per order line; priority queue spot ordering; conditional DB persistence  
**Author:** KevinG @ OpenTV/NAGRA (SchedulingCore2.h)

---

### 26 Google — Antaeus / AViK / Babel

**Files:** ~4,529–18,935 | **Era:** 2010s

**Purpose:** App Engine application for reviewing mobile app screens across locales (Antaeus) + AViK automated Android screen capture + Dart web clients (Babel).

**Structure:**
```
26 Google/
├── antaeus/Antaeus/           Main App Engine project
│   ├── src/                   Java (JPA/DataNucleus, Endpoints)
│   ├── war/                   Web assets
│   ├── dart/                  Dart clients, API generators
│   └── endpoint-libs/libantaeus-v1/
├── android/AndroidScreenGenerator/   AViK screen capture (avik-2.0.jar)
├── babel/, dart/              Duplicate Antaeus/Dart client trees
├── doc/TheProject.arch        Master architecture (RBAC, OAuth2, caching, BLL flow)
└── other/                     GWT/Mvp4g samples (gwtp-samples, gwtcx, EmployeeAdmin)
```

**Antaeus architecture (from TheProject.arch):**
- App Engine: Endpoints, Memcache, Task Queues, Channels, OAuth, Mail
- BLL: Endpoint → Controller → Authority (auth hash/vector) → CRUDL + validator
- Caching: global (applications/screens/reviews) + transient background refresh
- NEW PARADIGM: simplified schema; "start a round"; RBAC with round whitelisting

**Technologies:** Java GAE, JPA/DataNucleus, GWT, Mvp4g, Dart (pub), Android/Java, Maven, Python  
**Related:** LaBumpers `git/l10n-avik/` shares Antaeus/Bumpers1 fork

---

### 27 Vmware — Gemini HBR Test Framework

**Files:** 1,569

**Purpose:** Python test automation for VMware Host-Based Replication (HBR) — orchestrates ESX hosts, replicators, disks, replication groups.

**Structure:**
```
27 Vmware/
├── gemini/gemini/             Main framework
│   ├── configuration.yaml     HBR/ESX credentials, logging, paths
│   ├── run.py                 Test runner (py.sh)
│   ├── lib/framework/         Actor model: Machine, ReplicationGroup, Disk, Factory
│   └── tests/                 host/, replicator/, image/
├── gemini/g/gemini*           Historical version clones (gemini1–gemini99)
└── Python_With_Lib/SUITE_HbrApi/   HBR API test suites
```

**Technologies:** Python 2, YAML config, unittest, VMware py.sh, Doxygen  
**Patterns:** Actor model, Factory pattern, proxy layer, configuration-driven YAML anchors

---

### 28 Knurld — VIVA Voice Biometrics

**Files:** 1,715

**Purpose:** Speaker enrollment, verification, identification, diarization platform.

**Structure:**
```
28 Knurld/knurld/
├── viva/                      VIVA platform v1.0.3 (setup.py)
│   ├── applications/
│   │   ├── slams_engine.py    Core biometrics engine
│   │   ├── viva/viva_engine.py   Qt4 desktop GUI
│   │   ├── server/slams_server.py
│   │   └── viva_webapp/       AngularJS + bower
│   ├── audiotools/            Segmentation, activity detection, resample
│   └── system_tests/nightly/
├── viva_api/                  Flask REST API 2.0.0
└── work/flask-inputs/         Flask form validation library
```

**Technologies:** Python 2.7, Flask, PyQt4, scikits.audiolab, nginx/uWSGI, RabbitMQ, AngularJS  
**Architecture:** SLAMS engine factory; layered audio pipeline; multi-app (server/API/GUI/web/PBX)

---

### 29 Butterfleye — IoT Camera Cloud

**Files:** 948

**Purpose:** Cloud backend for Butterfleye smart camera — device registration, live streaming, file sync, push notifications.

**Structure:**
```
29 Butterfleye/butterfleye/
├── live555itk/                RTSP/media streaming fork (Makefile)
└── butterfleye-cloud/
    ├── srv/butterfleye/
    │   ├── proto/bcam.proto   Camera↔Server↔App protobuf protocol
    │   ├── cs/                Camera Server (SSL, NodeId, KeepAlive)
    │   ├── datarpc/           Client API (login, start_stream)
    │   ├── filesync/          Media upload/transcode
    │   ├── notifications/     Push notifications RPC
    │   └── db/sqla/           PostgreSQL + SQLAlchemy migrations
    ├── ansible/               Deployment automation
    └── emu/                   Camera emulator
```

**Technologies:** Python 2, PostgreSQL, SQLAlchemy, Protocol Buffers, live555 RTSP, Ansible, iOS test app  
**Protocol:** SSL WAN, 4-byte length-prefixed protobuf; NodeIdRequest/Response, KeepAlive with battery/camera state

---

### 30 Thuuz — Sports Broadcast Ingest

**Files:** 11 — minimal config snapshot

**Purpose:** Broadcast ingest coordinator for sports excitement scoring infrastructure (scoring logic not present in archive).

**Structure:**
```
30 Thuuz/
├── callsigns.json             Channel registry (FS1HD, FS2HD Fox Sports)
├── director.json, director2.json
├── callsigns_server.py        XML-RPC on port 8000
├── callsigns_sync_s3.py       S3 sync stub
└── test/gets3.py, puts3.py    boto S3 utilities
```

**Technologies:** Python 2, SimpleXMLRPCServer, JSON config, boto AWS S3

---

### 32 Chase — Conway's Game of Life

**Files:** 573 (mostly Doxygen HTML) | **Date:** Dec 2017 | **Context:** Coding interview takehome

**Structure:**
```
32 Chase/GameOfLife/
├── src/                       6 Java files
│   ├── GameOfLife.java        JFrame + menus
│   ├── GameGrid.java          JPanel + thread
│   ├── Cells.java / CellsImpl.java / Cell.java / CellState.java
├── tests/                     JUnit (CellTest, CellsTest)
├── gol.jar                    Runnable JAR
├── README, HOWTO, GameOfLife_Design
└── html/                      Doxygen docs
```

**Technologies:** Java Swing, manual Thread, JUnit 4, Eclipse, Doxygen  
**Patterns:** Engine/GUI separation (Cells interface); double-buffer swap; precomputed 8-neighbor lists; toroidal wrap toggle  
**Performance:** 1,000,000 step benchmark test; early exit neighbor counting  
**Author:** Kevin Guerra (kevingnet@gmail.com)

---

### 33 HiveMapper — Drone Airport Navigator

**Files:** 134 | **Date:** Dec 20, 2017 – Jan 5, 2018 | **Context:** Hivemapper coding interview

**Structure:**
```
33 HiveMapper/HiveMapper/
├── src/
│   ├── DroneNavigator.cpp     main()
│   ├── parsed/                Input domain (Circle, World, Route) — 296 SLOC
│   ├── airport/               Graph + planning — 1,440 SLOC
│   │   ├── Planner.cpp        Dijkstra, BFS, Exhaustive
│   │   ├── Graph.*            Custom adjacency list
│   │   └── Step.*             GO/STOP/REVERSE/TRANSFER physics
│   └── utility/               ParseInputFile, Geometry — 97 SLOC
├── bin/DroneNavigator         Precompiled binary (4.7 MB)
├── case/                      LinkedIn thread, SLOCCount billing notes
└── README, DroneNavigator_Design, test_cases.txt
```

**Problem:** Navigate drone through circular airport roads in minimum time (accel/decel 1 m/s², max 4 m/s, 8s direction reversal, 0.1s transfer).

**Technologies:** C++, Boost Graph Library (dijkstra_shortest_paths), Boost Lexical Cast, Graphviz DOT, Eclipse CDT, SLOCCount  
**Algorithms:** DIJKSTRA (default), BFS (incomplete), EXHAUSTIVE (all paths enumeration)  
**Total SLOC:** 1,873 C++ | **Author:** Kevin Guerra

**Note:** `Hivemapper-Coding-Question.pdf` referenced in case files but not on disk.

---

### graphics — Design Asset Archive

**Files:** 78 | **Era:** 1997–2009

```
graphics/
├── FRUITZ*.PSD, flower*.psd, cprts*.psd   Personal art (1997–1998)
└── escan/                   Electrosonic ESCAN UI assets (56 files)
    ├── escan*.psd, sitelinx.psd, pc monitor*.psd
    ├── SiteLinx User Guide3.doc, SiteLinx User Guide4.doc
    └── eleclog-120.TIF, elogo.EPS
```

**Related to:** 04 Electrosonic ESCAN product line.

---

### WEBSITE — Green Leaf Wellness Brand

**Files:** 16 | **Era:** 2012

```
WEBSITE/
├── CATEGORIAS                 Product taxonomy (Child Health, Weight Management, etc.)
├── LOGO GREEN LEAF.jpg
└── GreenLeaf/GREEN LEAF WEB/
    ├── WEBSITE GREEN LEAF.ai  Layout design
    └── Fonts/ (Cantabile, Humanist 521 TTF)
```

**Purpose:** Design-only deliverables for Green Leaf wellness/supplements e-commerce brand. No HTML/code — Illustrator + typography assets.

---

### work — JakeKnows Platform + Career Archive

**Files:** ~11,768 | **See also:** 24 JakeKnows (canonical overlap)

**Structure:**
```
work/
├── JakeKnows/                 Master archive (~22K files in full tree)
│   └── work/JakeKnows/        JakeKnowsEngineServices2012.sln + full solution
├── JakeKnowsWebService/       Extracted ASMX subset (7 files)
├── JakeKnowsComponent/        Extracted engine component (22 files)
├── JakeKnowsEngineServices/   Extracted Windows service (5 files)
├── JakeKnowsCodeGen/          Extracted code generator (38 files)
└── passport/                  Career + technical reference archive (~975 files)
    └── files/
        ├── KGResume.doc
        ├── career_search_policy.pdf
        ├── html/              Saved algorithm/CUDA/DSP articles
        └── pdf/refs/          CEA-608/708 broadcast standards
```

**passport categories:** Career docs, algorithms (Aggregate Magic, bithacks), DSP/FFT, CUDA/GPU, assembly optimization, computer vision, broadcast standards, networking, kernel dev references.

**Security note:** `JakeKnows/labumpers/drupal/labumpers.txt` contains plaintext hosting credentials — rotate before publication.

---

## Portfolio Highlights (Resume Bullets)

Use these as starting points; tailor to each job application.

### Systems / Security (HMS, Spirent, DirecTV)
- Designed and implemented **multi-language input validation library** (C++/Perl/Java JNI) with PCRE rule compilation pipeline and 900+ WAF rules for Zeus web servers
- Built **Scripting Abstraction Layer (SAL)** for Spirent TestCenter — C++ automation API with Tcl extension, documented in Phoenix P2 architecture
- Created **RedRat IR automation framework** for DirecTV STB QA — ACE Reactor concurrent server, Perl DSL, 19 OCR verification projects, regression suite mapped to UEG specs

### CAD/CAM / Industrial (Surfware, Electrosonic, Volt)
- Implemented **5-axis milling tool axis limits and gouge checking** in SURFCAM Velocity4 (C++/CLI, ModuleWorks integration)
- Developed **ESCAN broadcast monitoring suite** — MFC MDI apps, SiteLinx LAN/WAN distributor, scheduling, device monitoring (6K+ C++ headers)
- Built **X.25-to-TCP/IP gateway** with PVC-per-port mapping, NT service wrapper, and LayGO stack integration

### Cloud / Mobile / IoT (LaBumpers, Google, JakeKnows, Butterfleye, Knurld)
- Architected **Google App Engine e-commerce platform** for automotive reconditioning — Java command/strategy BLL, Cloud Endpoints, Dart frontend, RBAC security layer
- Built **Antaeus/AViK** App Engine application for mobile screen review — JPA, OAuth2, RBAC, Memcache, Task Queues; Dart and GWT clients
- Developed **JakeKnows mobile backend** — 100+ WCF/ASMX strategy operations, SQL code generation, Sony Taleo integration
- Implemented **Butterfleye IoT camera cloud** — protobuf-over-SSL camera protocol, live555 RTSP streaming, PostgreSQL backend, Ansible deployment
- Built **Knurld VIVA voice biometrics** — SLAMS engine (enroll/verify/diarize), Flask REST API, Qt desktop GUI, Angular web app

### Embedded / TV Platform (Motorola, OpenTV, Disney)
- Implemented **OCAP closed captioning renderer** — EIA-608/708 dual-parser with hysteresis-based format auto-detection, KreaTV GFX HAL, FLTK debug tool
- Refactored **OpenTV dynamic ad scheduling library** — Core2 FSM scheduler, multiton BLLService, priority queue spot placement
- Maintained **Disney studio IT tooling** — Generic Updater deployment system, Novell admin utilities, Classic ASP intranet apps

### QA / Test Automation (Yahoo, Vmware)
- Contributed to **Yahoo Search Inktest regression** — secore engine testing, 50+ TCL cluster deploy configs, query scrape/analysis tools
- Built **Vmware Gemini HBR test framework** — Python actor model for ESX hosts, replication groups, configuration-driven YAML test orchestration

### Algorithms / Interview Projects (Chase, HiveMapper)
- **Conway's Game of Life** (Java) — engine/GUI separation, double-buffer optimization, 1M-step benchmark, JUnit test suite, Doxygen docs
- **Drone airport navigator** (C++) — Boost Graph Dijkstra on intersection graph, physics simulation (accel/decel/reversal/transfer), 1,873 SLOC in ~2 weeks

### Early Career / Full-Stack (.NET, Access, POS)
- Built **complete retail POS ecosystem** for Punta Banda — 55 VS solutions, SQL Server + Access, barcode printing, MS Application Blocks
- Developed **Palm OS floral POS** with barcode scanning (ScanMgr) and **C# workflow engine** for TelVista (TELMEX, Mexicana Airlines clients)

---

## Security & Publication Notes

Before using this archive in a public portfolio:

| Risk | Location | Action |
|------|----------|--------|
| AWS/GCP private keys (.pem) | 06 LaBumpers/ | Remove or redact |
| SQL connection strings | JakeKnows source configs | Redact |
| Hosting credentials | work/JakeKnows/labumpers/drupal/labumpers.txt | Rotate + redact |
| AWS credentials | 30 Thuuz/.aws/ | Do not publish |
| Hardcoded auth secrets | 15 HMS/neti/ | Reference architecture only |

**Missing artifacts referenced but not on disk:**
- `Hivemapper-Coding-Question.pdf` (33 HiveMapper/case/)
- `01 Access!` is empty

**Duplicate trees (same project, multiple copies):**
- JakeKnows: `24 JakeKnows/` vs `work/JakeKnows/` vs `work/JakeKnows*`
- Google Antaeus: `26 Google/antaeus/`, `babel/`, `dart/`, `android/`
- Surfware 5-axis: `new feature/` vs `Velocity4/SCMachiningVOB/Milling/New5Axis/`
- Vmware Gemini: `gemini/g/gemini1` through `gemini99`

---

*End of compilation. Generated from exhaustive filesystem analysis, source header review, and documentation extraction across all Development subdirectories.*
