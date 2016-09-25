#try:	
#imports
from tkinter import *
import pafy
import requests
import sys
from bs4 import BeautifulSoup
import urllib
from PIL import Image, ImageTk
#fix warning error
import logging
logging.getLogger().setLevel(logging.ERROR)

class Ytvd(object):
	def __init__(self, main): # interface basica
		self.tela_inicial = Frame(main)
		self.tela_inicial.pack()
		self.text1 = Label(self.tela_inicial, text = 'Digite o link do vídeo')
		self.text1.pack()
		self.entry1 = Entry(self.tela_inicial)
		self.entry1.pack()
		self.button1 = Button(self.tela_inicial, text = 'Vai!', command= self.Calcular_video)
		self.button1.pack()
	
	def Calcular_video(self):
		# informações
		self.video = pafy.new(self.entry1.get()) #<<<<< transformar em codigo
		#self.video = pafy.new('https://www.youtube.com/watch?v=8UJwtWiTyno') # VIDEO ESPECIFICO 
		self.nome = self.video.title
		self.autor = self.video.author
		self.publicado = self.video.published
		self.thumb = self.video.thumb
		self.video_id = self.video.videoid
		self.views = self.video.viewcount
		self.like = self.video.likes
		self.dislike = self.video.dislikes
		self.time = self.video.duration

		#define a imagem da thumbnail
		urllib.request.urlretrieve(self.video.thumb, 'thumb.jpg')
		self.thumb = Image.open('thumb.jpg')
		self.thumb = self.thumb.resize((180,135), Image.ANTIALIAS)
		self.thumb_img = ImageTk.PhotoImage(self.thumb)


		# chama a segunda janela da GUI
		self.Segunda_tela()
	# pega o link informado e exibe 
	# informações do video
	def Segunda_tela(self): 
		# limpa a janela para exibir informações de video
		self.tela_inicial.pack_forget()
		# exibe informações de video
		
		# frame principal
		self.tela_video = Frame(main)
		self.tela_video.pack()
		
		# frame da thumbnail
		self.thumbnail = Frame(self.tela_video)
		self.thumbnail.pack(side= TOP)
		# frame das labels pré-definidas
		self.labels1 = Frame(self.tela_video)
		self.labels1.pack(side= LEFT)
		# frame das labels de informação
		self.labels2 = Frame(self.tela_video)
		self.labels2.pack(side= LEFT)
		# frame dos botões de download
		self.downloads = Frame(main)
		self.downloads.pack(side= LEFT)
		self.downloads2 = Frame(main)
		self.downloads2.pack(side= RIGHT)
		# frame da label de download
		self.labels3 = Frame(self.tela_video).pack()
		self.label3 = Label(self.labels3, font=('Verdana', 15, 'bold'), fg= 'red', text='Aguardando comando.')
		self.label3.pack()
		# Thumbnail do subframe1
		self.imagem_thumb = Label(self.thumbnail)
		self.imagem_thumb['image'] = self.thumb_img
		self.imagem_thumb.pack()
		
		# Informações do subframe1
		inf_list = ['Nome do vídeo: ' ,'Tempo de duração: ' , 
					'Nome do canal: ' ,'Data de publicação: ' , 
					'Total de vizualizações: '  , 'Total de gostei: '  , 
					'Total de não gostei: ']
		self.font1 = ('verdana', '12','bold')
		for item in inf_list:
			inf = Label(self.labels1, text=item, font=self.font1)
			inf.pack(anchor=E)
		# informações do subframe2
		inf_list2 = [str(self.nome), str(self.time), str(self.autor), str(self.publicado),str(self.views), str(self.like), str(self.dislike)]
		self.font2 = ('verdana', '12')
		for item in inf_list2:
			inf2 = Label(self.labels2, text=item, font=self.font2)
			inf2.pack(anchor=W)
		# botoes de download do subframe3
		self.voltar= Button(self.downloads, text='Voltar', command = self.Voltar, fg ='blue', font=('verdana', 15, 'bold'))
		self.voltar.pack(anchor= W)
		self.baixar = Button(self.downloads2, text='Baixar vídeo', command = self.Baixar,fg = 'red', font=('verdana', 15, 'bold'))
		self.baixar.pack(anchor = E)

	def Voltar(self):
		self.tela_video.pack_forget()
		self.downloads.pack_forget()
		self.downloads2.pack_forget()
		self.tela_inicial.pack()

	def Baixar(self):
		# escreve o xml
		self.video_num = 0
		self.arq_len = 3
		self.arq = open('file_des.xml', 'w')
		self.arq.write('<?xml verion="1.0" encoding ="utf-8" ?>\n')
		self.arq.write('<video>\n')
		for s in self.video.streams:
			self.video_num += 1
			self.arq.write('    <inf num="'+ str(self.video_num)+'"''>\n')
			self.arq.write('        <resulution>'+s.resolution+'</resolution>\n')
			self.arq.write('        <extension>'+s.extension+'</extension>\n')
			self.arq.write('    </inf>\n')
			self.arq_len += 4
		self.arq.write('</video>')
		self.arq.close()
		# transforma o arquivo em uma string manipulavel.
		self.arq = open('file_des.xml','r')
		self.arq_txt = ''
		for line in self.arq:
			self.arq_txt += line
		self.arq.close()
		self.arq = open('file_des.xml', 'r')

		# cria a segunda janela
		self.sec_wind = Toplevel()
		self.sec_wind.title('Baixar')
		# mensagem da segunda janela
		self.msg = Label(self.sec_wind, text='Selecione a qualidade desejada')
		self.msg.pack()
		# Frame das opções
		self.options = Frame(self.sec_wind)
		self.options.pack()
		# opções:
		self.v = IntVar()
		self.v.set(1)
		self.baixar_alta = Radiobutton(self.options, text='Alta', variable=self.v, value=1).pack()
		self.baixar_media = Radiobutton(self.options, text='Média', variable=self.v, value=2).pack()
		self.baixar_baixa = Radiobutton(self.options, text='Baixa', variable=self.v, value=3).pack()
		self.download = Button(self.options, text='Baixar', command=self.Predownloading).pack()
		self.audio = IntVar()
		self.baixar_audio = Checkbutton(self.options, text='Apenas áudio.', variable=self.audio).pack()
	def Predownloading(self):
		self.label3.configure(text='Baixando...',fg='yellow')
		self.label3.update()
		self.sec_wind.destroy()	
		self.Checkdownload()

	def Checkdownload(self):
		if (self.audio.get()) == 0:  # se for baixar o vídeo: 
			if (self.v.get()) == 1:
				self.best = self.video.getbest()
				try:
					self.filename = self.best.download()
					self.label3['text']= 'Download concluído.'
					self.label3['fg'] = 'green'
				except:
					self.label3['text']= 'Erro!'
					self.label3['fg'] = 'red'
				
			if (self.v.get()) == 2:
				if self.video_num >= 3:
					self.temp = self.video_num / 2
					self.temp = int(self.temp) * 3 + 2
					self.text = self.arq.readlines()[self.temp -1:self.temp +2]
					self.reso = str(self.text[1])
					self.reso = self.reso[8+12:len(self.reso) -14]
					self.ext = str(self.text[2])
					self.ext = self.ext[8+11:len(self.ext)-13]
				else:
					self.errormsg = Toplevel()
					self.errormsg.title('Erro!')
					self.erromsg_label = Label(self.errormsg, text='Este vídeo não possui uma qualidade média, por favor selecione outra opção.', fg='red', font='verdana').pack()# ARRUMAR AQUI !!!!!!!!		
			if (self.v.get()) == 3:
					self.arq_find = self.arq_txt.find('320x240')
					if self.arq_find > 0: #baixa 240p se tiver
						self.reso = '320x240'
						self.ext = self.arq_txt[self.arq_find + 7:self.arq_find + 44] 
						self.ext2 = self.ext.find('</extension>')
						self.ext = self.ext[self.ext2 - 3:self.ext2]
						print (self.reso)
						print (self.ext)
					else: # se não tiver 240, baixa a pior mesmo
						self.text = self.arq.readlines()[self.arq_len -5: self.arq_len -1]
						self.reso = str(self.text[1])
						self.reso = self.reso[8+12:len(self.reso) -14]
						self.ext = str(self.text[2])
						self.ext = self.ext[8+11:len(self.ext)-13]

		elif (self.audio.get()) == 1: #se for baixar apenas áudio:
			if (self.v.get()) == 1:
				self.bestaudio = self.video.getbestaudio()
				try:
					self.bestaudio.download()
					self.label3['text']= 'Download concluído.'
					self.label3['fg'] = 'green'
				except:
					self.label3['text']= 'Erro!'
					self.label3['fg'] = 'red'
			if (self.v.get()) == 2:
				self.count = 0
				self.count2 = 0
				for item in self.video.audiostreams:
					self.count += 1
				for item in self.video.audiostreams:
					self.count2 += 1
					if self.count2 == self.count:
						try:
							item.download()
							self.label3['text']= 'Download concluído.'
							self.label3['fg'] = 'green'
						except:
							self.label3['text']= 'Erro!'
							self.label3['fg'] = 'red'

			if (self.v.get()) == 3:
				print('a')

		else:
			print ('WTF !?!?!')
# define a GUI
main = Tk()
main.title('Youtube video downloader')
# main.geometry('500x300') #<<< transformar em codigo

# chama a GUI
Ytvd(main)
main.mainloop()
#except:
#	nada = input()   