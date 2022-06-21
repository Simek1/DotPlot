
def znajdz_wspolrzedne(seq1, seq2, okno, prog, start1=0, start2=0):
	if start1!=0 or start2!=0:
		seq1=seq1[start1:]
		seq2=seq2[start2:]
	if len(seq1)%okno!=0:
		seq1=seq1[0:-(len(seq1)%okno)]
	if len(seq2)%okno!=0:
		seq2=seq2[0:-(len(seq2)%okno)]

	matche=0
	WspolrzedneDopasowan=[]
	
	for colokna in range(0,len(seq1),okno): #Przesuwa sie oknami
		uzyte=[]
		for i in range(len(seq1)):
			for j in range(colokna,len(seq2)): #Ma sprawdzic 3 i przesunac się w dol, po sprawdzeniu tak 3 razy, dodaje do listy match(okno), to będzie do okno
				if seq1[i]==seq2[j]:
					#print(i,j, seq1[i], seq2[j])
					if j not in uzyte:
						matche+=1
						uzyte.append(j)
						break #zeby jeden nukleotyd nie zostal dopasowany kilka razy (zmiana koncepcji dopasowan, prog musi byc mniejszy od okna)
				if j==colokna+okno-1: #kiedy ma przeskoczyc do kolejnego wiersza
					break
			if (i+1)%okno==0: #Warunek mówiący kiedy doszło do końca okna
				uzyte=[]
				#print(i,j, "koniec okna")
				if matche>=prog:
					#print(i,j, "dopasowane okno")
					WspolrzedneDopasowan.append([i+1-okno,j+1-okno]) #Dodanie wspolrzednych poczatku okna jest w oknie jest wystarczajaca ilosc matchy
				matche=0
	return(WspolrzedneDopasowan)
#print(znajdz_wspolrzedne('ATGGCTTACC','CCATTCGGTAC',1,1))

def znajdz_wspolrzedne2(seq1, seq2, okno, prog, start1=0, start2=0):
	if start1!=0 or start2!=0:
		seq1=seq1[start1:]
		seq2=seq2[start2:]
	if len(seq1)%okno!=0:
		seq1=seq1[0:-(len(seq1)%okno)]
	if len(seq2)%okno!=0:
		seq2=seq2[0:-(len(seq2)%okno)]
	
	matche=0
	WspolrzedneDopasowan=[]
	for colokna in range(0, len(seq1), okno):
		for i in range(len(seq1)):
			for j in range(colokna, len(seq2)):
				if (i-((i+1)//okno)*okno)==(j-((j+1)//okno)*okno): #Sprawdzanie tylko przekątnej w danym oknie
					if seq1[i]==seq2[j]:
						matche+=1
				if j==colokna+okno-1: #kiedy ma przeskoczyc do kolejnego wiersza
					break
			if (i+1)%okno==0: #Warunek mówiący kiedy doszło do końca okna
				if matche>=prog:
					#print(i,j, "dopasowane okno")
					WspolrzedneDopasowan.append([i+1-okno,j+1-okno]) #Dodanie wspolrzednych poczatku okna jest w oknie jest wystarczajaca ilosc matchy
				matche=0
	return(WspolrzedneDopasowan)

#a=znajdz_wspolrzedne2('ATGGCTTACC','ATGGCTTACC',1,1)
#b=znajdz_wspolrzedne2('ATGGCTTACC','ATGGCTTACC',1,1)
	