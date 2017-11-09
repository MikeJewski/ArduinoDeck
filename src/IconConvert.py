import os
from PIL import Image
import wx

class MainFrame(wx.Frame):
    def __init__(self):

		wx.Frame.__init__(self, None, title="Arduino Deck",size=(870,650))



		dirname = os.getcwd()+"\\StreamDeckIcons\\"
		print os.getcwd()
		dlg = wx.FileDialog(self, "Load Layout File", dirname, "", "Picture files (*.png,*.jpg,*.bmp)|*.png;*.jpg;*.bmp", style=wx.FD_OPEN | wx.FD_MULTIPLE)
		if dlg.ShowModal() == wx.ID_CANCEL:
			None
		else:
			sel_dir = dlg.GetDirectory()
			pathnames = dlg.GetPaths()
			for i in range(0,len(pathnames)):
				im = Image.open(pathnames[i])
				im.thumbnail((58,58))
				file = pathnames[i].split("\\")
				im.save(dirname+file[len(file)-1].replace(".png",".bmp").replace(".jpeg",".bmp").replace(".jpg",".bmp"))

#----------------------------------------------------------------------
if __name__ == "__main__":
      app = wx.App(False)
      frame = MainFrame()
      #app.MainLoop()
