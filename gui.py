# -*- coding: utf-8 -*-

import wx
import math
import os
from fasta import *
from dotplot import *
from wykres import *
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from datetime import date

sciezki=[]
nazwysekwencji=[]
sek=[]
dotplotn=[]
dotplotseq=[]
nazwysekwencji, sek, sciezki=wczytaj_zapisane_dane()
wykresy=[]
Nplot=0
parametry=[]


def update(evt):
	tekst=wyszukiwarka.GetValue()
	t=tempn.copy()
	for x in tempn:
		if tekst.lower() not in x.lower():
			t.remove(x)
	hw.Clear()
	if len(t)>0 and len(tekst)>0:
		hw.InsertItems(t,hw.GetCount())
	if len(tekst)==0:
		hw.InsertItems(tempn, 0)
			

def wczyt_sek(evt):
	global tempn, temps, tempw
	okno1.Hide()
	dialog=wx.FileDialog(okno1,message='Wybierz plik')
	try:
		if dialog.ShowModal() == wx.ID_OK:
			s=dialog.GetPaths()
			tempn, temps=wczytaj_fasta(s[0])
			hw.InsertItems(tempn,hw.GetCount())
			tempw=s[0]
			okno2.Show()
			okno2.Center()
		else:
			okno1.Show()
	except:
		okno1.Show()
		wx.MessageBox("Plik ma niepoprawny format")

def choose(evt):
	naglowki=[]
	try:
		selected=hw.GetSelections()
		for i in selected:
			naglowki.append(hw.GetString(i))
		for x in naglowki:
			for i in range(len(tempn)):
				if tempn[i]==x:
					sek.append(temps[i])
		if wx.MessageDialog(okno2, "Czy chcesz zmienić nazwy wybranych sekwencji?", caption='Nazwy', style=wx.YES_NO).ShowModal()==wx.ID_YES:
			i=0
			for x in naglowki:
				inputbox=wx.TextEntryDialog(okno2, 'Podaj nową nazwę sekwencji: '+str(x))
				click=inputbox.ShowModal()
				while inputbox.GetValue() in nazwysekwencji:
					inputbox=wx.TextEntryDialog(okno2, "Nazwy nie mogą się powtarzać, podaj nazwę dla: "+str(x))
					inputbox.ShowModal()
				if click==wx.ID_OK:
					nazwysekwencji.append(inputbox.GetValue())
					sciezki.append(tempw)
				else:
					nazwysekwencji.append(x)
					sciezki.append(tempw)
		else:
			for x in naglowki:
				nazwysekwencji.append(x)
				sciezki.append(tempw)
		sekwencje.Clear()
		sekwencje.InsertItems(nazwysekwencji, 0)
		zapisz_sekwencje(nazwysekwencji[-len(naglowki):],naglowki,sciezki[-len(naglowki):])
		hw.Clear()
		okno2.Hide()
		okno1.Show()
	except:
		wx.MessageBox("Przed zatwierdzeniem musisz wybrać sekwencje", caption='Ostrzeżenie', parent=okno2)

def hide(evt):
	okno2.Hide()
	hw.Clear()
	wyszukiwarka.GetValue=''
	okno3.Hide()
	oknoW.Hide()
	oknoH.Hide()
	okno1.Show()
	
def add(evt):
	selected=sekwencje.GetSelection()
	if sekwencjedotplot.GetCount()>1:
		sekwencjedotplot.Delete(0)
		del(dotplotn[0])
		del(dotplotseq[0])
	sekwencjedotplot.InsertItems([nazwysekwencji[selected]], sekwencjedotplot.GetCount())
	dotplotn.append(nazwysekwencji[selected])
	dotplotseq.append(sek[selected])

def delete(evt):
	selected=sekwencjedotplot.GetSelection()
	sekwencjedotplot.Delete(selected)
	del(dotplotn[selected])
	del(dotplotseq[selected])
	
def usun_sek(evt):
	selected=sekwencje.GetSelection()
	usun_sekwencje(nazwysekwencji[selected])
	sek.pop(selected)
	sciezki.pop(selected)
	nazwysekwencji.pop(selected)
	sekwencje.Delete(selected)
def UstawieniaSeryjnejAnalizy(evt):
	okno3.Show()
	okno3.Center()
	
def PokazWykres(wykresy, inf, n, plotno):
	global mnw
	mnw.Destroy()
	mnw=wx.Panel(parent=oknoW, pos=(22,75), size=(738,480))
	pustywykres=FigureCanvas(mnw,-1,wykresy[n])
	infokna.SetLabel("Wielkosc okna: "+inf[n][0])
	infprog.SetLabel("Wartosc progowa: "+inf[n][1])
	if len(inf[n])>2:
		infstart.Show()
		infstart.SetLabel("Przesuniecie poczatku sekwencji: "+str(inf[n][2]))

#Very ugly function unnecessarily stretched by serval options of running it. I should make separate function for serial analysis
def StworzDotPlot(evt):
	global parametry, wykresy, Nplot
	infstart.Hide()
	parametry=[]
	wykresy=[]
	Nplot=0
	metoda=wybmet.GetSelection()
	if WOkna.GetValue()!="" and Prog.GetValue()!="" and len(dotplotseq)==2:
		if WOkna.GetValue().isnumeric() and Prog.GetValue().isnumeric():
			if StartSeq1.GetValue()=='' and StartSeq2.GetValue()=='':				
				#FigureCanvas(mnw,-1,wykresy[0])
				if metoda==0:
					if SeryjnaAnaliza.IsChecked():
						if Maksokno.GetValue().isnumeric() and Krokokna.GetValue().isnumeric():
							for i in range(int(WOkna.GetValue()),int(Maksokno.GetValue())+1, int(Krokokna.GetValue())):
								for krok in range(math.ceil(i*0.6),i+1):
									wspolrzedne=znajdz_wspolrzedne(dotplotseq[0], dotplotseq[1], i, krok)
									wykr=NarysujDotPlot(wspolrzedne,len(dotplotseq[0]),len(dotplotseq[1]))
									wykresy.append(wykr)
									parametry.append([str(i),str(krok)])
									PokazWykres(wykresy, parametry, Nplot, mnw)
									oknoW.Show()
						else:
							wx.MessageBox("Uzupełnij dane dotyczace seryjnej analizy prawidlowymi wartosciami")
					else:
						wspolrzedne=znajdz_wspolrzedne(dotplotseq[0], dotplotseq[1], int(WOkna.GetValue()), int(Prog.GetValue()))
						wykresik=NarysujDotPlot(wspolrzedne,len(dotplotseq[0]),len(dotplotseq[1]))
						wykresy.append(wykresik)
						parametry.append([WOkna.GetValue(), Prog.GetValue()])
						PokazWykres(wykresy, parametry, Nplot, mnw)
						oknoW.Show()
				else:
					if SeryjnaAnaliza.IsChecked(): 
						if Maksokno.GetValue().isnumeric() and Krokokna.GetValue().isnumeric():
							for i in range(int(WOkna.GetValue()),int(Maksokno.GetValue())+1, int(Krokokna.GetValue())):
								for krok in range(math.ceil(i*0.6),i+1):
									for przesuniecie in range(0,i):
										if radioseq1.GetValue():
											wspolrzedne=znajdz_wspolrzedne2(dotplotseq[0], dotplotseq[1], i, krok, start1=przesuniecie)
										else:
											wspolrzedne=znajdz_wspolrzedne2(dotplotseq[0], dotplotseq[1], i, krok, start2=przesuniecie)
										wykr=NarysujDotPlot(wspolrzedne,len(dotplotseq[0]),len(dotplotseq[1]))
										wykresy.append(wykr)
										parametry.append([str(i),str(krok), przesuniecie])
										PokazWykres(wykresy, parametry, Nplot, mnw)
										oknoW.Show()
						else:
							wx.MessageBox("Uzupełnij dane dotyczace seryjnej analizy prawidlowymi wartosciami")
					else:
						wspolrzedne=znajdz_wspolrzedne2(dotplotseq[0], dotplotseq[1], int(WOkna.GetValue()), int(Prog.GetValue()))
						wykresik=NarysujDotPlot(wspolrzedne,len(dotplotseq[0]),len(dotplotseq[1]))
						wykresy.append(wykresik)
						parametry.append([WOkna.GetValue(), Prog.GetValue()])
						PokazWykres(wykresy, parametry, Nplot, mnw)
						oknoW.Show()
			else:
				if StartSeq1.GetValue()!='' and StartSeq2.GetValue()!='':
					if StartSeq1.GetValue().isnumeric() and StartSeq2.GetValue().isnumeric():
						if metoda==0:
							if SeryjnaAnaliza.IsChecked():
								if Maksokno.GetValue().isnumeric() and Krokokna.GetValue().isnumeric():
									for i in range(int(WOkna.GetValue()),int(Maksokno.GetValue())+1, int(Krokokna.GetValue())):
										for krok in range(math.ceil(i*0.6),i+1):
											wspolrzedne=znajdz_wspolrzedne(dotplotseq[0], dotplotseq[1], i, krok, int(StartSeq1.GetValue()), int(StartSeq2.GetValue()))
											wykr=NarysujDotPlot(wspolrzedne,len(dotplotseq[0]),len(dotplotseq[1]))
											wykresy.append(wykr)
											parametry.append([str(i),str(krok)])
											PokazWykres(wykresy, parametry, Nplot, mnw)
											oknoW.Show()
								else:
									wx.MessageBox("Uzupełnij dane dotyczace seryjnej analizy prawidlowymi wartosciami")
							else:
								wspolrzedne=znajdz_wspolrzedne(dotplotseq[0], dotplotseq[1], int(WOkna.GetValue()), int(Prog.GetValue()), int(StartSeq1.GetValue()), int(StartSeq2.GetValue()))
								wykresik=NarysujDotPlot(wspolrzedne,len(dotplotseq[0]),len(dotplotseq[1]))
								wykresy.append(wykresik)
								parametry.append([WOkna.GetValue(), Prog.GetValue()])
								PokazWykres(wykresy, parametry, Nplot, mnw)
								oknoW.Show()
						else:
							if SeryjnaAnaliza.IsChecked(): 
								if Maksokno.GetValue().isnumeric() and Krokokna.GetValue().isnumeric():
									for i in range(int(WOkna.GetValue()),int(Maksokno.GetValue())+1, int(Krokokna.GetValue())):
										for krok in range(math.ceil(i*0.6),i+1):
											for przesuniecie in range(0,i):
												if radioseq1.GetValue():
													wspolrzedne=znajdz_wspolrzedne2(dotplotseq[0], dotplotseq[1], i, krok, int(StartSeq1.GetValue())+przesuniecie, int(StartSeq2.GetValue()))
												else:
													wspolrzedne=znajdz_wspolrzedne2(dotplotseq[0], dotplotseq[1], i, krok, int(StartSeq1.GetValue()), int(StartSeq2.GetValue())+przesuniecie)
												wykr=NarysujDotPlot(wspolrzedne,len(dotplotseq[0]),len(dotplotseq[1]))
												wykresy.append(wykr)
												parametry.append([str(i),str(krok),przesuniecie])
												PokazWykres(wykresy, parametry, Nplot, mnw)
												oknoW.Show()
							else:
								wspolrzedne=znajdz_wspolrzedne2(dotplotseq[0], dotplotseq[1], int(WOkna.GetValue()), int(Prog.GetValue()), int(StartSeq1.GetValue()), int(StartSeq1.GetValue()))
								wykresik=NarysujDotPlot(wspolrzedne,len(dotplotseq[0]),len(dotplotseq[1]))
								wykresy.append(wykresik)
								parametry.append([WOkna.GetValue(), Prog.GetValue()])
								PokazWykres(wykresy, parametry, Nplot, mnw)
								oknoW.Show()
					else:
						wx.MessageBox("Start pierwszej i drugiej sekwencji musi byc liczba", label="Ostrzezenie", parent=okno1)
				elif StartSeq1.GetValue()!='':
					if StartSeq1.GetValue().isnumeric():
						if metoda==0:
							if SeryjnaAnaliza.IsChecked():
								if Maksokno.GetValue().isnumeric() and Krokokna.GetValue().isnumeric():
									for i in range(int(WOkna.GetValue()),int(Maksokno.GetValue())+1, int(Krokokna.GetValue())):
										for krok in range(math.ceil(i*0.6),i+1):
											wspolrzedne=znajdz_wspolrzedne(dotplotseq[0], dotplotseq[1], i, krok, int(StartSeq1.GetValue()))
											wykr=NarysujDotPlot(wspolrzedne,len(dotplotseq[0]),len(dotplotseq[1]))
											wykresy.append(wykr)
											parametry.append([str(i),str(krok)])
											PokazWykres(wykresy, parametry, Nplot, mnw)
											oknoW.Show()
								else:
									wx.MessageBox("Uzupełnij dane dotyczace seryjnej analizy prawidlowymi wartosciami")
							else:
								wspolrzedne=znajdz_wspolrzedne(dotplotseq[0], dotplotseq[1], int(WOkna.GetValue()), int(Prog.GetValue()), int(StartSeq1.GetValue()))
								wykresik=NarysujDotPlot(wspolrzedne,len(dotplotseq[0]),len(dotplotseq[1]))
								wykresy.append(wykresik)
								parametry.append([WOkna.GetValue(), Prog.GetValue()])
								PokazWykres(wykresy, parametry, Nplot, mnw)
								oknoW.Show()
						else:
							if SeryjnaAnaliza.IsChecked(): 
								if Maksokno.GetValue().isnumeric() and Krokokna.GetValue().isnumeric():
									for i in range(int(WOkna.GetValue()),int(Maksokno.GetValue())+1, int(Krokokna.GetValue())):
										for krok in range(math.ceil(i*0.6),i+1):
											for przesuniecie in range(0,i):
												if radioseq1.GetValue():
													wspolrzedne=znajdz_wspolrzedne2(dotplotseq[0], dotplotseq[1], i, krok, int(StartSeq1.GetValue())+przesuniecie)
												else:
													wspolrzedne=znajdz_wspolrzedne2(dotplotseq[0], dotplotseq[1], i, krok, int(StartSeq1.GetValue()), przesuniecie)
												wykr=NarysujDotPlot(wspolrzedne,len(dotplotseq[0]),len(dotplotseq[1]))
												wykresy.append(wykr)
												parametry.append([str(i),str(krok), przesuniecie])
												PokazWykres(wykresy, parametry, Nplot, mnw)
												oknoW.Show()
							else:
								wspolrzedne=znajdz_wspolrzedne2(dotplotseq[0], dotplotseq[1], int(WOkna.GetValue()), int(Prog.GetValue()), int(StartSeq1.GetValue()))
								wykresik=NarysujDotPlot(wspolrzedne,len(dotplotseq[0]),len(dotplotseq[1]))
								wykresy.append(wykresik)
								parametry.append([WOkna.GetValue(), Prog.GetValue()])
								PokazWykres(wykresy, parametry, Nplot, mnw)
								oknoW.Show()
					else:
						wx.MessageBox("Start pierwszej sekwencji musi byc liczba", label="Ostrzezenie")
				elif StartSeq2.GetValue()!='':
					if StartSeq2.GetValue().isnumeric():
						if metoda==0:
							if SeryjnaAnaliza.IsChecked():
								if Maksokno.GetValue().isnumeric() and Krokokna.GetValue().isnumeric():
									for i in range(int(WOkna.GetValue()),int(Maksokno.GetValue())+1, int(Krokokna.GetValue())):
										for krok in range(math.ceil(i*0.6),i+1):
											wspolrzedne=znajdz_wspolrzedne(dotplotseq[0], dotplotseq[1], i, krok, start2=int(StartSeq2.GetValue()))
											wykr=NarysujDotPlot(wspolrzedne,len(dotplotseq[0]),len(dotplotseq[1]))
											wykresy.append(wykr)
											parametry.append([str(i),str(krok)])
											PokazWykres(wykresy, parametry, Nplot, mnw)
											oknoW.Show()
								else:
									wx.MessageBox("Uzupełnij dane dotyczace seryjnej analizy prawidlowymi wartosciami")
							else:
								wspolrzedne=znajdz_wspolrzedne(dotplotseq[0], dotplotseq[1], int(WOkna.GetValue()), int(Prog.GetValue()), start2=int(StartSeq2.GetValue()))
								wykresik=NarysujDotPlot(wspolrzedne,len(dotplotseq[0]),len(dotplotseq[1]))
								wykresy.append(wykresik)
								parametry.append([WOkna.GetValue(), Prog.GetValue()])
								PokazWykres(wykresy, parametry, Nplot, mnw)
								oknoW.Show()
						else:
							if SeryjnaAnaliza.IsChecked(): 
								if Maksokno.GetValue().isnumeric() and Krokokna.GetValue().isnumeric():
									for i in range(int(WOkna.GetValue()),int(Maksokno.GetValue())+1, int(Krokokna.GetValue())):
										for krok in range(math.ceil(i*0.6),i+1):
											for przesuniecie in range(0,i):
												if radioseq1.GetValue():
													wspolrzedne=znajdz_wspolrzedne2(dotplotseq[0], dotplotseq[1], i, krok, przesuniecie, int(StartSeq2.GetValue()))
												else:
													wspolrzedne=znajdz_wspolrzedne2(dotplotseq[0], dotplotseq[1], i, krok, start2=int(StartSeq2.GetValue())+przesuniecie)
												wykr=NarysujDotPlot(wspolrzedne,len(dotplotseq[0]),len(dotplotseq[1]))
												wykresy.append(wykr)
												parametry.append([str(i),str(krok), przesuniecie])
												PokazWykres(wykresy, parametry, Nplot, mnw)
												oknoW.Show()
							else:
								wspolrzedne=znajdz_wspolrzedne2(dotplotseq[0], dotplotseq[1], int(WOkna.GetValue()), int(Prog.GetValue()), start2=int(StartSeq2.GetValue()))
								wykresik=NarysujDotPlot(wspolrzedne,len(dotplotseq[0]),len(dotplotseq[1]))
								wykresy.append(wykresik)
								parametry.append([WOkna.GetValue(), Prog.GetValue()])
								PokazWykres(wykresy, parametry, Nplot, mnw)
								oknoW.Show()
					else:
						wx.MessageBox("Start drugiej sekwencji musi byc liczba", label="Ostrzezenie")
		else:
			wx.MessageBox("Wielkosc okna i wartosc progowa musza byc liczbami")
	else:
		if len(dotplotseq)<2:
			wx.MessageBox("Do stworzenia dot-plota potrzebne sa 2 sekwencje", caption="Ostrzezenie", parent=okno1)
		else:
			wx.MessageBox("Uzupelnij wielkosc okna oraz wartosc progowa", caption="Ostrzezenie", parent=okno1)

def NextPlot(evt):
	global Nplot
	if Nplot<len(wykresy)-1:
		Nplot+=1
		PokazWykres(wykresy, parametry, Nplot, mnw)
		
def PreviousPlot(evt):
	global Nplot
	if Nplot>0:
		Nplot-=1
		PokazWykres(wykresy, parametry, Nplot, mnw)

def ZapiszWykres(evt):
	td=str(date.today())
	files=0
	if os.path.exists(td):
		for x in os.listdir(td):
			files+=1
		wykresy[Nplot].savefig(td+"/"+td+"("+str(files+1)+").pdf")
	else:
		os.mkdir(td)
		wykresy[Nplot].savefig(td+"/"+td+"(1).pdf")
		
def WyswietlInfo(evt):
	wx.MessageBox("Program powstal w ramach zaliczenia przedmiotu Pracownia Informatyczna\nAutorzy: Tomasz Borowiak, Weronika Dunska","O programie")

def WyswietlHelp(evt):
	teksthelp.SetLabel(text1)
	teksthelp.Wrap(400)
	oknoH.Show()

def Wtext1(evt):
	teksthelp.SetLabel(text1)
	teksthelp.Wrap(400)
	
def Wtext2(evt):
	teksthelp.SetLabel(text2)
	teksthelp.Wrap(400)

def Wtext3(evt):
	teksthelp.SetLabel(text3)
	teksthelp.Wrap(400)

def Wtext4(evt):
	teksthelp.SetLabel(text4)
	teksthelp.Wrap(400)

def Wtext5(evt):
	teksthelp.SetLabel(text5)
	teksthelp.Wrap(400)

		
program=wx.App()
okno1=wx.Frame(None, title="Program", size=(800,600), style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.MINIMIZE_BOX)
okno1.Centre()
panel=wx.Panel(parent=okno1)
okno1.Show()

sekwencje=wx.ListBox(parent=panel, pos=(20,20), size=(400,400))
sekwencjedotplot=wx.ListBox(parent=panel,pos=(20,420), size=(400,80))

if len(nazwysekwencji)>0:
	sekwencje.InsertItems(nazwysekwencji, 0)

wczytsek=wx.Button(panel, wx.ID_ANY, "Wczytaj sekwencje", pos=(420,20))
okno1.Bind(wx.EVT_BUTTON, wczyt_sek, wczytsek)

usunsek=wx.Button(panel, wx.ID_ANY, 'Usun sekwencje', pos=(420,45))
okno1.Bind(wx.EVT_BUTTON, usun_sek, usunsek)
wx.Button()
tempn=[]
temps=[]
tempw=''

okno2=wx.Frame(okno1,title="Wczytywanie danych",size=(600,600), style= wx.CAPTION )
panel2=wx.Panel(parent=okno2)
ukryj=wx.Button(panel2, wx.ID_ANY, 'X', pos=(540,10), size=(30,30))
okno2.Bind(wx.EVT_BUTTON, hide, ukryj)
hw=wx.ListBox(parent=panel2, pos=(40,50), size=(500,500), style=wx.LB_MULTIPLE | wx.LB_HSCROLL)
wyszukiwarka=wx.TextCtrl(panel2, size=(500,30), pos=(40,10))
wyszukiwarka.Bind(wx.EVT_KEY_UP, update)
wybsek=wx.Button(panel2, wx.ID_ANY,'Ok', pos=(540,525),size=(25,25))
okno2.Bind(wx.EVT_BUTTON, choose, wybsek)

dodajdotplot=wx.Button(panel, wx.ID_ANY, "Dodaj do dot-plota", pos=(420,420))
okno1.Bind(wx.EVT_BUTTON,add,dodajdotplot)
usundotplot=wx.Button(panel, wx.ID_ANY, "Usun z dot-plota", pos=(420,445))
okno1.Bind(wx.EVT_BUTTON, delete, usundotplot)

WOkna=wx.TextCtrl(panel, size=(20,20), pos=(430,100))
Prog=wx.TextCtrl(panel, size=(20,20), pos=(430,125))
wokna=wx.StaticText(panel, pos=(452,102), label="Wielkosc okna")
prog=wx.StaticText(panel, pos=(452,127), label="Wartosc progowa")
StartSeq1=wx.TextCtrl(panel, pos=(430,150), size=(60,20))
StartSeq2=wx.TextCtrl(panel, pos=(430,175), size=(60,20))
stseq1=wx.StaticText(panel, pos=(492, 151), label='Poczatek przyrownania 1. sekwencji')
stseq2=wx.StaticText(panel, pos=(492, 176), label='Poczatek przyrownania 2. sekwencji')
SeryjnaAnaliza=wx.CheckBox(panel, pos=(610,300)) #(433,150)
serana=wx.StaticText(panel,pos=(630,300), label="Seryjna analiza")
#met1=wx.RadioButton(panel, wx.ID_ANY, pos=(440,250), label="Metoda pierwsza", style=wx.RB_GROUP)
#met2=wx.RadioButton(panel, wx.ID_ANY, pos=(560,250), label="Metoda druga")
#wybmet=wx.StaticText(panel, pos=(430,225), label="Wybor metody:")
wybmet=wx.RadioBox(panel, wx.ID_ANY, label="Wybor metody", pos=(430,215), choices=["Metoda pierwsza", "Metoda druga"])
menu=wx.MenuBar()
mn=wx.Menu()
meninfo=mn.Append(wx.ID_ANY, "Informacje", "Wyswietl informacje o aplikacji")
menhelp=mn.Append(wx.ID_ANY, "Pomoc", "Wyswietl pomoc")
menu.Append(mn,"Pomoc")
okno1.SetMenuBar(menu)
okno1.Bind(wx.EVT_MENU, WyswietlInfo, meninfo)
okno1.Bind(wx.EVT_MENU, WyswietlHelp, menhelp)



ustser=wx.Button(panel, pos=(430,295), label="Ustawienia seryjnej analizy")
okno1.Bind(wx.EVT_BUTTON, UstawieniaSeryjnejAnalizy, ustser)

okno3=wx.Frame(okno1, title="Ustawienia seryjnej analizy",size=(300,300), style=wx.CAPTION)
panel3=wx.Panel(parent=okno3)
Maksokno=wx.TextCtrl(panel3, pos=(10,10), size=(20,20))
maksokno=wx.StaticText(panel3, pos=(42,12), label="Maksymalne okno")
Krokokna=wx.TextCtrl(panel3, pos=(10,40), size=(20,20))
krokokna=wx.StaticText(panel3, pos=(42,42), label="Krok zmiany okna")
wybsek=wx.StaticText(panel3, pos=(10,70), label="Sekwencja, ktorej poczatek przesuwamy:")
radioseq1=wx.RadioButton(panel3, pos=(10,100))
radioseq2=wx.RadioButton(panel3, pos=(10,130))
radioseq1.SetValue(True)
tseq1=wx.StaticText(panel3, pos=(42,100), label="Sekwencja 1")
tseq2=wx.StaticText(panel3, pos=(42,130), label="Sekwencja 2")
SOk=wx.Button(panel3, pos=(100,230), label="Ok")
okno3.Bind(wx.EVT_BUTTON, hide, SOk)

#Kroksekwencji=wx.TextCtrl(panel3, pos=(10, 140), size=(60,20))
#kroksekwencji=wx.StaticText(panel3, pos=(80,142), label="Krok zmiany startu sekwencji")




uruchom=wx.Button(panel, pos=(420,470), label="Stworz dot-plot")
okno1.Bind(wx.EVT_BUTTON, StworzDotPlot, uruchom)


oknoW=wx.Frame(okno1, title="Wykresy", size=(800,600), style=wx.CAPTION)
oknoW.Center()
panelW=wx.Panel(parent=oknoW, size=(800,600))
poprzedni=wx.Button(panelW, pos=(0,0), size=(20,560), label="<")
oknoW.Bind(wx.EVT_BUTTON, PreviousPlot, poprzedni)
nast=wx.Button(panelW, pos=(763,0), size=(20,560), label=">")
oknoW.Bind(wx.EVT_BUTTON, NextPlot, nast)
mnw=wx.Panel(parent=oknoW, pos=(22,75), size=(738,480))
ZW=wx.Button(parent=panelW, pos=(22,5), label="Zamknij okno")
infokna=wx.StaticText(parent=panelW, label="Wielkosc okna: ", pos=(560,10))
infprog=wx.StaticText(parent=panelW, label="Wartosc progowa: ", pos=(560,30))
infstart=wx.StaticText(parent=panelW, label='', pos=(560,50))
pustywykres=0
oknoW.Bind(wx.EVT_BUTTON, hide, ZW)
zapis=wx.Button(parent=panelW, pos=(120,5), label="Zapisz wykres")
oknoW.Bind(wx.EVT_BUTTON, ZapiszWykres, zapis)


#testowe=wx.Frame(okno1,title=test, size=(800,600))

#wynik=OknoWynikowe(okno1)
oknoH=wx.Frame(okno1,wx.ID_ANY, "Pomoc", size=(600,600),style=wx.CAPTION)
panelH=wx.Panel(oknoH)
text1="Z glownego okna programu mozna wlaczyc okno wczytywania sekwencji oraz ustawic parametry przeprowadzanej analizy. Po lewej stronie w gornym listboxie znajduja sie wczytane sekwencje, natomiast w dolnym listboxie znajduja sie sekwnecje, ktore maja zostac uzyte w analizie. Zarzadzanie sekwencjami odbywa sie za pomoca przyciskow umieszczonych obok list boxow"
text2="Wczytywanie sekwencji odbywa sie poprzez klikniecie przycisku \"Wczytaj sekwencje\". Klikniecie go powoduje otwarcie okna w ktorym mozliwe jest wybranie sciezki do pliku fasta, ktory chcemy wczytac. Po wybraniu pliku program pokazuje wszystkie sekwencje fasta ktore sie w nim znajduje, mozna wszukac interesujace nas sekwencje po nazwie. Po wybraniu sekwencji ktore chcemy wczytac mozemy zmienic im wyswietlana w programie nazwe."
text3="Uzytkownik moze ustawic takie parametry jak wielkosc sprawdzanego okna, oraz wartosc progowa dopasowan przy ktorej dane okno zostanie oznaczone jako match. Mozliwe jest tez uruchomienie analizy od konkretnego nukleotydu. Sekwencje moga byc analizowane na 2 rozne metody"
text4="Pierwsza metoda znajduje w oknie wszystkie dopasowania, dopasowujac kazdy z nukleotydow maksymalnie raz.\nDruga metoda znajduje dopasowania tylko na glownej przekatnej w danym oknie.\n\nWarto zauwazyc ze obie metody zwroca dokladnie taki sam wynik, kiedy okno oraz wartosc progowa beda rowne 1."
text5="Seryjna analiza pozwala na wykonanie wielu analiz z roznymi parametrami. Okno jest zwiekszane o ustalona przez uzytkownika wartosc, a nastepnie sprawdzana jest kazda wartosc progowa zaczynajac od 60% wartosci aktualnego okna. Seryjna analiza konczy sie gdy zostanie osiagniete maksymalne okno ustalone przez uzytkownika. W przypadku metodu drugiej po za zmiana okna i wartosci progowej zmienia sie rowniez startowy nukleotyd, pozwala to na wykrycie sekwencji, kiedy w oryginalnym ustawieniu nie znajduje sie ona na glownej przekatnej okna."
teksthelp=wx.StaticText(parent=panelH, pos=(175,20),label=text1)
teksthelp.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
teksthelp.Wrap(400)
gokno=wx.Button(panelH,wx.ID_ANY, label="Glowne okno", pos=(10,20))
wczytsek=wx.Button(panelH,wx.ID_ANY, label="Wczytywanie sekwencji",pos=(10,45))
params=wx.Button(panelH,wx.ID_ANY, label="Parametry analizy",pos=(10,70))
metan=wx.Button(panelH,wx.ID_ANY, label="Metody analizy",pos=(10,95))
sran=wx.Button(panelH,wx.ID_ANY, label="Seryjna analiza",pos=(10,120))
zmkn=wx.Button(panelH,wx.ID_ANY,label="Zamknij", pos=(10,145))
oknoH.Bind(wx.EVT_BUTTON,Wtext1,gokno)
oknoH.Bind(wx.EVT_BUTTON,Wtext2,wczytsek)
oknoH.Bind(wx.EVT_BUTTON,Wtext3,params)
oknoH.Bind(wx.EVT_BUTTON,Wtext4,metan)
oknoH.Bind(wx.EVT_BUTTON,Wtext5,sran)
oknoH.Bind(wx.EVT_BUTTON,hide,zmkn)

oknoH.Center()

program.MainLoop()
