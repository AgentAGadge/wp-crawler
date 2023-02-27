# Issue to solve
This app should provide a tool to retrieve some data from a URL (HTML file and list of hyperlinks as a sitemap.html file), and keep that data up-to-date.

The tool must be easy to use through a back-office interface, and serve the user with the available results.

# Technical specification
See README.md - Technical Architecutre

# Technical choices
- Django framework will be used as it offers an easy-to-use MVC framework, which fits the goal of quickly setting-up a complete app with back-end logic, a database, file storage and a back-office with a login.
- The default sqlite database of Django is sufficient as the database performances and storage capacity are not at stake in this project. It is easy to set up and reliable in various environments.
- The apscheduler module will be used as it provides easy-to-use "kron jobs"-like features.
- Django login/accounts built-in system will be used as we only need to restrict access to the back-office, without advanced management.
- BeautifulSoup will be used to handle HTTPResponse and parse HTML files as this can be done with a low amount of code. It is highly customable so the project could evolve with refinements without being too limited. In the future, and as the actual crawl could require advanced customization, those features could be internally developped.

# How does it work?
See README.md

# Does it solve the user story?
<em>As an administrator, I want to see how my website web pages are linked together to my home page so that I can manually search for ways to improve my SEO rankings.</em>

Administrators now have a tool to map all pages accessible from a given one. This is a first basic tool to help users to build a map of their websites and to keep this map up-to-date

However, the answer could be improved (see README.md - Next steps). With this tool, building a complete map of a website still requires manual work: each "crawl" remains on the "origin" URL, so users have to registers all the pages of their websites if they want a complete map of the website. Additionnally, results are provided "by page", and aggregation at website level is still manual. <em>This is linked to the "keep it simple" instruction "Only crawl the home webpage, i.e. instead of recursively crawling through all of the internal hyperlinks."
</em>

Note that the current solution maps all links found in a page, without filtering out external links. Such filter is needed to fully answer the expressed need, as the administrator is not interested in links to external sites.

# What was the approach?

The request has a lot of aspects: back-office logic, database + files to store, front-end with login, etc. A framework is definetely needed to bootstrap such a project in a short time, and Django works well for this. The Django approach of MVC model works well here and the built-in back-office features can be leveraged.

Because of the variety of small topics to handle, I realized I would not be able to provide a complete, bullet-proof, well-polished answer. Therefore, I went for a MVP approach where every component is very basic and solely performs the minimum required for the complete project to be usable. I believe it demonstrates my ability to manage every part of the project better than having a wonderful back-office without any front-end, for instance. On the other hand, several aspects are far from being "state-of-the-art" grade (see README.md - Next steps) and one can probably spot issues and bugs if trying to do a bit more than the basic usage.

I decided not to go for a TDD approach. Even if it is an industry standard, it may not be well fitted to bootstrap a project, especially when trying to do it fast. 
<em>However, now that a MVP is available, robust testing with high coverage should be implemented before buliding up new features on top of this version. I started to work on this at the very end, but it is far from being complete.</em>

## First step: performing a crawl
The first step was to get a working back-end logic to perform a crawl (of a single page). While the task can sound complex,it can be broken down into basic tasks:
- Retrieve the HTML data of the page
- Search within it all the links
- Delete/Store (database and files)

All those tasks are basic features easily implemented, so I could get started.

To start fast, I started without storing the files but simply by validating that the database was correctly updated. Storing/generating files was done afterwards, once the "crawl" itself was implemented.

## Second step: Scheduling updates
Once we have a <code>crawl</code> function, it is easy to do several of them from a list of URL (the database). 

Then doing this on a hourly basis can be done through "kron-job"-like tools. I was familiar with <code>apscheduler</code>.

## Third step: Front-end
So far, I could use the <code>admin</code> buit-in page of Django to check the database entries and validate that the project worked (as well as the stored files) but this interface cannot be used easily by a non-tech person.

Therefore, I build a (very) basic back-office page to access the features. I identified two features that needed to be accessed:
- Perform a crawl and display its results: this is the first part of the home page.
- List all previous crawl results and retrieve them: this is the second part of the home page.

## Fourth step: Exception management
To make the tool more reliable and a bit more easy-to-use, I added exception managements around the riskier parts of the codebase (URL Request, File management). Those errors are leveraged up to the user interface to provide potential work-arounds.

