zOpen Directory

VERSION

Initial realease: 0.3

zOpen Directory works on Zope 2.3.3. We think it should work with 2.4

zOpen Directory needs two additional Zope Products to work: the PathHandler (http://www.zope.org/Members/NIP/PathHandler) and Localizer (downloadable from http://sourceforge.net/projects/lleu). 

Our version works as tested with PathHandler 0.9.0 and Localizer 0.5

INSTALLATION

First, you should install PathHandler and Localizer.

Then install px6.py in ...

DISCLAIMER: If you have a look at the Python code there, you may cry horrified at what you see... Sure: it's the most awful piece of written code you ever saw. Well, it's all Luistxo's fault (Luistxo@eibar.org). I'm no programmer at all. I am a journalist with no technical background, and I began programming for the first time in my life in february 2001, at the advanced age of 34, and finished that Python parser two months later... Even after that, things like modules, functions, imports and classes sound like greek to me. However, this little monster that I created somehow manages to work. I suppose any Python programmer could do the same in just 30 minutes with %10 of lines... Well, I release zOpen Directory under GPL, hoping someone may help improving the code... Feedback is welcomed.

Then uncompress zOpenDirectory.zexp and place it wherever you want. You may rename the folder, but if you do so, then in Properties you should also rename the dir_name string with the folder name that you choose.

IMPORTANT NOTE: In order to manage zOpenDirectory, it will not work in the usual "zOpenDirectory/manage" or "RenamedFolder/manage", but, as it happens when Localizer is involved, you have to manage the folder this way: "zOpenDirectory/Z/manage" or "RenamedFolder/Z/manage"

And there you have it, zOpenDirectory is visible and working in 8 languages (in order to work, you need a running connection to the Internet).

WHAT IS zOpen Directory?

zOpen Directory lets you integrate the whole content of the Open Directory Project (ODP, http://dmoz.org) into your Zope website. It's a remote parser. So no database has to be downloaded. Each click or query is sent to Dmoz.org, and results are parsed and recreated for Zope.

The zOpen Directory interface and usage has one additional feature you don't see in the original ODP: it has two fixed search options, with two buttons.

The first button is the restricted search option. The second one searches the whole directory. That way, you may choose a German-only search option... Each locale may have it's own restricted search option, not necessarily coincidental with the language. That is, you may have use the German locale with a German interface, yet the restricted search option may be used for the World/Français category or Arts/Music... 

In the English locale, the default restricted search option is pre-set for Computers... But you can change that. You may set it to Arts/Music and then you have a Music Directory for Zope... 
The options that appear in the search buttons and the restriction option are defined by locale. 

LOCALIZED STRINGS

If you view the DTML methods included in zOpen Directory, you will see a bunch of variables like this one: <dtml-var "gettext('zNextSites')">

Well, Localizer detects those gettext strings and produces the right localized string. To modify the strings, go to the Localizer folder and modify the strings at Localized Strings. 

All gettext strings at zOpen Directory begin with z (like 'zNextSites'), so you can easily detect them. But there are 3 gettext strings that do not begin with z, and they are important. Those are the button strings, and the restriction string.
<dtml-var "gettext('button1')">
<dtml-var "gettext('button2')">
<dtml-var "gettext('Restricted')">

These particular strings are important. For instance, you want your restricted search option in English to be Music and not Computers, as it is preset in zOpen Directory. How to modify that? Go to the Localizer folder, click Localized Strings, choose the Restricted string, and set the English string to Arts/Music. Then choose the 'button1' string, change it (you may write, for instance, 'Find all about Music' or 'I'm feeling musical' or...), and there it is. Of course, you should also change the index_html page that... That's in the next chapter: entry page customization.

NOTE: Take care of non-ascii characters if your Restricted search option category includes them. So, if you want a Québécois searching option, you should set the Restricted string like this:
'World/Fran%e7ais/R%e9gional/Am%e9rique/Canada/Qu%e9bec'

ENTRY PAGES.

You will see that zOpen Directory has two main pages. One is the Locale Entry Page and the other one the Top page. 

You may customize every Locale Entry modifying the index_html page that is located inside every locale folder, which in turn are located inside the Localizer folder.

The Top page is unique for all locales, and it's based in the home_page DTML method. You may customize that as you like.

Besides the entry pages, zOpen Directory has two kind of pages that result from parsing the original ODP content, the Category Pages and the Search Result Pages.

HEADER AND FOOTER

* The standard_html_header includes:
zodp_title --> This creates the page Title.
charset --> Chooses the appropiate charset for every World version of Dmoz. It seems that zOpen Directory works fine displaying Russian, Korean...

The header calls a CSS style sheet, which is zodp_styles. 

* The Footer includes the 'zAtt' gettext string inside a table. You should not remove that table. The ODP is open content, but the license demands that an attribution to ODP and a link to it should be made. The attribution text is already localised in zOpen Directory, and that's what you get with the 'zAtt' gettext string. 

CATEGORY PAGES

Category pages are created following the template at the 'odp' DTML method.

The different components are as follow:

The functions variable. Shows clickable feedback options, and the editors of the page (if present). You may also check the functions DTML method to customize this.ç

The path variable. You may also check the path DTML method to customize this.

The alphabar (a series of alphabetical subcategories, if present).

The first_subcats variable: Shows a pre-sorted block of subcategories. If present, each element is composed by the 3 items:
['sequence-item'][0] is the subcategory link
['sequence-item'][1] is the subcategory name
['sequence-item'][2] is the number of links present in the subcategory.

The main_subcats variable: Shows the main block of subcategories. If present, each element is composed by the 3 items:
['sequence-item'][0] is the subcategory link
['sequence-item'][1] is the subcategory name
['sequence-item'][2] is the number of links present in the subcategory.

The related_cats variable: Shows the block of related categories (marked in dmoz by 'see also'). If present, each element is composed by the 3 items:
['sequence-item'][0] is the subcategory link
['sequence-item'][1] is the subcategory name
['sequence-item'][2] is the number of links present in the subcategory.

The site variable: Shows the block of sites in this category. If present, each element in sites  consists of 4 items:
['sequence-item'][0] is the site URL
['sequence-item'][1] is the site title
['sequence-item'][2] is the site description.
['sequence-item'][3] is the "cool" mark. If absent, nothing appears. If present, the localised string given by the 'zCool' gettext string is rendered.

the alt_lang variable: Thos is the block for related categories in other languages. If present, each element in alt_lang consists of 3 items:
['sequence-item'][0] is the subcategory link
['sequence-item'][1] is the subcategory name
['sequence-item'][2] is the number of links present in the subcategory.
(In zOpen Directory, we have place this variable below the sites. In the original Dmoz, the order is inverse. You may set what you like changing the odp DTML method)

SEARCH RESULT PAGES

Search result pages are created following the template at the 'searchAnswers' DTML method. The different components are as follow:

The term variable: what you searched. If it's a restricted search (button1 was clicked), gettext strings are rendered that indicate that.

The cats variable: The block of found categories. If present, car_number and cats_overall also appear; cat_number is the number of categories present in the page, like '1-5' in ('1-5 of 12'), and cats_overall is the total number of found categories, like '12  in ('1-5 of 12')
Then, each element in the block consists of 3 items:
['sequence-item'][0] is the link to the category
['sequence-item'][1] is the name of the category
['sequence-item'][2] is the number of links present

The more_cats variable: This will appear as a clickable link, if there are more categories found than those present in the page.

The sites variable. The block of found sites. If present, site_number and sites_overall also appear; site_number is the number of sites present in the page, like '1-20' in ('1-20 of 123'), and sites_overall is the total number of found sites, like '123  in ('1-20 of 123')
Then, each element present consists of 5 items:
['sequence-item'][5] is the indicator for a Cool site. If present, the localised string given by the 'zCool' gettext string is rendered.
['sequence-item'][0] is the site URL
['sequence-item'][1] is the site title
['sequence-item'][2] is the site description
['sequence-item'][3] is the site's category link
['sequence-item'][4] is the site's category name

The next_sites variable: This will appear as a clickable link, if there are more sites found than those present in the page.

OTHER STUFF

There are other DTML methods in zOpen Directory, like parseCat, parseResult and some other. You don't need to worry about them, they work fine, thanks.

The searchForm DTML method lets you transform the searchbox. Do not alter the 'button1' and 'button2' gettext strings that are present there. To adapt the text of the buttons, remember, you must go to Localized Strings area of the Localizer folder.

DEALING WITH LANGUAGES...

For monolingual Zope websites, go to Properties at the Localizer folder, and leave only your  language locale of choice at available_languages.

To create additional language interfaces, go to the Localizer folder and click in Add Language... Then, go to properties and mark the locale in supported_languages and available_languages.

Then, get all those localized strings and translate them. Remember: all begin with z, except button1, button2 and Restricted. Also, you should also create a customized Entry page, name it index_html and place it in the precise locale folder at the Localizer folder.

MARKING STYLES

The zodp_styles DTML document is the CSS style sheet guide for zOpen Directory. You can change the look of the category and result pages just transforming the styles in this DTML document.

The following styles are used for...

.link --> Site titles.
.linkcat --> Category names associated to sites found in results. Also for categories in "other languages" and for 2nd level categories in the entry pages.
.linktxt --> Site descriptions.
.cat --> Category names
.button --> applied to search buttons.
.cool --> applied to the 'zCool' gettext string.
.path1 --> applied to the first elements of the category path
.path2 --> applied to the last element of the category path
.section --> Marks the main blocks in which pages are divided.
.numbers --> used for number of links, etc.
.result1 --> used in the result pages to mark several texts (links to additional pages, for instance).
.result2 --> marks the searched term in results.
.function1 --> marks the zEditors and zThisCat gettext strings in functions variable.
.function2 --> marks the strings for functionalities and the editor names in functions variable.





