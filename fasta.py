from os.path import exists
import csv

def wczytaj_fasta(sciezka):
	plik=open(sciezka)
	tekst=plik.read()
	tekst=tekst.splitlines()
	sekwencje=[]
	nazwy=[]
	sekwencja=''
	for i in range(len(tekst)):
		if '>' in tekst[i]:
			nazwy.append(tekst[i][1:])
			j=i+1
			while len(tekst[j])>=1 and '>' not in tekst[j]:
				sekwencja+=tekst[j]
				if j<len(tekst)-1:
					j+=1
				else:
					break
			sekwencje.append(sekwencja)
	return nazwy, sekwencje

def zapisz_sekwencje(nazwauzytkownika, naglowek, sciezka):
	with open('dane.txt', mode='a') as plik:
		for i in range(len(nazwauzytkownika)):
			plik.write(nazwauzytkownika[i]+'\t'+naglowek[i]+'\t'+sciezka[i]+'\n')
			
def wczytaj_zapisane_dane():
	sekwencje=[]
	nazwy=[]
	sciezki=[]
	if exists('dane.txt'):
		wiersze=[]
		with open('dane.txt') as plik:
			dane=csv.reader(plik, delimiter='\t')
			for x in dane:
				wiersze.append(x)
		zapis=wiersze.copy()
		for x in wiersze:
			if exists(x[2]):
				with open(x[2]) as plik:
					tekst=plik.read()
					tekst=tekst.splitlines()
				for i in range(len(tekst)):
					if x[1] in tekst[i]:
						j=i+1
						sekwencja=''
						while len(tekst[j])>=1 and '>' not in tekst[j]:
							sekwencja+=tekst[j]
							if j<len(tekst)-1:
								j+=1
							else:
								break
						sekwencje.append(sekwencja)
						nazwy.append(x[0])
						sciezki.append(x[2])
						break
			else:
				with open('dane.txt', mode='w') as plik:
					for r in zapis:
						if r[2]==x[2]:
							zapis.pop(zapis.index(r))
							break
					gotowyzapis=[]
					for x in zapis:
						wiersz=''
						for i in range(len(x)):
							if i<2:
								wiersz+=str(x[i])+'\t'
							else:
								wiersz+=str(x[i])+'\n'
						gotowyzapis.append(wiersz)
					plik.writelines(gotowyzapis)					
	return nazwy, sekwencje, sciezki

def usun_sekwencje(nazwasekwencji):
	with open('dane.txt', mode='r') as plik:
		wiersze=[]
		dane=csv.reader(plik, delimiter='\t')
		for x in dane:
			wiersze.append(x)
		for wiersz in wiersze:
			if wiersz[0]==nazwasekwencji:
				wiersze.pop(wiersze.index(wiersz))
				break
	with open('dane.txt', mode='w') as plik:
		zapis=[]
		for x in wiersze:
			wiersz=''
			for i in range(len(x)):
				if i<2:
					wiersz+=str(x[i])+'\t'
				else:
					wiersz+=str(x[i])+'\n'
			zapis.append(wiersz)
		plik.writelines(zapis)
			