# GPO Duplicate Bib Record Finder
Extracts data from Alma from the 035, 245, 856, and 956 to look for duplicate GPO records for cleanup 

(We found that while some records had an OCLC number and others had a GPO number, the string of numbers at the end of the URL in the 856 seemed to be a common identifier regardless of the record source or specific URL)

# Requirements:
- Alma Bibs API Key for where the Bibs live (for shared bibliographic enviroments, NZ key is recommended)
- Input file of MMS IDs in Excel format (code needs to be altered if you wish to use other formats)
