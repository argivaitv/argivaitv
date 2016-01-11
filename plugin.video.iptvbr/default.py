#!/usr/bin/env python
# -*- coding: UTF-8 -*-
##############BIBLIOTECAS A IMPORTAR####################
import xbmcplugin,xbmcgui,xbmc,xbmcaddon,os,sys,urllib,urllib2,re,base64,HTMLParser,time
from bs4 import BeautifulSoup
import mechanize
import cookielib 
import urlresolver

#######################SETTINGS#########################
addon_name = 'IPTVBrasil'
addon_id = 'plugin.video.iptvbr'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
datafolder = addonfolder+'/data'
icon = addonfolder + '/icon.png'
ds24 = addonfolder +'/ds24h.png'
fanart = addonfolder + '/fanart.jpg'
fav = datafolder + '/fav'
epg = datafolder + '/epg'
msg = datafolder+'/msg'
urlbase = 'http://filmesserieshd.com/'
basecat = base64.b64decode('aHR0cDovL2lwdHZici5vcmcvYWRkb25pcHR2YnIvY2F0ZWdvcmlhcy5odG1s')
urlbase2 = base64.b64decode('aHR0cDovL2Nhcm9saW5lb2xpdmVpcmEuY29tLmJyL3R2YW1pZ29zLw==')
base2 = base64.b64decode('aHR0cDovL3d3dy5hb3Zpdm9icmFzaWwuY29tL3R2YW1pZ29zMi8=')
baseguia ='http://meuguia.tv/'
setepg = selfAddon.getSetting('setepg')
###################################################MENUS############################################

def menu():
	mensagem()
	addDir('Tv ao Vivo','-',1,'https://iptvbr.org/images/slide/01.png')
	addDir('Guia de Programação','-',31,'https://d13yacurqjgara.cloudfront.net/users/18738/screenshots/178628/meuguiatv_logo.jpg')
	addDir('Agenda Esportiva','-',101,'http://3.bp.blogspot.com/-nv_s-m1_0EM/VgXTUmLskBI/AAAAAAAAB3A/3B8dGyXp_Rs/s640/Agenda333.png')
	addDir('Desenhos e Séries 24h','-',20,ds24)
	addDir('Cine em Casa','-',40,'https://upload.wikimedia.org/wikipedia/pt/5/57/Cinema_em_casa_logo.jpg')
	addDir('Filmes Online Grátis','-',50,'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-xap1/v/t1.0-1/c13.12.154.154/1237151_397828540319331_929212767_n.jpg?oh=2d75a2f623fe36e74a70bdaa93c01042&oe=565FF780&__gda__=1454060369_e426226c7accc8bace3b22d5e9e39a4d')
	addDir('Filmes OnDemand','-',9,'http://www.teclasap.com.br/wp-content/uploads/2013/03/on-demand1.jpg')
	addDir('Configurações','-',100,'https://cdn4.iconfinder.com/data/icons/imod/512/Hardware/iEngrenages.png')
	xbmc.executebuiltin('Container.SetViewMode(500)')
	
def deftv():
	try:
		html = gethtml(basecat)
		soup = html.findAll("li")
		addDir('Jogo ao Vivo','-',4,'http://www.futebolms.com.br/v4/images/n_20130515092214_quarta_e_dia_de_pre_jogo_ao_vivo_e_partidas_decisivas_em_tempo_real.jpg')			
		for item in soup:
			name = item.a.text
			img = item.img["src"]
			url = item.a["href"]
			addDir(name.encode('utf8'),url.encode('utf8'),2,img.encode('utf8'))
		addDir('Reporte aqui canais off','-',6,'http://img15.deviantart.net/e4bd/i/2009/244/8/3/off_air_screen_by_zaku_man.png',False)
		xbmc.executebuiltin('Container.SetViewMode(500)')
	except:
		xbmcgui.Dialog().ok(addon_name, 'Addon em manutenção,Desculpe o transtorno.')
		menu()
		
def listarcanais(url):
	html = gethtml(url)
	soup = html.findAll("li")
	if setepg== 'true':
		for item in soup:
			try:
				check = item.a["mt"]
				name = item.a.text.encode('utf-8')
				img = item.img["src"]
				url = item.a["href"]
				addDir(name,url,8,img,False)
			except:
				name = item.a.text.encode('utf-8')
				img = item.img["src"]
				url = item.a["href"]
				addDir(name,url,3,img,False)
	else:
		getepg()
		for item in soup:
			try:
				check = item.a["mt"]
				name = item.a.text
				img = item.img["src"]
				url = item.a["href"]
				idguia = item.a["epg"]
				if idguia == 'nulo':
						addDirc(name,url,8,img,False)
				else:
					for line in open(epg,'r').readlines():
						params = line.split(',')
						ch = params[0]
						prog = params[1]
						if ch == idguia:
							addDirc(name+' [COLOR green]- '+prog.decode("utf-8")+'[/COLOR]',url,8,img,False)
						else:
							pass
					
			except:
				name = item.a.text
				img = item.img["src"]
				url = item.a["href"]
				idguia = item.a["epg"]
				if idguia == 'nulo':
						addDirc(name,url,3,img,False)
				else:
					for line in open(epg,'r').readlines():
						params = line.split(',')
						ch = params[0]
						prog = params[1]
						if ch == idguia:
							addDirc(name+' [COLOR green]- '+prog.decode("utf-8")+'[/COLOR]',url,3,img,False)
						else:
							pass
		xbmc.executebuiltin("Container.SetViewMode(500)")
		
def jogos_aovivo():
	for line in urllib2.urlopen(base64.b64decode('aHR0cDovL2lwdHZici5vcmcvYWRkb25pcHR2YnIvYW92aXZvLnR4dA==')).readlines():
		params = line.split(',')
		try:
			nome = params[0]
			img = params[1].replace(' http','http')
			rtmp = params[2]
			addDir(nome,rtmp,5,img,False)
		except:
			pass
	html = gethtml(base64.b64decode('aHR0cDovL2lwdHZici5vcmcvYWRkb25pcHR2YnIvYW92aXZvLmh0bWw='))
	soup = html.findAll("li")
	for item in soup:
		name = item.a.text.encode('utf-8')
		img = item.img["src"]
		url = item.a["href"]
		addDir(name,url,3,img,False)
	xbmc.executebuiltin("Container.SetViewMode(500)")

def canaloff():
	keyb = xbmc.Keyboard('', 'Qual canal não esta funcionando?...')
	keyb.doModal()
	if (keyb.isConfirmed()):
		mensagem = keyb.getText()
		keyb2 = xbmc.Keyboard('', 'Digite seu nome...')
		keyb2.doModal()
		if (keyb2.isConfirmed()):
			user = keyb2.getText()
			br = mechanize.Browser()
			cj = cookielib.LWPCookieJar()
			br.set_cookiejar(cj)
			br.set_handle_equiv(True)
			br.set_handle_gzip(False)
			br.set_handle_redirect(True)
			br.set_handle_referer(True)
			br.set_handle_robots(False)
			br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
			br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
			br.open(base64.b64decode('aHR0cDovL2lwdHZici5vcmcvYWRkb25pcHR2YnIvY2FuYWxvZmYv'))
			br.select_form(nr=0)
			br.form['nomeremetente'] = user
			br.form['mensagem'] = mensagem
			logged_in = br.submit()
			xbmcgui.Dialog().ok(addon_name, '                            Obrigado por seu contato...')
		
def playertv(name,url,iconimage):	
	pg = 0
	caixastatus = xbmcgui.DialogProgress()
	caixastatus.create(addon_name, 'Abrindo sinal do canal...','Por Favor Aguardar...')
	caixastatus.update(pg)
	time.sleep(1)
	try:
		pg +=50 
		caixastatus.update(pg)
		playlist = xbmc.PlayList(1)
		playlist.clear()
		listitem = xbmcgui.ListItem(name,thumbnailImage=iconimage)
		listitem.setInfo("Video", {"Title":name})
		listitem.setProperty('mimetype', 'video/mp4')
		playlist.add(url,listitem)
		pg=100
		caixastatus.update(pg)
		caixastatus.close()
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)
	except:
		caixastatus.close()
		xbmcgui.Dialog().ok('IPTVBrasil', 'Canal Temporariamente indisponivel,Desculpe o transtorno.')	
		
def playermaster(name,url,iconimage):
	pg = 0
	caixastatus = xbmcgui.DialogProgress()
	caixastatus.create(addon_name, 'Abrindo sinal do canal...','Por Favor Aguardar...')
	caixastatus.update(pg)
	playlist = xbmc.PlayList(0)
	playlist.clear()
	params = url.split(',')
	pg +=30 
	caixastatus.update(pg)
	try:
		playpath = params[0]
		ip = params[1]
		pg +=30 
		caixastatus.update(pg)
		link = 'rtmp://'+ip+'/live?wmsAuthSign='+getwms() +' playpath='+playpath+' swfUrl=http://www.tv-msn.com/player/player.swf live=1 pageUrl=http://tv-msn.com/disney.php token='+gettoken()
		pg +=30 
		caixastatus.update(pg)
		listitem = xbmcgui.ListItem(name,thumbnailImage=iconimage)
		listitem.setInfo("Video", {"Title":name})
		listitem.setProperty('mimetype', 'video/mp4')
		playlist.add(link,listitem)
		pg=100
		caixastatus.update(pg)
		caixastatus.close()
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)
	except:
		caixastatus.update(pg)
		xbmcgui.Dialog().ok(addon_name, 'Canal Temporariamente indisponivel,Desculpe o transtorno.')		
		
def player_youtube(url):
	xbmcPlayer = xbmc.Player()
	xbmcPlayer.play('plugin://plugin.video.youtube/play/?video_id=' +url)			
	
def agendaesportiva():
	html = gethtml('http://esportes.estadao.com.br/programacao/natv/')
	table = html.find("div",{'class':'bb-md-noticia programacao-tv'})
	items = table.findAll("div",{'class':'item-agenda'})
	for item in items:
		canal = re.compile(r'</var></p><p>(.*?)</p></div>').findall(str(item))[0]
		tipo = re.compile(r'<strong>(.*?)</strong>').findall(str(item))[0]
		hora = re.compile(r'<div class="item-hr">(.*?)</div>').findall(str(item))[0]
		programa = re.compile(r'<var>(.*?)</var>').findall(str(item))[0]
		addDir('[COLOR blue]'+hora+'[/COLOR] - [COLOR white]'+programa+'[/COLOR] - [COLOR orange]'+tipo+'[/COLOR] -[COLOR red]'+canal+'[/COLOR]',base64.b64decode('aHR0cDovL2lwdHZici5vcmcvYWRkb25pcHR2YnIvZXNwb3J0ZXMuaHRtbA=='),2,'https://www.primecursos.com.br/arquivos/uploads/2013/10/introducao-a-psicologia-do-esporte.jpg')
	xbmc.executebuiltin('Container.SetViewMode(51)')
###############guia####################
def catguia():
	html = gethtml(baseguia)
	soup = html.findAll("li")
	for item in soup:
		name = item.a["href"].replace('/programacao/categoria/','')
		url = item.a["href"]
		addDir(name.encode('utf-8'),baseguia +url,32,icon)
		xbmc.executebuiltin('Container.SetViewMode(51)')
def canaisguia(url):
	html = gethtml(url)
	soup = html.findAll("li")
	for item in soup:
		name = item.span.text
		program = item.a["title"]
		img = item["style"].replace(') no-repeat 8px center;','').replace('background: url(','')
		url = item.a["href"]
		addDir('[COLOR white]'+program.encode('utf-8')+'[/COLOR]'+ ' ' + name.encode('utf-8'),baseguia +url,33,baseguia+img)
		xbmc.executebuiltin('Container.SetViewMode(51)')

def progcomplt(url,iconimage):
	html = gethtml(url)
	soup = html.findAll("li")
	for item in soup:
		url = ''
		filme = ''
		hora = ''
		data1 = ''
		data = ''
		try:
			url = item.a["href"]
		except:
			pass
		try:
			style = item.div.text
			if style == 'Publicidade':
				name = ''
		except:
			pass
		try:
			filme = item.span.text
		except:
			pass
		try:
			hora = item.div.text
			if hora == 'Publicidade':
				hora = ''
		except:
			pass
		try:
			data1 = item.a["href"]
		except:
			data = item.text
		addDir('[COLOR green]'+hora.encode('utf-8')+'[/COLOR]'+' '+'[COLOR white]'+filme.encode('utf-8')+'[/COLOR]'+'[COLOR red]'+data.encode('utf-8')+'[/COLOR]',baseguia +url,34,iconimage,False)
	xbmc.executebuiltin('Container.SetViewMode(51)')
	
def programa(url):
	try:
		html = abrir_url(url)
		titulo = re.compile(r'class="tit">(.+?)</span').findall(html)[0]
		texto = re.compile(r'var str="(.+?)"').findall(html)[0]
		xbmcgui.Dialog().ok(titulo,texto)
	except:
		pass
##############filmes#####################	
def menufilmes():
	addDir('Categorias','-',10,'http://www.netshoping.com.br/layout/img/tit_categorias.png')
	addDir('Favoritos','-',17,'http://www.iconesbr.net/iconesbr/2008/07/140/140_256x256.png')
	xbmc.executebuiltin('Container.SetViewMode(500)')
	

def listarcat():
	addDir('Ação','http://filmesserieshd.com/acao/',11,icon)
	addDir('Animação','http://filmesserieshd.com/animacao/',11,icon)
	addDir('Aventura','http://filmesserieshd.com/aventura/',11,icon)
	addDir('Biografia','http://filmesserieshd.com/biografia/',11,icon)
	addDir('Comédia','http://filmesserieshd.com/comedia/',11,icon)
	addDir('Desenhos e Animes','http://filmesserieshd.com/desenhos-e-animes/',11,icon)
	addDir('Drama','http://filmesserieshd.com/drama/',11,icon)
	addDir('Ficção Científica','http://filmesserieshd.com/ficcao-cientifica/',11,icon)
	addDir('Full HD 1080p','http://filmesserieshd.com/full-hd-1080p/',11,icon)
	addDir('Guerra','http://filmesserieshd.com/guerra/',11,icon)
	addDir('HD 720p','http://filmesserieshd.com/hd-720p/',11,icon)
	addDir('Lançamentos','http://filmesserieshd.com/lancamentos/',11,icon)
	addDir('Legendado','http://filmesserieshd.com/legendado/',11,icon)
	addDir('Policial','http://filmesserieshd.com/policial/',11,icon)
	addDir('Romance','http://filmesserieshd.com/uncategorized/',11,icon)
	addDir('Séries','http://filmesserieshd.com/series/',11,icon)
	addDir('Suspense','http://filmesserieshd.com/suspense/',11,icon)
	addDir('Terror','http://filmesserieshd.com/terror/',11,icon)
	xbmc.executebuiltin('Container.SetViewMode(51)')
	
def listarfilmes(url):
	html = gethtml(url)
	htmla = abrir_url(url)
	soup = html.find("div",{"id":"categoria"})
	filmes = soup.findAll("div",{"class":"item"})
	for filme in filmes:
		name = filme.img["alt"].encode('utf-8')
		url = filme.a["href"] 
		img = filme.img["src"]
		titulo = name.replace('-','').replace('–','').replace('Assistir','').replace('Dublado','').replace('Online','').replace('1080p ','').replace('HD ','').replace('Legendado ','').replace('ou','').replace('/','').replace(' e ','')
		addDir(titulo,url,12,img)
	page = re.compile(r'<link rel="next" href="(.+?)" />').findall(str(htmla))[0]
	addDir('Próxima Página >>',page,11,'http://jullianoegiselle.xpg.uol.com.br/proxima%20pagina.png')	
	xbmc.executebuiltin('Container.SetViewMode(501)')	

def menufilme(name,url,iconimage):	
	addDir('Assistir o Filme: '+name,url,13,iconimage,False)
	addDir('Sinopse',url,14,iconimage,False)
	addDir('Trailer',name,15,iconimage,False)
	addDir('Adicionar aos Favoritos',name+','+iconimage+','+url,16,'http://4.bp.blogspot.com/-gci8DGnKWYM/TZsWlCtafdI/AAAAAAAAAJo/I_Q7pqqANFg/s1600/add-favoritos.png',False)

def playerfilmes(name,url,iconimage):
	caixastatus = xbmcgui.DialogProgress()
	caixastatus.create(addon_name, 'Resolvendo Links...','Por favor aguarde...')
	caixastatus.update(10)
	playlist = xbmc.PlayList(1)
	playlist.clear()
	html = abrir_url(url)
	caixastatus.update(20)
	try:
		caixastatus.update(35)
		seg = re.compile(r'<iframe width="560" height="315" src="(.+?)"').findall(html)[1]
		html2 = abrir_url(seg)
		seg2 = re.compile(r'http://videopw.com(.+?)"').findall(html2)[0]
		pw = 'http://videopw.com'+seg2
		html3 = abrir_url(pw)
		link = re.compile(r'var vurl2 = "(.+?)"').findall(html3)[0]
		listitem = xbmcgui.ListItem(name,thumbnailImage=iconimage)
		listitem.setInfo("Video", {"Title":name.replace('Assistir o Filme: ','')+' [COLOR gray](Video PW)[/COLOR]'})
		listitem.setProperty('mimetype', 'video/mp4')
		playlist.add(link,listitem)
		caixastatus.update(49)
	except:
		pass
	try:
		caixastatus.update(63)
		seg = re.compile(r'<iframe width="560" height="315" src="(.+?)"').findall(html)[1]
		html2 = abrir_url(seg)
		seg2 = re.compile(r'http://neodrive.co/(.+?)"').findall(html2)[0]
		neo = 'http://neodrive.co/'+seg2
		html3 = abrir_url(neo)
		link = re.compile(r'var vurl = "(.+?)"').findall(html3)[0]
		listitem = xbmcgui.ListItem(name,thumbnailImage=iconimage)
		listitem.setInfo("Video", {"Title":name.replace('Assistir o Filme: ','')+' [COLOR gray](Neo Drive)[/COLOR]'})
		listitem.setProperty('mimetype', 'video/mp4')
		playlist.add(link,listitem)
		caixastatus.update(80)
	except:
		pass
	caixastatus.update(90)	
	xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
	xbmcPlayer.play(playlist)
	caixastatus.update(100)
	caixastatus.close()
	

def getsinopse(url):
	try:
		html = abrir_url(url)
		desc = re.compile(r'<p>(.+?)<A HREF="').findall(html)[0]
		if desc == '':
			xbmcgui.Dialog().ok(addon_name, 'Sinopse não disponivel,Desculpe o transtorno.')
		else:
			xbmcgui.Dialog().ok('Sinopse', desc)
	except:
		xbmcgui.Dialog().ok(addon_name, 'Sinopse não disponivel,Desculpe o transtorno.')

		
def gettrailer(url):
	caixastatus = xbmcgui.DialogProgress()
	caixastatus.create(addon_name, 'Abrindo Trailer...','Por favor aguarde...')
	html = abrir_url('https://www.youtube.com/results?search_query='+url.replace(' ','+')+'+trailer')
	idd = re.compile('v=(.+?)"').findall(html)[0]
	caixastatus.close()
	xbmcPlayer = xbmc.Player()
	xbmcPlayer.play('plugin://plugin.video.youtube/play/?video_id=' +idd)	
	
	
def depois(url):
	arquivo = open(fav, 'r')
	texto = arquivo.readlines()
	texto.append('\n'+url) 
	arquivo = open(fav, 'w')
	arquivo.writelines(texto)
	arquivo.close()
	xbmcgui.Dialog().ok(addon_name, 'Filme adicionado a lista de Favoritos.')

def favoritos():
	arquivo = open(fav, 'r').readlines()
	for line in arquivo:
		params = line.split(',')
		try:
			nome = params[0]
			img = params[1].replace(' http','http')
			rtmp = params[2]
			addDir(nome,rtmp,12,img)
		except:
			pass
	addDir('Limpar Favoritos','-',18,'https://cdn0.iconfinder.com/data/icons/icons-unleashed-vol1/256/-trash.png')	
	xbmc.executebuiltin('Container.SetViewMode(500)')

def limpar():
	arquivo = open(fav, 'w')
	arquivo.write('')
	xbmcgui.Dialog().ok(addon_name, 'Lista de Favoritos limpa com sucesso.')
	menufilmes()

	
	
####################cine em casa######################################

def menucine():
	addDir('Lançamentos','http://cineemcasa.com/category/filme/lancamentos',42,'http://taxigas.pt/wp-content/uploads/2013/12/taxigas_icon.png')
	addDir('Categorias','-',41,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Pesquisar','-',44,'http://www.imoveisras.com.br/site/temas/mediagenerico/icon_pesquisar_2_laranja.png')
	xbmc.executebuiltin('Container.SetViewMode(51)')

def categoriascine():
	#addDir('SEQUÊNCIAS DE FILMES / TRILOGIAS','http://cineemcasa.com/category/filme/sequencias-de-filmes',2,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('LANÇAMENTOS NO CINEMA','http://cineemcasa.com/category/filme/lancamentos-no-cinema',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('RECENTEMENTE ADICIONADOS','http://cineemcasa.com/category/filme',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Ação','http://cineemcasa.com/category/filme/acao',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Animação','http://cineemcasa.com/category/filme/animacao-filme',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Artes Marciais','http://cineemcasa.com/category/filme/artes-marciais',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Aventura','http://cineemcasa.com/category/filme/aventura',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Besteirol','http://cineemcasa.com/category/filme/besteirol',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Biografia','http://cineemcasa.com/category/filme/biografia',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Clássicos','http://cineemcasa.com/category/filme/classicos',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Comédia','http://cineemcasa.com/category/filme/comedia-filme',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Comédia Dramática','http://cineemcasa.com/category/filme/comedia-dramatica',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Comédia Romântica','http://cineemcasa.com/category/filme/comedia-romantica',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Corrida','http://cineemcasa.com/category/filme/corrida',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Crime','http://cineemcasa.com/category/filme/crime',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Desenhos','http://cineemcasa.com/category/filme/desenhos',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Drama','http://cineemcasa.com/category/filme/drama-filme',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Dublado','http://cineemcasa.com/category/filme/dublado',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Épico','http://cineemcasa.com/category/filme/epico',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Erótico','http://cineemcasa.com/category/filme/erotico',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Espionagem','http://cineemcasa.com/category/filme/espionagem',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Esporte','http://cineemcasa.com/category/filme/esporte',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Família','http://cineemcasa.com/category/filme/familia',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Fantasia','http://cineemcasa.com/category/filme/fantasia-filme',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Faroeste','http://cineemcasa.com/category/filme/faroeste',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Ficção Científica','http://cineemcasa.com/category/filme/ficcao-cientifica-filme',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Guerra','http://cineemcasa.com/category/filme/guerra',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Heróis','http://cineemcasa.com/category/filme/herois',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Histórico','http://cineemcasa.com/category/filme/historico',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Infantil','http://cineemcasa.com/category/filme/infantil',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Legendado','http://cineemcasa.com/category/filme/legendado',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Musical','http://cineemcasa.com/category/filme/musical',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Nacional','http://cineemcasa.com/category/filme/nacional',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Policial','http://cineemcasa.com/category/filme/policial',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Religiosos','http://cineemcasa.com/category/filme/religiosos',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Romance','http://cineemcasa.com/category/filme/romance',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Suspense','http://cineemcasa.com/category/filme/suspense-filme',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	addDir('Terror','http://cineemcasa.com/category/filme/terror-filme',42,'http://www.agatek.com.br/sitecontent/produto/images/laranja-icon-celular-icone-595445829.png')
	xbmc.executebuiltin('Container.SetViewMode(51)')
def listarfilmescine(url):
	soup = gethtml(url)
	table = soup.findAll("ul",{"class":"lista-filmes"})[0]
	filmes = table.findAll("li")
	for filme in filmes:
		name = filme.img['alt']
		img = filme.img['src']
		link = filme.a['href']
		addDir(name.encode('utf8'),link,43,img.encode('utf8'),False)
	try:
		page = re.compile(r'class="next page-numbers" href="(.+?)"').findall(str(soup))[0]
		addDir('Proxima Página',page,42,'http://images.clipartlogo.com/files/images/16/162773/arrow-orange-right_t')
	except:
		pass
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin('Container.SetViewMode(500)')	
def pesquisacine():
    keyb = xbmc.Keyboard('', 'Digite o Filme desejado...')
    keyb.doModal()
    if (keyb.isConfirmed()):
        search = keyb.getText()
        parametro_pesquisa=urllib.quote(search)
        url = 'http://cineemcasa.com/?s='+parametro_pesquisa
        listarfilmescine(url)	
	return
def Playercine(name,url,iconimage):
	pg = 0
	caixastatus = xbmcgui.DialogProgress()
	caixastatus.create(addon_name, 'Procurando e Resolvendo Links..','Por Favor Aguardar...')
	caixastatus.update(pg)
	html = abrir_url(url)   
	names = []
	urls  = []
	pg +=30 
	caixastatus.update(pg)
	try:
		link = re.compile(r'href="(.*?vidzi.tv/embed.*?)"').findall(html)[0]
		nhos = 'Vidiz'
		names.append(nhos)
		urls.append(link)
	except:
		pass
	try:
		link = re.compile(r'href="(.*?streamin.to/embed.*?)"').findall(html)[0]
		nhos = 'Streamin.to'
		names.append(nhos)
		urls.append(link)
	except:
		pass
	try:
		link = re.compile(r'href="(.*?vidto.me.*?)"').findall(html)[0]
		nhos = 'Vidto'
		names.append(nhos)
		urls.append(link)
	except:
		pass
	try:
		link = re.compile(r'href="(.*?cloudzilla.*?)"').findall(html)[0]
		nhos = 'Cloudzilla'
		names.append(nhos)
		urls.append(link)
	except:
		pass
	try:
		link = re.compile(r'href="(.*?videomega.*?)"').findall(html)[0]
		nhos = 'VideoMega'
		names.append(nhos)
		urls.append(link)
	except:
		pass
	try:
		link = re.compile(r'href="(.*?nowvideo.*?)"').findall(html)[0]
		nhos = 'NowVideo'
		names.append(nhos)
		urls.append(link)
	except:
		pass
	#try:
	#	link = re.compile(r'href="(.*?openload.co.*?)"').findall(html)[0]
	#	nhos = 'Openload'
	#	names.append(nhos)
	#	urls.append(link)
	#except:
	#	pass
	#try:
	#	link = re.compile(r'href="(.*?youwatch.org.*?)"').findall(html)[0]
	#	media_url = urlresolver.resolve(link)
	#	nhos = 'YouWatch'
	#	urls.append(link)
	#except:
	#	pass
	#try:
	#	link = re.compile(r'href="(.*?flashx.tv.*?)"').findall(html)[0]
	#	nhos = 'FlashX'
	#	names.append(nhos)
	#	urls.append(link)
	#except:
	#	pass
	#try:
	#	link = re.compile(r'href="(.*?ok.ru.*?)"').findall(html)[0]
	#	nhos = 'ok.ru'
	#	names.append(nhos)
	#	urls.append(link)
	#except:
	#	pass
	#try:
	#	link = re.compile(r'href="(.*?video.tt.*?)"').findall(html)[0]
	#	nhos = 'video.tt'
	#	names.append(nhos)
	#	urls.append(link)
	#except:
	#	pass
	pg +=30
	caixastatus.update(pg)
	opcao = xbmcgui.Dialog().select('Selecione o Host desejado:', names)
	#if opcao == -1 : return
	pg +=30
	caixastatus.update(pg)
	url = urls[opcao]
	media_url = urlresolver.resolve(url)
	pg=100
	caixastatus.update(pg)
	caixastatus.close()
	playlist = xbmc.PlayList(1)
	playlist.clear()
	listitem = xbmcgui.ListItem(name,thumbnailImage=iconimage)
	listitem.setInfo("Video", {"Title":name})
	listitem.setProperty('mimetype', 'video/mp4')
	playlist.add(str(media_url),listitem)	
	xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
	xbmcPlayer.play(playlist)	

################################filmes online##########################

def menuonline():
	addDir('Lançamentos','http://www.filmesonlinegratis.net/filmes-lancamentos',52,'http://png.clipart.me/graphics/thumbs/175/blue-fire-icon_175761860.jpg')
	addDir('Categorias','-',51,'http://s2.glbimg.com/l-MpNzaPppp2zQ1DU_DcRxH4nuU=/110x83/smart/http://s.glbimg.com/po/tt2/f/original/2015/11/26/appblock-icone.png')
	addDir('Pesquisar','-',54,'http://www.imoveisvalemetropolitana.com.br/site/temas/mediagenerico/icon_pesquisar_2_azul.png')
	xbmc.executebuiltin('Container.SetViewMode(51)')

def categoriasonline():
	addDir('Ação','http://www.filmesonlinegratis.net/acao',52,'http://s2.glbimg.com/l-MpNzaPppp2zQ1DU_DcRxH4nuU=/110x83/smart/http://s.glbimg.com/po/tt2/f/original/2015/11/26/appblock-icone.png')
	addDir('Animação','http://www.filmesonlinegratis.net/animacao',52,'http://s2.glbimg.com/l-MpNzaPppp2zQ1DU_DcRxH4nuU=/110x83/smart/http://s.glbimg.com/po/tt2/f/original/2015/11/26/appblock-icone.png')
	addDir('Aventura','http://www.filmesonlinegratis.net/aventura',52,'http://s2.glbimg.com/l-MpNzaPppp2zQ1DU_DcRxH4nuU=/110x83/smart/http://s.glbimg.com/po/tt2/f/original/2015/11/26/appblock-icone.png')
	addDir('Comédia','http://www.filmesonlinegratis.net/comedia',52,'http://s2.glbimg.com/l-MpNzaPppp2zQ1DU_DcRxH4nuU=/110x83/smart/http://s.glbimg.com/po/tt2/f/original/2015/11/26/appblock-icone.png')
	addDir('Comédia Romântica','http://www.filmesonlinegratis.net/comedia-romantica',52,'http://s2.glbimg.com/l-MpNzaPppp2zQ1DU_DcRxH4nuU=/110x83/smart/http://s.glbimg.com/po/tt2/f/original/2015/11/26/appblock-icone.png')
	addDir('Crime','http://www.filmesonlinegratis.net/crime',52,'http://s2.glbimg.com/l-MpNzaPppp2zQ1DU_DcRxH4nuU=/110x83/smart/http://s.glbimg.com/po/tt2/f/original/2015/11/26/appblock-icone.png')
	addDir('Documentário','http://www.filmesonlinegratis.net/documentario',52,'http://s2.glbimg.com/l-MpNzaPppp2zQ1DU_DcRxH4nuU=/110x83/smart/http://s.glbimg.com/po/tt2/f/original/2015/11/26/appblock-icone.png')
	addDir('Drama','http://www.filmesonlinegratis.net/drama',52,'http://s2.glbimg.com/l-MpNzaPppp2zQ1DU_DcRxH4nuU=/110x83/smart/http://s.glbimg.com/po/tt2/f/original/2015/11/26/appblock-icone.png')
	addDir('Faroeste','http://www.filmesonlinegratis.net/faroeste',52,'http://s2.glbimg.com/l-MpNzaPppp2zQ1DU_DcRxH4nuU=/110x83/smart/http://s.glbimg.com/po/tt2/f/original/2015/11/26/appblock-icone.png')
	addDir('Ficção Científica','http://www.filmesonlinegratis.net/ficcao-cientifica',52,'http://s2.glbimg.com/l-MpNzaPppp2zQ1DU_DcRxH4nuU=/110x83/smart/http://s.glbimg.com/po/tt2/f/original/2015/11/26/appblock-icone.png')
	addDir('Guerra','http://www.filmesonlinegratis.net/guerra',52,'http://s2.glbimg.com/l-MpNzaPppp2zQ1DU_DcRxH4nuU=/110x83/smart/http://s.glbimg.com/po/tt2/f/original/2015/11/26/appblock-icone.png')
	addDir('Musical','http://www.filmesonlinegratis.net/musical',52,'http://s2.glbimg.com/l-MpNzaPppp2zQ1DU_DcRxH4nuU=/110x83/smart/http://s.glbimg.com/po/tt2/f/original/2015/11/26/appblock-icone.png')
	addDir('Policial','http://www.filmesonlinegratis.net/policial',52,'http://s2.glbimg.com/l-MpNzaPppp2zQ1DU_DcRxH4nuU=/110x83/smart/http://s.glbimg.com/po/tt2/f/original/2015/11/26/appblock-icone.png')
	addDir('Romance','http://www.filmesonlinegratis.net/romance',52,'http://s2.glbimg.com/l-MpNzaPppp2zQ1DU_DcRxH4nuU=/110x83/smart/http://s.glbimg.com/po/tt2/f/original/2015/11/26/appblock-icone.png')
	addDir('Suspense','http://www.filmesonlinegratis.net/suspense',52,'http://s2.glbimg.com/l-MpNzaPppp2zQ1DU_DcRxH4nuU=/110x83/smart/http://s.glbimg.com/po/tt2/f/original/2015/11/26/appblock-icone.png')
	addDir('Terror','http://www.filmesonlinegratis.net/terror',52,'http://s2.glbimg.com/l-MpNzaPppp2zQ1DU_DcRxH4nuU=/110x83/smart/http://s.glbimg.com/po/tt2/f/original/2015/11/26/appblock-icone.png')
	xbmc.executebuiltin('Container.SetViewMode(51)')
def listarfilmesonline(url):
	soup = gethtml(url)
	table = soup.findAll("div",{"class":"miniaturas"})[0]
	filmes = table.findAll("article")
	for filme in filmes:
		name = filme.img['alt']
		foto = re.compile(r'php(.*?h=185.*?)"').findall(str(filme))[0]
		link = filme.a['href']
		addDir(name.encode('utf8'),link,53,foto.replace('?src=',''),False)
	try:
		page = re.compile(r'class="nextpostslink" href="(.+?)"').findall(str(soup))[0]
		addDir('Proxima Página',page,52,'http://www.inovamobil.com.br/images/icone_navegacao_05.gif')
	except:
		pass
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin('Container.SetViewMode(500)')	
def pesquisaonline():
    keyb = xbmc.Keyboard('', 'Digite o Filme desejado...')
    keyb.doModal()
    if (keyb.isConfirmed()):
        search = keyb.getText()
        parametro_pesquisa=urllib.quote(search)
        url = 'http://www.filmesonlinegratis.net/?s='+parametro_pesquisa
        listarfilmesonline(url)
	return
def Playeronline(name,url,iconimage):
	pg = 0
	caixastatus = xbmcgui.DialogProgress()
	caixastatus.create(addon_name, 'Procurando e Resolvendo Links..','Por Favor Aguardar...')
	caixastatus.update(pg)
	html = abrir_url(url)   
	names = []
	urls  = []
	pg +=30 
	caixastatus.update(pg)
	try:
		link = re.compile(r'src="(.*?vidzi.tv/embed.*?)"').findall(html)[0]
		nhos = 'Vidiz'
		names.append(nhos)
		urls.append(link)
	except:
		pass
	try:
		link = re.compile(r'src="(.*?streamin.to/embed.*?)"').findall(html)[0]
		nhos = 'Streamin.to'
		names.append(nhos)
		urls.append(link)
	except:
		pass
	try:
		link = re.compile(r'src="(.*?vidto.me.*?)"').findall(html)[0]
		nhos = 'Vidto'
		names.append(nhos)
		urls.append(link)
	except:
		pass
	try:
		link = re.compile(r'src="(.*?cloudzilla.*?)"').findall(html)[0]
		nhos = 'Cloudzilla'
		names.append(nhos)
		urls.append(link)
	except:
		pass
	try:
		link = re.compile(r'src="(.*?videomega.*?)"').findall(html)[0]
		nhos = 'VideoMega'
		names.append(nhos)
		urls.append(link)
	except:
		pass
	try:
		link = re.compile(r'src="(.*?nowvideo.*?)"').findall(html)[0]
		nhos = 'NowVideo'
		names.append(nhos)
		urls.append(link)
	except:
		pass
	try:
		link = re.compile(r'data-src="(.*?openload.co.*?)"').findall(html)[0]
		nhos = 'Openload'
		names.append(nhos)
		urls.append(link)
	except:
		pass
	#try:
	#	link = re.compile(r'href="(.*?youwatch.org.*?)"').findall(html)[0]
	#	media_url = urlresolver.resolve(link)
	#	nhos = 'YouWatch'
	#	urls.append(link)
	#except:
	#	pass
	#try:
	#	link = re.compile(r'href="(.*?flashx.tv.*?)"').findall(html)[0]
	#	nhos = 'FlashX'
	#	names.append(nhos)
	#	urls.append(link)
	#except:
	#	pass
	#try:
	#	link = re.compile(r'"(.*?ok.ru.*?)"').findall(html)[0]
	#	nhos = 'ok.ru'
	#	names.append(nhos)
	#	urls.append(link)
	#except:
	#	pass
	#try:
	#	link = re.compile(r'href="(.*?video.tt.*?)"').findall(html)[0]
	#	nhos = 'video.tt'
	#	names.append(nhos)
	#	urls.append(link)
	#except:
	#	pass
	pg +=30
	caixastatus.update(pg)
	opcao = xbmcgui.Dialog().select('Selecione o Host desejado:', names)
	if opcao == -1 : return
	pg +=30
	caixastatus.update(pg)
	url = urls[opcao]
	media_url = urlresolver.resolve(url)
	pg=100
	caixastatus.update(pg)
	caixastatus.close()
	playlist = xbmc.PlayList(1)
	playlist.clear()
	listitem = xbmcgui.ListItem(name,thumbnailImage=iconimage)
	listitem.setInfo("Video", {"Title":name})
	listitem.setProperty('mimetype', 'video/mp4')
	playlist.add(str(media_url),listitem)	
	xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
	xbmcPlayer.play(playlist)	
################################24h###############################

def listar24h():
	html = gethtml(urlbase2)
	items = html.findAll("li")
	for item in items:
		url = base2+item.a["href"].replace('.html','.php')
		name = item.a["href"].replace('.html','')
		img = "-"
		if name == '/':
			name = 'Desenhos e Series'
			img = ds24
			url = 'https://copy.com/Vq3DQcVHwXf6thbC?download=1'
		if name == 'batman':
			name = 'Batman'
			img = 'http://www.thecartoonpictures.com/data/media/44/batman_logo.jpg'
		if name == 'ben10':
			name = 'Ben 10'
			img = 'https://upload.wikimedia.org/wikipedia/en/thumb/b/bc/Ben_10_logo.svg/991px-Ben_10_logo.svg.png'	
		if name == 'bigbang':
			name = 'The Big Bang Theory'
			img = 'http://www.academiawashington.com.br/wp-content/uploads/2015/03/The_Big_Bang_Theory.jpg'
		if name == 'bobby':
			name = 'O Fantastico Mundo de Bobby'
			img = 'http://2.bp.blogspot.com/_-TryMvAR14c/TQ5ura9IdlI/AAAAAAAAABM/qlze8Zayg2w/s1600/wall1_1024.jpg'
		if name == 'bobesponja':
			name = 'Bob Esponja'
			img = 'https://upload.wikimedia.org/wikipedia/pt/c/c2/Bob_Esponja_Logo.png'
		if name == 'breaking':
			name = 'Breaking Bad'
			img = 'https://d3ui957tjb5bqd.cloudfront.net/uploads/2013/09/breaking-bad.png'
		if name == 'castelo':
			name = 'Castelo Ra-Tim-Bum'
			img = 'https://upload.wikimedia.org/wikipedia/pt/c/c8/Castelo_R%C3%A1-Tim-Bum.jpg'
		if name == 'caverna':
			name = 'Caverna do Dragao'
			img = 'http://caverna.mushi-san.com/m_i/caverna2013.png'
		if name == 'cdz':
			name = 'Os Cavaleiros do Zodiaco'	
			img = 'https://angelotti.files.wordpress.com/2011/02/saintseiya011.jpg'
		if name == 'chaves':
			name = 'Chaves'	
			img = 'http://i.ytimg.com/vi/b_3yEcFROws/maxresdefault.jpg'
		if name == 'chuck':
			name = 'Chunk'	
			img = 'http://www.entertainmentwallpaper.com/images/desktops/movie/tv-chuck37.jpg'
		if name == 'criminalminds':
			name = 'Criminal Minds'	
			img = 'https://upload.wikimedia.org/wikipedia/en/d/d2/Criminal_Minds_Logo,_dec_2014.png'
		if name == 'cris':
			name = 'Todo Mundo Odeia o Chris'	
			img = 'http://1.bp.blogspot.com/-yxKlXHbod9c/VeZDRgdlBeI/AAAAAAAAALY/B-iD4yZXC0c/s1600/capachris.png'
		if name == 'csi':
			name = 'CSI: Investigacao Criminal'	
			img = 'https://autopsiandoseries.files.wordpress.com/2013/10/csilogo.jpg'
		if name == 'dbz':
			name = 'Dragon Ball Z'	
			img = 'http://iptv.codigolivre.net/logos/Dragon-Ball-Z-logo.png'
		if name == 'dinossauros':
			name = 'Familia Dinossauros'	
			img = 'http://i.ytimg.com/vi/aIDhXUVeHB4/maxresdefault.jpg'
		if name == 'doug':
			name = 'Doug'	
			img = 'http://3.bp.blogspot.com/-BZsOG-gbUgQ/VedNTJPNQvI/AAAAAAAAIMo/WfOXCtlnD8M/s640/899f3b_c50e8121a2c94f749a8225dbe6e6b24c.png_srz_525_225_75_22_0.50_1.20_0.00_png_srz.png'
		if name == 'drakejosh':
			name = 'Drake e Josh'	
			img = 'http://vignette1.wikia.nocookie.net/fictionalcrossover/images/7/71/Drake_and_Josh_logo.png/revision/latest?cb=20150706030147'
		if name == 'ducktales':
			name = 'DuckTales - Os Cacadores de Aventuras'	
			img = 'http://vignette3.wikia.nocookie.net/disney/images/d/da/Ducktales_Logo.png/revision/latest?cb=20141110120149'
		if name == 'family':
			name = 'Uma Familia da Pesada'	
			img = 'http://1.bp.blogspot.com/-stOnt1SWERM/U85wlmdZjBI/AAAAAAABgcU/z7EsRW49rYc/s1600/4.png'
		if name == 'filmes':
			name = 'Filmes 24h/dia'	
			img = 'http://1.bp.blogspot.com/-AwHKJlNb2aE/UY80p7hyqKI/AAAAAAAACA8/52Mv1dney3c/s1600/filmes-24-horas.png'
		if name == 'flintstones':
			name = 'Os Flintstones'	
			img = 'https://upload.wikimedia.org/wikipedia/commons/3/3d/The_Flintstones.png'
		if name == 'friends':
			name = 'Friends'	
			img = 'http://www.blindfiveyearold.com/wp-content/uploads/2014/02/friends-tv-show-logo.png'
		if name == 'futurama':
			name = 'Futurama'	
			img = 'http://www.buckbokai.com/wp-content/uploads/2012/07/Futurama-logo-with-characters-1024x602.png'
		if name == 'galinhapintadinha':
			name = 'Galinha Pintadinha'	
			img = 'http://mlb-s2-p.mlstatic.com/vetores-galinha-pintadinha-e-turma-em-cdr-png-e-jpeg-15130-MLB20097695230_052014-F.jpg'
		if name == 'glee':
			name = 'Glee - Em Busca Da Fama'	
			img = "http://img2.wikia.nocookie.net/__cb20130812200618/diannaagron/images/1/17/Glee'sd_logo.png"
		if name == 'gossip':
			name = 'Gossip Girl: A Garota do Blog'	
			img = 'http://excetoaescrita.com.br/wp-content/uploads/2015/06/635644706140430508-638559820_GossipGirl.png'
		if name == 'heroes':
			name = 'Heroes'	
			img = 'https://upload.wikimedia.org/wikipedia/en/7/70/Heroes_logo.png'
		if name == 'icarly':
			name = 'iCarly'	
			img = 'http://vignette3.wikia.nocookie.net/icarly/images/c/c9/Logo.png/revision/latest?cb=20100807230659'
		if name == 'jackie':
			name = 'As Aventuras de Jackie Chan'	
			img = 'http://orig01.deviantart.net/946c/f/2012/167/1/5/it__s_just_the_cover_for_jackie_chan_adventures_by_g3stalt-d53rnem.jpg'
		if name == 'jaspion':
			name = 'O Fantastico Jaspion'	
			img = 'https://nextconqueror.files.wordpress.com/2011/08/o-fantc3a1stico-jaspion.jpg'
		if name == 'kenanekel':
			name = 'Kenan e Kel'	
			img = 'http://vignette3.wikia.nocookie.net/nickelodeon/images/f/f6/Kenan_and_Kel_logo.png/revision/latest?cb=20140906040452'
		if name == 'lost':
			name = 'Lost'	
			img = 'http://i93.photobucket.com/albums/l66/reavenm/clearArt/lost.png'
		if name == 'maluconopedaco':
			name = 'Um Maluco no Pedaco'	
			img = 'http://vacanerd.com.br/wp-content/uploads/2014/01/Freshprincelogo.jpg'
		if name == 'maskara':
			name = 'O Maskara'	
			img = 'http://vignette2.wikia.nocookie.net/the-mask/images/7/78/The-mask-5188b3e1c43d3.png/revision/latest?cb=20150211203317'
		if name == 'naruto':
			name = 'Naruto'	
			img = 'http://b1969d.medialib.glogster.com/media/3232b6b56942d928c5004fbb7c5be61cd9c34903e8729ae78d0d8097de6ba5f5/naruto-logo.jpg'
		if name == 'padrinhos':
			name = 'Os Padrinhos Magicos'	
			img = 'http://vignette3.wikia.nocookie.net/vvikipedia/images/0/08/Os_Padrinhos_M%C3%A1gicos_logotipo_Brasil.png/revision/latest?cb=20150406191131&path-prefix=pt'
		if name == 'patroa':
			name = 'Eu a Patroa e as Crianças'	
			img = 'http://assistirfilmesonline.club/wp-content/uploads/2015/09/eu-a-patroa-e-as-criancas-logo.jpg'
		if name == 'picapau':
			name = 'Pica-Pau '	
			img = 'http://tv.recordjp.com/wp-content/uploads/2013/11/Pica_pau_W.png'
		if name == 'pinguins':
			name = 'Os Pinguins de Madagascar'	
			img = 'http://nick-intl.mtvnimages.com/uri/mgid:file:gsp:scenic:/international/mundonick.com.br/NickV2/MOBILE/BRASIL/PINGUINOS-MADAGASCAR_property-header-480x270_port.png?height=0&width=480&matte=true&crop=false'
		if name == 'prisonbreak':
			name = 'Prison Break: Em Busca da Verdade'	
			img = 'http://www.fun-lover.com/graphic-shop/Clips/images/Television/prison-break-e3.png'
		if name == 'scooby':
			name = 'Scooby-Doo'	
			img = 'http://www.clipartsegifs.com.br/cliparts/variados/scoobydoo/scooby_logo.gif'
		if name == 'simpsons':
			name = 'Os Simpsons'	
			img = 'http://img3.wikia.nocookie.net/__cb20140919202759/futuramabr/pt-br/images/1/1b/Simpsons.png'
		if name == 'small':
			name = 'Smallville: As Aventuras do Superboy'	
			img = 'http://vectorise.net/logo/wp-content/uploads/2010/08/smallville.jpg'
		if name == 'southpark':
			name = 'South Park'	
			img = 'http://i.imgur.com/qvmONHu.png'
		if name == 'supernatural':
			name = 'Sobrenatural'	
			img = 'http://www.dailymovies.ir/wp-content/uploads/2015/06/supernatural___hunters_logo_by_shervell-d5txon6.png'
		if name == 'thunder':
			name = 'ThunderCats'	
			img = 'http://img00.deviantart.net/b4fa/i/2011/100/e/2/thundercats_logo___2011_by_camarinox-d3dpkkn.png'
		if name == 'tomejerry':
			name = 'Tom e Jerry'	
			img = 'http://2.bp.blogspot.com/-Ee4iiZ34NLM/UyJA92WuixI/AAAAAAAAAs0/6H1YlM9fAEg/s1600/4rpd39.jpg.png'
		if name == 'two':
			name = 'Dois Homens e Meio'
			img = 'https://lh3.googleusercontent.com/-CFuIug3wPfA/AAAAAAAAAAI/AAAAAAAAAAA/-MLIu-Ob2w8/s0-c-k-no-ns/photo.jpg'
		if name == 'xmen':
			name = 'X-Men'	
			img = 'http://img4.wikia.nocookie.net/__cb20140212195020/logopedia/images/f/ff/X-men-logo.png'
		if name == 'yugioh':
			name = 'Yu-Gi-Oh!'	
			img = 'http://img1.wikia.nocookie.net/__cb20100108162659/yugiohsecrets/images/8/86/Yu-Gi-Oh_Logo.png'	
		addDir(name,url,21,img,False)
	xbmc.executebuiltin('Container.SetViewMode(500)')

def player24h(name,url,iconimage):
	try:
		html = abrir_url(url)
		rtmp = re.compile('streamer=(.+?)&autostart').findall(html)[0].replace('206.190.132.244/tvamigos','208.53.180.218/ctv')
		palypath = re.compile('file=(.+?).flv').findall(html)[0]
		link = rtmp + ' playpath='  + palypath + ' swfUrl=http://www.carolineoliveira.com.br/swf/player.swf pageUrl='+ url
		playlist = xbmc.PlayList(1)
		playlist.clear()
		listitem = xbmcgui.ListItem(name,thumbnailImage=iconimage)
		listitem.setInfo("Video", {"Title":name})
		listitem.setProperty('mimetype', 'video/mp4')
		playlist.add(link,listitem)	
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)
	except:
		playlist = xbmc.PlayList(1)
		playlist.clear()
		listitem = xbmcgui.ListItem(name,thumbnailImage=iconimage)
		listitem.setInfo("Video", {"Title":name})
		listitem.setProperty('mimetype', 'video/mp4')
		playlist.add(url,listitem)	
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)


##############################################################################################################
##											FUNÇÕES															##
##############################################################################################################

def addDir(name,url,mode,iconimage,pasta=True,total=1,plot=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="iconimage", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', iconimage)
	liz.setInfo( type="video", infoLabels={ "title": name, "plot": plot } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok

def addDirc(name,url,mode,iconimage,pasta=True,total=1,plot=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode('utf-8'))+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="iconimage", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', iconimage)
	liz.setInfo( type="video", infoLabels={ "title": name, "plot": plot } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok
	
	
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
    soup = BeautifulSoup(link,"html.parser")
    return soup

def getwms():
	req = urllib2.Request(base64.b64decode('aHR0cDovL3R2LW1zbi5jb20vbWVzdHJlLnBocA=='))
	req.add_header('referer',base64.b64decode('aHR0cDovL3R2LW1zbi5jb20vZGlzbmV5Lmh0bWw='))
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	wms = re.compile(r"AuthSign=(.+?)&auto").findall(link)[0]
	return wms
def gettoken():
	req = urllib2.Request(base64.b64decode('aHR0cDovL2lwdHZici5vcmcvYWRkb25pcHR2YnIvdG9rZW4udHh0'))
	response = urllib2.urlopen(req)
	token=response.read()
	response.close()
	return token	
	
def getepg():
	limp = open(epg, 'w')
	limp.write('')
	limp.close()
	html = gethtml('http://meuguia.tv/programacao/categoria/Todos')
	soup = html.findAll("li")
	for item in soup:
		nome = item.a["href"].replace('/programacao/canal/','')
		program = item.a["title"]
		full = nome+','+program
		arquivo = open(epg, 'a')
		arquivo.write(full.encode('utf-8')+'\n') 
		arquivo.close()

def configurar():
	xbmcaddon.Addon(addon_id).openSettings()
	return menu()
		
def mensagem():
	html = abrir_url(base64.b64decode('aHR0cDovL2lwdHZici5vcmcvYWRkb25pcHR2YnIvbWVuc2FnZW0udHh0'))
	local = open(msg,'r').read()
	if html != local:
		limp = open(msg, 'w')
		limp.write(html) 
		limp.close()
		xbmcgui.Dialog().ok(addon_name,html)
	else:
		pass	
############################################################################################################
#                                               GET PARAMS                                                 #
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
abrir_url('http://iptvbr.org/addoniptvbr/acessos.php')

if mode==None or url==None or len(url)<1:
        menu()
elif mode==1:		
	deftv()
elif mode==2:		
	listarcanais(url)	
elif mode==3:		
	playertv(name,url,iconimage)
elif mode==4:	
	jogos_aovivo()
elif mode==5:
	player_youtube(url)
elif mode==6:
	canaloff()
elif mode==8:
	playermaster(name,url,iconimage)
elif mode==9:
	menufilmes()	
elif mode==10:
	listarcat()		
elif mode==11:
	listarfilmes(url)
elif mode==12:
	menufilme(name,url,iconimage)	
elif mode==13:
	playerfilmes(name,url,iconimage)
elif mode==14:
	getsinopse(url)	
elif mode==15:	
	gettrailer(url)
elif mode==16:
	depois(url)
elif mode==17:
	favoritos()
elif mode==18:
	limpar()
elif mode==20:
	listar24h()
elif mode==21:
	player24h(name,url,iconimage)
elif mode==31:
	catguia()	
elif mode==32:
	canaisguia(url)		
elif mode==33:
	progcomplt(url,iconimage)
elif mode==34:	
	programa(url)	
elif mode==40:
	menucine()
elif mode==41:
	categoriascine()
elif mode==42:	
	listarfilmescine(url)
elif mode==43:
	Playercine(name,url,iconimage)	
elif mode==44:
	pesquisacine()	
elif mode==50:
	menuonline()
elif mode==51:
	categoriasonline()
elif mode==52:	
	listarfilmesonline(url)
elif mode==53:
	Playeronline(name,url,iconimage)	
elif mode==54:
	pesquisaonline()
elif mode==100:
	configurar()
elif mode==101:
	agendaesportiva()
xbmcplugin.endOfDirectory(int(sys.argv[1]))