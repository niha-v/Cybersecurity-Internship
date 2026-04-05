# Security Assessment Report
![Role](https://img.shields.io/badge/Role-Cybersecurity%20Intern-blue?style=for-the-badge&logo=shield)
![Duration](https://img.shields.io/badge/Duration-1%20Month-green?style=for-the-badge&logo=clockify)
![Type](https://img.shields.io/badge/Assessment-Grey%20Box-orange?style=for-the-badge&logo=target)
![Scope](https://img.shields.io/badge/Scope-Web%20App%20%26%20Corporate%20Network-red?style=for-the-badge&logo=network-wired)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge)

## Overview
During a one-month cybersecurity internship, I conducted a comprehensive grey box penetration test and vulnerability assessment targeting a web application and the associated corporate network. The engagement covered the full offensive security lifecycle — from passive intelligence gathering all the way through to phishing simulation and remediation reporting.
This document details the techniques, tools, methodologies, and workflows used throughout the assessment. All client data has been fully anonymized. This report is intended as a portfolio reference and methodology showcase.

## 🎯 Scope & Objectives
 
| Parameter | Details |
|-----------|---------|
| **Assessment Type** | Grey Box Penetration Test + Vulnerability Assessment |
| **Target Surface** | Web Application & Corporate Network Infrastructure |
| **Knowledge Level** | Partial — internal documentation and basic network topology provided |
| **Primary Goal** | Identify exposed assets, enumerate attack surface, discover vulnerabilities |
| **Secondary Goal** | Simulate real-world phishing threats and test employee awareness |
| **Deliverable** | Full vulnerability report with risk-rated findings and remediation guidance |
 
---
 
## 🧭 Methodology Framework
 
This assessment followed a structured, five-phase offensive security lifecycle modeled after industry-standard frameworks including PTES (Penetration Testing Execution Standard) and the OWASP Testing Guide. The grey box approach meant I had partial knowledge of the environment — enough to simulate a realistic insider threat or a well-researched external attacker, without the full visibility of a white box test.

Each phase was designed to build on the previous one. Intelligence gathered in passive recon directly shaped what to target in active enumeration.
Enumeration results fed into the vulnerability assessment. And 
the OSINT findings — particularly exposed emails and weak email security policies — informed the entire phishing campaign design.      
 
---
 
## 🕵️ Phase 1 — Passive Reconnaissance & OSINT
 
The first phase focused on gathering maximum intelligence about the target **without touching their systems directly** — simulating what a real attacker would know before launching an attack.
 
### 1.1 DNS Analysis
 
Performed comprehensive DNS reconnaissance to map the target's infrastructure:
 
- Queried DNS records: `A`, `MX`, `TXT`, `NS`, `CNAME`, `SOA`
- Identified mail server configurations and potential misconfigurations (SPF, DKIM, DMARC)
- Attempted **DNS Zone Transfer** to check for misconfigured name servers
- Tools: `dig`, `nslookup`, `dnsx`
 
### 1.2 Domain Squatting & Spoofing Analysis
 
Analyzed the attack surface from a **brand impersonation** perspective:
 
- Identified lookalike and typosquatted domains that could be used against the organization
- Detected potential **domain spoofing** vectors by analyzing SPF/DMARC policy weaknesses
- This intelligence directly informed the phishing campaign phase
- Tools: `dnstwist`, manual review
 
### 1.3 Subdomain Enumeration
 
Conducted multi-layered subdomain discovery to map the full external attack surface:
 
- Used **bbot** for automated, recursive subdomain enumeration combining multiple passive and active sources
- Sources included: certificate transparency logs (crt.sh), DNS brute-forcing, web crawling, and third-party APIs
- Discovered development, staging, and forgotten subdomains exposing internal services
 
```bash
# Example bbot workflow (generic)
bbot -t target.com -f subdomain-enum -o output/
```
 
### 1.4 Google Dorking
 
Used advanced Google search operators to identify **publicly exposed sensitive information**:
 
| Dork Type | Purpose |
|-----------|---------|
| `site:target.com filetype:pdf` | Discover exposed documents |
| `site:target.com inurl:admin` | Find admin panels |
| `site:target.com ext:env OR ext:log` | Locate config/log files |
| `"target.com" filetype:xls` | Exposed spreadsheets |
| `intext:"index of" site:target.com` | Directory listing exposure |
 
### 1.5 File Metadata Analysis
 
Extracted **hidden metadata** from publicly available documents (PDFs, Word docs, images):
 
- Recovered author names, internal usernames, software versions, and directory paths
- Used metadata to map internal naming conventions and expand the employee wordlist
- Tools: `exiftool`, `FOCA` methodology
 
### 1.6 Breach Data Analysis — Have I Been Pwned (Custom Script)
 
Harvested employee email addresses and checked for **credential exposure in known data breaches**:
 
- Collected emails via OSINT (LinkedIn, company website, metadata)
- Built a **[HIBP Batch Checker](https://github.com/niha-v/Cybersecurity-Internship/blob/main/HIBP.py)** using the HIBP API to batch-check all discovered emails
- Identified accounts with exposed credentials from past breaches — a critical risk for credential stuffing attacks
 
---
 
## 🔬 Phase 2 — Active Enumeration & Scanning
 
### 2.1 Network Scanning with Nmap
 
Performed internal and external network scanning to identify live hosts, open ports, and running services:
 
- **Host Discovery:** Identified live hosts across the corporate network range
- **Port Scanning:** Full TCP and targeted UDP scans
- **Service & Version Detection:** Identified running services and software versions
- **OS Fingerprinting:** Determined operating system types
- **Script Scanning:** Used NSE scripts to check for common vulnerabilities
 
```bash
# Example scan types used (generic)
nmap -sV -sC -O -p- <target>          # Full version + script scan
nmap -sU --top-ports 200 <target>      # UDP top ports
nmap --script vuln <target>            # NSE vulnerability scripts
```
 
### 2.2 Cloud Infrastructure Enumeration
 
Assessed the organization's cloud footprint for **misconfigured or exposed resources**:
 
- Enumerated publicly accessible cloud storage buckets
- Checked for exposed cloud metadata endpoints
- Identified cloud-hosted assets not covered in the initial scope definition
- Tools: `cloud_enum`, `S3Scanner`, manual checks
 
### 2.3 WordPress Scanning
 
Targeted the organization's WordPress installation with dedicated scanning:
 
- Enumerated installed **plugins and themes** — including outdated and vulnerable versions
- Identified WordPress version disclosure
- Checked for exposed `wp-config.php`, `xmlrpc.php`, and backup files
- Enumerated users via the WordPress REST API
- Tools: `WPScan`
 
```bash
# Example WPScan usage (generic)
wpscan --url https://target.com --enumerate p,t,u --api-token <token>
```
 
---
 
## 🔥 Phase 3 — Vulnerability Assessment
 
### 3.1 Nessus Internal & External Scanning
 
Ran authenticated and unauthenticated **Nessus scans** against both the internal network and external-facing assets:
 
- **External Scan:** Identified internet-exposed services with known CVEs
- **Internal Scan:** Deeper authenticated scan revealing patching gaps, misconfigurations, and legacy systems
- Results included CVSS-scored findings across Critical, High, Medium, and Low severity
 
### 3.2 Nessus Results Parser (Custom Python Tool)
 
Raw Nessus output contains thousands of rows of data — difficult to use directly for reporting. I built a **[Nessus Parser](https://github.com/niha-v/Cybersecurity-Internship/blob/main/Python%20Parser.py)**
 
- Parse Nessus `.nessus` XML export files
- Filter and deduplicate findings
- Categorize by severity (Critical / High / Medium / Low)
- Output a clean, structured format (CSV/JSON) ready for reporting
 
 
> This dramatically reduced manual reporting time and improved consistency across findings.
 
---
 
## 🎣 Phase 4 — Phishing Campaign Simulation
 
Designed and executed a **controlled phishing simulation** to assess employee security awareness and susceptibility to social engineering attacks.
 
### Campaign Design
 
Three distinct phishing concepts were developed, each targeting a different psychological trigger:
 
| Campaign | Concept | Psychological Vector |
|----------|---------|---------------------|
| **Campaign 1** | IT Help Desk Password Reset | Authority + Urgency |
| **Campaign 2** | HR Policy Document Update | Trust + Routine |
| **Campaign 3** | Suspicious Login Alert | Fear + Curiosity |
 
### Tools Used
 
- **GoPhish** — campaign management, email delivery, and click tracking
- Custom HTML email templates designed to mimic legitimate internal communications
- Landing pages crafted to capture interaction data (no real credentials collected)
 
### Results (General Terms)
 
- A **measurable percentage** of employees interacted with at least one phishing email
- Campaign 3 (fear-based) achieved the **highest engagement rate**, consistent with industry research
- Results were reported to management with recommended awareness training initiatives
 
---
 
## 🛠️ Custom Tools & Scripts
 
| Tool | Language | Purpose |
|------|----------|---------|
| **[Nessus Parser](https://github.com/niha-v/Cybersecurity-Internship/blob/main/Python%20Parser.py)** | Python | Parses raw Nessus scan output into clean, reportable format |
| **[HIBP Batch Checker](https://github.com/niha-v/Cybersecurity-Internship/blob/main/HIBP.py)** | Python | Bulk-checks employee emails against Have I Been Pwned API |
 
Both scripts were written to solve real inefficiencies encountered during the engagement and significantly improved reporting speed and accuracy.
 
---
 
## 📊 Findings Summary
 
> ⚠️ *Specific findings, hostnames, CVEs, and client details are intentionally omitted to protect confidentiality.*
 
| Category | Finding Type | Severity Range |
|----------|-------------|----------------|
| Network | Outdated services with known CVEs | High – Critical |
| Web Application | Vulnerable/outdated WordPress plugins | Medium – High |
| OSINT | Employee credentials in breach databases | High |
| Cloud | Misconfigured cloud resources | Medium – High |
| Email Security | Weak SPF/DMARC policies enabling spoofing | Medium |
| Social Engineering | Employee susceptibility to phishing | High |
| File Exposure | Sensitive metadata in public documents | Low – Medium |
 
---
 
## 🔧 Remediation Approach
 
For each finding, a structured remediation recommendation was provided covering:
 
- **Short-term (Quick Wins):** Patch outdated software, enforce MFA, fix DNS policies
- **Medium-term:** Plugin audits, cloud access policy review, credential reset for breached accounts
- **Long-term:** Security awareness training program, continuous vulnerability management, phishing simulation schedule
 
Recommendations were risk-prioritized using **CVSS scores** and potential business impact.
 
---
 
## 💡 Lessons Learned
 
**What was most effective:**
- bbot's multi-source subdomain enumeration consistently surfaced assets missed by single-tool approaches
- Breach data correlation with active employee lists provided some of the highest-impact findings
- The phishing campaign produced findings that no technical scan could replicate — human behavior is a critical attack surface
 
**What I'd do differently:**
- Automate more of the OSINT phase earlier to save time for deeper manual analysis
- Build the Nessus parser before the scan (not after) to process results in real time
 
**Key takeaway:**
> The most dangerous vulnerabilities weren't always the highest CVSS score — they were the combinations: an exposed email + a breached password + a weak MFA policy = a realistic account takeover chain.
 
 
---
 
## Author

Niharika Umrani | *Cybersecurity Analyst* 


</br>






</br>

⚖️ Disclaimer
 
> This assessment was conducted as part of an authorized internship engagement. All testing was performed within an agreed scope with explicit written permission. No client data, hostnames, IP addresses, or identifying information is shared in this document. The techniques described are for **educational and portfolio purposes only**. Unauthorized use of these techniques against systems you do not have permission to test is illegal.
