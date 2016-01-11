#!/usr/bin/env python
# -*- coding: UTF-8 -*-

############################################################################################################
#                                     BIBLIOTECAS A IMPORTAR E DEFINICÕES                                  #
############################################################################################################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,xmltosrt,os
import jsunpack
from bs4 import BeautifulSoup
try:
    import json
except:
    import simplejson as json
h = HTMLParser.HTMLParser()

versao = '0.0.1'
addon_id = 'plugin.video.armagedompirata'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
fanart = addonfolder + '/fanart.jpg'
fav = addonfolder + '/fav'
favseries = addonfolder + '/favseries'
favanimes = addonfolder + '/favanimes'
url_base = 'http://www.armagedomfilmes.biz/'
url_base2 = 'https://copy.com/'

############################################################################################################
#                                                  MENUS                                                   #
############################################################################################################

def menu():
    addDir("[B]Gêneros[/B]",url_base2+'PQcbgvHfYmf47yuB?download=1',2,url_base2+'ZLG0E8EeWlWfxpNA')
    addDir("[B]Lançamentos[/B]",url_base+'?cat=3236',3,url_base2+'AJYjCOn6mPpqLORX')	
    addDir("[B]Séries[/B]",url_base+'?cat=21',7,url_base2+'BkoXzq0WLzdlK61z')
    addDir("[B]Animes[/B]",url_base+'?cat=36',12,url_base2+'Nbwfa9VUn6jXlUzD')
    addDir("[B]Bluray[/B]",url_base+'?cat=5529',3,url_base2+'0VnWFQQ6EzOkr9Fl')
    addDir("[B]Coleções de Filmes[/B]",url_base+'?cat=4509',5,url_base2+'CABnrk8ARqVG3IK6')	
    addDir("[B]Favoritos[/B]",'-',22,url_base2+'E1ebCG3qH1eEfP2v')	
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmc.executebuiltin('Container.SetViewMode(502)')
	
def todas_categorias(url):	
	html = gethtml(url)
	soup = html.find("div",{"class":"bi-cat"})
	categorias = soup.findAll("li")
	for categoria in categorias:
		titulo = categoria.a.text
		url = categoria.a["href"]
		img = categoria.img["src"]
		addDir("[B]"+titulo.encode('utf-8')+"[/B]",url,3,url_base2+img)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin('Container.SetViewMode(502)')
		
def menu_filme(name,url,iconimage):	
	addDir('[B]Assistir Agora: [/B]'+name,url,4,iconimage,False)
	addDir('[B]Trailer[/B]',url,21,iconimage,False)
	addDir('[B]Adicionar aos Favoritos[/B]',name+','+iconimage+','+url,17,url_base2+'E1ebCG3qH1eEfP2v',False)
	xbmc.executebuiltin('Container.SetViewMode(502)')
	
def menu_series(name,url,iconimage):	
	addDir('[B]Assistir Agora: [/B]'+name,url,8,iconimage)
	addDir(name.replace('Dublado e Legendado','').replace('Dublado ou Legendado','')+'[B] - Trailer [/B]'+'[B] Série [/B]',url,31,iconimage,False)
	addDir('[B]Adicionar aos Favoritos[/B]',name+','+iconimage+','+url,23,url_base2+'E1ebCG3qH1eEfP2v',False)
	xbmc.executebuiltin('Container.SetViewMode(502)')

def menu_animes(name,url,iconimage):	
	addDir('[B]Assistir Agora: [/B]'+name,url,13,iconimage)
	addDir(name.replace('Dublado e Legendado','').replace('Dublado ou Legendado','')+'[B] - Trailer [/B]'+'[B] Anime [/B]',url,31,iconimage,False)
	addDir('[B]Adicionar aos Favoritos[/B]',name+','+iconimage+','+url,26,url_base2+'E1ebCG3qH1eEfP2v',False)
	xbmc.executebuiltin('Container.SetViewMode(502)')	
	
def listar_filmes(url):
    print url
    addDir("[B][COLOR red]PESQUISAR FILMES[/B][/COLOR]",'-',11,url_base2+'PyJEKKphI7CuvJPe')
    html = gethtml(url)
    soup = html.find("div",{"class":"bic-miniaturas"})
    filmes = soup("div",{"class":"bic-miniatura"})
    for filme in filmes:
        titulo = filme.a["title"].replace('Assistir ','').replace('&#8211;',"-")
        url = filme.a["href"]
        img = filme.img["src"]
        addDir("[B]"+titulo.encode('utf-8')+"[/B]",url,20,img)	
    soup = html.find('div',{"class":"wp-pagenavi"})
    page = soup("a",{"class":"nextpostslink"})
    for prox_pagina in page:
        addDir("[B]"'Próxima Página >>'"[/B]",prox_pagina["href"],3,url_base2+'vsWirE1tLGWPSUJK')		
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin('Container.SetViewMode(515)')

def listar_filmes_colecoes(url):
    print url
    html = gethtml(url)
    soup = html.find("div",{"class":"bic-miniaturas"})
    filmes = soup("div",{"class":"bic-miniatura"})
    for filme in filmes:
        titulo = filme.a.text.replace('Assistir ','').replace('&#8211;',"-")
        url = filme.a["href"]
        img = filme.img["src"]
        addDir("[B]"+titulo.encode('utf-8')+"[/B]",url,6,img)	
    soup = html.find('div',{"class":"wp-pagenavi"})
    page = soup("a",{"class":"nextpostslink"})
    for prox_pagina in page:
        addDir("[B]"'Próxima Página >>'"[/B]",prox_pagina["href"],5,url_base2+'vsWirE1tLGWPSUJK')		
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin('Container.SetViewMode(515)')

def listar_filmes_colecoes2(url):
    print url
    codigo_fonte = abrir_url(url)
    match = re.compile('<a title="(.+?)" href="(.+?)"><img src="(.+?)" alt=".+?" /></a>').findall(codigo_fonte)
    for titulo, url, img in match:	
	    addDir(titulo.replace('Assistir ',''),url,20,img)
	    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	    xbmc.executebuiltin('Container.SetViewMode(515)')
		
def listar_series(url):
    print url
    addDir("[B][COLOR red]PESQUISAR SÉRIES[/B][/COLOR]",'-',10,url_base2+'XU3qvW80Lk2CalVK')
    html = gethtml(url)
    soup = html.find("div",{"class":"bic-miniaturas"})
    series = soup("div",{"class":"bic-miniatura"})
    for serie in series:
        titulo = serie.a["title"].replace('Assistir ','').replace('&#8211;',"-")
        url = serie.a["href"]
        img = serie.img["src"]
        addDir("[B]"+titulo.encode('utf-8')+"[/B]",url,29,img)	
    soup = html.find('div',{"class":"wp-pagenavi"})
    page = soup("a",{"class":"nextpostslink"})
    for prox_pagina in page:
        addDir("[B]"'Próxima Página >>'"[/B]",prox_pagina["href"],7,url_base2+'vsWirE1tLGWPSUJK')		
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin('Container.SetViewMode(515)')

def listar_temporadas_series(url):
	print url
	html = gethtml(url)
	soup = html.find("ul",{"class":"bp-series"})
	temporadas = soup("li")
	total = len(temporadas)
	i=1
	print total
	while i <= total:
		temporada = soup("li",{"class":"serie"+str(i)+"-code"})
		for temp in temporada:
			img = temp.img["src"]
			titulo = str(i)+" temporada"
			try:
				addDir(titulo,url,9,img,True,total)
			except:
				pass
		i=i+1
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin('Container.SetViewMode(515)')

def listar_episodios_series(name,url,iconimage):
	print url
	codigo = name.replace(' temporada','')
	html = gethtml(url)
	soup = html.find("li",{"class":"serie"+codigo+"-code"})
	episodios = soup("a")
	
	print episodios[0]
	
	a = []
	
	for episodio in episodios:
		try:
			xml = BeautifulSoup(abrir_url(episodio["href"]+'/feed'))
			title = xml.title.string.encode('utf-8').replace('Comentários sobre: Assistir ','')
			try:
				if "html" in os.path.basename(episodio["href"]):
					temp = [episodio["href"],title]
					a.append(temp)
			except:
				pass
		except:
			pass

	total = len(a)
	for url2, titulo, in a:
		titulo = titulo.replace('&#8211;',"-").replace('&#8217;',"'").replace('Assistir ','')
		addDir(titulo,url2,4,iconimage,False,total)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin('Container.SetViewMode(515)')

def listar_animes(url):
    print url
    addDir("[B][COLOR red]PESQUISAR ANIMES[/B][/COLOR]",'-',15,url_base2+'lXYxZEbCfUhgrWHb')
    html = gethtml(url)
    soup = html.find("div",{"class":"bic-miniaturas"})
    animes = soup("div",{"class":"bic-miniatura"})
    for anime in animes:
        titulo = anime.a["title"].replace('Assistir ','').replace('&#8211;',"-")
        url = anime.a["href"]
        img = anime.img["src"]
        addDir("[B]"+titulo.encode('utf-8')+"[/B]",url,30,img)	
    soup = html.find('div',{"class":"wp-pagenavi"})
    page = soup("a",{"class":"nextpostslink"})
    for prox_pagina in page:
        addDir("[B]"'Próxima Página >>'"[/B]",prox_pagina["href"],12,url_base2+'vsWirE1tLGWPSUJK')		
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin('Container.SetViewMode(515)')

def listar_temporadas_animes(url):
	print url
	html = gethtml(url)
	soup = html.find("ul",{"class":"bp-series"})
	temporadas = soup("li")
	total = len(temporadas)
	i=1
	print total
	while i <= total:
		temporada = soup("li",{"class":"serie"+str(i)+"-code"})
		for temp in temporada:
			img = temp.img["src"]
			titulo = str(i)+" temporada"
			try:
				addDir(titulo,url,14,img,True,total)
			except:
				pass
		i=i+1
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin('Container.SetViewMode(515)')
	
def listar_episodios_animes(name,url,iconimage):	
	print url
	codigo = name.replace(' temporada','')
	html = gethtml(url)
	soup = html.find("li",{"class":"serie"+codigo+"-code"})
	episodios = soup("a")
	
	print episodios[0]
	
	a = []
	
	for episodio in episodios:
		try:
			xml = BeautifulSoup(abrir_url(episodio["href"]))
			title = xml.title.string.encode('utf-8').replace('Assistir ','')
			try:
				if "html" in os.path.basename(episodio["href"]):
					temp = [episodio["href"],title]
					a.append(temp)
			except:
				pass
		except:
			pass

	total = len(a)
	for url2, titulo, in a:
		titulo = titulo.replace('Assistir ','')
		addDir(titulo,url2,16,iconimage,False,total)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin('Container.SetViewMode(515)')

def resolve_animes(name,url,iconimage):
	print url
	playlist = xbmc.PlayList(1)
	playlist.clear()	
	try:
		html = abrir_url(url)
		link = re.compile(r'<video src="(.+?)" width=".+?" height=".+?" controls autobuffer">').findall(html)[0]
		listitem = xbmcgui.ListItem(name,thumbnailImage=iconimage)
		listitem.setInfo("Video", {"Title":name.replace('Assistir o Filme: ','')})
		listitem.setProperty('mimetype', 'video/mp4')
		playlist.add(link,listitem)
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)
	except:
	    pass
		
def adicionar_favoritos_filmes(url):
	arquivo = open(fav, 'r')
	texto = arquivo.readlines()
	texto.append('\n'+url) 
	arquivo = open(fav, 'w')
	arquivo.writelines(texto)
	arquivo.close()
	xbmcgui.Dialog().ok('Armagedom Pirata', '                             Adicionado a lista de Favoritos.')	

def favoritos_filmes():
	arquivo = open(fav, 'r').readlines()
	for line in arquivo:
		params = line.split(',')
		try:
			nome = params[0]
			img = params[1].replace(' http','http')
			rtmp = params[2]
			addDir(nome,rtmp,4,img,False)
		except:
			pass
	addDir('[B]Remover Favoritos[/B]','-',19,url_base2+'nglhskXKjB2xShIB')	
	xbmc.executebuiltin('Container.SetViewMode(500)')

def limpar_lista_favoritos_filmes():	
	arquivo = open(fav, 'w')
	arquivo.write('')
	xbmcgui.Dialog().ok('Armagedom Pirata', '                      Lista de Favoritos limpa com sucesso.')
	menu()
	
def adicionar_favoritos_series(url):
	arquivo = open(favseries, 'r')
	texto = arquivo.readlines()
	texto.append('\n'+url) 
	arquivo = open(favseries, 'w')
	arquivo.writelines(texto)
	arquivo.close()
	xbmcgui.Dialog().ok('Armagedom Pirata', '                             Adicionado a lista de Favoritos.')	

def favoritos_series():
	arquivo = open(favseries, 'r').readlines()
	for line in arquivo:
		params = line.split(',')
		try:
			nome = params[0]
			img = params[1].replace(' http','http')
			rtmp = params[2]
			addDir(nome,rtmp,8,img)
		except:
			pass
	addDir('[B]Remover Favoritos[/B]','-',25,url_base2+'nglhskXKjB2xShIB')	
	xbmc.executebuiltin('Container.SetViewMode(500)')

def limpar_lista_favoritos_series():	
	arquivo = open(favseries, 'w')
	arquivo.write('')
	xbmcgui.Dialog().ok('Armagedom Pirata', '                      Lista de Favoritos limpa com sucesso.')
	menu()

def adicionar_favoritos_animes(url):
	arquivo = open(favanimes, 'r')
	texto = arquivo.readlines()
	texto.append('\n'+url) 
	arquivo = open(favanimes, 'w')
	arquivo.writelines(texto)
	arquivo.close()
	xbmcgui.Dialog().ok('Armagedom Pirata', '                             Adicionado a lista de Favoritos.')	

def favoritos_animes():
	arquivo = open(favanimes, 'r').readlines()
	for line in arquivo:
		params = line.split(',')
		try:
			nome = params[0]
			img = params[1].replace(' http','http')
			rtmp = params[2]
			addDir(nome,rtmp,13,img)
		except:
			pass
	addDir('[B]Remover Favoritos[/B]','-',19,url_base2+'nglhskXKjB2xShIB')	
	xbmc.executebuiltin('Container.SetViewMode(500)')

def limpar_lista_favoritos_animes():	
	arquivo = open(favanimes, 'w')
	arquivo.write('')
	xbmcgui.Dialog().ok('Armagedom Pirata', '                      Lista de Favoritos limpa com sucesso.')
	menu()	
	
def categoria_favorito():
    addDir("[B]Filmes Favoritos[/B]",'-',18,url_base2+'oHdcc77U8Zb3SqfM')
    addDir("[B]Séries Favoritas[/B]",'-',24,url_base2+'thfbPOgDpEOlmNq6')
    addDir("[B]Animes Favoritos[/B]",'-',27,url_base2+'WzykgvwpNri1l4I1')	
	
def trailer(name,url,iconimage):  
	    html = abrir_url(url)
	    link = re.compile(r'<iframe width=".+?" height=".+?" data-src=".+?://www.youtube.com/embed/(.+?)" frameborder=".+?" allowfullscreen>').findall(html)[0]
	    print link
	    xbmcPlayer = xbmc.Player()
	    xbmcPlayer.play('plugin://plugin.video.youtube/play/?video_id='+link)
		
def trailer2(name,url,iconimage):
	yt = "https://www.youtube.com/results?search_query="
	codigo_fonte = abrir_url(yt+name.replace(' ','%20'))
	#print html
	a=[]
	idd = re.compile('" data-context-item-id="(.+?)"').findall(codigo_fonte)[0]
	print idd	
	xbmcPlayer = xbmc.Player()
	xbmcPlayer.play('plugin://plugin.video.youtube/play/?video_id='+idd)

def obtem_url_dropvideo(url):

	codigo_fonte = abrir_url(url)
	try:
		soup = BeautifulSoup(codigo_fonte)
		lista = soup.findAll('script')
		#print lista
		js = str(lista).replace('<script>',"").replace('</script>',"")
		#print js
		sUnpacked = jsunpack.unpack(js)
		#print sUnpacked
		url_video = re.findall(r'var vurl2="(.*?)";', sUnpacked)
		url_video = str(url_video).replace("['","").replace("']","")
		return [url_video,"-"]
	except:
		pass	
	
def obtem_videobis(url):
	codigo_fonte = abrir_url(url)
	
	try:
		url_video = re.findall(r'file: "(.*?)"',codigo_fonte)[1]
		return [url_video,"-"]
	except:
		return ["-","-"]
		
def obtem_neodrive(url):
	codigo_fonte = abrir_url(url)
	
	try:
		url_video = re.findall(r'vurl.=."(.*?)";',codigo_fonte)[0]
		return [url_video,"-"]
	except:
		return ["-","-"]

def obtem_videopw(url):
	codigo_fonte = abrir_url(url)
	
	try:
		url_video = re.findall(r'var vurl2 = "(.*?)";',codigo_fonte)[0]
		return [url_video,"-"]
	except:
		return ["-","-"]		
	
def obtem_cloudzilla(url):
	codigo_fonte = abrir_url(url)
	
	try:
		url_video = re.findall(r'vurl.=."(.*?)";',codigo_fonte)[0]
		return [url_video,"-"]
	except:
		return ["-","-"]

def player(name,url,iconimage):
	
	try:
		dropvideo = r'src="(.*?dropvideo.*?/embed.*?)"'
		dropmega = r'src=".*?drop.*?id=(.*?)"'
		neodrive = r'src="(.*?neodrive.*?/embed.*?)"'
		neomega = r'src=".*?neodrive.*?id=(.*?)"'
		videobis = r'SRC="(.*?videobis.*?/embed.*?)"'
		videopw = r'src=".*?videopw.*?id=(.*?)"'
		cloudzilla = r'cloudzilla.php.id=(.*?)"'
		cloudzilla_f = r'http://www.cloudzilla.to/share/file/(.*?)"'
		
		mensagemprogresso = xbmcgui.DialogProgress()
		mensagemprogresso.create('Armagedon Pirata', 'A resolver link','Por favor aguarde...')
		mensagemprogresso.update(33)
		links = []
		hosts = []
		matriz = []
		codigo_fonte = abrir_url(url)
		
		try:
			links.append(re.findall(dropvideo, codigo_fonte)[0])
			hosts.append('Dropvideo')
		except:
			pass
		
		try:
			links.append('http://www.dropvideo.com/embed/'+re.findall(dropmega, codigo_fonte)[0])
			hosts.append('Dropvideo')
		except:
			pass
		
		try:
			links.append('http://videopw.com/e/'+re.findall(videopw, codigo_fonte)[0])
			hosts.append('Videopw')
		except:
			pass
			
		try:
			links.append(re.findall(videobis, codigo_fonte)[0])
			hosts.append('Videobis')
		except:
			pass
		
		try:
			links.append(re.findall(neodrive, codigo_fonte)[0])
			hosts.append('Neodrive')
		except:
			pass
		
		try:
			links.append('http://neodrive.co/embed/'+re.findall(neomega, codigo_fonte)[0])
			hosts.append('Neodrive')
		except:
			pass	
			
		try:
			links.append('http://www.cloudzilla.to/embed/'+re.findall(cloudzilla,codigo_fonte)[0])
			hosts.append('CloudZilla')
		except:
			pass
		
		try:
			links.append('http://www.cloudzilla.to/embed/'+re.findall(cloudzilla_t,codigo_fonte)[0])
			hosts.append('CloudZilla(Legendado)')
		except:
			pass
			
		if not hosts:
			return
		
		index = xbmcgui.Dialog().select('Selecione um dos hosts suportados :', hosts)
		
		if index == -1:
			return
		
		url_video = links[index]
		mensagemprogresso.update(66)
		
		print 'Player url: %s' % url_video
		if 'dropvideo.com/embed' in url_video:
			matriz = obtem_url_dropvideo(url_video)  
		elif 'cloudzilla' in url_video:
			matriz = obtem_cloudzilla(url_video)
		elif 'videobis' in url_video:
			matriz = obtem_videobis(url_video)
		elif 'neodrive' in url_video:
			matriz = obtem_neodrive(url_video)
		elif 'videopw' in url_video:
			matriz = obtem_videopw(url_video)			
		else:
			print "Falha: " + str(url_video)
		print matriz
		url = matriz[0]
		print url
		if url=='-': return
		legendas = matriz[1]
		print "Url do gdrive: " + str(url_video)
		print "Legendas: " + str(legendas)
		
		mensagemprogresso.update(100)
		mensagemprogresso.close()
		
		playlist = xbmc.PlayList(1)
		playlist.clear()
		
		listitem = xbmcgui.ListItem(name,thumbnailImage=iconimage) # name, iconImage="DefaultVideo.png", thumbnailImage="DefaultVideo.png"
		listitem.setPath(url)
		listitem.setProperty('mimetype','video/mp4')
		listitem.setProperty('IsPlayable', 'true')
		playlist.add(url,listitem)
		#try:
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)
		if legendas != '-':
			if 'timedtext' in legendas:
				#legenda = xmltosrt.convert(legendas)
				#try:
					import os.path
					sfile = os.path.join(xbmc.translatePath("special://temp"),'sub.srt')
					sfile_xml = os.path.join(xbmc.translatePath("special://temp"),'sub.xml')#timedtext
					sub_file_xml = open(sfile_xml,'w')
					sub_file_xml.write(urllib2.urlopen(legendas).read())
					sub_file_xml.close()
					print "Sfile.srt : " + sfile_xml
					xmltosrt.main(sfile_xml)
					xbmcPlayer.setSubtitles(sfile)
				#except:
				#	pass
			else:
				xbmcPlayer.setSubtitles(legendas)
		#except:
		#	dialog = xbmcgui.Dialog()
		#	dialog.ok(" Erro:", " Impossível abrir vídeo! ")
		#	pass
	except:
		print "erro ao abrir o video"
		print url_video
		pass

def pesquisar_series():
    keyb = xbmc.Keyboard('', 'Pesquisar...')
    keyb.doModal()
    if (keyb.isConfirmed()):
        search = keyb.getText()
        parametro_pesquisa=urllib.quote(search)
        url = 'http://www.armagedomfilmes.biz/?s=%s&s-btn=buscar' % str(parametro_pesquisa)
        print url
        listar_series(url)
		
def pesquisar_filmes():
    keyb = xbmc.Keyboard('', 'Pesquisar...')
    keyb.doModal()
    if (keyb.isConfirmed()):
        search = keyb.getText()
        parametro_pesquisa=urllib.quote(search)
        url = 'http://www.armagedomfilmes.biz/?s=%s&s-btn=buscar' % str(parametro_pesquisa)
        print url
        listar_filmes(url)

def pesquisar_animes():
    keyb = xbmc.Keyboard('', 'Pesquisar...')
    keyb.doModal()
    if (keyb.isConfirmed()):
        search = keyb.getText()
        parametro_pesquisa=urllib.quote(search)
        url = 'http://www.armagedomfilmes.biz/?s=%s&s-btn=buscar' % str(parametro_pesquisa)
        print url
        listar_animes(url)		

############################################################################################################
#                                                  FUNCÕES                                                 #
############################################################################################################
	
def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link
	
def gethtml(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    soup = BeautifulSoup(link)
    return soup

def addDir(name,url,mode,iconimage,pasta=True,total=1,plot=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="iconimage", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": plot})
	contextMenuItems = []
	contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
	contextMenuItems.append(("[COLOR lime]Add to Favourite Movies[/COLOR]",'XBMC.RunPlugin(%s?name=name%s&url=url%s&mode=17&iconimage=iconimage%s)'%(sys.argv[0], urllib.quote(name), url, urllib.quote(iconimage))))
	contextMenuItems.append(("[COLOR orange]Remove from Favourite Movies[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=19&iconimage=%s)'%(sys.argv[0], urllib.quote(name), url, urllib.quote(iconimage))))
	liz.addContextMenuItems(contextMenuItems, replaceItems=True)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok	

def addLink(name,url,iconimage):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok	

############################################################################################################
#                                             MAIS PARÂMETROS                                              #
############################################################################################################
              
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

      
params=get_params()
url=None
name=None
mode=None
iconimage=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

try:        
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass


print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)

###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################

if mode==None or url==None or len(url)<1:
    print ""
    menu()
elif mode==2:
	print ""
	todas_categorias(url)
elif mode==3:
    print  ""
    listar_filmes(url)
elif mode==4:
    print ""
    player(name,url,iconimage)
elif mode==5:
    print ""
    listar_filmes_colecoes(url)	
elif mode==6:
    print ""
    listar_filmes_colecoes2(url)
elif mode==7:
    print ""
    listar_series(url)
elif mode==8:
    print "Mode 8"
    listar_temporadas_series(url)
elif mode==9:
    print ""
    listar_episodios_series(name,url,iconimage)
elif mode==10:
    print ""
    pesquisar_series()
elif mode==11:
    print ""
    pesquisar_filmes()
elif mode==12:
    print ""
    listar_animes(url)
elif mode==13:
    print ""
    listar_temporadas_animes(url)
elif mode==14:
    print ""
    listar_episodios_animes(name,url,iconimage)
elif mode==15:
    print ""
    pesquisar_animes()
elif mode==16:
    print ""
    resolve_animes(name,url,iconimage)
elif mode==17:
    print ""
    adicionar_favoritos_filmes(url)
elif mode==18:
    print ""
    favoritos_filmes()	
elif mode==19:
    print ""
    limpar_lista_favoritos_filmes()
elif mode==20:
    print ""
    menu_filme(name,url,iconimage)
elif mode==21:
    print ""
    trailer(name,url,iconimage)
elif mode==22:
    print ""
    categoria_favorito()
elif mode==23:
    print ""
    adicionar_favoritos_series(url)
elif mode==24:
    print ""
    favoritos_series()	
elif mode==25:
    print ""
    limpar_lista_favoritos_series()
elif mode==26:
    print ""
    adicionar_favoritos_animes(url)
elif mode==27:
    print ""
    favoritos_animes()	
elif mode==28:
    print ""
    limpar_lista_favoritos_animes()
elif mode==29:
    print ""
    menu_series(name,url,iconimage)
elif mode==30:
    print ""
    menu_animes(name,url,iconimage)
elif mode==31:
    print ""
    trailer2(name,url,iconimage)	
	
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))	