import urllib, string, re#, botlib
import socket

if hasattr(socket, 'setdefaulttimeout'):
    socket.setdefaulttimeout(20)
else:
    try:
        import timeoutsocket # http://www.timo-tasi.org/python/timeoutsocket.py
        timeoutsocket.setDefaultSocketTimeout(10)
    except ImportError:
        pass 

# /A/">  alphabar detektorea.

# :</td> honek detektatzen du beste hizkuntzekoak
# :<ul> honek detektatzen see also
# <li><a href="http://  --> honek linkak badaudela
# hr-ak 5badira, badago bloke selektoa
# hr-ak 4 badira, eta ez badago linkik, badago bloke selektoa
# "text/html; charset= honek detektatzen du charseta.
# <li><a href="/  --> catak badaude
# editorcount == 0, editorea behar da, editorcount > 0, orduan badaude editoreak.
# <a href="desc.html">
# <a href="faq.html">
# /cgi-bin/add.cgi?where=
# /cgi-bin/update.cgi?where=
# /cgi-bin/apply.cgi?where=
# /cgi-bin/feedback.cgi?where="  --> hau beti dago. Honekin detektatzen dugu zein den path-a.
#                 eta baita bidean jarri beharreko url-ak
# name=cat value="World"> --> honekin detektatzen dugu bidearen, testua.
# text/html; charset= --> honek detektatzen du balekoa ote den, eta charseta zein den.


#cleanUtf da garbitzeko emaitzetan helbideak
#d%c3%b1 Ã± ñ %f1
#%c3%a1 Ã¡ á %e1
#%c3%a9 Ã© é %e9
#%c3%ad Ã­ í %ed
#%c3%b3 Ã³ ó %f3
#%c3%ba','Ãº', ú %fa
#%c3%a7 Ã§ ç %e7
#h%c3%b4 Ã´ ô %f4

def cleanUtf(t):
    t=re.sub('%c3%b1','%f1',t)
    t=re.sub('%c3%a1','%e1',t)
    t=re.sub('%c3%a9','%e9',t)
    t=re.sub('%c3%ad','%ed',t)
    t=re.sub('%c3%b3','%f3',t)
    t=re.sub('%c3%ba','%fa',t)
    t=re.sub('%c3%a7','%e7',t)
    t=re.sub('%c3%b4','%f4',t) 
    return t

def lema(t):
    t = t.lower()
    t=re.sub(' ','+',t)
    hiztegia = {
        'egia' : 'egia*',
        'altza' : 'altza*',
        'eta' : 'eta'
        }
    if hiztegia.has_key(t):
        return hiztegia[t]
    if t[-1:] == 'a':
        return t[:-1]+'*'
    elif t[-1:] == '*':
        return t
    elif t[-2:] == 'ak':
        return t[:-2]+'*'
    else:
        return t+'*'


def localize(loc):
    locales = {
        'en': ['Add URL', 'Update URL', 'Category Description', 'FAQ', 'Become an Editor', 'Edit', 'Editors', 'This category needs an Editor', 'See also', 'This category in other languages', 'Categories', 'Sites', 'Search results for gas*', 'Categories (1-5 of 500)', 'More Categories', 'Next Sites', 'Only in'],
        'ca': ['Afegeix un URL', 'Actualitzar un URL', 'Descripció', 'FAQ', 'fes-te editor', 'edita ', 'Editors de la categoria', 'Aquesta categoria necessita un editor', 'Mira també', 'Aquesta categoria en altres idiomes', 'Categories', 'Webs', 'Resultats de la Recerca: ', 'de ', 'Següents', 'Següents', 'només a'],
        'fr': ['Proposer un site', 'mettre à jour l\'URL', 'Description', 'FAQ', 'Devenir éditeur', 'éditer', 'Editeurs de la catégorie ', 'Cette catégorie attend un éditeur', 'Voir également', 'Cette catégorie en d\'autres langues ', 'Catégories ', 'Sites ', 'Résultats  ', 'sur ', 'Page suivante', 'Page suivante', 'uniquement dans a'],
        'de': ['URL hinzufügen', 'URL aktualisieren', 'Beschreibung', 'FAQ', 'werde Editor', 'editieren', 'Kategorie-Editoren', 'Diese Kategorie braucht einen Editor', 'Siehe auch', 'Diese Kategorie in anderen Sprachen', 'Kategorien ', 'Sites ', 'Suchergebnis', 'von ', 'Weitere Kategorien anzeigen', 'Weitere 20 Einträge anzeigen', 'nur in'],
        'it': ['aggiungi URL', 'aggiorna URL', 'Descrizione', 'FAQ', 'diventa editore', 'modifica', 'Editori della categoria', 'Questa categoria ha bisogno di editori', 'Vedi anche', 'Questa categoria in altre lingue', 'Categorie ', 'Siti ', 'Risultati trovati per', 'su ', 'Vai ai prossimi 25 risultati', 'Vai ai prossimi 20 risultati', 'solo in'],
        'nl': ['voeg URL toe', 'verander URL', 'Omschrijving', 'FAQ', 'word redacteur', 'aanpassen', 'Redacteuren van deze categorie:', 'Deze categorie heeft een redacteur nodig', 'Zie ook', 'Deze categorie met sites in andere talen', 'Categorieën', 'Sites', 'Resultaten met', 'van ongeveer', 'Vai ai prossimi 25 risultati', 'Vai ai prossimi 20 risultati', 'alleen in'],
        'pt': ['adicionar sítio', 'actualizar o sítio', 'Descrição', 'FAQ', 'Tornar-se editor', 'editar', 'Redacteuren van deze categorie:', 'Esta categoria necessita um editor', 'Veja também', 'Esta categoria noutros idiomas', 'Categorias', 'Sítios', 'Resultado da busca para ', 'de', 'Próximas 25', 'Próximos 20', 'somente dentro de'],
        'eu': ['Lotura bat gehitu', 'Lotura bat eguneratu', 'Azalpena', 'FAQ (Galderak)', 'Editore bihur zaitez', 'editatu', 'Editoreak ', 'Atal honek editorea behar du', 'Ikus halaber', 'Atal hau beste hizkuntza batzuetan ', 'Atalak ', 'Guneak ', 'Zera bilatu dugu', '; guztira: ', 'atal gehiago', 'gune gehiago', 'soilik hemen']
        }
    loctext = locales[loc]
    return loctext


def erdu(t):
    t = re.sub('Euskadi','Oklahoma',t)
    t = re.sub('Eusko','Oklahomako',t)
    t = re.sub('Eusk','Erd',t)
    t = re.sub('eusk','erd',t)
    return t
    
def alphabar(path, url):
    resu = ''
    abc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    for item in abc:
        resu = resu + '| <a href="'+url+'/'+path+'/'+item +'/"><b>'+item+'</b></a>\n'
    return resu+'|'
    
def cleanPath(path):
    localize = {
        'Armenian' : 'ArmSCII-8',
        'Bulgarian' : 'ARRAY(0X3BEC80)',
        'Chinese_Traditional' : 'BIG5',
        'Japanese' : 'EUC-JP',
        'Korean' : 'EUC-KR',
        'Chinese_Simplified' : 'GB2312',
        'Simplified_Chinese' : 'GB2312',
        'Magyar' : 'ISO-8859-2',
        'Polska' : 'ISO-8859-2',
        'Slovensky' : 'ISO-8859-2',
        'Croatian' : 'ISO-8859-2',
        'Rom\342n\343' : 'ISO-8859-2',
        'Esperanto' : 'ISO-8859-3',
        'Hebrew' : 'ISO-8859-8',
        'T\374rk\347e' : 'ISO-8859-9',
        'Belarusian' : 'KOI8-F',
        'Russian' : 'koi8-r',
        'Thai' : 'TIS-620',
        'Farsi' : 'UTF-8',
        'Czech' : 'WINDOWS-1250',
        'Slovensko' : 'WINDOWS-1250',
        'Bosnian' : 'WINDOWS-1250"',
        'Ukrainian' : 'WINDOWS-1251',
        'Greek' : 'windows-1253',
        'Arabic' : 'WINDOWS-1256',
        'Eesti' : 'WINDOWS-1257',
        'Latvian' : 'WINDOWS-1257',
        'Lietuviu' : 'WINDOWS-1257'
        }
    charset = 'ISO-8859-1'
    if len(path) == 1:
        return charset, path[0]
    if path[0] == 'World':
        if localize.has_key(path[1]):
            charset = localize[path[1]]

    bidea = string.join(path,'/')
    return charset, bidea    

        
def atala(url):

    def parse_first(url):

        det_nopage = -1
        hrcount = 0
        coolcount = 0
        det_charset = -1
        det_add = ''
        det_update = ''
        det_apply = ''
        det_desc = ''
        det_faq = ''
        det_lang = -1
        det_see = -1
        det_alphabar = -1

        det_links = 0
        det_subs = 0
        dena = ''
        editore = ''
        tex_charset = ''
        tex_path1 = ''
        tex_path2 = ''
        pu = string.find(url, '//dmoz.org/')
        pu2 = string.find(url, '/index.html')
        path00 = url[pu+11:pu2]


        
        f = urllib.urlopen(url)
        
        
        lines = f.readlines()
        for line in lines:
            line = unicode(line,'utf-8')
            line = re.sub('<', '\n<', line)
            line = re.sub('>', '>\n', line)
            line = re.sub('\n\n', '\n', line)
            
            if string.find(line, 'text/html; charset=') != -1:
                det_charset = 1
                tex_charset = line
                tex_charset = re.sub('"', '=', tex_charset)
                tex_charset = string.splitfields(tex_charset, '=')
                tex_charset = tex_charset[-2:-1]
    
#'''            if string.find(line, 'feedback.cgi?where=') != -1:
#                tex_path1 = line
#                tex_path1 = re.sub('"', '=', tex_path1)
#                tex_path1 = string.splitfields(tex_path1, '=')
#                tex_path0 = tex_path1[-2:-1]
#                tex_path1 = string.splitfields(tex_path0[0], '/')
    
                
            if string.find(line, 'name=cat value="') != -1:
                tex_path2 = line
                tex_path2 = re.sub('"', '=', tex_path2)
                tex_path2 = string.splitfields(tex_path2, '=')
                tex_path2 = tex_path2[-2:-1]
                tex_path2 = string.splitfields(tex_path2[0], '/')
    

            if string.find(line, 'The page you attempted to access does not exist') != -1:
                det_nopage = 1                
                
            if string.find(line, 'add.cgi?where=') != -1:
                det_add = 'http://dmoz.org/cgi-bin/add.cgi?where='+path00    
            if string.find(line, 'update.cgi?where=') != -1:
                det_update = 'http://dmoz.org/cgi-bin/update.cgi?where='+path00    
            if string.find(line, 'apply.cgi?where=') != -1:
                det_apply = 'http://dmoz.org/cgi-bin/apply.cgi?where='+path00        
            if string.find(line, '<a href="desc.html">') != -1:
                det_desc = 'http://dmoz.org/'+path00+'/desc.html'
            if string.find(line, '<a href="faq.html">') != -1:
                det_faq = 'http://dmoz.org/'+path00+'/faq.html'
            if string.find(line, ':\n</td>') != -1:
                det_lang = 1
                line = re.sub(':\n</td>', ':\n</td><!--end2--><!--langhas-->',line)
    
            if string.find(line, ':\n<ul>') != -1:
                det_see = 1
                line = re.sub(':\n<ul>', ':\n<ul><!--end2--><!--seehas-->',line)
    
            if string.find(line, '/L/">') != -1:
                det_alphabar = det_alphabar+1
            if string.find(line, '/O/">') != -1:
                det_alphabar = det_alphabar+1
            if string.find(line, '<li>\n<a href="http://') != -1:
                det_links = det_links+1
                line = re.sub('<li>\n', '\n<!--end2-->\n<li>\n',line)
            if string.find(line, '<li>\n<a href="/') != -1:
                det_subs = det_subs+1
            if string.find(line, '<hr>') != -1:
                line = re.sub('<hr>', '<!--end--><!--end2-->\n<hr>\n<!--hrcount'+repr(hrcount+1)+'-->',line)
                hrcount = hrcount+1
            if string.find(line, 'img/star.gif') != -1:
                coolcount = coolcount+1
            if string.find(line, 'href="/profiles/') != -1:
                editore = editore + line
            dena = dena + line
            
        editors = string.splitfields(editore, '\n')
        editors.sort()
        editorcount = editors.count('</a>')
        if editorcount == 0:
            editors = ''
        else:
            editors = editors[-editorcount:]
            
            
        

        if det_charset != 1:
            charset = -1


        if hrcount == 5:
            del_selecto = 1
        elif hrcount == 4 and det_links == 0:
            del_selecto = 1
        else:
            del_selecto = -1
    
        funtz = [det_apply, det_add, det_update, det_faq, det_desc]
        
        return dena, del_selecto, det_subs, det_see, det_lang, editors, path00, funtz, tex_path1, tex_path2, det_links, hrcount, det_alphabar, tex_charset, det_nopage
    

    
    
    def subs_atera(testua, nondik, noraino, zer):
        pbai = -1
        pstop = -1
        subs_text = ''
        for item in testua:
            if pbai == 1 and pstop != 1:
                subs_text = subs_text + item
                if item.find(noraino) != -1:
                    pstop = 1
            if item.find(nondik) != -1:
                pbai = 1
        subs_text = subs_text.split(zer)
        subs_text = subs_text[1:]
        return subs_text
        

    def garbitu(item0):
        p1 = string.find(item0, 'href="/')
        p2 = string.find(item0, '">')
        p3 = string.find(item0, '</a>')
        p4 = string.find(item0, '<i>')
        p5 = string.find(item0, '</i>')
        if string.find(item0, '@ &nbsp;') != -1:
            item2 = item0[p2+5:p3-4]+'@'
        else:
            item2 = item0[p2+5:p3-4]
        return item0[p1+6:p2], item2, item0[p4+3:p5]


    
    def garbitu2(item0):
        p1 = string.find(item0, 'href="/')
        p2 = string.find(item0, '">')
        p3 = string.find(item0, '</a>')
        p4 = string.find(item0, '<i>(')
        p5 = string.find(item0, ')</i>')
        return item0[p1+6:p2], item0[p2+2:p3], item0[p4+3:p5+1]
    
    def garbitu3(item0):
        pstar = string.find(item0, 'img/star.gif')
        item0 = re.sub('<!--end2-->','',item0)
        if pstar != -1:
            item0 = re.sub('<b>', '"', item0)
            item0 = re.sub('</b>', '"', item0)
            pdes = string.find(item0, '""> &nbsp; ')+14
        else:
            pdes = string.find(item0, '</a>')+7
        p1 = string.find(item0, 'href="/')
    
        p2 = string.find(item0, '">')
        p3 = string.find(item0, '</a>')
        p3b = string.find(item0, ' - ', p3)
        p5 = string.find(item0, '<p>')
        p6 = string.find(item0, '</ul>')
            
        if p5 == -1 and p6 ==  -1:
            p_final = len(item0)
        elif p6 != -1:
            p_final = p6
        else:
            p_final = p5
        return item0[p1+10:p2], item0[p2+2:p3], item0[p3b:p_final] , pstar
        

    
    def bide_atera(testua, nondik, zer):
        pbai = -1
        pstop = -1
        subs_text = ''
        for item in testua:
            if pbai == 1 and pstop != 1:
                subs_text = subs_text + item
                if string.find(item, '</i>') != -1:
                    pstop = 1
            if string.find(item, nondik) != -1:
                pbai = 1
        subs_text = string.splitfields(subs_text, zer)
        subs_text = subs_text[1:]
        return subs_text


    
    def garbide1(item0):
        p1 = string.find(item0, 'href="/')
        p2 = string.find(item0, '">')
        return item0[p1+6:p2], item0[p2+2:], ''
        
    def garbide2(item0):
        p1 = string.find(item0, '</b>')
        p2 = string.find(item0, '<i>(')
        p3 = string.find(item0, ')</i>')
        return item0[1:p1], item0[p2+4:p3], ''


    try:
        a = parse_first(url)
    except:
        a=['kk', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1]

    a2 = string.splitfields(a[0],'\n')
    
    det_selecto = a[1]
    det_subs = a[2]
    det_see = a[3]
    det_lang = a[4]
    editors = a[5]
    pathon = a[6]
    funtz = a[7]
    path1 = a[8]
    path2 = a[9]
    zenbatlink = a[10]
    
    hrcount = a[11]    
    alphabar = a[12]
    charset = a[13]
    
    if a[14] == 1:
        return ''
    
    othersubs_bis = -1
    selecto_bis = -1
    catmarkasubs = '_'
    
    if det_see != -1:
        catmarka = '<!--seehas-->'
        catmarkasubs = '<!--seehas-->'
    elif det_lang != -1:
        catmarka = '<!--langhas-->'
	catmarkasubs = '<!--langhas-->'
    else:
        catmarka = '--hrcount'+repr(hrcount-2)+'--'
        catmarkasubs = '--hrcount'+repr(hrcount-1)+'--'

    
    if zenbatlink < 1:
        link_bis = -1
        if hrcount < 3:
            othersubs_text = subs_atera(a2, '<hr>', '--hrcount2--','<li>')
            othersubs_bis = map (garbitu, othersubs_text)
        elif hrcount == 3 and det_see != -1:
            othersubs_text = subs_atera(a2, '<hr>', catmarka,'<li>')
            othersubs_bis = map (garbitu, othersubs_text)
        elif hrcount == 3 and det_lang != -1:
            othersubs_text = subs_atera(a2, '<hr>', catmarka,'<li>')
            othersubs_bis = map (garbitu, othersubs_text)
        elif hrcount == 3:
            othersubs_text = subs_atera(a2, '<hr>', '--hrcount'+repr(hrcount-1)+'--','<li>')
            othersubs_bis = map (garbitu, othersubs_text)
                    
        elif hrcount == 4:
            othersubs_text = subs_atera(a2, '--hrcount2--', catmarkasubs,'<li>')
            othersubs_bis = map (garbitu, othersubs_text)
            selecto_text = subs_atera(a2, '--hrcount1--', '--hrcount2--','<li>')
            selecto_bis = map (garbitu, selecto_text)
        else:
            othersubs_text = subs_atera(a2, '--hrcount3--', catmarka,'<li>')
            othersubs_bis = map (garbitu, othersubs_text)
            selecto_text = subs_atera(a2, '--hrcount1--', '--hrcount3--','<li>')
            selecto_bis = map (garbitu, selecto_text)
    else:
        linkmarka = '--hrcount'+repr(hrcount-2)+'--'
        link_text = subs_atera(a2, linkmarka, '--end--', '<li>')
        link_bis = map (garbitu3, link_text)
        if hrcount < 5:
            othersubs_text = subs_atera(a2, '<hr>', catmarka,'<li>')
            othersubs_bis = map (garbitu, othersubs_text)
        elif hrcount == 5:
            othersubs_text = subs_atera(a2, '--hrcount2--', catmarka,'<li>')
            othersubs_bis = map (garbitu, othersubs_text)
            selecto_text = subs_atera(a2, '--hrcount1--', '--hrcount2--','<li>')
            selecto_bis = map (garbitu, selecto_text)
        else:
            othersubs_text = subs_atera(a2, '--hrcount3--', catmarka,'<li>')
            othersubs_bis = map (garbitu, othersubs_text)
            selecto_text = subs_atera(a2, '--hrcount1--', '--hrcount3--','<li>')
            selecto_bis = map (garbitu, selecto_text)
            
    

    

    
    ######
    if det_lang == 1:
        lang_text = subs_atera(a2, '--langhas--', '--end--', '<td>')
        lang_bis = map (garbitu2, lang_text)
    else:
        lang_bis = -1
    
    if det_see == 1:
        see_text = subs_atera(a2, '--seehas--', '--end2--','<li>')
        see_bis = map (garbitu, see_text)
    else:
        see_bis = -1
    
    
      
    
    funtz.append('http://dmoz.org/editors/editcat.cgi?cat='+pathon)

    
#    bide_text = bide_atera(a2, 'Top', '</a>')    

    if pathon == 'Kids_and_Teens':
        bide_bis = -1
        bide_tris = ['Kids and Teens', '']
    else:
        bide_text = bide_atera(a2, '<font size="+1">', '</a>')
        bide_final = bide_text.pop()
        bide_tris = garbide2(bide_final)
        bide_bis = map (garbide1, bide_text)
        if len(bide_tris[0]) == 1:
            alphabar = -1


    if zenbatlink < 1 and hrcount == 2:
        othersubs_bis = -1

    if othersubs_bis !=-1:
        if len(othersubs_bis) == 0:
            othersubs_bis = -1
    
    if bide_bis == -1:
        bide_bis=''
    if selecto_bis == -1:
        selecto_bis=''
    if othersubs_bis == -1:
        othersubs_bis=''
    if see_bis == -1:
        see_bis=''       
    if lang_bis == -1:
        lang_bis=''    
    if link_bis == -1:
        link_bis=''
    if alphabar == -1:
        alphabar=''
    return editors, bide_bis, bide_tris, funtz, selecto_bis, othersubs_bis, see_bis, lang_bis, charset, link_bis, alphabar, pathon


 #return editors, bide_bis, bide_tris, funtz, selecto_bis, othersubs_bis, see_bis, lang_bis, charset, link_bis, alphabar, pathon

#'file:///Macintosh%20HD/Desktop%20Folder/CodeSy/PyLuis/Return-py/railways.html'
#'http://dmoz.org/World/Euskara/index.html' / 
# food, recreation, opencontent, artisti, software, bowling, eskoriatza, korean, tauromaquia
# railways, euskara. manchester

# this = 'http://dmoz.org/Society/Military/index.html'

#this = 'http://dmoz.org/World/Espa%f1ol/Sociedad/Gente/Militares/index.html'
#a = atala(this)

#editors = a[0]
#bide_bis = a[1]
#bide_tris = a[2]
#funtz = a[3]
#selecto_bis = a[4]
#othersubs_bis = a[5]
#see_bis = a[6]
#lang_bis = a[7]
#cools = a[8]
#link_bis = a[9]

#print
#print '************************'
#print 'egitura: bidea, funtzioak, selekto, subcats, see alsol, other langs, cool links, links, editors)'
#print
#print 'bidea'
#print bide_bis
#print bide_tris
#print
#print 'funtzioak: [apply, add, update, faq, desc, edit]'
#print funtz
#print
#print "selecto: "
#print selecto_bis
#print
#print "other subcats: "
#print othersubs_bis
#print
#print "see also: "
#print see_bis
#print
#print "this cat in other languages: "
#print lang_bis
#print
#print "cools: "
#print cools
#print
#print "link text"
#print link_bis
#print
#print "editors"
#print editors

def searching(term, mode, fro, rescat):
    
    url1 = 'http://search.dmoz.org/cgi-bin/search?search='

    url2 = {
         'Un': [url1 + term, 'term=' + term + '&mode=AllCats&at=1', 'term=' + term + '&mode=AllSites&at=21', -1],
         'Re': [url1 + term + '&all=no&cat=' + rescat, 'term=' + term + '&mode=RestrictCats&at=1', 'term=' + term + '&mode=RestrictSites&at=21', 1],
         'AllCats' : [url1 + term + '&morecat=' + fro, 'term=' + term + '&mode=AllCats&at=' + repr(string.atoi(fro)+25), -1, -1],
         'AllSites' : [url1 + term + '&jstart=' + fro, -1, 'term=' + term + '&mode=AllSites&at=' + repr(string.atoi(fro)+20), -1],
         'RestrictCats': [url1 + term + '&morecat=' + fro + '&all=no&cat=' + rescat, 'term=' + term + '&mode=RestrictCats&at=' + repr(string.atoi(fro)+25), -1, 1],
         'RestrictSites': [url1 + term + '&all=no&cat=' + rescat + '&jstart=' + fro,  -1, 'term=' + term + '&mode=RestrictSites&at=' + repr(string.atoi(fro)+20), 1]
         }
       
         
    emaitza = url2[mode]

    url = emaitza[0]
    morecats = emaitza[1]
    moresites = emaitza[2]
    rescatbai = emaitza[3]

    

    def parse_first(url):
    
        f = urllib.urlopen (url)
        lines = f.readlines()
        morebai = -1
        term2 = '7'
        nextbai = -1
        zenbatsite = 'nosite'
        catbai = -1
        sitbai = -1
        dena = ''
        resubai = 1
        
        for line in lines:
            line = re.sub('<', '\n<', line)
            line = re.sub('>', '>\n', line)
            line = re.sub('\n\n', '\n', line)
            
            if string.find(line, '<b>\nOpen Directory Sites\n</b>') != -1:
                zenbatsite = line
                sitbai = 1
                line = re.sub('<b>\nOpen', '<!--end--><b>\nOpen<odpsit>',line)
            
            if string.find(line, '<b>\nOpen Directory Categories\n</b>') != -1:
                catbai = 1
                line = re.sub('Categories\n</b>', 'Categories<odpcat>\n</b>',line)
            
            if string.find(line, 'Try your search on:') != -1:
                resubai = -1
                
            if string.find(line, '">\nmore...\n</a>\n') != -1:
                morebai = 1
                line = re.sub('">\nmore...', '<!--end-->\nmore...',line)
                p1 = string.find(line, 'search?search=')
                p2 = string.find(line, '&morecat')
                term2 = line[p1+len('search?search='):p2]
            if string.find(line, '\nPrevious\n</a>') != -1:
                line = re.sub('</a>', '<!--end-->\n</a>',line)
            if string.find(line, 'No sites matching your query were found in') != -1:
                emabai = -1

            if string.find(line, '\nNext\n</a>') != -1:
                nextbai = 1
                line = re.sub('</a>', '<!--end-->\n</a>',line)
                p1 = string.find(line, 'search?search=')
                p2 = string.find(line, '&jstart')
                term2 = line[p1+len('search?search='):p2]
            if string.find(line, '<FORM METHOD=GET ACTION="search"') != -1:
                line = re.sub('<FORM METHOD', '<!--end-->\n<FORM METHOD',line)
            dena = dena + line
    
        return morebai, term2, nextbai, zenbatsite, catbai, dena, sitbai, resubai
        
    def subs_atera(testua, nondik, noraino, zer):
        pbai = -1
        pstop = -1
        subs_text = ''
        for item in testua:
            if pbai == 1 and pstop != 1:
                subs_text = subs_text + item
                if string.find(item, noraino) != -1:
                    pstop = 1
            if string.find(item, nondik) != -1:
                pbai = 1
        subs_text = string.splitfields(subs_text, zer)
        return subs_text[1:], subs_text[0]
        
    def garbicat(item0):
        p1 = string.find(item0, 'href="http://dmoz.org/')
        p2 = string.find(item0, '">')
        p3 = string.find(item0, '</a>')
        p4 = string.rfind(item0, '">')
        p5 = string.rfind(item0, '</a>')
        return item0[p1+21:p2], item0[p2+2:p3], item0[p4+2:p5]

    def garbizenbatcat(item0):
        p1 = string.find(item0, '(')
        p2 = string.find(item0, ' of ')
        p3 = string.find(item0, ')')
        return item0[p1+1:p2], item0[p2+4:p3]
        
    def garbisit(item0):
        p1 = string.find(item0, 'href="')
        p2 = string.find(item0, '">')
        p3a = string.find(item0, '</a>')
        p3 = string.find(item0, ' - ', p3a)
        p4 = string.find(item0, '<br>')
        p6 = string.rfind(item0, 'href="http://dmoz.org/')
        p7 = string.rfind(item0, '/">')
        p8 = string.find(item0, '</a>', p7)
        p9 = string.find(item0, 'alt="Editor')
        return item0[p1+6:p2], item0[p2+2:p3a], item0[p3+3:p4], item0[p6+21:p7], item0[p7+3:p8], p9
    
    try:
        a = parse_first(url)
    except:
        a =[0, 1, 2, 3, 4, 'kk', 6, -1]

    moreb = a[0]
    term2 = a[1]
    nextb = a[2]
    zenbatsi = a[3]
    catbai = a[4]
    sitbai = a[6]
    resubai = a[7]
    dena = string.splitfields(a[5],'\n')

    if resubai == -1:
        return ''
        
    if catbai == 1:
        cat_text = subs_atera(dena, '<odpcat>', '<!--end-->', '<li>')
        cat_bis = map (garbicat, cat_text[0])
        zenbatcat_bis = garbizenbatcat(cat_text[1])
    else:
        cat_bis = -1
        zenbatcat_bis = -1
    
    if sitbai == 1:
        sit_text = subs_atera(dena, '<odpsit>', '<!--end-->', '<li>')
        sit_bis = map (garbisit, sit_text[0])
        zenbatsi_bis = garbizenbatcat(zenbatsi)
    else:
        sit_bis = -1
        zenbatsi_bis = -1

      
    
    
    if moreb != -1:
        moreb = morecats
    else:
        moreb = ''
    if nextb != -1:
        nextb = moresites
    else:
        nextb = ''
    
    if cat_bis == -1:
        cat_bis = ''
    if sit_bis == -1:
        sit_bis = ''
    
    if zenbatcat_bis == -1:
        zenbatcat_bis = ''
    if zenbatsi_bis == -1:
        zenbatsi_bis = ''
        
    if rescatbai == -1:
        rescatbai = ''
        
    return cat_bis, sit_bis, zenbatcat_bis, zenbatsi_bis, moreb, nextb, rescatbai, term
    
