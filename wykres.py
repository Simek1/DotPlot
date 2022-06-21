from matplotlib import pyplot as plt

def NarysujDotPlot(wspolrzedne, dlugoscsek1, dlugoscsek2):
	#plt.rcParams["figure.figsize"] = [dlugoscsek1, dlugoscsek2]
	x=[x[0] for x in wspolrzedne]
	y=[-x[1] for x in wspolrzedne]
	wykres=plt.Figure(figsize=(7.38,4.80), dpi=100)
	sct=wykres.add_subplot(111)
	sct.scatter(x,y,s=20/(max((dlugoscsek1,dlugoscsek2))*0.1))
	sct.axis("off")
	return(wykres)
	
