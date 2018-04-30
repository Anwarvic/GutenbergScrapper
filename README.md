# GutenbergScrapper
This repo contains a multi-threading scrapper for the Gutenberg's project website which contains 56,920 books free to read and download. It can scrape the whole website in just 5 hours. Also in this repo, you can find a text file containing the whole data until April 2018 containing only the _Ebook-No._, _title_, _authors_ and _language_ for every book because these attributes are the only ones that I cared about.

You can add these attributes as well:

- Subject
- LoC Class
- Category
- Release Date
- Copyright Status
- Downloads
- Price

If you want to add any of/all these attributes, you can modify the script to add whatever you want by only modifying the member variable _INCLUDE_ like so:
<pre>self.INCLUDE = set(['Title', 'Author', 'EBook-No.', 'Language'])</pre>
  
Then, run the script.

The collected data will be like this:
<pre>
ID: 1
Author: Jefferson, Thomas, 1743-1826
Title: The Declaration of Independence of the United States of America
Language: English

ID: 2
Author: United States
Title: The United States Bill of Rights
The Ten Original Amendments to the Constitution of the United States
Language: English

ID: 3
Author: Kennedy, John F. (John Fitzgerald), 1917-1963
Title: John F. Kennedy's Inaugural Address
Language: English

...
</pre>

##prerequisites

You need to install:

- Python3
- Beautiful Soap 4.0
- requests
- multiprocessing




