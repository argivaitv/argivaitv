#!/usr/bin/env python
# -*- coding: UTF-8 -*-
##############BIBLIOTECAS A IMPORTAR####################

import xbmcplugin,xbmcgui,xbmc,xbmcaddon,os,sys,urllib,urllib2
from bs4 import BeautifulSoup

#######################SETTINGS#########################

addon_id = 'plugin.audio.palcomp3'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
fanart = addonfolder + '/fanart.png'
urlbase = 'http://palcomp3.com/'


###################################################MENUS############################################
	

def menus():
	addDir('Artistas mais acessados',urlbase,6,'-')
	addDir('Destaques',urlbase + 'destaques.htm',5,'-')
	addDir('Estilos Musicais',urlbase + 'estilos-musicais.htm',1,'-')
	addDir('Top Musica','-',11,'-')
	addDir('Top Artista','-',12,'-')
	
def topmusica():
	addDir('Hoje',urlbase + 'top-musicas/hoje.htm',7,'-')
	addDir('Semana',urlbase + 'top-musicas/',7,'-')
	addDir('Mes',urlbase + 'top-musicas/mes.htm',7,'-')
	addDir('Geral',urlbase + 'top-musicas/geral.htm',7,'-')

def topartista():
	addDir('Hoje',urlbase + 'top-artistas/hoje.htm',6,'-')
	addDir('Semana',urlbase + 'top-artistas/',6,'-')
	addDir('Mes',urlbase + 'top-artistas/mes.htm',6,'-')
	addDir('Geral',urlbase + 'top-artistas/geral.htm',6,'-')
	
def estilos(url):
	html = gethtml(url)
	soup = html.find("div", { "id" : "lista_estilos_musicais" })
	estilos = soup.findAll("li")
	for estilo in estilos:
		name = estilo.a.text
		url = estilo.a["href"]
		addDir(name.encode('utf-8'),urlbase + url,2,'-')
		
def submenu(url):
	addDir('Destaques',url,5,'-')
	addDir('Artistas mais acessados',url,6,'-')
	addDir('Todos os artistas',url+'todos.htm',4,'-')

def todos(url):
	html = gethtml(url)
	soup = html.find("div", { "id" : "lista_especifico" })
	artistas = soup.findAll("li")
	for artista in artistas:
		name = artista.a.text
		url = artista.a["href"]
		addDir(name.encode('utf-8'),urlbase + url,7,'-')		

def destaques(url):
	html = gethtml(url)
	soup = html.find("ul", { "id" : "ul_destaques"})
	destaques = soup.findAll("a")
	for destaque in destaques:
		name = destaque.img["alt"]
		img = destaque.img["src"]
		url = destaque["href"]
		addDir(name.encode('utf-8'),urlbase + url,7,img)		

def acessados(url):		
	html = gethtml(url)
	soup = html.find("ol", { "id" : "top-listagem"})
	acessados = soup.findAll("li")
	for acessado in acessados:
		name = acessado.a["href"].replace('/',' ').replace('-',' ')
		url = acessado.a["href"]	
		addDir(name.encode('utf-8'),urlbase + url,7,img)		
	
def playlistplay(url):
	playlist = xbmc.PlayList(1)
	playlist.clear()
	html = gethtml(url)
	soup = html.find("div", { "class" : "player_lista"})
	musicas = soup.findAll("li")
	for musica in musicas:
		name = musica.a.text
		faixa = musica["data-url_mp3"]
		url = 'http:' + faixa
		liz = xbmcgui.ListItem(name, thumbnailImage=iconimage)
		liz.setInfo('video', {'Title': name})
		liz.setProperty('mimetype','audio/mp3')				
		playlist.add(url,liz)
	xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
	xbmcPlayer.play(playlist)
	
	
def listarmusicas(url):
	addDir('[B][COLOR white]Tocar Todas[/COLOR][/B]',url,10,'http://www.bandfmlages.com.br/fmanager/tvbv/promocoes/foto19_1.jpg',False)
	html = gethtml(url)
	soup = html.find("div", { "class" : "player_lista"})
	im = html.find("div", { "class" : "player_media initial_info"})
	img = im.img["src"]
	musicas = soup.findAll("li")
	for musica in musicas:
		name = musica.a.text
		faixa = musica["data-url_mp3"]
		url = 'http:' + faixa
		addDir(name.encode('utf-8'),url,8,urlbase +img,False)
		xbmc.executebuiltin('Container.SetViewMode(51)')		

def play(name,url):
	playlist = xbmc.PlayList(1)
	playlist.clear()
	liz = xbmcgui.ListItem(name, thumbnailImage=iconimage)
	liz.setInfo('video', {'Title': name})
	liz.setProperty('mimetype','audio/mp3')				
	playlist.add(url,liz)
	xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
	xbmcPlayer.play(playlist)
	
##############################################################################################################
##											FUNÇÕES															##
##############################################################################################################


def addDir(name,url,mode,iconimage,pasta=True,total=1):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok
	
def gethtml(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    soup = BeautifulSoup(link)
    return soup

	
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


if mode==None or url==None or len(url)<1:
        print ""
        menus()
elif mode==1:
	estilos(url)
elif mode==2:
	submenu	(url)
elif mode==4:
	todos(url)
elif mode==5:
	destaques(url)	
elif mode==6:
	acessados(url)	
elif mode==7:
	listarmusicas(url)
elif mode==8:
	play(name,url)
elif mode==10:
	playlistplay(url)
elif mode==11:	
	topmusica()
elif mode==12:	
	topartista()
xbmcplugin.endOfDirectory(int(sys.argv[1]))
