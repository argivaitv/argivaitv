#!/usr/bin/env python
# -*- coding: UTF-8 -*-
##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP

addon_id = 'plugin.video.PortugalTv'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = os.path.join(addonfolder,'resources','img')
fanart = os.path.join(addonfolder,'fanart.png')

################################################## 

#MENUS############################################

def CATEGORIES():
	addDir('TV','http://pastebin.com/raw.php?i=BGZbtKzu',2,os.path.join(artfolder,'1.png'))
	addDir('Generalistas','http://pastebin.com/raw.php?i=sDA7CCSk',2,os.path.join(artfolder,'2.png'))
	addDir('Noticias','http://pastebin.com/raw.php?i=0wuRWr3H',2,os.path.join(artfolder,'3.png'))
	addDir('Filmes','http://pastebin.com/raw/e4HBUCHx',2,os.path.join(artfolder,'4.png'))
	addDir('Infantil','https://dl.dropboxusercontent.com/s/wc0b810rgxa49xk/Infantil.txt?dl=0',2,os.path.join(artfolder,'7.png'))
	addDir('xxx','https://dl.dropboxusercontent.com/s/fk700x5nlwc855u/xxx.txt?dl=0',2,os.path.join(artfolder,'6.png'))
	addDir('Plexus','http://pastebin.com/raw.php?i=2WAz27e3',2,os.path.join(artfolder,'9.png'))
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	if "confluence" in xbmc.getSkinDir(): xbmc.executebuiltin('Container.SetViewMode(1000)')

###################################################################################
#FUNCOES

def listar_videos(url):
	soup = getSoup(url)
	items = soup.findAll("item")
	a = []
	for item in items:
		try: nomeprog = '  [B][COLOR yellow]%s[/COLOR][/B]' % canais[item.sigla.string]['nomeprog'].decode("utf-8","ignore")
		except: nomeprog = ''
		try: descprog = canais[item.sigla.string]['descprog']
		except: descprog = ''
		temp = [item.link.string,"[COLOR red]%s[/COLOR]" % item.title.text.upper() + nomeprog,item.thumbnail.string,descprog]
		if temp not in a: a.append(temp)
	total = len(a)
	for url2, titulo, img, plot in a: 
		if 'plugin' in url2: url2 = url2.replace(';=','=')
		addLink(titulo,url2,img,plot)
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	if "confluence" in xbmc.getSkinDir(): xbmc.executebuiltin('Container.SetViewMode(1000)')

def play(url):
	listitem = xbmcgui.ListItem()
	listitem.setPath(url)
	listitem.setProperty('mimetype', 'video/x-msvideo')
	listitem.setProperty('IsPlayable', 'true')
	try:
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(url)
	except:
		dialog = xbmcgui.Dialog()
		dialog.ok(" Erro:", " Impossível abrir vídeo! ")
		pass

################################################
#    Funções relacionadas a media.             #
#                                              #
################################################

def makeRequest(url, headers=None):
        try:
            if headers is None: headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0'}
            req = urllib2.Request(url,None,headers)
            response = urllib2.urlopen(req)
            data = response.read()
            response.close()
            return data
        except urllib2.URLError, e:
            print 'URL: '+url
            if hasattr(e, 'code'):
                print 'CODIGO ERRO - %s.' % e.code
                xbmc.executebuiltin("XBMC.Notification(PORTUGALTV,CODIGO ERRO - "+str(e.code)+",10000,"+icon+")")
            elif hasattr(e, 'reason'):
                addon_log('ERRO AO CONECTAR AO SERVIDOR.')
                addon_log('Reason: %s' %e.reason)
                xbmc.executebuiltin("XBMC.Notification(PORTUGALTV,CODIGO ERRO. - "+str(e.reason)+",10000,"+icon+")")

def getSoup(url):
        data = makeRequest(url)
        return BeautifulSOAP(data, convertEntities=BeautifulStoneSoup.XML_ENTITIES)



def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def addLink(name,url,iconimage,plot=''):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "plot": plot } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,pasta=True,total=1,plot=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	liz.setInfo( type="video", infoLabels={ "title": name, "plot": plot } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok

############################################################################################################
#                                               GET PARAMS                                                 #
############################################################################################################
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]
        return param

params=get_params()
url=None
name=None
mode=None
iconimage=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)

###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################
if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==2: listar_videos(url)
elif mode==3: encontrar_fontes(url)
elif mode==4: play(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
