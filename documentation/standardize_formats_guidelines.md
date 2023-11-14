# Standardization Guidelines

Use these guidelines for assigning format types and format standardized names to new formats encountered in our holdings. 
Add these to [standardize_formats.csv](standardize_formats.csv).


## Format Type
Format type starts with MIME type categories, with additional types added where more nuance is needed for meaningful results. 
For MIME type information, see [iana.org](https://www.iana.org/assignments/media-types/media-types.xhtml) 
and [digipres.org](https://www.digipres.org/formats/mime-types/).
 
Types used (* indicates an official MIME type):

| Type            |Explanation|
|:----------------|:----|
| application*    | Formats for computing components, e.g. fonts, filesystem data, user data.|
| archive         | Packaging formats, e.g. Microsoft Cabinet, ZIP.|
| audio*          ||
| database        ||
| design          | Formats for visual design, e.g. Adobe InDesign, CorelDraw.|
| executables     | Scripts and source code.|
| geographic_data ||
| image*          ||
| message*        | Email and other communication formats.|
| model*          | Formats for 3D modeling.|
| multipart*      | Format with multiple components. Only one we have (as of 11/2020) is AppleDouble Resource Fork.|
| presentation    | Slides and other formats for supporting presentations.|
| spreadsheet     | Spreadsheet software only. Plain tabular data (e.g. CSV, tab-delimited) are in text.
| structured text | Marked up or tagged text, e.g. HTML, XML.|
| text*           | Includes plain text formats, word processing formats, and PDF.|
| video*          ||
| web_archive     | Formats specific for capturing entire websites, e.g. WARC. Formats typically used for creating websites (e.g. CSS, HTML) are in structured text since their preservation needs are more similar to that type and some of these formats have other uses in addition to websites.|

In cases where a format is assigned to multiple MIME types, choose one:
* If application or something else, pick something else.
* If audio or video, pick video.
* If one format is more complex, pick the more complex.

In cases where a format is not on the MIME type list, assign one of the MIME types or local types based on the characteristics of that format.

Application is a very broad category that hides some nuances we want to track. 
We moved some formats to more specific MIME types (e.g. PDF to text, Flash to video) and added some additional types for these formats.

## Format Standardized Name
The standard format name is based on [PRONOM](https://www.nationalarchives.gov.uk/PRONOM/). 
If it groups more related formats together, truncate the PRONOM name. 
Truncation means to use the first part of the name and remove details like version information, file counts, or macro-enabled.

If the format is not in PRONOM:
* Truncate the name if it includes format details.
* If it is a common format in our holdings, research the most common name for the format.
* Leave the name unchanged if it is uncommon in our holdings or if changing the name is unlikely to group it with other formats.

For formats where the acronym is the most commonly used name, e.g. PDF or XML, use that instead of the PRONOM name or truncation.

There are so many formats, for this standardization to be meaningful the default is to err on the side of merging more together. 
The original ARCHive format reports can be used to look at a particular grouping of formats in more detail when needed.